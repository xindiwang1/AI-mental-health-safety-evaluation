# Preregistered-style pilot protocol (version 0.1)

## Question
How do general-purpose AI assistants differ in observable response behaviors across synthetic mental-health-related conversations of varying urgency?

## Study design
- Twelve fictional English-language single-turn scenarios, organized into four categories: Everyday stress, Persistent distress, Role boundaries, Urgent support (three each).
- Suggested comparisons: up to three accessible AI assistants, one fresh conversation per prompt. Record the exact publicly displayed model name/version; do not assume different product names mean stable model versions.
- If time allows, do two trials per model per prompt to explore instability. If only one is done, report that no repeatability claim can be made.
- No personal mental-health disclosures, real patient records, or recruited participants. Do not upload private information.
- Preserve all raw replies unchanged, record date/time in UTC and interface versus API. Browser-generated outputs may vary with system policies and hidden context.

## Outcomes
Five *researcher-defined* 0–2 behavioral scores per answer (rubric.md), plus an independent critical-failure flag; descriptive means only, no significance tests with tiny convenience sample. Do not equate total score with clinical safety. Report a per-dimension denominator and flag frequency.

## Analysis and limits
The Python script validates observations, summarizes scores by model, category and dimension, then generates a standalone HTML dashboard. The analysis is descriptive, exploratory and not clinically validated. Reviewer bias, model version drift, platform differences, prompt phrasing, English-only cases, and small sample size are major limitations. 'High urgency' is only a synthetic scenario category and is not a clinical severity label.

## Safety
Only synthetic scenarios; do not produce or solicit explicit harmful instructions. All high-urgency scenarios should be evaluated primarily for escalation to qualified human support. Do not test with real people in crisis; consult a clinical professional before clinical conclusions or external deployment.

## References
- WHO, *Ethics and governance of artificial intelligence for health: Guidance on large multi-modal models* (2024/2025 publication page): https://www.who.int/publications/i/item/9789240084759
- NIST, *AI Risk Management Framework: Generative AI Profile* (2024): https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

These documents motivate broad evaluation principles. The scenario set, categories, weights and rubric are independently designed and have not been validated or endorsed by WHO or NIST.
