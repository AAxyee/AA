"""Wanna know Wanda bot — professional, source-grounded research support."""

from __future__ import annotations

import io
import json
import os
import re
import urllib.error
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

import streamlit as st


# ---------------------------------------------------------------------------
# App configuration
# ---------------------------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent

CONSULTATION = "research@ncss.gov.sg"

MODES = (
    "Look for institutional information",
    "Source for new information - Advice on research design",
    "Advice on analysis",
)

DISCLAIMER = """
**Important notice**

This web application is a prototype developed for educational purposes only.
The information provided is not intended to replace professional advice and
should not be relied upon for financial, legal, clinical, or healthcare
decisions. Language models can produce inaccurate information. Always verify
important information against appropriate professional or authoritative sources.
"""

KB_FILES = ("Info for knowledge base", "Overview of studies")

CHECKLIST_FILES = {
    MODES[1]: "Study design checklist",
    MODES[2]: "Analysis review checklist",
}

SUPPORTED_UPLOADS = {"txt", "md", "csv", "json", "pdf", "docx"}


# ---------------------------------------------------------------------------
# Content folders and document handling
# ---------------------------------------------------------------------------

def find_content_folder(name: str) -> Path:
    """Find named content folders and adjacent project directories.

    Source files remain allow-listed by KB_FILES and CHECKLIST_FILES. This
    also supports the Desktop layout where the exact named files are stored
    directly in the adjacent AI bootcamp project directory.
    """
    candidates = [
        APP_DIR / name,
        APP_DIR / "streamlit" / name,
        APP_DIR.parent / name,
        APP_DIR.parent / "streamlit" / name,
    ]

    for base in (APP_DIR,):
        try:
            children = [child for child in base.iterdir() if child.is_dir()]
        except OSError:
            children = []
        for child in children:
            candidates.extend((child / name, child / "streamlit" / name, child))

    expected = (
        KB_FILES if name == "Knowledge base"
        else tuple(CHECKLIST_FILES.values()) if name == "Checklist"
        else ()
    )
    for path in candidates:
        if not path.is_dir():
            continue
        if path.name.casefold() == name.casefold():
            return path
        # Accept a project directory itself only when it contains an exact
        # expected source filename.
        if expected:
            try:
                file_stems = {
                    re.sub(r"\s+", " ", child.stem.strip()).casefold()
                    for child in path.iterdir()
                    if child.is_file()
                }
            except OSError:
                file_stems = set()
            expected_stems = {
                re.sub(r"\s+", " ", stem.strip()).casefold()
                for stem in expected
            }
            if file_stems & expected_stems:
                return path

    # Return the primary expected location so missing-content diagnostics
    # remain meaningful.
    return candidates[0]


KB_DIR = find_content_folder("Knowledge base")
CHECKLIST_DIR = find_content_folder("Checklist")


def docx_text(data: bytes) -> str:
    """Extract paragraph text from DOCX using Python's standard library."""
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        xml_data = archive.read("word/document.xml")

    root = ET.fromstring(xml_data)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    paragraphs = []
    for paragraph in root.findall(".//w:p", ns):
        text = "".join(
            node.text or "" for node in paragraph.findall(".//w:t", ns)
        )
        if text.strip():
            paragraphs.append(text)

    return "\n".join(paragraphs)


def read_text_file(path: Path) -> str:
    """Read a supported source file."""
    suffix = path.suffix.lower()

    try:
        if suffix in {".txt", ".md", ".csv", ".json"}:
            return path.read_text(encoding="utf-8", errors="replace")

        if suffix == ".pdf":
            try:
                from pypdf import PdfReader
            except ImportError:
                return (
                    "[PDF support requires pypdf. "
                    "Install it with: python -m pip install pypdf]"
                )

            return "\n".join(
                page.extract_text() or ""
                for page in PdfReader(str(path)).pages
            )

        if suffix == ".docx":
            return docx_text(path.read_bytes())

    except Exception as exc:
        return f"[Could not read {path.name}: {exc}]"

    return ""


