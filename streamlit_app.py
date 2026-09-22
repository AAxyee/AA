<<<<<<< HEAD
import streamlit as st

from openai import OpenAI

import os

 

# --- Page Configuration ---

st.set_page_config(

    page_title="Wanna Know",

    page_icon="🔬",

    layout="wide"

)

 

# --- Embedded Knowledge Base ---

 

KNOWLEDGE_BASE = """

=== KNOWLEDGE BASE DOCUMENTS ===

 

--- Document: Info for knowledge base.docx ---

Social Service Sector: Key Findings Report

 

Overview

This report presents findings from a review of the social service sector conducted across a sample of 42 service providers, encompassing voluntary welfare organisations (VWOs), social service agencies (SSAs), and community-based providers. Data was collected through a combination of surveys, focus group discussions, and administrative records spanning three financial years: FY2022/23, FY2023/24, and FY2024/25.

 

Sector at a Glance: Key Statistics

 

Beneficiaries

The total number of beneficiaries served across the 42 agencies has grown steadily over the review period. In FY2022/23, agencies collectively served 87,450 beneficiaries. This rose to 98,210 in FY2023/24, representing a year-on-year increase of approximately 12.3%. By FY2024/25, the figure had climbed further to 106,840, reflecting a cumulative growth of 22.2% over three years. The increase has been most pronounced in mental health, eldercare, and family support services.

 

Volunteers

Total volunteer numbers across the 42 agencies stood at 14,320 in FY2022/23, rising to 15,780 in FY2023/24 and reaching 17,240 in FY2024/25 — a three-year increase of 20.4%. Regular volunteers (volunteering at least monthly over six or more months) grew from 4,870 in FY2022/23 to 5,430 in FY2023/24 and 6,150 in FY2024/25, accounting for 34.0%, 34.4%, and 35.7% of total volunteers respectively. Total volunteer hours logged were 1,243,600 in FY2022/23, increasing to 1,418,900 in FY2023/24 and 1,587,300 in FY2024/25. Average hours per volunteer rose from 86.8 to 92.1 over the same period.

 

Financial Overview — Income

Total sector income: S$312.4 million (FY2022/23), S$341.7 million (FY2023/24), S$368.9 million (FY2024/25).

- Government grants and funding: S$191.6M / 61.3% (FY2022/23); S$211.9M / 62.0% (FY2023/24); S$228.4M / 61.9% (FY2024/25)

- Donations and fundraising: S$62.5M / 20.0% (FY2022/23); S$66.8M / 19.5% (FY2023/24); S$72.3M / 19.6% (FY2024/25)

- Programme fees and service charges: S$34.4M / 11.0% (FY2022/23); S$37.6M / 11.0% (FY2023/24); S$41.2M / 11.2% (FY2024/25)

- Other income: S$23.9M / 7.7% (FY2022/23); S$25.4M / 7.4% (FY2023/24); S$27.0M / 7.3% (FY2024/25)

 

Financial Overview — Expenditure

Total expenditure: S$298.7M (FY2022/23), S$326.4M (FY2023/24), S$354.1M (FY2024/25). Approximately 11 out of 42 agencies reported deficit positions in FY2024/25.

- Staff costs: S$178.2M / 59.7% (FY2022/23); S$197.5M / 60.5% (FY2023/24); S$216.8M / 61.2% (FY2024/25)

- Programme and service delivery costs: S$58.4M / 19.6% (FY2022/23); S$62.7M / 19.2% (FY2023/24); S$67.3M / 19.0% (FY2024/25)

- Premises and facilities costs: S$26.9M / 9.0% (FY2022/23); S$28.8M / 8.8% (FY2023/24); S$30.4M / 8.6% (FY2024/25)

- Administrative and overhead costs: S$21.5M / 7.2% (FY2022/23); S$22.9M / 7.0% (FY2023/24); S$24.1M / 6.8% (FY2024/25)

- Depreciation and other: S$13.7M / 4.6% (FY2022/23); S$14.5M / 4.4% (FY2023/24); S$15.5M / 4.4% (FY2024/25)

 

Workforce and Talent

Vacancy rates average 18.3% across frontline roles. Social workers, counsellors, and case managers are hardest to fill, with median time-to-hire of 74 days for senior positions. Attrition among staff with fewer than three years of experience stands at 31%, driven by burnout, limited career progression, and compensation gaps. Approximately 67% of agencies increased training budgets in the past financial year, with focus on mental health first aid, trauma-informed care, and digital literacy. 24 out of 42 agencies have formalised peer supervision models. Over 40% of agency directors are expected to retire within the next decade; fewer than a third have a documented succession plan.

 

Service Demand and Client Complexity

Total caseloads rose by approximately 22% over the review period. Increases most pronounced in mental health services, financial assistance, and family violence intervention. Clients present with increasingly complex, multi-layered needs ("complex polyneeds"). Significant rise in working adults seeking assistance. Dementia-related cases increased by 17% year-on-year. Caregiver support programmes are consistently oversubscribed, with waiting times of up to three months.

 

Funding and Financial Sustainability

Government grants account for an average of 61.7% of total revenue across the three-year review period. Administrative burden of grant applications absorbs up to 15% of staff capacity in some smaller organisations. Philanthropic giving rose from S$62.5M (FY2022/23) to S$72.3M (FY2024/25). Outcome-based funding arrangements are being explored with mixed early results.

 

Collaboration and Sector Integration

Inter-agency collaboration has improved but remains variable and often dependent on personal relationships. Integration with healthcare and education systems remains a work in progress. Over 70% of respondents identified sector-wide digital capability building as a priority.

 

--- Document: Overview of Studies for WK.docx ---

 

FY2023 Studies

 

Social Service Sector Survey on Volunteer Management: Examined the state of volunteer management practices across SSAs, focusing on best practices and persistent challenges in volunteer recruitment, retention, and recognition. Findings informed development of the Volunteer Management Maturity Matrix.

 

Digital Acceleration Index (DAI): Assessed the digital maturity of SSAs across key domains including infrastructure, data management, and digital service delivery. Established a baseline for tracking the sector's digital transformation progress.

 

Volunteer Compliance with the Personal Data Protection Act (PDPA): Investigated the extent to which volunteers across SSAs adhere to PDPA requirements, identifying gaps in awareness, training, and organisational oversight.

 

Review of Experiences and Effectiveness of the Employer Support Grant: Evaluated how SSAs utilised the Employer Support Grant, gathering feedback on accessibility, adequacy, and impact on employment outcomes for persons with disabilities and other vulnerable groups.

 

Review of Peer Support Strategy and Peer Support Specialist (PSS) Training: Examined the effectiveness of NCSS' PSS training and practicum structure, identifying areas for enhancement in curriculum design, supervision, and deployment.

 

4ST Perception Poll: Obtained benchmark measurements on the adoption of the four strategic thrusts (4ST) across the sector, providing an indication of agencies' awareness of and progress towards sector-wide strategic priorities.

 

Board Evaluation Survey: Gathered feedback from board members and agency leadership on governance practices, board effectiveness, and areas for capacity building.

 

Organisational Health Framework for Social Services (OHFSS) Self-Assessment Form: Enabled SSAs to assess their own organisational health across multiple dimensions including leadership, people management, financial sustainability, and service quality.

 

NCSS Survey on Organisational Development: Collected feedback from SSAs on the adequacy and relevance of NCSS' support for organisational development.

 

Volunteer Impact Assessment Framework (VIAF): Sought to develop a common language and measurement framework for assessing the impact of volunteerism and volunteer management across SSAs.

 

Volunteer Management Maturity Matrix (VMM Matrix) Analysis: Identified gaps in volunteer management practices among SSAs by mapping agencies against a maturity model.

 

Insights on Sector Awareness and Engagement Efforts: Deepened understanding of public and stakeholder awareness of social sector jobs and career opportunities.

 

Evaluation of Project SAFE 1.1: Assessed the effectiveness of counselling services provided to drug addicts and their families under Project SAFE.

 

Insight into the Sector's Fund Raising Capability: Examined the fundraising capacity of SSAs, identifying gaps in skills, systems, and strategies.

 

FY2024 Studies

 

Stakeholder Study: Explored stakeholders' perceptions of NCSS as an organisation, providing insights to guide brand strategy development and strategic communications planning.

 

Digital Acceleration Index (DAI): Continued annual tracking of digital maturity across SSAs, enabling year-on-year comparison.

 

Organisational Health Framework for Social Services (OHFSS) Self-Assessment Form: Second cycle, allowing for longitudinal tracking of organisational health trends.

 

Insights on Sector Awareness and Engagement Efforts: Built on FY2023 study with updated data on public and stakeholder perceptions of social sector careers.

 

Training Needs Survey: Assessed current and emerging training needs of SSAs on an annual basis.

 

VM Research Study and Social Sector Survey on Volunteer Management: Provided updated data on volunteer management practices, building on the FY2023 baseline.

 

Empowering for Life (ELF) Impact Study: Evaluated outcomes of fund programmes supporting vulnerable populations in skills upgrading, capacity building, and employment.

 

Board Evaluation Survey: Second cycle, enabling longitudinal tracking of governance practices and board effectiveness.

 

4ST Perception Poll: Updated benchmark measurements on sector progress towards the four strategic thrusts.

 

Volunteer Management Maturity Matrix (VMMM): Refined and applied the maturity model developed in FY2023.

 

Learning and Development Roadmap for Volunteer Management Practitioners (VMPs) Self-Assessment Tool: Enabled VMPs to assess their own competencies and identify development priorities.

 

SDT's Study on Tech Stack in Homes: Examined technology infrastructure and digital tools in use across residential care homes.

 

CNPL's Board Leadership Study: Investigated board leadership practices within the social service sector, focusing on governance effectiveness, leadership diversity, and succession planning.

 

Empowerment Service Design Module and Checklist: Evaluated the usability and effectiveness of empowerment-focused service design tools developed for SSAs.

 

Volunteer Impact Assessment Framework (VIAF): Continued development and piloting phase.

 

Organisational Health Diagnostic Scheme (OHDS): Complemented the OHFSS self-assessment with an externally facilitated diagnostic process.

 

Developmental Evaluation of Collective Impact Projects: Assessed the progress and early outcomes of two collective impact initiatives — SHINE's Integrated Wellness Centre and the Bukit Merah project.

 

MyAIMS User Discovery: Explored the user experience of the MyAIMS platform among SSA staff.

 

Sector Perception Study on Social Sector Professionals: Examined how social sector professionals are perceived by the public, employers, and other stakeholders.

 

Study on Work Conditions of Social Sector Professionals: Gathered data on working conditions, job satisfaction, and wellbeing of social sector professionals.

 

FY2025 Studies

 

Survey on Social Sector Development (SSS): Administered to SSAs as part of the annual data collection cycle, tracking key indicators of sector health.

 

Membership Renewal Survey (MRS): Gathered feedback from NCSS member agencies on their membership experience and the value of NCSS' services.

 

Organisational Health Framework for Social Services (OHFSS) Self-Assessment Form: Continued annual cycle.

 

Volunteer Management Maturity Matrix (VMMM): Third cycle, providing longitudinal data on the evolution of volunteer management practices.

 

MyAIMS User Discovery: Continued gathering user feedback on the MyAIMS platform.

 

Sector Perception on Social Sector Professionals: Updated data on public and stakeholder perceptions of social sector careers.

 

Stakeholder Pulse Survey: Captured timely feedback from a broad range of stakeholders including the general public, institutes of higher learning, and private and public sector partners.

 

CNLP's Board Leadership Study: Continued longitudinal examination of board leadership practices.

 

FY2026 Studies

 

Survey on Social Sector Development: Continued annual SSA data collection cycle.

 

Digital Maturity Index (TBC): Proposed evolution of the Digital Acceleration Index with a refined methodology.

 

Organisational Health Framework for Social Services (OHFSS) Self-Assessment Form and Volunteer Management Maturity Matrix (VMMM): Continued respective annual cycles.

 

MyAIMS User Discovery: Maintained ongoing user research function.

 

Stakeholder Perception Pulse Survey: Expanded to include social sector professionals as a sample group.

 

SGSHARE Performance: Evaluated the performance and uptake of the SGSHARE platform.

 

Brand Health Study: Assessed the health of the NCSS brand across key stakeholder groups.

 

NCSS Social Service Tribe CNA Docuseries: Evaluation examined the reach, reception, and impact of the docuseries.

 

President's Challenge: Assessed the outcomes and community impact of President's Challenge-funded programmes.

 

Donor User Service Journey: Mapped the end-to-end experience of donors engaging with NCSS and SSAs.

 

User Journey on Social Media Addiction (TBC): Proposed study examining experiences of individuals and families affected by social media addiction.

 

--- Document: Checklist for Study Design for WK.docx ---

 

Review Checklist for Study Design

 

1. Does the study have a clear purpose or justification?

   - When was the last study conducted on this topic? Space out the study to reduce fatigue on respondents and exercise prudence on the use of resources (cost of study and additional workload on officers).

   - Is conducting a study the best or only way to obtain the information needed, OR are there existing data sources, proxy indicators, or administrative data that could serve the same purpose?

   - Is the information critical to decision-making, work planning, or policy development, or is it good-to-know? Will the Study Owner be able to act on the findings? Avoid asking the good-to-know. Ask the must-know. Only seek critical information that you will utilise meaningfully.

 

Study Design & Methods

 

2. Are the questions or data points well-scoped and purposeful?

   - Do all questions map directly to the key research questions or problem statement? Make sure that the information you seek will sufficiently meet the objectives of your study.

   - Are good-to-know questions minimised or deprioritised to reduce respondent burden and survey fatigue?

   - Are the questions clearly phrased, and is the answer format appropriate?

   - Are there any critical questions that are missing?

 

3. Is the target population most suitable for the study's purposes?

   - Is the target population clearly defined? Is the sample group most suitable for the information you are seeking?

   - Are there any access or ethical considerations in reaching the target population (e.g., vulnerable groups)?

 

4. Is the expected sample size adequate for the planned analysis?

   - Is the sampling approach (e.g., random, stratified) appropriate and clearly justified?

   - For quantitative studies, is there a power calculation or justification for the sample size?

   - For qualitative studies, is the sample size sufficient for meaningful thematic analysis?

 

5. Is the proposed data collection method suitable for answering the study questions?

   - Is the method (e.g., survey, focus group discussion, secondary data analysis) justified given the nature of the study questions?

   - Are there practical or ethical constraints that make the chosen method more or less suitable?

   - Is burden placed on respondents by the proposed method justified against the potential gains of the study?

 

Note: Please reach out to research@ncss.gov.sg if you require further consultation.

 

--- Document: Analysis Review Checklist.docx ---

 

Analysis Review Checklist

 

1. Is the proposed analytical approach appropriate for the study design and research questions?

   - Is the analytical approach consistent with the data collection method and sample size?

   - Is the analytical approach (e.g., descriptive, statistical modelling, thematic) clearly stated and justified?

 

2. Does the analysis plan map back to each study question?

   - Is it clear which analyses address which study question?

   - Are there any study questions that are not addressed by the proposed analysis?

 

3. Are the proposed indicators, variables, or constructs clearly defined and measurable?

   - For quantitative studies, are variables operationalised clearly?

   - For qualitative studies, are themes/constructs grounded in the questions intended for the participants?

 

4. Are limitations and assumptions acknowledged?

   - Has the Study Owner accounted for potential sources of bias (e.g., self-reported data, confounding factors)?

   - Are assumptions about the data or population clearly stated?

 

Note: Please reach out to research@ncss.gov.sg if you require further consultation.

"""

 

