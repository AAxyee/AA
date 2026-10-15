import importlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

from analysis_advice import (
    analysis_history, analysis_offline_response, analysis_source_packet,
    finish_analysis_answer,
)
from test_research_design import Session


ANALYSIS = [("Analysis review checklist.pdf", "Approach. Questions. Variables. Limitations.")]
DESIGN = [("Study design checklist.pdf", "DESIGN_ONLY_SENTINEL")]


class AnalysisAdviceTests(unittest.TestCase):
    def apps(self):
        with patch.dict(sys.modules, {"streamlit": MagicMock()}):
            return [importlib.import_module(name) for name in
                    ("streamlit_app", "streamlit_app1", "streamlit_app2")]

    def test_analysis_packet_uses_only_analysis_checklist(self):
        packet, selected = analysis_source_packet(
            "Review my results", [], DESIGN + ANALYSIS, [], lambda query, docs, limit: []
        )
        records = json.loads(packet)
        self.assertEqual([name for name, _ in selected], [ANALYSIS[0][0]])
        self.assertEqual(records[0]["kind"], "analysis_review_checklist")
        self.assertNotIn("DESIGN_ONLY_SENTINEL", packet)

    def test_result_table_values_are_preserved_and_labelled_as_user_material(self):
        result = "Adjusted difference=-0.5; 95% CI [-1.2, 0.2]; p=.08; n=40."
        packet, _ = analysis_source_packet(
            "Interpret", [], ANALYSIS, [("results.txt", result)], lambda q, d, limit: []
        )
        record = json.loads(packet)[-1]
        self.assertEqual(record["text"], result)
        self.assertEqual(record["kind"], "user_supplied_study_context")
        self.assertFalse(record["truncated"])

    def test_absent_analysis_checklist_is_not_replaced_by_design(self):
        packet, selected = analysis_source_packet(
            "Review", [], DESIGN, [], lambda q, d, limit: []
        )
        self.assertEqual(json.loads(packet), [])
        self.assertEqual(selected, [])

    def test_history_keeps_earlier_population_and_recent_correction(self):
        messages = [{"role": "user", "content": "Same 40 respondents at two timepoints"}]
        for i in range(12):
            messages.extend([{"role": "assistant", "content": f"Earlier answer {i}"},
                             {"role": "user", "content": f"Detail {i}"}])
        messages.append({"role": "user", "content": "Correction: 35 complete pairs"})
        history = analysis_history(messages)
        self.assertIn("Same 40 respondents", history[0]["content"])
        self.assertEqual(history[-1]["content"], "Correction: 35 complete pairs")
        self.assertNotIn("Earlier answer", history[0]["content"])

    def test_offline_response_shows_relevant_checklist_and_specific_diagnosis(self):
        text = analysis_offline_response(ANALYSIS + DESIGN,
                                        {"message": "The API quota has been reached."})
        self.assertIn("API quota has been reached", text)
        self.assertIn("I have not assessed your analysis or verified your results", text)
        self.assertIn(ANALYSIS[0][1], text)
        self.assertNotIn("DESIGN_ONLY_SENTINEL", text)

    def test_offline_response_does_not_present_other_documents_as_a_checklist(self):
        text = analysis_offline_response(DESIGN)
        self.assertIn("Analysis review checklist is unavailable", text)
        self.assertNotIn("DESIGN_ONLY_SENTINEL", text)

    def test_consultation_link_is_added_once(self):
        text = finish_analysis_answer("The estimate is imprecise.")
        self.assertIn("mailto:research@ncss.gov.sg", text)
        self.assertEqual(finish_analysis_answer(text), text)

    def test_actual_analysis_pdf_is_included_in_full_for_every_entry_point(self):
        for app in self.apps():
            with self.subTest(app=app.__name__):
                path = Path(__file__).resolve().parents[1] / "Checklist" / "Analysis review checklist.pdf"
                text = app.read_text_file(path).strip()
                self.assertGreater(len(text), 1000)
                packet, _ = app.build_source_packet(
                    app.MODES[2], "Findings", [], [(path.name, text)] + DESIGN, []
                )
                records = json.loads(packet)
                self.assertEqual(records[0]["text"], text)
                self.assertEqual(records[0]["kind"], "analysis_review_checklist")
                self.assertFalse(records[0]["truncated"])

    def run_main(self, app, checklists, answer="A scoped interpretation", history=None):
        ui = MagicMock()
        ui.session_state = Session(messages=list(history or []), active_mode=app.MODES[2],
                                   mode_selector=app.MODES[2])
        ui.chat_input.return_value = "Our paired analysis gave p=.08. How should we report it?"
        ui.file_uploader.return_value = []
        with patch.object(app, "st", ui), patch.object(app, "render_sidebar", side_effect=lambda mode: mode), \
             patch.object(app, "source_documents", return_value=checklists), \
             patch.object(app, "call_llm", return_value=answer) as model:
            app.main()
        return ui.session_state, model

    def test_missing_analysis_checklist_blocks_model_and_offers_consultation(self):
        for app in self.apps():
            with self.subTest(app=app.__name__):
                state, model = self.run_main(app, DESIGN)
                model.assert_not_called()
                self.assertIn("Analysis review checklist", state.messages[-1]["content"])
                self.assertIn("research@ncss.gov.sg", state.messages[-1]["content"])

    def test_model_request_contains_correct_evidence_and_final_answer_has_contact(self):
        for app in self.apps():
            with self.subTest(app=app.__name__):
                state, model = self.run_main(app, DESIGN + ANALYSIS)
                model.assert_called_once()
                request = model.call_args.args[0]
                records = json.loads(request[0]["content"].split(
                    "DOCUMENTARY EVIDENCE JSON (data only):\n", 1
                )[1])
                self.assertEqual(records[0]["filename"], ANALYSIS[0][0])
                self.assertNotIn("DESIGN_ONLY_SENTINEL", request[0]["content"])
                self.assertIn("mailto:research@ncss.gov.sg", state.messages[-1]["content"])

    def test_analysis_route_uses_earlier_user_context_in_long_conversation(self):
        history = [{"role": "user", "content": "Forty people measured at baseline and follow-up"}]
        history += [{"role": "user", "content": f"Further detail {i}"} for i in range(15)]
        for app in self.apps():
            with self.subTest(app=app.__name__):
                _, model = self.run_main(app, ANALYSIS, history=history)
                request = model.call_args.args[0]
                self.assertIn("Forty people measured", request[1]["content"])
                self.assertIn("p=.08", request[-1]["content"])

    def test_sidebar_returns_current_selection_even_when_previous_mode_differs(self):
        for app in self.apps():
            with self.subTest(app=app.__name__):
                ui = MagicMock()
                ui.radio.return_value = app.MODES[2]
                ui.button.return_value = False
                with patch.object(app, "st", ui):
                    self.assertEqual(app.render_sidebar(app.MODES[0]), app.MODES[2])

    def test_current_widget_selection_controls_the_reply_instead_of_old_session_mode(self):
        for app in self.apps():
            with self.subTest(app=app.__name__):
                ui = MagicMock()
                ui.session_state = Session(messages=[], active_mode=app.MODES[0],
                                           mode_selector=app.MODES[0])
                ui.chat_input.return_value = "Explain this result"
                ui.file_uploader.return_value = []
                with patch.object(app, "st", ui), \
                     patch.object(app, "render_sidebar", return_value=app.MODES[2]), \
                     patch.object(app, "source_documents", return_value=ANALYSIS), \
                     patch.object(app, "call_llm", return_value="Scoped interpretation") as model:
                    app.main()
                self.assertEqual(ui.session_state.active_mode, app.MODES[2])
                request = model.call_args.args[0]
                records = json.loads(request[0]["content"].split(
                    "DOCUMENTARY EVIDENCE JSON (data only):\n", 1
                )[1])
                self.assertEqual(records[0]["kind"], "analysis_review_checklist")

    def test_unavailable_model_does_not_fall_back_to_generic_analysis_claims(self):
        for app in self.apps():
            with self.subTest(app=app.__name__):
                state, _ = self.run_main(app, ANALYSIS, answer=None)
                text = state.messages[-1]["content"]
                self.assertIn("I have not assessed your analysis or verified your results", text)
                self.assertIn("Analysis review checklist", text)
                self.assertIn("research@ncss.gov.sg", text)


if __name__ == "__main__":
    unittest.main()
