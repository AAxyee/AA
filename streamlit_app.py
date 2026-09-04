import streamlit as st

# --- Preloaded Institutional Documents ---
INFO_KNOWLEDGE_BASE = """
Social Service Sector: Key Findings Report

Beneficiaries: Agencies served 87,450 beneficiaries in FY2022/23, 98,210 in FY2023/24 (+12.3%), and 106,840 in FY2024/25 (+22.2% cumulative). Growth strongest in mental health, eldercare, and family support services.

Volunteers: Total volunteers grew from 14,320 (FY2022/23) to 17,240 (FY2024/25). Regular volunteers rose from 4,870 to 6,150, accounting for ~35% of total. Volunteer hours increased from 1.24M to 1.59M. Agencies attribute growth to structured management and skills-based volunteering.

Financial Overview: Income rose from S$312.4M (FY2022/23) to S$368.9M (FY2024/25). Government funding ~62% of total. Donations grew from S$62.5M to S$72.3M. Expenditure rose from S$298.7M to S$354.1M. Staff costs ~60% of expenditure, rising steadily.

Workforce: Vacancy rates ~18.3% in frontline roles. Attrition among <3 years staff ~31%. Training budgets increased in 67% of agencies, with focus on mental health first aid, trauma-informed care, and digital literacy. Leadership succession planning remains weak.

Service Demand: Caseloads rose ~22%. Growth in mental health, financial assistance, family violence intervention. Dementia cases up 17% year-on-year. Caregiver stress rising. More working adults seeking assistance, requiring flexible service models.

Funding: Government grants ~61.7% of revenue. Concerns about adequacy and predictability. Smaller agencies struggle with compliance burden. Philanthropy grew modestly. Outcome-based funding explored but controversial.

Collaboration: Improved but uneven. Integration with healthcare/education limited by systemic barriers. Digital capability uneven; 70% of agencies identify it as priority.

Conclusion: Sector expanding in reach but facing structural challenges in workforce, funding, and integration. Sustainability requires diversified income, stronger workforce pipelines, and integrated service delivery.
"""

NCSS_FORM_FIELDS = [
    "Name of study",
    "Requestor's email address",
    "Objectives and intended use of findings",
    "Does your study involve any vulnerable group?",
    "Describe sample group",
    "Describe how you will recruit participants",
    "Does your study involve any of the following? (systematic investigation, testing interventions, collecting data, evaluation study)",
    "Briefly describe the research design, including analysis plan",
    "Stage of the study",
    "Frequency of the study",
    "Was a previous study on this topic conducted? When?"
]

OVERVIEW_STUDIES = """
FY2023 Studies: Volunteer Management Survey, Digital Acceleration Index, PDPA compliance, Employer Support Grant review, Peer Support Strategy evaluation, 4ST Perception Poll, Board Evaluation Survey, Organisational Health Framework, Volunteer Impact Assessment Framework, Volunteer Management Maturity Matrix, Project SAFE evaluation, Fundraising capability study.
FY2024 Studies: Stakeholder Study, Digital Acceleration Index (continued), Organisational Health Framework cycle 2, Training Needs Survey, Empowering for Life Impact Study, Board Evaluation Survey cycle 2, Volunteer Management Maturity Matrix refinement, Tech Stack in Homes study, Board Leadership Study, Empowerment Service Design Module, Collective Impact Projects evaluation, MyAIMS User Discovery, Sector Perception Study, Work Conditions Study.
FY2025 Studies: Social Sector Development Survey, Membership Renewal Survey, Organisational Health Framework cycle 3, Volunteer Management Maturity Matrix cycle 3, MyAIMS User Discovery, Stakeholder Pulse Survey, Board Leadership Study cycle 2.
FY2026 Studies: Social Sector Development Survey, Digital Maturity Index (proposed), Organisational Health Framework cycle 4, Volunteer Management Maturity Matrix cycle 4, Stakeholder Perception Pulse Survey, SGSHARE Performance evaluation, Brand Health Study, Social Service Tribe CNA Docuseries evaluation, President’s Challenge study, Donor User Service Journey, Social Media Addiction study (proposed).
"""

STUDY_DESIGN_CHECKLIST = """
**Study Design Checklist**
1. Clear purpose/justification: Is the study necessary, critical, and actionable?
2. Questions/data points: Are they purposeful, scoped, and directly mapped to objectives?
3. Target population: Is it suitable, clearly defined, and ethically accessible?
4. Sample size: Is it adequate and justified (power calculation for quantitative, sufficiency for qualitative)?
5. Data collection method: Is it suitable, justified, and ethical? Is respondent burden reasonable?
"""

ANALYSIS_REVIEW_CHECKLIST = """
**Analysis Review Checklist**
1. Analytical approach: Appropriate, consistent with design, clearly stated and justified.
2. Mapping: Does the analysis plan address each study question?
3. Indicators/variables: Clearly defined, measurable, operationalized (quantitative) or grounded (qualitative).
4. Limitations/assumptions: Acknowledged, bias accounted for, assumptions clearly stated.
"""

# --- Helper: keyword search ---
def search_text(query, text):
    results = []
    for line in text.splitlines():
        if query.lower() in line.lower():
            results.append(line.strip())
    return results

# --- App Title ---
st.title("📚 Institutional Knowledge Assistant")

# --- Introduction ---
st.markdown("""
I am a **research support assistant** that helps staff access institutional knowledge and provide study design guidance.  

For study proposals, I will guide you through a few questions and generate a summary for submission to your director for study approval.  
For advice on your study design and analysis, I will run you through a checklist.  
""")

# --- User Options ---
option = st.radio(
    "Please select one of the following:",
    [
        "I want information from our database",
        "I want to conduct a study",
        "I want advice on my study design",
        "I want advice on my analysis"
    ]
)

# --- Step 1: Knowledge Database Search ---
if option == "I want information from our database":
    st.header("Step 1: Knowledge Database Search")
    query = st.text_input("Enter your question or keyword:")
    if query:
        results = search_text(query, INFO_KNOWLEDGE_BASE)
        if results:
            st.markdown("**Search Results (from knowledge base):**")
            for r in results:
                st.write(f"[1] \"{r}\"")
        else:
            st.warning("No matching information found in the knowledge base. You may state: *'I cannot find the information I want.'*")

# --- Step 2: Conduct a Study (Information Request Form) ---
elif option == "I want to conduct a study":
    st.header("Step 2: Information Request Form")
    responses = {}
    for field in NCSS_FORM_FIELDS:
        responses[field] = st.text_input(field)

    if st.button("Generate Summary"):
        st.subheader("📄 Information Request Form")
        for field, response in responses.items():
            st.write(f"{field}: {response}")

        st.subheader("📌 Summary for Submission")
        summary_text = "\n".join([f"{field}: {resp}" for field, resp in responses.items()])
        st.success("Copy and paste this summary to send to the Director for study approval.")
        st.text(summary_text)

# --- Step 3: Study Design Guidance ---
elif option == "I want advice on my study design":
    st.header("Step 3: Study Design Guidance")
    st.markdown("**Similar Studies Analysis**")
    st.text(OVERVIEW_STUDIES[:1000])  # preview
    st.markdown(STUDY_DESIGN_CHECKLIST)
    st.info("Next Steps: Please review each item and let me know if you need clarification.")

# --- Step 4: Analysis Review Guidance ---
elif option == "I want advice on my analysis":
    st.header