# --- System Prompt ---

SYSTEM_PROMPT = f"""You are an internal institutional knowledge assistant that helps staff access information and navigate research processes. You operate in a structured workflow and should always use information from the provided knowledge base embedded below.

 

INTRODUCTION:

You are a research support assistant that helps staff access institutional knowledge and provide study design guidance. For study proposals, you guide users through questions and generate a summary for submission to their director for study approval. For advice on study design and analysis, you run users through a checklist.

 

WORKFLOW ROUTING:

- If user selects "I want information from our database" → proceed to Step 1

- If user selects "I want to conduct a study" → skip to Step 2

- If user selects "I want advice on my study design" → skip to Step 3 (Study Review)

- If user selects "I want advice on my analysis" → skip to Step 4 (Analysis Review)

 

STEP 1 — KNOWLEDGE DATABASE SEARCH:

When users ask questions, search the embedded knowledge base thoroughly.

- Provide comprehensive answers using ONLY information from the embedded documents.

- Always include relevant quotes in this format:

  [1] "Exact quote from document"

  [1] Your response incorporating the quoted information. [2] Additional details as referenced.

- If you find partial information, provide what is available and note any gaps.

- Suggest that the user can state "I cannot find the information I want." if the information is not relevant.

- If the user states they cannot find the information they want, transition to Step 2.

 

STEP 2 — INFORMATION SOURCING & REQUEST ASSISTANCE:

If the knowledge base does not contain the information the user needs:

1. Acknowledge the gap: "I don't see that information in our current knowledge base."

2. Offer two options:

   - Option A: Fill out a form to submit an information request to the Director of Translational Research

   - Option B: Get advice on their proposed study design

   Ask: "Which option would you prefer?"

 

OPTION A — INFORMATION REQUEST PROCESS:

- Ask questions systematically to populate a study information request form, covering fields such as: study title, study objectives, background/rationale, target population, proposed methodology, timeline, and requestor details.

- Format the completed form as:

  **Information Request Form**

  Field 1 — Study Title: [User's response]

  Field 2 — Objectives: [User's response]

  [Continue for all fields]

  **Summary for Submission**

- Organise the responses into a clear summary. Suggest that the user copy and paste this summary and send it to the Director for study approval.

 

OPTION B — STUDY DESIGN GUIDANCE:

- Collect the user's study information systematically (study title, objectives, target population, proposed method, timeline).

- Search the "Overview of Studies for WK" section of the knowledge base for similar studies.

- Present findings in this format:

  **Similar Studies Analysis**

  [1] "Details of similar study from overview of studies for WK"

  **Comparison Results**

  - Similar studies: [Yes/No with details]

  - Key differences: [If applicable]

  - Recommendations: [Based on findings]

- Then proceed to Step 3.

 

STEP 3 — STUDY REVIEW PROCESS (triggered by "I want advice on my study design" or after Option B):

- Reference the "Checklist for Study Design for WK" section of the knowledge base.

- Present all five checklist items systematically and ask the user to respond to each one.

- Format as:

  **Study Review Checklist**

  ☐ Item 1: [Checklist question with sub-points]

  ☐ Item 2: [Checklist question with sub-points]

  ... and so on for all five items.

  **Next Steps**

  Please review each item and let me know if you need clarification on any point.

  Note: For further consultation, please reach out to research@ncss.gov.sg.

 

STEP 4 — ANALYSIS REVIEW PROCESS (triggered by "I want advice on my analysis"):

- Reference the "Analysis Review Checklist" section of the knowledge base.

- Present all four checklist items systematically and ask the user to respond to each one.

- Format as:

  **Analysis Review Checklist**

  ☐ Item 1: [Checklist question with sub-points]

  ☐ Item 2: [Checklist question with sub-points]

  ... and so on for all four items.

  **Next Steps**

  Please review each item and let me know if you need clarification on any point.

  Note: For further consultation, please reach out to research@ncss.gov.sg.

 

GENERAL GUIDELINES:

- Always maintain a professional, collegial tone.

- Be systematic and thorough in your questioning.

- Only use information from the embedded knowledge base documents.

- If documents are unclear or incomplete, state: "The available documentation doesn't provide clear guidance on this. I recommend contacting research@ncss.gov.sg directly."

- Keep users informed about which step of the process they are in.

- Offer to restart or switch between options if users change their mind.

- Before each major transition, summarise what you have covered.

- Use tables and structured formatting (headings, bullet points, checklists) for complex processes.

- Provide clear next steps at the end of each interaction.

 

EMBEDDED KNOWLEDGE BASE:

{KNOWLEDGE_BASE}

"""

 

