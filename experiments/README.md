
# Experiment Logs Overview


## Methodology Legend

- **Baseline**: Simple prompt with basic task description
- **CP**: Construction Prompt - explicit step-by-step instructions
- **CP-A**: Construction Prompt Augmented - CP enhanced with example queries
- **CoT (Baseline)**: Chain-of-Thought with baseline prompt
- **CoT (CP)**: Chain-of-Thought with construction prompt
- **few-shot CoT**: Chain-of-Thought with hand-curated examples
- **LtM**: Least-to-Most - three-stage decomposition approach


### Notes

- Experiments prefixed with `multi_run_` represent 10 independent trials for statistical analysis



| Name | Variant | LLM Model | Temperature |
|------|---------|-----------|-------------|
| ev_2025-04-21_18-31-20 | Baseline | gemini 2.0 flash | 0.8 |
| ev_2025-04-22_02-04-22 | Baseline | gemini 2.5 flash (no thinking) | 0.8 |
| ev_2025-04-23_11-26-44 | CP | gemini 2.0 flash | 0.8 |
| ev_2025-04-22_16-27-37 | CP | gemini 2.5 flash (no thinking) | 0.8 |
| ev_2025-04-22_17-38-49 | CoT (Baseline) | gemini 2.0 flash | 0.8 |
| ev_2025-04-22_21-44-48 | CoT (CP) | gemini 2.0 flash | 0.8 |
| ev_2025-04-23_10-26-29 | CoT (CP) | gemini 2.5 flash (no thinking) | 0.8 |
| ev_2025-04-25_16-58-55 | CoT (CP) | gemini 2.0 flash | 0.1 |
| ev_2025-04-25_17-49-29 | CP | gemini 2.0 flash | 0.1 |
| ev_2025-04-26_16-52-04 | few-shot CoT | gemini 2.0 flash | 0.1 |
| ev_2025-04-26_18-21-19 | CoT (CP) | gemini 2.5 flash (no thinking) | 0.1 |
| ev_2025-04-27_15-06-28 | few-shot CoT | gemini 2.5 flash (no thinking) | 0.1 |
| ev_2025-04-27_16-18-37 | few-shot CoT | gemini 2.5 flash (thinking) | 0.1 |
| ev_2025-04-27_17-31-27 | few-shot CoT | gemini 2.0 flash | 0.1 |
| ev_2025-04-27_19-52-47 | few-shot CoT | gemini 2.5 flash (thinking) | 0.1 |
| ev_2025-04-30_18-18-41 | CP-A | gemini 2.0 flash | 0.1 |
| ev_2025-05-01_09-04-25 | CP-A | gemini 2.5 flash (no thinking) | 0.1 |
| ev_2025-05-01_11-36-06 | CP-A | gemini 2.5 flash (thinking) | 0.1 |
| ev_2025-05-01_13-24-50 | CP-A | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-02_00-31-21 | CP-A | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-04_00-51-30 | few-shot CoT | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-06_22-14-46 | LtM | gemini 2.0 flash | 0.1 |
| ev_2025-05-08_18-12-10 | Baseline | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-10_14-26-00 | Baseline | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-10_18-05-54 | CP | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-11_00-21-16 | CoT (CP) | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-25_17-14-57 | LtM | gemini 2.5 flash (thinking) | 0.1 |