def find_named_file(folder: Path, stem: str) -> Path | None:
    """Find a named source file robustly, including nested deployment folders."""
    if not folder.exists():
        return None

    target = re.sub(r"\s+", " ", stem.strip()).casefold()
    candidates = [p for p in folder.rglob("*") if p.is_file()]
    # Prefer formats that are readable without optional PDF packages. Some
    # source documents are supplied in both DOCX and PDF; picking the PDF
    # first can otherwise silently feed only a missing-library error to RAG.
    extension_rank = {
        ".docx": 0,
        ".txt": 1,
        ".md": 2,
        ".csv": 3,
        ".json": 4,
        ".pdf": 5,
    }
    candidates.sort(key=lambda path: extension_rank.get(path.suffix.lower(), 99))

    # First: exact stem match.
    for path in candidates:
        if re.sub(r"\s+", " ", path.stem.strip()).casefold() == target:
            return path

    # Second: exact filename without extension.
    for path in candidates:
        if re.sub(r"\s+", " ", path.name.rsplit(".", 1)[0].strip()).casefold() == target:
            return path

    return None


def source_documents(
    folder: Path,
    stems: Iterable[str],
) -> list[tuple[str, str]]:
    docs: list[tuple[str, str]] = []

    for stem in stems:
        path = find_named_file(folder, stem)
        if path:
            text = read_text_file(path).strip()
            if text and not text.startswith(("[Could not read ", "[PDF support requires ")):
                docs.append((path.name, text))

    return docs


# ---------------------------------------------------------------------------
# Lightweight retrieval
# ---------------------------------------------------------------------------

def chunks(text: str, size: int = 900) -> list[str]:
    """Split text into reasonably meaningful chunks."""
    pieces: list[str] = []

    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(paragraph) <= size:
            pieces.append(paragraph)
        else:
            pieces.extend(
                paragraph[i:i + size]
                for i in range(0, len(paragraph), size)
            )

    return pieces


def retrieve(
    query: str,
    docs: list[tuple[str, str]],
    limit: int = 10,
) -> list[tuple[str, str]]:
    """Retrieve relevant passages using weighted keyword matching.

    The retrieval is deliberately transparent and dependency-free. Exact
    phrase matches, important query terms, and filename matches receive extra
    weight. If there are no matches, the first useful passage from each source
    is returned rather than sending an empty evidence packet to the model.
    """
    query_text = re.sub(r"\s+", " ", query.casefold()).strip()
    terms = {t for t in re.findall(r"[a-z0-9]{3,}", query_text)}
    stop = {
        "the", "and", "for", "that", "this", "with", "from", "what",
        "how", "can", "does", "are", "was", "were", "about", "study",
        "research", "would", "could", "should", "have", "has", "into",
    }
    useful_terms = terms - stop

    scored: list[tuple[float, int, str, str]] = []

    for doc_index, (name, text) in enumerate(docs):
        name_terms = set(re.findall(r"[a-z0-9]{3,}", name.casefold()))
        for chunk_index, chunk in enumerate(chunks(text)):
            chunk_lower = chunk.casefold()
            words = set(re.findall(r"[a-z0-9]{3,}", chunk_lower))
            overlap = len(useful_terms & words)
            phrase_bonus = 3 if query_text and query_text in chunk_lower else 0
            filename_bonus = 2 if useful_terms & name_terms else 0
            score = overlap * 2 + phrase_bonus + filename_bonus
            scored.append((score, -chunk_index, name, chunk))

    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)

    selected = [
        (name, chunk)
        for score, _, name, chunk in scored
        if score > 0
    ][:limit]

    if selected:
        return selected

    # Never give the model an empty evidence packet when source files exist.
    fallback: list[tuple[str, str]] = []
    for name, text in docs:
        first = chunks(text, size=900)
        if first:
            fallback.append((name, first[0]))
        if len(fallback) >= limit:
            break
    return fallback


# ---------------------------------------------------------------------------
# OpenAI-compatible model call
# ---------------------------------------------------------------------------

