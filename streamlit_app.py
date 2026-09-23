"""Wanna know Wanda bot — a source-grounded research support prototype."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
import io
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

import streamlit as st


APP_DIR = Path(__file__).resolve().parent


def find_content_folder(name: str) -> Path:
    """Find content beside the script or in the bundled streamlit subfolder."""
    candidates = (APP_DIR / name, APP_DIR / "streamlit" / name)
    return next((path for path in candidates if path.is_dir()), candidates[0])


KB_DIR = find_content_folder("Knowledge base")
CHECKLIST_DIR = find_content_folder("Checklist")
CONSULTATION = "research@ncss.gov.sg"
MODES = (
    "Look for institutional information",
    "Source for new information - Advice on research design",
    "Advice on analysis",
)
DISCLAIMER = """IMPORTANT NOTICE:&#x20;
This web application is a prototype developed for educational purpos8 only. The information provided here is NOT intended for real- world usage and should not be relied for making any , especially those related to financial, legal, or healthcare matters. Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume responsibility for how you use any generated output.
Always consult with qualified professionals for accurate and personalised advice."""

KB_FILES = ("Info for knowledge base", "Overview of studies")
CHECKLIST_FILES = {
    MODES[1]: "Study design checklist",
    MODES[2]: "Analysis review checklist",
}
SUPPORTED_UPLOADS = {"txt", "md", "csv", "json", "pdf", "docx"}


def docx_text(data: bytes) -> str:
    """Extract paragraph text from DOCX with Python's standard library."""
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        xml_data = archive.read("word/document.xml")
    root = ET.fromstring(xml_data)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs = []
    for paragraph in root.findall(".//w:p", ns):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", ns))
        if text.strip():
            paragraphs.append(text)
    return "\n".join(paragraphs)


def read_text_file(path: Path) -> str:
    """Read a supported source file, returning an empty string on parse errors."""
    suffix = path.suffix.lower()
    try:
        if suffix in {".txt", ".md", ".csv", ".json"}:
            return path.read_text(encoding="utf-8", errors="replace")
        if suffix == ".pdf":
            try:
                from pypdf import PdfReader
            except ImportError as exc:
                return "[PDF support requires pypdf. Install it with: python -m pip install pypdf]"

            return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
        if suffix == ".docx":
            return docx_text(path.read_bytes())
    except Exception as exc:  # keep one malformed file from breaking the app
        return f"[Could not read {path.name}: {exc}]"
    return ""


def find_named_file(folder: Path, stem: str) -> Path | None:
    if not folder.exists():
        return None
    matches = [p for p in folder.iterdir() if p.is_file() and p.stem.casefold() == stem.casefold()]
    return matches[0] if matches else None


def source_documents(folder: Path, stems: Iterable[str]) -> list[tuple[str, str]]:
    docs: list[tuple[str, str]] = []
    for stem in stems:
        path = find_named_file(folder, stem)
        if path:
            text = read_text_file(path).strip()
            if text:
                docs.append((path.name, text))
    return docs


def chunks(text: str, size: int = 700) -> list[str]:
    # Preserve paragraphs where possible, then split long paragraphs safely.
    pieces: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        pieces.extend(paragraph[i : i + size] for i in range(0, len(paragraph), size))
    return pieces