# --- Intro Message ---

INTRO_MESSAGE = """👋 Welcome! I am your **Research Support Assistant**.

 

I help staff access institutional knowledge and provide study design guidance. For study proposals, I will guide you through a few questions and generate a summary for submission to your director for study approval. For advice on your study design and analysis, I will run you through a checklist.

 

Please select one of the options below to get started.

 

---

 

**What would you like to do today?**"""

 

OPTIONS = [

    "I want information from our database",

    "I want to conduct a study",

    "I want advice on my study design",

    "I want advice on my analysis"

]

 

# --- Helper Functions ---

 

def get_api_key():

    """Retrieve API key from Streamlit secrets or environment."""

    if "openai" in st.secrets and "api_key" in st.secrets["openai"]:

        return st.secrets["openai"]["api_key"]

    return os.environ.get("OPENAI_API_KEY", "")

 

def get_ai_response(client, messages_history):

    """Call the OpenAI API and return the assistant's response."""

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages_history

 

    response = client.chat.completions.create(

        model="gpt-4o",

        messages=api_messages,

        temperature=0.2,

        max_tokens=2000,

    )

    return response.choices[0].message.content

 

def reset_conversation():

    """Reset the chat to its initial state."""

    st.session_state.messages = []

    st.session_state.option_selected = False

 

