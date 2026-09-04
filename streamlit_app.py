import streamlit as st

# --- Preloaded Institutional Documents ---
FORM_FIELDS = [
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
FY2023 Studies included: Volunteer Management Survey, Digital Acceleration Index, PDPA compliance, Employer Support Grant review, Peer Support Strategy evaluation, 4ST Perception Poll, Board Evaluation Survey, Organisational Health Framework, Volunteer Impact Assessment Framework, Volunteer Management Maturity Matrix, Project SAFE evaluation, Fundraising capability study.
FY2024 Studies included: Stakeholder Study, Digital Acceleration Index (continued), Organisational Health Framework cycle 2, Training Needs Survey, Empowering for Life Impact Study, Board Evaluation Survey cycle 2, Volunteer Management Maturity Matrix refinement, Tech Stack in Homes study, Board Leadership Study, Empowerment Service Design Module, Collective Impact Projects evaluation, MyAIMS User Discovery, Sector Perception Study, Work Conditions Study.
FY2025 Studies included: Social Sector Development Survey, Membership Renewal Survey, Organisational Health Framework cycle 3, Volunteer Management Maturity Matrix cycle 3, MyAIMS User Discovery, Stakeholder Pulse Survey, Board Leadership Study cycle 2.
FY2026 Studies included: Social Sector Development Survey, Digital Maturity Index (proposed), Organisational Health Framework cycle 4, Volunteer Management Maturity Matrix cycle 4, Stakeholder Perception Pulse Survey, SGSHARE Performance evaluation, Brand Health Study, Social Service Tribe CNA Docuseries evaluation, President’s Challenge study, Donor User Service Journey, Social Media Addiction study (proposed).
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
    query = st.text_input("Enter your question:")
    if query:
        st.markdown("**Search Results (from overview of studies):**")
        st.text(OVERVIEW_STUDIES[:1000])  # preview first 1000 chars
        st.info("If you cannot find the information you want, please state: *'I cannot find the information I want.'*")

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
    st.header("Step 4: Analysis Review Process")
    st.markdown(ANALYSIS_REVIEW_CHECKLIST)
    st.info("Next Steps: Please review each item and let me know if you need clarification.")

# --- Restart Option ---
st.markdown("---")
if st.button("🔄 Restart"):
    st.experimental_rerun()
