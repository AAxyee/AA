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


### Research-design consultation

When **Source for new information - Advice on research design** is selected,
Wanda uses only **Study design checklist** as the checklist framework, considers
existing evidence before new data collection, and is instructed to recommend a
feasible design with reasons, alternatives, limitations and next steps. Earlier
user requirements are retained as bounded context for longer conversations.

Tailored advice requires the configured language model to be reachable. Without
it, Wanda explicitly says it has not assessed the study and shows the checklist
and starting questions instead. See [the research-design review scenarios](docs/research-design-review.md)
for examples to evaluate with the configured model.

### Model connection settings and troubleshooting

For Streamlit Community Cloud, open the app's **Settings > Secrets**, save the
API configuration there, and retry a new chat message after the app restarts.
Use the empty-key example in [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example)
as a template; do not commit an actual key to GitHub.

```toml
OPENAI_API_KEY = "your-api-key"
OPENAI_MODEL = "gpt-4.1-mini"
OPENAI_BASE_URL = "https://api.openai.com/v1"
```

Alternatively, the same settings can be supplied in one `[openai]` table using
`api_key`, `model` and `base_url`. Top-level Secrets take precedence over the
nested table, then environment variables, then model/endpoint defaults. Lowercase
`openai_api_key`, `openai_model` and `openai_base_url` are also recognised.
The key must belong to the provider specified by the base URL.

The **Language model status** expander reports whether a key was detected and
the last request's outcome without displaying the key. Key presence alone does
not prove validity or model access. Failures distinguish missing configuration,
rejected credentials, permissions, unavailable model/endpoint, quota/billing,
rate limiting, network failure and unusable responses. Temporary failures have
one bounded retry; authentication and quota failures are not blindly retried.

The client uses Chat Completions, omits model-specific temperature assumptions,
and supports providers requiring either output-token parameter name. It does
not switch models or providers automatically. A full `/chat/completions` URL is
accepted without appending that path twice.

References: [Streamlit app settings](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/app-settings)
and [OpenAI API error guidance](https://developers.openai.com/api/docs/guides/error-codes).
