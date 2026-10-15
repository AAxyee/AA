"""Run with: python -m unittest discover -s tests -v."""

import importlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from knowledge_sources import load_knowledge_sources


STEMS = ("Info for knowledge base", "Overview of studies")


class KnowledgeSourcesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / "Knowledge base"
        self.folder.mkdir()

    def write(self, name, text="Approved source text"):
        path = self.folder / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def load(self, reader=None):
        return load_knowledge_sources(
            self.folder, STEMS, reader or (lambda path: path.read_text(encoding="utf-8"))
        )

    def test_only_named_sources_are_loaded(self):
        self.write("Info for knowledge base.txt")
        self.write("Overview of studies.md")
        self.write("Unapproved policy.txt", "Must not enter context")
        self.write("Overview of studies draft.txt", "Must not enter context")
        docs, issues = self.load()
        self.assertEqual([name for name, _ in docs],
                         ["Info for knowledge base.txt", "Overview of studies.md"])
        self.assertEqual(issues, [])

    def test_case_whitespace_and_nested_sources(self):
        self.write("nested/INFO  FOR KNOWLEDGE BASE.TXT")
        self.write("OVERVIEW OF STUDIES.md")
        docs, issues = self.load()
        self.assertEqual(len(docs), 2)
        self.assertEqual(issues, [])

    def test_missing_overview_does_not_block_existing_source(self):
        self.write("Info for knowledge base.txt")
        docs, issues = self.load()
        self.assertEqual(len(docs), 1)
        self.assertEqual(len(issues), 1)
        self.assertIn("Overview of studies: file not found", issues[0])

    def test_empty_pdf_reports_searchable_document_needed(self):
        self.write("Info for knowledge base.pdf", "")
        docs, issues = self.load()
        self.assertEqual(docs, [])
        self.assertTrue(any("searchable PDF" in issue for issue in issues))

    def test_dependency_error_is_diagnostic_not_evidence(self):
        self.write("Info for knowledge base.pdf")
        docs, issues = self.load(lambda path: "[PDF support requires pypdf. Install it]")
        self.assertEqual(docs, [])
        self.assertTrue(any("pypdf" in issue for issue in issues))

    def test_reader_exception_preserves_other_source(self):
        self.write("Info for knowledge base.pdf")
        self.write("Overview of studies.txt")
        def reader(path):
            if path.suffix == ".pdf":
                raise ValueError("Unreadable PDF")
            return path.read_text()
        docs, issues = self.load(reader)
        self.assertEqual([name for name, _ in docs], ["Overview of studies.txt"])
        self.assertTrue(any("Unreadable PDF" in issue for issue in issues))

    def test_unreadable_preferred_format_tries_alternative(self):
        self.write("Info for knowledge base.docx")
        self.write("Info for knowledge base.pdf", "Readable alternative")
        self.write("Overview of studies.txt")
        def reader(path):
            if path.suffix == ".docx":
                return "[Could not read document: corrupt archive]"
            return path.read_text()
        docs, issues = self.load(reader)
        self.assertEqual(docs[0], ("Info for knowledge base.pdf", "Readable alternative"))
        self.assertEqual(issues, [])

    def test_missing_folder_reports_configuration_issue(self):
        docs, issues = load_knowledge_sources(self.folder / "missing", STEMS, lambda p: "")
        self.assertEqual(docs, [])
        self.assertIn("folder not found", issues[0])

    def test_real_pdf_and_source_packet_in_all_entry_points(self):
        # Import without running Streamlit or making model requests.
        with patch.dict(sys.modules, {"streamlit": MagicMock()}):
            for name in ("streamlit_app", "streamlit_app1", "streamlit_app2"):
                with self.subTest(entry_point=name):
                    app = importlib.import_module(name)
                    fixture = Path(__file__).resolve().parents[1] / "Knowledge Base" / "Info for knowledge base.pdf"
                    (self.folder / fixture.name).write_bytes(fixture.read_bytes())
                    docs, issues = load_knowledge_sources(self.folder, app.KB_FILES,
                                                         app.read_text_file)
                    self.assertEqual([filename for filename, _ in docs],
                                     ["Info for knowledge base.pdf"])
                    self.assertGreater(len(docs[0][1]), 1000)
                    self.assertTrue(any("Overview of studies" in issue for issue in issues))
                    packet, selected = app.build_source_packet(
                        app.MODES[0], "institutional information", docs,
                        [("Checklist.txt", "CHECKLIST_SENTINEL")],
                        [("User upload.txt", "UPLOAD_SENTINEL")],
                    )
                    self.assertIn("Info for knowledge base.pdf", packet)
                    self.assertNotIn("CHECKLIST_SENTINEL", packet)
                    self.assertNotIn("UPLOAD_SENTINEL", packet)
                    self.assertTrue(selected)


if __name__ == "__main__":
    unittest.main()