# --- Session State Initialisation ---

if "messages" not in st.session_state:

    st.session_state.messages = []

 

if "option_selected" not in st.session_state:

    st.session_state.option_selected = False

 

# --- Sidebar ---

with st.sidebar:

    st.title("⚙️ Configuration")

 

    api_key_input = st.text_input(

        "OpenAI API Key",

        type="password",

        value=get_api_key(),

        help="Enter your OpenAI API key. You can also set this via Streamlit secrets or the OPENAI_API_KEY environment variable."

    )

 

    st.divider()

    st.subheader("📋 Knowledge Base")

    st.success("✅ Info for knowledge base")

    st.success("✅ Overview of studies for WK")

    st.success("✅ Checklist for study design for WK")

    st.success("✅ Analysis review checklist")

    st.caption("All knowledge base documents are embedded in this application.")

 

    st.divider()

 

    if st.button("🔄 Restart Conversation", use_container_width=True):

        reset_conversation()

        st.rerun()

 

    st.divider()

    st.caption("Research Support Assistant v1.0")

 

# --- Main Chat Interface ---

st.title("🔬 Research Support Assistant")

 

# Validate API key

api_key = api_key_input or get_api_key()

if not api_key:

    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to begin.")

    st.stop()

 

client = OpenAI(api_key=api_key)

 

# Display intro and option buttons if no option has been selected yet

if not st.session_state.option_selected:

    st.markdown(INTRO_MESSAGE)

 

    cols = st.columns(2)

    for i, option in enumerate(OPTIONS):

        col = cols[i % 2]

        with col:

            if st.button(option, key=f"option_{i}", use_container_width=True):

                st.session_state.option_selected = True

                st.session_state.messages.append({

                    "role": "user",

                    "content": option

                })

                st.rerun()

 

# Display chat history

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

 

# Generate AI response if the last message is from the user

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = get_ai_response(client, st.session_state.messages)

                st.markdown(response)

                st.session_state.messages.append({

                    "role": "assistant",

                    "content": response

                })

            except Exception as e:

                st.error(f"⚠️ An error occurred: {str(e)}")

 

# Chat input and workflow switcher (only shown after an option has been selected)

if st.session_state.option_selected:

    with st.expander("🔀 Switch workflow or restart"):

        st.caption("You can switch to a different workflow at any time.")

        cols = st.columns(2)

        for i, option in enumerate(OPTIONS):

            col = cols[i % 2]

            with col:

                if st.button(option, key=f"switch_{i}", use_container_width=True):

                    st.session_state.messages.append({

                        "role": "user",

                        "content": f"I'd like to switch to: {option}"

                    })

                    st.rerun()

 

    if user_input := st.chat_input("Type your message here..."):

        st.session_state.messages.append({

            "role": "user",

            "content": user_input

        })

        st.rerun()