def retrieve(query: str, docs: list[tuple[str, str]], limit: int = 6) -> list[tuple[str, str]]:
    terms = {t for t in re.findall(r"[a-z0-9]{3,}", query.casefold())}
    scored: list[tuple[int, str, str]] = []
    for name, text in docs:
        for chunk in chunks(text):
            words = set(re.findall(r"[a-z0-9]{3,}", chunk.casefold()))
            score = len(terms & words)
            if score:
                scored.append((score, name, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [(name, chunk) for _, name, chunk in scored[:limit]]


def call_llm(messages: list[dict[str, str]]) -> str | None:
    """Use the OpenAI-compatible Chat Completions endpoint when configured."""
    # Prefer Streamlit's secrets store; environment variables remain a fallback
    # for local development and compatible deployment environments.
    api_key = ""
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if not api_key and "openai" in st.secrets:
            api_key = st.secrets["openai"].get("api_key", "")
    except Exception:
        # Streamlit raises when no secrets file/store is configured.
        pass
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    endpoint = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/chat/completions"
    payload = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": messages,
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, KeyError, IndexError, ValueError, TimeoutError) as exc:
        return f"I couldn't reach the configured language model ({exc}). Please try again later."


def grounded_system(mode: str, context: str) -> str:
    return f"""You are Wanna know Wanda bot, a careful research support assistant for NCSS.
Current service: {mode}.
Use only the source excerpts below for claims that depend on those sources. If they do not contain the answer, say you cannot confirm it from the provided material. Never invent institutional policies, study records, or checklist requirements. For research design and analysis, present the relevant checklist questions to the user in manageable groups, ask for their answers, and offer practical advice tied to their responses and the checklist pointers. Clearly separate source-based information from general research guidance. Explain uncertainty, and do not provide financial, legal, clinical, or healthcare advice. End research design or analysis advice with a reminder that users can request consultation at {CONSULTATION}.

SOURCE EXCERPTS:
{context or '[No matching source excerpts were found.]'}"""


def main() -> None:
    st.set_page_config(page_title="Wanna know Wanda bot", page_icon="🔎", layout="wide")
    st.title("🔎 Wanna know Wanda bot")
    st.markdown("A research support chatbot for finding institutional information and thinking through research design and analysis.")
    with st.expander("Important notice — please read", expanded=False):
        st.markdown(DISCLAIMER, unsafe_allow_html=True)

    with st.sidebar:
        st.header("Choose what you need")
        mode = st.radio("Service", MODES, index=0, label_visibility="collapsed")
        st.divider()
        st.caption("You can change services at any time. Your current conversation remains until you clear it or refresh the session.")

    st.subheader("Add documents for this session")
    st.caption("Upload reference files to help with your research design or analysis conversation. Institutional answers are restricted to the two Knowledge base files listed in the app setup guide.")
    uploads = st.file_uploader(
        "Upload documents",
        type=sorted(SUPPORTED_UPLOADS),
        accept_multiple_files=True,
        help="Supported: TXT, Markdown, CSV, JSON, PDF and DOCX. Uploaded files are used only in research design and analysis modes.",
    )
    uploaded_docs: list[tuple[str, str]] = []
    for item in uploads or []:
        try:
            suffix = Path(item.name).suffix.lower()
            if suffix in {".txt", ".md", ".csv", ".json"}:
                content = item.getvalue().decode("utf-8", errors="replace")
            elif suffix == ".pdf":
                try:
                    from pypdf import PdfReader
                except ImportError as exc:
                    raise RuntimeError("PDF support requires pypdf. Install it with: python -m pip install pypdf") from exc
                content = "\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(item.getvalue())).pages)
            elif suffix == ".docx":
                content = docx_text(item.getvalue())
            else:
                content = ""
            if content.strip():
                uploaded_docs.append((item.name, content))
        except Exception as exc:
            st.warning(f"Could not read {item.name}: {exc}")
    if uploads:
        st.caption(f"{len(uploaded_docs)} of {len(uploads)} uploaded file(s) ready for this session.")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "active_mode" not in st.session_state:
        st.session_state.active_mode = mode
    if st.session_state.active_mode != mode:
        st.session_state.messages = []
        st.session_state.active_mode = mode
    if st.button("Clear conversation", type="secondary"):
        st.session_state.messages = []
        st.rerun()

    if mode == MODES[0]:
        kb_docs = source_documents(KB_DIR, KB_FILES)
        missing = [stem for stem in KB_FILES if find_named_file(KB_DIR, stem) is None]
        if missing:
            expected = "; ".join(f"`{KB_DIR / (name + '.*')}`" for name in missing)
            st.info(
                "Institutional source files are not available yet. Add the supplied files "
                f"{', '.join(f'`{name}`' for name in missing)} to `{KB_DIR}` using a supported extension "
                f"(.txt, .md, .csv, .json, .pdf, or .docx). Expected location: {expected}. "
                "Institutional answers will be limited to these source files."
            )
    else:
        checklist_name = CHECKLIST_FILES[mode]
        checklist_docs = source_documents(CHECKLIST_DIR, [checklist_name])
        missing = not checklist_docs
        if missing:
            st.info(f"Add `{checklist_name}` (any supported extension) to the `Checklist` folder to load the requested prompts and pointers.")
        kb_docs = checklist_docs + uploaded_docs

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not st.session_state.messages:
        if mode == MODES[0]:
            st.caption("Ask about institutional information or whether a similar study has been conducted.")
        elif mode == MODES[1]:
            st.caption("We’ll work through the study design checklist and practical research design advice.")
        else:
            st.caption("We’ll work through the analysis review checklist and practical analysis advice.")

    prompt = st.chat_input("What would you like to know?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        selected = retrieve(prompt, kb_docs) if mode == MODES[0] else kb_docs
        context = "\n\n".join(f"[{name}]\n{text}" for name, text in selected)
        system = grounded_system(mode, context)
        history = [{"role": item["role"], "content": item["content"]} for item in st.session_state.messages[-10:]]
        answer = call_llm([{"role": "system", "content": system}, *history])
        if answer is None:
            if selected:
                excerpts = "\n\n".join(f"**{name}:**\n> {text.replace(chr(10), chr(10) + '> ')}" for name, text in selected)
                if mode == MODES[0]:
                    answer = f"Here are the closest passages I found in the institutional files:\n\n{excerpts}\n\nIs this the information you were looking for, or would you like to conduct a research study and get advice on research design?"
                else:
                    answer = f"These checklist or uploaded document passages may help:\n\n{excerpts}\n\nTell me a little more about your project and I can help you work through them. For a consultation on research design or analysis, contact [{CONSULTATION}](mailto:{CONSULTATION})."
            elif mode == MODES[0]:
                answer = "I couldn’t find a matching passage in the institutional files, so I can’t confirm an answer or whether a related study was conducted. Please check that both `Info for knowledge base` and `Overview of studies` are in the Knowledge base folder and contain searchable text. Is there another institutional topic you’d like to ask about, or would you like to conduct a research study and get advice on research design?"
            else:
                checklist_name = CHECKLIST_FILES[mode]
                answer = f"I don’t have readable checklist passages for this question yet. Add `{checklist_name}` to the Checklist folder. In the meantime, describe your research question, population, data, and constraints, and I can help with general research guidance. For a consultation on research design or analysis, contact [{CONSULTATION}](mailto:{CONSULTATION})."
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
