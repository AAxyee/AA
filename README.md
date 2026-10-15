# 💬 Chatbot template

A simple Streamlit app that shows how to build a chatbot using OpenAI's GPT-3.5.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

### Institutional knowledge sources

Install all dependencies from `requirements.txt`, including `pypdf`, before
starting the app. On an existing deployment, rebuild/restart after updating
requirements so the PDF reader is installed.

Institutional answers use only these document names inside `Knowledge Base/`
(or `Knowledge base/`; folder matching is case-insensitive):

- `Info for knowledge base.pdf`
- `Overview of studies.pdf`

DOCX, TXT, Markdown, CSV and JSON versions with the same base names are also
supported. Other filenames in this folder are excluded from institutional
answers. Do not add confidential documents to a public repository.

Both approved PDFs are included in the repository. The app uses
`Info for knowledge base.pdf` for institutional information and
`Overview of studies.pdf` to identify similar or related studies.
If either file cannot be read, the app reports that limitation and continues
with the approved sources that are available.

Open **Source status** in `streamlit_app.py` or `streamlit_app2.py` to see the
readable sources and per-document loading errors. `streamlit_app1.py` displays
source warnings directly. Image-only/scanned PDFs need searchable text or a
DOCX/text alternative; OCR is not performed by the app.

Run the source-loading regression checks with:

```sh
python -m unittest discover -s tests -v
```