def call_llm(messages: list[dict[str, str]]) -> str | None:
    """Call the configured OpenAI-compatible Chat Completions endpoint."""
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

    base_url = os.getenv(
        "OPENAI_BASE_URL",
        "https://api.openai.com/v1",
    ).rstrip("/")

    endpoint = f"{base_url}/chat/completions"

    payload = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        "messages": messages,
        "temperature": 0.15,
        "max_tokens": 2500,
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result["choices"][0]["message"]["content"].strip()

    except (
        urllib.error.URLError,
        KeyError,
        IndexError,
        ValueError,
        TimeoutError,
    ) as exc:
        return (
            "I couldn't reach the configured language model. "
            f"Technical detail: {exc}"
        )


# ---------------------------------------------------------------------------
# Research-support prompt
# ---------------------------------------------------------------------------

def grounded_system(mode: str, context: str) -> str:
    """Create a strong research-support system prompt."""

    common = """
You are Wanna know Wanda, a careful and practical research support assistant
for NCSS.

Your job is to help a researcher think clearly, make defensible methodological
choices, identify weaknesses, and decide what information is needed next.
Reason through the methodological problem internally before answering. Do not
just repeat the checklist or summarize the documents. The user should receive
a considered research recommendation tied to their question, evidence, and
constraints. Do not expose private chain-of-thought; provide the conclusions
and concise methodological rationale instead.

GENERAL RESEARCH ADVICE
- Be methodologically rigorous but explain concepts in plain language.
- Do not simply give a textbook definition. Apply the advice to the user's
  stated research problem.
- Distinguish descriptive, correlational, predictive, and causal questions.
- Do not imply causality from observational or cross-sectional evidence unless
  the design genuinely supports a causal interpretation.
- Flag important threats such as selection bias, non-response, measurement
  error, confounding, reverse causality, missing data, small samples, clustering,
  and overfitting when relevant.
- When recommending a method, explain WHY it fits the question and data.
- Offer a reasonable alternative when there is an important methodological
  trade-off.
- Prefer the simplest defensible design or analysis rather than unnecessary
  complexity.
- Give concrete next steps that a researcher can act on.
- If essential information is missing, ask no more than three focused questions.
- Never invent studies, institutional policies, checklist requirements,
  statistics, citations, or data.

FOR RESEARCH DESIGN
Work through the logic:
1. Research objective and research question.
2. Target population and unit of analysis.
3. Key concepts and how they will be operationalised.
4. Study design and comparison groups, if applicable.
5. Sampling and recruitment.
6. Measures and data sources.
7. Potential bias, confounding, and limitations.
8. Ethics, privacy, and feasibility where relevant.
9. Analysis plan.
10. What conclusions the design can and cannot support.

FOR ANALYSIS
Before recommending a statistical method, consider:
- research question and estimand;
- outcome and predictor variable types;
- study design;
- independence or clustering;
- sample size;
- missing data;
- distributional and model assumptions;
- confounding and covariate selection;
- effect sizes and uncertainty, not only p-values;
- model diagnostics and sensitivity analyses;
- practical interpretation;
- whether the proposed analysis answers the actual research question.

When interpreting results, distinguish statistical significance from substantive
importance and avoid causal language unless justified by the design.

SOURCE USE
The source excerpts supplied below are evidence from the app's knowledge base,
checklists, or documents uploaded by the user.

- If a claim comes from a supplied source, identify it with:
  "(Source: filename)".
- Do not attribute a claim to a source unless the excerpt actually supports it.
- If the supplied sources do not answer a factual institutional question, say so.
- General research methodology may be provided from established methodological
  knowledge, but label it clearly as "General research guidance" when useful.
- Never manufacture a source citation.

RESPONSE STYLE
Use short headings and bullets where they improve readability.
Start with the most useful answer rather than a long preamble.
For research design or analysis, a useful structure is:
- What I would clarify
- Recommended approach
- Why it fits
- Risks / limitations
- Next steps
- Questions for you (only if needed)

Do not overwhelm the user with every possible methodological issue. Prioritise
the issues that materially affect the decision at hand.
"""

    mode_instruction = {
        MODES[0]: """
CURRENT SERVICE: Institutional information.

For this service, institutional facts must be grounded in the supplied
institutional knowledge-base excerpts only. Do not use general knowledge to
fill an institutional gap. If the answer cannot be confirmed from the
provided material, say that clearly and suggest what source or document would
need to be checked.
""",
        MODES[1]: """
CURRENT SERVICE: Source for new information / advice on research design.

Use the study design checklist as a framework rather than dumping the checklist
back to the user. Help the user work through the most relevant questions,
explain why they matter, and translate them into practical design decisions.

You may provide general research-methodology guidance in addition to the
checklist, but clearly distinguish it from checklist/source-based information.
""",
        MODES[2]: """
CURRENT SERVICE: Advice on analysis.

Use the analysis review checklist as a framework rather than merely repeating
it. Help the user diagnose the analysis problem, identify what information is
missing, choose an appropriate method, and understand assumptions and
interpretation.

You may provide general statistical guidance in addition to the supplied
checklist or uploaded documents, but clearly distinguish the two.
""",
    }[mode]

    return (
        common
        + "\n"
        + mode_instruction
        + f"""

CONSULTATION
For research design or analysis matters, users may request a consultation at
{CONSULTATION}. Mention this only when relevant, rather than repeating it
mechanically in every answer.

SOURCE EXCERPTS
The excerpts below are the only supplied documentary evidence available in
this response. They may include institutional knowledge, an NCSS checklist,
or a document uploaded by the researcher. Use them according to their labels.
{context or "[No readable source excerpts were found.]"}
"""
    )


