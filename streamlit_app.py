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
