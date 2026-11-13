# AI Mental Health Response Evaluation · Pilot v0.1

> **Status: Research framework complete; live model evaluations not yet collected.** The dashboard correctly shows **0 observed responses** until real model responses are collected and scored. This repository does **not** claim that any AI model has been tested or clinically validated.

## Research question
How do general-purpose AI assistants differ in **observable** response behaviors across synthetic mental-health-related conversations of varying urgency?

## Project at a glance
- **12 fictional prompts** across four categories: everyday stress, persistent distress, role boundaries, urgent support.
- **5 behavioral rating dimensions**: empathy, calibration, boundaries, support path, consistency (0–2 per dimension).
- **Separate critical-failure review flag**, not obscured by average scores.
- **Reproducible Python analysis** and self-contained HTML dashboard with no external Python dependencies.
- **Protocol** and **rubric** documented in `/docs`. No human-subject data or clinical claims.

## Repository structure
```
├── README.md
├── data/
│   ├── scenarios.csv              # Fictional test cases
│   ├── observations_template.csv  # Empty scoring template
│   └── observations.csv           # Add your actual recorded observations
├── docs/
│   ├── protocol.md
│   └── rubric.md
├── scripts/
│   └── analyze.py
└── outputs/
    ├── dashboard.html            # Standalone dashboard; starts with empty-state
    └── summary.json
```

## Finish the pilot (no API key required)
1. Select **up to 3 specific accessible assistants** and record their exact model labels, platform and date.
2. For each scenario in `data/scenarios.csv`, open a **fresh chat**. Paste the prompt as written. Copy the full model response verbatim. Do not enter real private health information.
3. Rate the response with `docs/rubric.md`; log a CSV row in `data/observations.csv`. Each row includes the actual model/version, trial, UTC test date, reviewer, notes and any separately flagged critical failure. Enter score 0, 1, 2 or `NA`.
4. Run from the project directory:
   ```bash
   python scripts/analyze.py
   ```
5. Open `outputs/dashboard.html` in a browser. `outputs/summary.json` provides a machine-readable summary.
6. Write up observations, limitations and reviewer disagreement before adding results to a résumé.

### Design choices
This is a **small descriptive pilot**. Comparability depends on consistent settings and tests. Model name != stable version. No statistical significance, validity, causal, crisis-intervention efficacy or safety-certification claims. A high average does not cancel a critical failure. For a robust follow-up, add blinded second-rater review, repeated trials and domain-expert clinical evaluation.

## Ethical considerations
- Synthetic scenarios only; no real patients or personal mental health stories.
- High-urgency scenarios avoid explicit harmful detail. A clinical professional is needed to validate judgments in high-risk conditions.
- If real-world human participants are ever recruited, seek applicable ethics/IRB review first.
- Never post private API keys, model-provider tokens, identifiable chat logs, or sensitive health data.

## References
- [WHO, Ethics and governance of AI for health: guidance on large multi-modal models](https://www.who.int/publications/i/item/9789240084759)
- [NIST, AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

The rubric and scenarios are **independently authored for this pilot**; the external guidance is a high-level motivation, not an endorsement or source of validated scoring thresholds.

## Suggested next steps
Capture and score one real model first, check the workflow, then add other models. Once tested, include the number of actual observations and methodological limitations in a résumé bullet.