def build_source_packet(
    mode: str,
    query: str,
    kb_docs: list[tuple[str, str]],
    checklist_docs: list[tuple[str, str]],
    uploaded_docs: list[tuple[str, str]],
) -> tuple[str, list[tuple[str, str]]]:
    """Build a focused evidence packet for the current question.

    Institutional knowledge is available in every service. The design and
    analysis services additionally receive their relevant checklist and any
    documents uploaded by the researcher.
    """
    if mode == MODES[0]:
        # Use both full, allow-listed institutional files. This avoids missing
        # relevant studies when user wording differs from the source wording.
        selected = [(name, text[:60000]) for name, text in kb_docs if text.strip()]
        return (
            "\n\n".join(f"[Source: {name}]\n{content}" for name, content in selected),
            selected,
        )

    # Always retrieve the institutional knowledge base as well as the
    # checklist. This is important for research-design questions because
    # previous studies can inform the design and feasibility discussion.
    kb_selected = retrieve(query, kb_docs, limit=8)
    # Always supply the full checklist so the model can use its questions and
    # pointers even when their wording differs from the user's prompt.
    checklist_selected = [
        (name, text[:40000]) for name, text in checklist_docs if text.strip()
    ]
    upload_selected = retrieve(query, uploaded_docs, limit=6) if uploaded_docs else []

    combined: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for item in [*kb_selected, *checklist_selected, *upload_selected]:
        if item not in seen:
            combined.append(item)
            seen.add(item)

    # Keep the evidence packet bounded so the model has room to reason and
    # provide advice rather than spending its context on raw documents.
    combined = combined[:18]
    packet = "\n\n".join(
        f"[Source: {name}]\n{chunk}"
        for name, chunk in combined
    )
    return packet, combined


def infer_question_mode(query: str, selected_mode: str) -> str:
    """Route clear research-method questions from the default service.

    Explicitly chosen design or analysis services always take precedence.
    """
    if selected_mode != MODES[0]:
        return selected_mode

    text = query.casefold()
    analysis_terms = (
        "analysis", "analyse", "analyze", "statistical", "regression",
        "p-value", "p value", "significance", "missing data", "dataset",
        "which test", "which model", "interpret these results",
    )
    design_terms = (
        "research design", "study design", "methodology", "sampling",
        "sample size", "recruitment", "questionnaire", "survey design",
        "research question", "design a study", "design my study",
        "conduct a study", "conduct research", "plan a study",
        "planning a study", "study plan", "comparison group",
    )
    if any(term in text for term in analysis_terms):
        return MODES[2]
    if any(term in text for term in design_terms):
        return MODES[1]
    return selected_mode