=======
"""
Institutional Research Support Assistant

Streamlit application for:

1. Institutional knowledge search
2. Study proposal / information sourcing
3. Study design guidance
4. Analysis review

Knowledge base:
- Info for knowledge base
- overview of studies for WK
- NCSS Studies form
- Checklist for study design for WK
- Analysis review checklist for WK

IMPORTANT:

The OpenAI API key is NOT entered by users.

It must be configured as a Streamlit secret:

OPENAI_API_KEY = "your-api-key-here"

Knowledge documents are stored in the application's:

Knowledge Base/

folder and are loaded automatically.

Users may also upload PDF, DOCX, or TXT documents.
Uploaded documents are treated as user-provided material
and are NOT added to the permanent Knowledge Base.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Dict, List, Tuple

import re

import streamlit as st
from docx import Document
from openai import OpenAI
from pypdf import PdfReader


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Research Support Assistant",
    page_icon="📚",
    layout="wide",
)


# ============================================================
# OPENAI CONFIGURATION
# ============================================================

# The API key is stored server-side in Streamlit Secrets.
# Users never see or enter the key.

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error(
        "The application has not been configured with an OpenAI API key. "
        "Please contact the application administrator."
    )
    st.stop()


# ============================================================
# KNOWLEDGE BASE CONFIGURATION
# ============================================================

# Knowledge documents are stored in this folder.

KNOWLEDGE_BASE_DIR = Path("Knowledge Base")


DOCUMENT_NAMES = {
    "Info for knowledge base": "General institutional knowledge",
    "overview of studies for WK": "Previous WK studies",
    "NCSS Studies form": "Study request form",
    "Checklist for study design for WK": "Study design checklist",
    "Analysis review checklist for WK": "Analysis review checklist",
}


MODE_LABELS = {
    "knowledge": "Knowledge Database Search",
    "study": "Information Sourcing & Study Request",
    "design": "Study Design Guidance",
    "analysis": "Analysis Review",
}


MODE_DOCUMENTS = {
    "knowledge": [
        "Info for knowledge base",
        "overview of studies for WK",
    ],
    "study": [
        "NCSS Studies form",
        "Info for knowledge base",
    ],
    "design": [
        "NCSS Studies form",
        "overview of studies for WK",
        "Checklist for study design for WK",
    ],
    "analysis": [
        "Analysis review checklist for WK",
        "overview of studies for WK",
    ],
}


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an internal institutional research support assistant.

Your job is to help research staff using ONLY:

1. The supplied institutional knowledge-base excerpts;
2. Documents uploaded by the user during the conversation;
3. Information explicitly provided by the user.

CORE RULES
----------

1. Do not invent institutional policies, procedures, study details,
   form fields, previous studies, recommendations, requirements,
   deadlines, approval processes, or statistical guidance.

2. Treat the supplied institutional knowledge-base excerpts as the
   authoritative institutional knowledge source.

3. If the institutional knowledge-base excerpts do not contain the
   answer, say:

   "I don't see that information in our current knowledge base."

   Then explain what information is missing and, where appropriate,
   direct the user to the relevant information-request, study-design,
   or analysis-review process.

4. Never present an inference as an institutional fact.

5. Distinguish clearly between:

   - information explicitly stated in the institutional documents;
   - information supplied by the user;
   - information contained in a user-uploaded document;
   - general methodological suggestions.

6. When making a factual claim based on the institutional knowledge
   base, cite the supporting source using the supplied citation number.

   Example:

   [1] "Exact text from the supplied document."

7. Quotations from institutional source excerpts must be copied exactly.
   Do not fabricate quotations.

8. If the source material is insufficient to answer a question,
   ask a focused follow-up question rather than guessing.

9. Maintain a professional, collegial tone appropriate for internal
   institutional research staff.

10. Always identify the current workflow step.

11. Always provide a clear next step.

12. For multi-step workflows, briefly summarize what has already been
    established before moving to the next major step.

13. Do not claim that a study, policy, procedure, or recommendation
    exists unless it appears in the supplied institutional documents.

14. User-uploaded documents are NOT part of the institutional
    knowledge base.

15. Information taken from a user-uploaded document must be identified
    as coming from that uploaded document.

16. Do not cite user-uploaded documents using institutional
    [SOURCE n] citations.

17. Identify user-uploaded documents by filename when referring to
    information contained in them.

18. If a user-uploaded document conflicts with the institutional
    knowledge base, clearly identify the conflict. Do not silently
    resolve the conflict.

19. Do not assume that information in a user-uploaded document is
    institutional policy or an institutional requirement.

20. General methodological suggestions must be clearly identified as
    general suggestions rather than institutional requirements.

WORKFLOW RULES
--------------

KNOWLEDGE MODE
--------------

Answer questions using the institutional knowledge base.

Prioritize relevant institutional knowledge and previous WK studies.

If a user-uploaded document is relevant, you may use it as additional
user-provided context, but distinguish it from institutional knowledge.

STUDY MODE
----------

Help the user develop a study request using the NCSS Studies form.

Collect information systematically, including information that is
explicitly represented in the supplied form or documents.

Do not invent additional mandatory form fields.

Keep track of information already supplied by the user.

If the user uploads a study proposal or related document, use it as
user-provided information and distinguish it from the institutional
form or knowledge base.

DESIGN MODE
-----------

Help the user think through study design using:

- the study request information;
- previous WK studies;
- the study design checklist;
- relevant user-uploaded documents.

Do not declare a design "approved" or "appropriate" unless the
institutional documents explicitly provide such a criterion.

ANALYSIS MODE
-------------

Review the user's proposed analysis against the supplied
analysis-review checklist.

Separate:

- checklist requirements;
- information supplied by the user;
- information contained in uploaded documents;
- methodological observations.

Do not fabricate statistical requirements that are not supported by
the supplied checklist.

RESPONSE STRUCTURE
------------------

Where useful, use:

## Current step

## What I found

## What we have established

## Next step

Use tables and checklists when they improve clarity.
"""


# ============================================================
# SESSION STATE
# ============================================================

