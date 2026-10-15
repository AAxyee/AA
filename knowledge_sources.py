"""Load only approved institutional documents and explain extraction failures."""

from pathlib import Path
import re
from typing import Callable, Iterable


def _normalise(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip()).casefold()


def load_knowledge_sources(
    folder: Path,
    stems: Iterable[str],
    read_text: Callable[[Path], str],
) -> tuple[list[tuple[str, str]], list[str]]:
    """Return readable approved sources plus per-document diagnostics.

    An unavailable document must not prevent other approved sources loading.
    Prefer a readable alternative format when multiple versions are present.
    """
    documents: list[tuple[str, str]] = []
    issues: list[str] = []
    if not folder.is_dir():
        return [], [f"Knowledge Base folder not found: {folder}"]

    rank = {".docx": 0, ".txt": 1, ".md": 2, ".csv": 3, ".json": 4, ".pdf": 5}
    try:
        paths = sorted(
            (path for path in folder.rglob("*")
             if path.is_file() and path.suffix.lower() in rank),
            key=lambda path: (rank[path.suffix.lower()], str(path).casefold()),
        )
    except OSError as exc:
        return [], [f"Could not list Knowledge Base files: {exc}"]

    for stem in stems:
        matches = [path for path in paths if _normalise(path.stem) == _normalise(stem)]
        if not matches:
            issues.append(f"{stem}: file not found in {folder.name}.")
            continue

        failures: list[str] = []
        for path in matches:
            name = path.relative_to(folder).as_posix()
            try:
                text = read_text(path).strip()
            except Exception as exc:
                failures.append(f"{name}: {exc}")
                continue
            if text.startswith(("[Could not read ", "[PDF support requires ")):
                failures.append(f"{name}: {text.strip('[]')}")
            elif not text:
                failures.append(
                    f"{name}: no readable text extracted. For a scanned PDF, "
                    "provide a searchable PDF or a DOCX/text version."
                )
            else:
                documents.append((name, text))
                break
        else:
            issues.extend(failures)

    return documents, issues