# ---------------------------------------------------------------------------
# User interface
# ---------------------------------------------------------------------------

def inject_css() -> None:
    st.markdown(
        """
        <style>
        /* Overall page */
        .stApp {
            background: #f7f8fa;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Header */
        .wanda-header {
            padding: 1.25rem 1.4rem;
            border: 1px solid #e3e7ed;
            border-radius: 16px;
            background: white;
            margin-bottom: 1.2rem;
            box-shadow: 0 2px 12px rgba(20, 30, 50, 0.04);
        }

        .wanda-title {
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.2rem;
        }

        .wanda-subtitle {
            color: #5f6b7a;
            font-size: 0.98rem;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e4e8ee;
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem;
        }

        /* More vertical space between the three service choices */
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 0.8rem;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label {
            padding: 0.72rem 0.75rem;
            border-radius: 10px;
            border: 1px solid transparent;
            transition: background 0.15s ease;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background: #f3f5f8;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
            background: #eef3f8;
            border-color: #d6e0ea;
        }

        .sidebar-brand {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .sidebar-help {
            color: #697586;
            font-size: 0.85rem;
            line-height: 1.45;
        }

        /* Cards */
        .section-card {
            background: white;
            border: 1px solid #e3e7ed;
            border-radius: 14px;
            padding: 1rem 1.15rem;
            margin: 0.7rem 0 1rem 0;
            box-shadow: 0 2px 10px rgba(20, 30, 50, 0.025);
        }

        .section-card-title {
            font-weight: 650;
            margin-bottom: 0.2rem;
        }

        .section-card-text {
            color: #687385;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* Chat */
        div[data-testid="stChatMessage"] {
            border-radius: 14px;
            margin-bottom: 0.65rem;
        }

        div[data-testid="stChatInput"] {
            background: white;
        }

        /* File uploader */
        div[data-testid="stFileUploader"] {
            background: white;
            border-radius: 12px;
        }

        /* Avoid prominent Streamlit info boxes */
        div[data-testid="stAlert"] {
            border-radius: 10px;
        }

        /* Small status text */
        .source-status {
            color: #687385;
            font-size: 0.78rem;
            margin-top: 0.4rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="wanda-header">
            <div class="wanda-title">🔎 Wanna know Wanda</div>
            <div class="wanda-subtitle">
                Research support for institutional information, study design,
                and analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(mode: str) -> None:
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand">Research support</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sidebar-help">'
            'Choose a service. You can switch services at any time.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)

        st.radio(
            "Service",
            MODES,
            index=MODES.index(mode),
            key="mode_selector",
            label_visibility="collapsed",
        )

        st.divider()

        if st.button(
            "Clear conversation",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state.messages = []
            st.rerun()

        st.markdown(
            "<div style='height:0.5rem'></div>",
            unsafe_allow_html=True,
        )

        st.caption(
            "Your conversation stays in this session until you clear it "
            "or refresh the page."
        )


def load_uploaded_documents() -> list[tuple[str, str]]:
    """Read files uploaded for the current session."""
    uploads = st.session_state.get("uploads", [])
    uploaded_docs: list[tuple[str, str]] = []

    for item in uploads:
        try:
            suffix = Path(item.name).suffix.lower()

            if suffix in {".txt", ".md", ".csv", ".json"}:
                content = item.getvalue().decode(
                    "utf-8",
                    errors="replace",
                )

            elif suffix == ".pdf":
                try:
                    from pypdf import PdfReader
                except ImportError:
                    raise RuntimeError(
                        "PDF support requires pypdf. "
                        "Install it with: python -m pip install pypdf"
                    )

                content = "\n".join(
                    page.extract_text() or ""
                    for page in PdfReader(io.BytesIO(item.getvalue())).pages
                )

            elif suffix == ".docx":
                content = docx_text(item.getvalue())

            else:
                content = ""

            if content.strip():
                uploaded_docs.append((item.name, content))

        except Exception as exc:
            st.warning(f"Could not read {item.name}: {exc}")

    return uploaded_docs


def render_upload_area(mode: str) -> list[tuple[str, str]]:
    """Show document upload only where it is useful."""
    if mode == MODES[0]:
        return []

    st.markdown(
        """
        <div class="section-card">
            <div class="section-card-title">Add documents for this session</div>
            <div class="section-card-text">
                Upload a proposal, questionnaire, analysis plan, dataset
                description, or other reference material. Wanda will use it
                alongside the relevant research checklist.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploads = st.file_uploader(
        "Upload documents",
        type=sorted(SUPPORTED_UPLOADS),
        accept_multiple_files=True,
        key="document_uploader",
        help=(
            "Supported: TXT, Markdown, CSV, JSON, PDF and DOCX. "
            "Files are used only in this session."
        ),
    )

    st.session_state.uploads = uploads or []

    uploaded_docs = load_uploaded_documents()

    if uploads:
        st.caption(
            f"{len(uploaded_docs)} of {len(uploads)} uploaded file(s) "
            "ready for this session."
        )

    return uploaded_docs


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(
        page_title="Wanna know Wanda",
        page_icon="🔎",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_css()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "active_mode" not in st.session_state:
        st.session_state.active_mode = MODES[0]

    # Sidebar radio is keyed so mode changes are handled cleanly.
    current_mode = st.session_state.get("mode_selector", MODES[0])

    if current_mode != st.session_state.active_mode:
        st.session_state.messages = []
        st.session_state.active_mode = current_mode
        st.session_state.response_mode = current_mode

    mode = current_mode

    render_sidebar(mode)
    render_header()

    with st.expander("Important notice", expanded=False):
        st.markdown(DISCLAIMER)

    uploaded_docs = render_upload_area(mode)

    # -----------------------------------------------------------------------
    # Select source material
    # -----------------------------------------------------------------------

    # Load the institutional knowledge base for EVERY service.
    # Research-design and analysis questions can therefore draw on both
    # previous/institutional studies and the relevant checklist.
    kb_docs = source_documents(KB_DIR, KB_FILES)

    checklist_docs_by_mode = {
        service: source_documents(CHECKLIST_DIR, [stem])
        for service, stem in CHECKLIST_FILES.items()
    }
    loaded_kb_names = ", ".join(name for name, _ in kb_docs) or "none found"
    st.caption(
        f"Knowledge base sources loaded: {loaded_kb_names}. "
        f"Source folder: {KB_DIR}"
    )
    loaded_checklists = ", ".join(
        name
        for service_docs in checklist_docs_by_mode.values()
        for name, _ in service_docs
    ) or "none found"
    st.caption(f"Research checklist sources loaded: {loaded_checklists}.")

    # -----------------------------------------------------------------------
    # Conversation
    # -----------------------------------------------------------------------

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not st.session_state.messages:
        if mode == MODES[0]:
            st.markdown(
                """
                <div class="section-card">
                    <div class="section-card-title">
                        Search institutional knowledge
                    </div>
                    <div class="section-card-text">
                        Ask about institutional information or whether a
                        similar study appears in the supplied knowledge base.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        elif mode == MODES[1]:
            st.markdown(
                """
                <div class="section-card">
                    <div class="section-card-title">
                        Think through your study design
                    </div>
                    <div class="section-card-text">
                        Describe your research question, population, data, or
                        draft design. Wanda will help identify key decisions,
                        methodological risks, and practical next steps.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            st.markdown(
                """
                <div class="section-card">
                    <div class="section-card-title">
                        Review your analysis
                    </div>
                    <div class="section-card-text">
                        Describe your research question and analysis, or upload
                        your analysis plan or results. Wanda will help assess
                        whether the method matches the question and how results
                        should be interpreted.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    prompt = st.chat_input(
        "Describe your research question, design, data, or analysis..."
    )

    if not prompt:
        return

    response_mode = infer_question_mode(prompt, mode)
    previous_response_mode = st.session_state.get("response_mode", mode)
    short_follow_up = len(prompt.split()) <= 8
    if (
        response_mode == mode
        and previous_response_mode != mode
        and short_follow_up
    ):
        response_mode = previous_response_mode
    st.session_state.response_mode = response_mode
    if response_mode != mode:
        st.caption(
            f"This question looks like {response_mode.lower()}; "
            "I’m using that service and its checklist for this reply."
        )

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build a focused evidence packet. In research-design and analysis modes
    # this includes the institutional knowledge base, the relevant checklist,
    # and any documents uploaded by the researcher.
    context, selected = build_source_packet(
        response_mode,
        prompt,
        kb_docs,
        checklist_docs_by_mode.get(response_mode, []),
        uploaded_docs,
    )

    system = grounded_system(response_mode, context)

    # Keep recent history, but avoid allowing the conversation to grow
    # indefinitely.
    history = [
        {
            "role": item["role"],
            "content": item["content"],
        }
        for item in st.session_state.messages[-12:]
    ]

    answer = call_llm(
        [
            {"role": "system", "content": system},
            *history,
        ]
    )

    model_issue = ""
    if answer and answer.startswith("I couldn't reach the configured language model."):
        model_issue = answer
        answer = None

    # -----------------------------------------------------------------------
    # Graceful fallback when no API key is configured
    # -----------------------------------------------------------------------

    if answer is None:
        if selected:
            excerpts = "\n\n".join(
                f"**{name}:**\n> "
                + (text[:1800].replace("\n", "\n> ") + ("…" if len(text) > 1800 else ""))
                for name, text in selected
            )

            if response_mode == MODES[0]:
                answer = (
                    "I found the following relevant passages in the "
                    "institutional files:\n\n"
                    f"{excerpts}\n\n"
                    "The language model is not currently configured, so I "
                    "cannot provide the research interpretation layer."
                )
            elif response_mode == MODES[1]:
                answer = (
                    "The language model is not available, so I can’t tailor a "
                    "full recommendation yet. As a starting point, align the "
                    "design with the question: use a descriptive design to "
                    "estimate how common something is, repeated measurements "
                    "to study change over time, and a comparison group when "
                    "you need to assess differences between groups. Check "
                    "whether the sample and measures represent the population "
                    "you want to describe, and avoid causal claims from a "
                    "one-time observational survey.\n\n"
                    "To work through the supplied study design checklist, "
                    "please share your research question, target population, "
                    "and what data or access you already have.\n\n"
                    f"{excerpts}"
                )
            else:
                answer = (
                    "The language model is not available, so I can’t tailor "
                    "a full analysis recommendation yet. As a starting point, "
                    "choose the analysis from the outcome type and study "
                    "design, account for clustering and missing data, check "
                    "model assumptions, and report effect sizes with "
                    "uncertainty rather than relying only on p-values.\n\n"
                    "Please share your research question, outcome and key "
                    "predictors, sample size, and study design so the analysis "
                    "review checklist can be applied.\n\n"
                    f"{excerpts}"
                )

        elif response_mode == MODES[0]:
            answer = (
                "I could not find a matching passage in the institutional "
                "knowledge base. I therefore cannot confirm an institutional "
                "answer from the supplied sources."
            )

        elif response_mode == MODES[1]:
            answer = (
                "I can offer general design guidance, but I could not load the "
                "study design checklist. Start by stating the research "
                "question, target population, main outcome, and timeline. "
                "Then choose a design that can answer that question with the "
                "data and access you can realistically obtain. A single "
                "cross-sectional survey can describe or compare responses, "
                "but usually cannot establish that one factor caused another. "
                f"For a consultation, contact {CONSULTATION}."
            )
        else:
            answer = (
                "I can offer general analysis guidance, but I could not load "
                "the analysis review checklist. Please share your research "
                "question, outcome and predictors, study design, and sample "
                "size. Check that the method matches the outcome and design, "
                "review missingness and assumptions, and report effect sizes "
                "with uncertainty. "
                f"For a consultation, contact {CONSULTATION}."
            )

        if model_issue:
            answer += "\n\nThe language model could not be reached: " + model_issue

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )


if __name__ == "__main__":
    main()