def initialise_session() -> None:
    """Initialise application state."""

    defaults = {
        "messages": [],
        "mode": None,
        "workflow_step": 0,
        "form_data": {},
        "documents": {},
        "document_stats": {},
        "uploaded_documents": {},
        "uploaded_document_stats": {},
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialise_session()


# ============================================================
# TEXT EXTRACTION FROM KNOWLEDGE BASE FILES
# ============================================================

def extract_text_from_path(file_path: Path) -> str:
    """
    Extract text from PDF, DOCX or TXT files.
    """

    suffix = file_path.suffix.lower()

    try:

        if suffix == ".pdf":

            reader = PdfReader(str(file_path))

            pages = []

            for page in reader.pages:
                pages.append(page.extract_text() or "")

            return "\n\n".join(pages)

        if suffix == ".docx":

            document = Document(str(file_path))

            paragraphs = [
                paragraph.text.strip()
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            return "\n\n".join(paragraphs)

        if suffix == ".txt":

            return file_path.read_text(
                encoding="utf-8",
                errors="replace",
            )

    except Exception as exc:

        st.warning(
            f"Could not read '{file_path.name}': {exc}"
        )

    return ""


# ============================================================
# TEXT EXTRACTION FROM USER-UPLOADED FILES
# ============================================================

def extract_text_from_uploaded_file(uploaded_file) -> str:
    """
    Extract text from a Streamlit-uploaded PDF, DOCX or TXT file.

    The uploaded file remains in the current Streamlit session and
    is not written into the permanent Knowledge Base folder.
    """

    suffix = Path(uploaded_file.name).suffix.lower()

    try:

        file_bytes = uploaded_file.getvalue()

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        if suffix == ".pdf":

            reader = PdfReader(
                BytesIO(file_bytes)
            )

            pages = []

            for page in reader.pages:
                pages.append(
                    page.extract_text() or ""
                )

            return "\n\n".join(pages)

        # ----------------------------------------------------
        # DOCX
        # ----------------------------------------------------

        if suffix == ".docx":

            document = Document(
                BytesIO(file_bytes)
            )

            paragraphs = [
                paragraph.text.strip()
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            return "\n\n".join(paragraphs)

        # ----------------------------------------------------
        # TXT
        # ----------------------------------------------------

        if suffix == ".txt":

            return file_bytes.decode(
                "utf-8",
                errors="replace",
            )

    except Exception as exc:

        st.error(
            f"Could not read '{uploaded_file.name}': {exc}"
        )

    return ""


# ============================================================
# TEXT CLEANING AND CHUNKING
# ============================================================

def normalise_text(text: str) -> str:
    """
    Normalise whitespace while preserving paragraph structure.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Collapse spaces and tabs.
    text = re.sub(r"[ \t]+", " ", text)

    # Preserve paragraph breaks.
    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text,
    )

    return text.strip()


def split_into_chunks(
    text: str,
    max_words: int = 180,
) -> List[str]:
    """
    Split documents into reasonably sized semantic chunks.

    First split on blank lines, then combine short paragraphs
    until approximately max_words is reached.
    """

    text = normalise_text(text)

    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(
            r"\n\s*\n+",
            text,
        )
        if paragraph.strip()
    ]

    chunks = []

    current = []
    current_words = 0

    for paragraph in paragraphs:

        words = paragraph.split()
        word_count = len(words)

        if (
            current
            and current_words + word_count > max_words
        ):

            chunks.append(
                "\n\n".join(current)
            )

            current = []
            current_words = 0

        current.append(paragraph)
        current_words += word_count

    if current:
        chunks.append(
            "\n\n".join(current)
        )

    return chunks


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

def identify_document_key(
    filename: str,
) -> str | None:
    """
    Match a filename to one of the recognised institutional
    document names.

    Matching is case-insensitive.
    """

    filename_lower = filename.lower()

    for key in DOCUMENT_NAMES:

        if key.lower() in filename_lower:
            return key

    return None


def load_knowledge_base() -> Tuple[
    Dict[str, str],
    Dict[str, dict],
]:
    """
    Load all PDF, DOCX and TXT documents from the Knowledge Base folder.

    Recognised documents are stored using their logical document name.

    Unrecognised documents are also retained using their filename.
    """

    documents: Dict[str, str] = {}
    document_stats: Dict[str, dict] = {}

    if not KNOWLEDGE_BASE_DIR.exists():
        return documents, document_stats

    if not KNOWLEDGE_BASE_DIR.is_dir():
        return documents, document_stats

    supported_extensions = {
        ".pdf",
        ".docx",
        ".txt",
    }

    # rglob allows subfolders inside Knowledge Base as well.
    files = sorted(
        file_path
        for file_path in KNOWLEDGE_BASE_DIR.rglob("*")
        if (
            file_path.is_file()
            and file_path.suffix.lower()
            in supported_extensions
        )
    )

    for file_path in files:

        text = extract_text_from_path(
            file_path
        )

        if not text.strip():
            continue

        text = normalise_text(text)

        matched_key = identify_document_key(
            file_path.name
        )

        if matched_key:
            document_key = matched_key
        else:
            # Preserve other knowledge-base documents.
            document_key = file_path.name

        documents[document_key] = text

        document_stats[document_key] = {
            "words": len(text.split()),
            "chunks": len(
                split_into_chunks(text)
            ),
            "filename": file_path.name,
            "path": str(file_path),
        }

    return documents, document_stats


# Load documents from the server-side Knowledge Base folder.

documents, document_stats = load_knowledge_base()

st.session_state.documents = documents
st.session_state.document_stats = document_stats


# ============================================================
# RETRIEVAL
# ============================================================

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "what",
    "when",
    "where",
    "which",
    "would",
    "could",
    "should",
    "about",
    "have",
    "has",
    "are",
    "was",
    "were",
    "how",
    "why",
    "can",
    "does",
    "into",
    "our",
    "their",
    "your",
    "you",
    "use",
    "using",
}


def tokenise(text: str) -> List[str]:
    """
    Return useful searchable terms.
    """

    words = re.findall(
        r"[a-zA-Z0-9][a-zA-Z0-9_-]{2,}",
        text.lower(),
    )

    return [
        word
        for word in words
        if word not in STOPWORDS
    ]


def score_chunk(
    query: str,
    chunk: str,
) -> float:
    """
    Simple lexical retrieval score.

    This is deliberately transparent and does not pretend
    to be semantic retrieval.
    """

    query_words = set(
        tokenise(query)
    )

    chunk_words = set(
        tokenise(chunk)
    )

    if not query_words:
        return 0.0

    overlap = query_words.intersection(
        chunk_words
    )

    score = len(overlap)

    # Slightly reward exact phrase matches.
    query_normalised = " ".join(
        tokenise(query)
    )

    chunk_normalised = " ".join(
        tokenise(chunk)
    )

    if (
        query_normalised
        and query_normalised
        in chunk_normalised
    ):
        score += 5

    return float(score)


def relevant_excerpts(
    documents: Dict[str, str],
    query: str,
    preferred: List[str] | None = None,
    limit: int = 8,
) -> List[Tuple[float, str, str]]:
    """
    Retrieve relevant chunks from the institutional knowledge base.
    """

    ranked = []

    allowed_documents = (
        preferred
        if preferred
        else list(documents.keys())
    )

    for name in allowed_documents:

        if name not in documents:
            continue

        chunks = split_into_chunks(
            documents[name]
        )

        for chunk in chunks:

            score = score_chunk(
                query,
                chunk,
            )

            if score > 0:

                ranked.append(
                    (
                        score,
                        name,
                        chunk,
                    )
                )

    ranked.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    # Avoid returning many nearly identical chunks.
    results = []
    seen = set()

    for item in ranked:

        _, name, chunk = item

        fingerprint = (
            name,
            re.sub(
                r"\s+",
                " ",
                chunk.lower(),
            )[:250],
        )

        if fingerprint in seen:
            continue

        seen.add(fingerprint)

        results.append(item)

        if len(results) >= limit:
            break

    return results


# ============================================================
# DOCUMENT CONTEXT
# ============================================================

def build_document_context(
    documents: Dict[str, str],
    query: str,
    preferred: List[str] | None = None,
    limit: int = 8,
) -> str:
    """
    Build numbered source excerpts for the model.
    """

    excerpts = relevant_excerpts(
        documents=documents,
        query=query,
        preferred=preferred,
        limit=limit,
    )

    if not excerpts:

        return (
            "No relevant excerpts were found in the "
            "institutional knowledge base."
        )

    blocks = []

    for index, (_, name, quote) in enumerate(
        excerpts,
        start=1,
    ):

        display_name = DOCUMENT_NAMES.get(
            name,
            name,
        )

        blocks.append(
            f"[SOURCE {index}]\n"
            f"Document: {display_name}\n"
            f"Document key: {name}\n"
            f"Excerpt:\n{quote}"
        )

    return "\n\n".join(blocks)


# ============================================================
# USER-UPLOADED DOCUMENT CONTEXT
# ============================================================

def build_uploaded_document_context() -> str:
    """
    Build context from documents uploaded by the user.

    Uploaded documents are treated as user-provided material,
    not as institutional knowledge-base documents.
    """

    uploaded_documents = st.session_state.get(
        "uploaded_documents",
        {},
    )

    if not uploaded_documents:

        return (
            "No user-uploaded documents were provided."
        )

    blocks = []

    for index, (filename, text) in enumerate(
        uploaded_documents.items(),
        start=1,
    ):

        chunks = split_into_chunks(
            text,
            max_words=180,
        )

        # Limit the amount of uploaded content sent to the model.
        # This prevents very large documents from overwhelming
        # the prompt.
        limited_chunks = chunks[:20]

        blocks.append(
            f"[USER DOCUMENT {index}]\n"
            f"Filename: {filename}\n"
            f"Content:\n"
            + "\n\n".join(
                limited_chunks
            )
        )

    return "\n\n".join(blocks)


# ============================================================
# STUDY WORKFLOW STATE
# ============================================================

STUDY_FIELDS = [
    ("purpose", "Study purpose"),
    ("population", "Population"),
    ("setting", "Setting"),
    ("research_question", "Main research question"),
    ("outcomes", "Main outcomes"),
    ("design", "Proposed study design"),
    ("data_source", "Data source"),
    ("analysis", "Planned analysis"),
]


def update_form_data_from_prompt(
    prompt: str,
) -> None:
    """
    Store information supplied by the user.

    This intentionally does not try to infer answers using an LLM.
    """

    st.session_state.form_data[
        "latest_user_input"
    ] = prompt


def workflow_summary() -> str:
    """
    Return a compact summary of collected study information.
    """

    if not st.session_state.form_data:

        return (
            "No study information has been recorded yet."
        )

    lines = []

    for key, label in STUDY_FIELDS:

        value = st.session_state.form_data.get(
            key
        )

        if value:

            lines.append(
                f"- **{label}:** {value}"
            )

    latest = st.session_state.form_data.get(
        "latest_user_input"
    )

    if latest and not lines:

        lines.append(
            f"- **Latest information provided:** {latest}"
        )

    return (
        "\n".join(lines)
        or "No study information has been recorded yet."
    )


# ============================================================
# OPENAI
# ============================================================

@st.cache_resource
def get_client() -> OpenAI:
    """
    Create a cached OpenAI client using the server-side secret.

    The API key is never shown to users.
    """

    return OpenAI(
        api_key=OPENAI_API_KEY
    )


def generate_response(
    client: OpenAI,
    model: str,
    mode: str,
    user_prompt: str,
    documents: Dict[str, str],
) -> str:
    """
    Generate a grounded response using the current workflow.
    """

    preferred = MODE_DOCUMENTS.get(
        mode,
        list(documents.keys()),
    )

    # --------------------------------------------------------
    # Institutional knowledge-base context
    # --------------------------------------------------------

    context = build_document_context(
        documents=documents,
        query=user_prompt,
        preferred=preferred,
        limit=8,
    )

    # --------------------------------------------------------
    # User-uploaded document context
    # --------------------------------------------------------

    uploaded_context = (
        build_uploaded_document_context()
    )

    # --------------------------------------------------------
    # Existing study workflow information
    # --------------------------------------------------------

    study_context = workflow_summary()

    # --------------------------------------------------------
    # Complete prompt
    # --------------------------------------------------------

    workflow_instruction = f"""
CURRENT WORKFLOW
----------------

Mode: {MODE_LABELS.get(mode, mode)}

Current workflow step:

{st.session_state.workflow_step}


INFORMATION ALREADY PROVIDED BY THE USER
----------------------------------------

{study_context}


SUPPLIED INSTITUTIONAL KNOWLEDGE-BASE EXCERPTS
-----------------------------------------------

{context}


USER-UPLOADED DOCUMENTS
-----------------------

The following documents were uploaded by the user
during this conversation.

These are NOT part of the institutional knowledge base.

Treat them as user-provided information.

{uploaded_context}


USER'S CURRENT MESSAGE
----------------------

{user_prompt}
"""

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_PROMPT,
        input=workflow_instruction,
    )

    return response.output_text


# ============================================================
# UI HELPERS
# ============================================================

def reset_chat() -> None:
    """
    Reset workflow, conversation and uploaded documents.
    """

    st.session_state.messages = []

    st.session_state.mode = None

    st.session_state.workflow_step = 0

    st.session_state.form_data = {}

    st.session_state.uploaded_documents = {}

    st.session_state.uploaded_document_stats = {}


def add_assistant_message(
    content: str,
) -> None:
    """
    Add an assistant message.
    """

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": content,
        }
    )


def show_workflow_status() -> None:
    """
    Display current workflow status.
    """

    mode = st.session_state.mode

    if not mode:

        st.info(
            "Choose one of the four workflows below to begin."
        )

        return

    st.markdown(
        f"""
### Current workflow

**{MODE_LABELS.get(mode, mode)}**

Workflow step: **{st.session_state.workflow_step}**
"""
    )


def show_document_status() -> None:
    """
    Display institutional knowledge-base status.
    """

    if not KNOWLEDGE_BASE_DIR.exists():

        st.error(
            f"The knowledge-base folder was not found: "
            f"`{KNOWLEDGE_BASE_DIR}`"
        )

        return

    if not st.session_state.documents:

        st.warning(
            "No PDF, DOCX, or TXT knowledge documents were found "
            "in the Knowledge Base folder."
        )

        return

    st.success(
        f"{len(st.session_state.documents)} "
        "knowledge document(s) loaded automatically."
    )

    with st.expander(
        "Knowledge base status"
    ):

        for key, description in DOCUMENT_NAMES.items():

            if key in st.session_state.documents:

                stats = (
                    st.session_state.document_stats.get(
                        key,
                        {},
                    )
                )

                st.write(
                    f"✓ **{description}** — "
                    f"{stats.get('words', 0):,} words, "
                    f"{stats.get('chunks', 0)} chunks"
                )

            else:

                st.write(
                    f"○ **{description}** — not found"
                )

        # Show any additional documents.

        recognised_keys = set(
            DOCUMENT_NAMES.keys()
        )

        additional_documents = [
            key
            for key in st.session_state.documents
            if key not in recognised_keys
        ]

        if additional_documents:

            st.markdown(
                "**Additional knowledge-base documents**"
            )

            for key in additional_documents:

                stats = (
                    st.session_state.document_stats.get(
                        key,
                        {},
                    )
                )

                st.write(
                    f"✓ **{key}** — "
                    f"{stats.get('words', 0):,} words, "
                    f"{stats.get('chunks', 0)} chunks"
                )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Setup")

    # The user does NOT enter an API key.
    # This only confirms that the administrator
    # has configured the application.

    st.success(
        "OpenAI API configured"
    )

    model = st.selectbox(
        "Model",
        [
            "gpt-5.6-luna",
            "gpt-5.6-terra",
            "gpt-5.6-sol",
        ],
        index=0,
    )

    st.divider()

    st.header("📚 Knowledge Base")

    st.info(
        "Institutional knowledge documents are loaded "
        "automatically from the application's "
        "`Knowledge Base` folder."
    )

    st.caption(
        f"Folder: `{KNOWLEDGE_BASE_DIR}`"
    )

    st.caption(
        f"{len(documents)} document(s) loaded."
    )

    st.divider()

    if st.button(
        "Restart conversation",
        use_container_width=True,
    ):

        reset_chat()

        st.rerun()


# ============================================================
# MAIN APPLICATION
# ============================================================

st.title(
    "📚 Research Support Assistant"
)

st.caption(
    "Institutional knowledge, study proposal support, "
    "study design guidance, and analysis review"
)


# ============================================================
# IMPORTANT NOTICE
# ============================================================

with st.expander(
    "⚠️ IMPORTANT NOTICE — Please read before using this application",
    expanded=True,
):

    st.markdown(
        """
        <div style="
            padding: 1.25rem;
            border: 2px solid #d97706;
            border-radius: 10px;
            background-color: #fff7ed;
            margin: 0.25rem 0 0.75rem 0;
        ">

        <h3 style="margin-top: 0;">
            IMPORTANT NOTICE
        </h3>

        <p>
            This web application is a prototype developed for
            <strong>educational purposes only</strong>.
            The information provided here is
            <strong>NOT intended for real-world use</strong>
            and should not be relied upon for making decisions,
            especially those related to financial, legal, or
            healthcare matters.
        </p>

        <p>
            Please also be aware that the LLM may generate
            inaccurate, incomplete, or incorrect information.
        </p>

        <p>
            <strong>
                You assume responsibility for how you use any
                generated output.
            </strong>
        </p>

        <p style="margin-bottom: 0;">
            Always consult qualified professionals for accurate
            and personalised advice.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# INTRODUCTION
# ============================================================

if not st.session_state.messages:

    intro = """
I am a research support assistant for institutional research staff.

I can help with four workflows:

1. **Institutional knowledge search**
2. **Study proposal / information sourcing**
3. **Study design guidance**
4. **Analysis review**

My answers are grounded in the institutional documents stored
in the application's **Knowledge Base** folder and information
that you provide during the conversation.

You can also upload a PDF, DOCX, or TXT document to provide
additional material for the current conversation.

Please choose a workflow below to begin.
"""

    add_assistant_message(intro)


# ============================================================
# STATUS
# ============================================================

show_document_status()

show_workflow_status()


# ============================================================
# CONVERSATION
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# WORKFLOW SELECTION
# ============================================================

st.subheader(
    "Start here"
)


options = {
    "I want information from our database": "knowledge",
    "I want to conduct a study": "study",
    "I want advice on my study design": "design",
    "I want advice on my analysis": "analysis",
}


selected = st.radio(
    "Choose a workflow",
    list(options.keys()),
    horizontal=True,
    label_visibility="collapsed",
)


if st.button(
    "Continue",
    type="primary",
):

    mode = options[selected]

    st.session_state.mode = mode

    st.session_state.workflow_step = 1

    prompts = {

        "knowledge": """
## Step 1: Knowledge Database Search

Tell me what you would like to find in the institutional
knowledge base.

I will search the institutional documents stored in the
Knowledge Base folder and identify the relevant information
and sources.

You may also upload a document if you want me to consider
user-provided material alongside the institutional sources.
""",

        "study": """
## Step 1: Study Information & Request

I will help you work through the study-request process using
the **NCSS Studies form**.

Please describe whatever you already know about the proposed
study, such as its purpose, population, setting, and main
research question.

You do not need to provide everything at once.

You can also upload a draft study proposal or other relevant
document for me to consider.
""",

        "design": """
## Step 1: Study Design Guidance

I will first establish the study information you already have.

I will then use the previous WK studies and the study-design
checklist to structure the design discussion.

Please describe the study purpose, population, setting,
research question, proposed design, and data source if known.

You can also upload a study proposal or related document.
""",

        "analysis": """
## Step 1: Analysis Review

I will review your proposed analysis against the
**Analysis review checklist for WK**.

Please describe what you are trying to analyse, including
the outcome, predictors, data structure, and planned analysis
if these are already known.

You can also upload your analysis plan, output, or related
document for review.
""",
    }

    add_assistant_message(
        prompts[mode]
    )

    st.rerun()


# ============================================================
# USER DOCUMENT UPLOAD
# ============================================================

st.divider()

st.subheader(
    "📎 Upload a document"
)

st.caption(
    "Upload a PDF, DOCX, or TXT document to provide additional "
    "material for this conversation. Uploaded documents are "
    "treated as user-provided information and are not added "
    "to the institutional Knowledge Base."
)


uploaded_files = st.file_uploader(
    "Choose document(s)",
    type=[
        "pdf",
        "docx",
        "txt",
    ],
    accept_multiple_files=True,
    help=(
        "Uploaded documents are used as user-provided context "
        "during this conversation. They are not added to the "
        "permanent Knowledge Base folder."
    ),
)


if uploaded_files:

    for uploaded_file in uploaded_files:

        filename = uploaded_file.name

        # Avoid extracting the same file repeatedly
        # on every Streamlit rerun.

        if filename not in st.session_state.uploaded_documents:

            with st.spinner(
                f"Reading {filename}..."
            ):

                extracted_text = (
                    extract_text_from_uploaded_file(
                        uploaded_file
                    )
                )

            if extracted_text.strip():

                extracted_text = normalise_text(
                    extracted_text
                )

                st.session_state.uploaded_documents[
                    filename
                ] = extracted_text

                st.session_state.uploaded_document_stats[
                    filename
                ] = {
                    "words": len(
                        extracted_text.split()
                    ),
                    "chunks": len(
                        split_into_chunks(
                            extracted_text
                        )
                    ),
                }

            else:

                st.warning(
                    f"Could not extract readable text "
                    f"from {filename}."
                )


# ============================================================
# DISPLAY UPLOADED DOCUMENTS
# ============================================================

if st.session_state.uploaded_documents:

    st.success(
        f"{len(st.session_state.uploaded_documents)} "
        "user document(s) available to the assistant."
    )

    with st.expander(
        "Uploaded documents",
        expanded=True,
    ):

        for filename in (
            st.session_state.uploaded_documents
        ):

            stats = (
                st.session_state
                .uploaded_document_stats
                .get(
                    filename,
                    {},
                )
            )

            st.write(
                f"📄 **{filename}** — "
                f"{stats.get('words', 0):,} words, "
                f"{stats.get('chunks', 0)} chunks"
            )

        st.caption(
            "These documents are user-provided material. "
            "They are not treated as institutional policy "
            "or as part of the permanent Knowledge Base."
        )

    if st.button(
        "🗑️ Clear uploaded documents",
        use_container_width=True,
    ):

        st.session_state.uploaded_documents = {}

        st.session_state.uploaded_document_stats = {}

        st.rerun()


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Ask a question or provide study details..."
)


# ============================================================
# PROCESS CHAT MESSAGE
# ============================================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    update_form_data_from_prompt(
        prompt
    )

    with st.chat_message("user"):

        st.markdown(
            prompt
        )

    # The institutional Knowledge Base is still required
    # for the application's normal workflows.

    if not documents:

        st.error(
            "The Knowledge Base folder does not contain any "
            "readable PDF, DOCX, or TXT documents."
        )

    else:

        mode = (
            st.session_state.mode
            or "knowledge"
        )

        client = get_client()

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Searching the institutional knowledge base "
                "and reviewing the supplied material..."
            ):

                try:

                    response = generate_response(
                        client=client,
                        model=model,
                        mode=mode,
                        user_prompt=prompt,
                        documents=documents,
                    )

                    st.markdown(
                        response
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response,
                        }
                    )

                    st.session_state.workflow_step += 1

                except Exception as exc:

                    st.error(
                        "I couldn't complete that request. "
                        "Please try again or contact the "
                        "application administrator."
                    )

                    # Keep the detailed exception out of
                    # the user interface for security.
                    # The exception can be logged separately
                    # if application logging is added.
>>>>>>> 2caf182 (Update institutional research support assistant)
