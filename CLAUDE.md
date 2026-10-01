# BLK-AIMLOPS Skills

This repository is an MLOps skills framework. It lets a user build and train ML models by answering guided questions — no code required.

## Skills system

All reasoning rules live in `skills/`. When the user makes any ML or MLOps request, follow the orchestrator:

```
skills/orchestrator/SKILL.md
```

The orchestrator coordinates:

- `skills/requirements/SKILL.md` — progressive requirements gathering
- `skills/ml/SKILL.md` — ML design
- `skills/ml/common/SKILL.md` — shared ML rules (transformation consistency, leakage)
- `skills/ml/anamoly-detection/SKILL.md` — anomaly detection workflow (fully implemented)
- `skills/ml/anamoly-detection/options.md` — fixed option menus (use these; do not invent options)

## Entry points

| Trigger | What to do |
|---|---|
| `/anomaly-detection` | Read `skills/ml/anamoly-detection/SKILL.md` and start Phase 0 |
| Any ML/MLOps natural-language request | Read `skills/orchestrator/SKILL.md` and follow the workflow |

## Key rules

- Read the relevant skill file **before** asking the user any questions.
- Never invent model or metric options — always use the menus in `skills/ml/anamoly-detection/options.md`.
- Ask **one menu at a time**. Wait for the answer before proceeding.
- Do not generate implementation code before the requirements gate passes.
- New projects are created with: `python new_project.py --name <project-name>`
- All project configs live in `projects/<project-name>/ml-project.yaml`.
- The template for new projects is `template/anomaly-detection/`.

## Supported ML problem types

| Problem | Status |
|---|---|
| Anomaly detection | Fully implemented |
| Classification | Planned |
| Regression | Planned |
| Forecasting | Planned |
| Clustering | Planned |
