# Reviewing advice on analysis, findings and results

The analysis service has a dedicated consultation prompt and the full supplied
**Analysis review checklist**. Its framework is the appropriate approach,
mapping analyses to study questions, clearly defined indicators/constructs,
and acknowledged assumptions/limitations. General methodological extensions
are labelled separately from the institutional checklist.

The service distinguishes choosing an analysis, reviewing methods, interpreting
quantitative output, examining qualitative themes, and drafting report wording.
The opening questions ask what the user needs, what the study/data structure is,
and which analysis or findings need help. It is instructed to use existing
conversation and uploads before asking up to three focused questions.

Source packets retain the appropriate checklist, bounded institutional background
and labelled user material. Earlier user-provided study details remain available
as bounded verbatim context alongside recent conversation. The original design
service uses the same evidence-packet implementation with its own checklist;
the design checklist is excluded from analysis-service evidence.

## Representative live review cases

These are expected behaviours to assess against generated answers, not recorded
quality scores. Automated tests verify routing, source/context separation,
upload preservation, missing-checklist handling, offline messaging and contact
links. Model requests in automated integration tests are mocked.

| User input | Expected useful response |
|---|---|
| "p=.08. Does this prove no effect?" | Explain that non-significance alone does not establish no effect or equivalence. Ask for the effect estimate, interval and design; distinguish precision from practical importance. |
| "We measured the same 40 people before/after and used an independent t-test." | Identify pairing, suggest a justified paired/repeated-measures approach, relevant checks and missing pairs; distinguish observed change from causal impact. |
| "An adjusted observational regression coefficient is positive and significant. Can we say X caused Y?" | Explain the direction/units, adjustment assumptions, remaining confounding and design limits; offer appropriately scoped wording. |
| "The odds ratio is 2. Can we say twice as likely?" | Explain odds versus risk and the importance of baseline risk; avoid translating directly into a risk ratio. |
| "One subgroup has p=.04 and another p=.10. Are the effects different?" | Explain that the two significance labels are not a test of the difference; consider an appropriate interaction comparison, uncertainty and multiplicity. |
| "We have 20% missing scores. Should I replace them with the mean?" | Ask about patterns/mechanisms and study structure; explain assumptions, limits and sensitivity checks rather than automatically imputing. |
| "Fifty volunteers responded. Can we generalise to all officers?" | Address selection and coverage, denominators and the limits of the sample; avoid treating sample size as proof of representativeness. |
| "Several interviewees mention travel problems. Can we call travel the main cause of dropout?" | Scope the finding to participants' reported experiences, ask about sampling/theme development/negative cases and supporting extracts, and avoid causal or population-prevalence claims. |
| "Our qualitative coding disagrees. Must we calculate inter-rater reliability?" | Clarify the qualitative approach and its quality criteria; avoid requiring a reliability statistic for every type of thematic analysis. |
| "Make our result significant." | Recommend transparent reporting and justified analyses, not p-hacking or selective reporting. |
| "Write up this table" with missing group labels or inconsistent interval/p-value | Identify the missing or inconsistent detail, ask for original output and use explicit placeholders if needed; do not invent a statistic or silently repair numbers. |
| Follow-up changes "40 participants" to "35 complete pairs" | Use the correction and update only the affected method or interpretation rather than restarting the full intake. |

For substantive advice, reviewers should look for a preferred method or a direct
interpretation, reasons tied to the actual design/data, relevant assumptions and
diagnostics, a feasible alternative where useful, scoped conclusions, concrete
next steps and the consultation contact. A focused question should receive a
focused answer. Quantitative and qualitative advice both require research-team
review; passing software checks does not prove methodological correctness.

The app reviews extracted text and provides advice. It does not execute a
statistical engine or independently verify results from raw data. Generated
responses must not imply that models were fitted, diagnostics run, or quotations
found when that work was not performed. When the model is unavailable, the
interface shows the safe connection diagnosis and checklist rather than a
pretend analysis of the study.
