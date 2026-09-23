# BLK AI MLOps Skills

Standard way for anyone at Blackstraw to build ML projects — same questions, same rules, same output.

**Goal:** If two people give the same answers, they get almost the same project (about 5–10% difference max).

---

## What this does (today)

1. Understand the ML request (anomaly detection first).
2. Ask only the missing questions.
3. Save every answer into one file: `schemas/ml-project.yaml`.
4. Fail if required fields are missing (do not invent).
5. Apply **locked rules** for model, metrics, and pipelines.
6. Later: fill fixed templates (Databricks) — do not invent new pipelines.

**Not done yet:** full Databricks code generation, regression, classification.

---

## Why this exists

Without locks, AI can pick different models and layouts for the same use case.

With locks:

```text
Same answers → same decision table → same template → same project
```

---

## The 5 rules that keep it deterministic

1. **Lock rules** — e.g. no labels + anomaly → Isolation Forest.
2. **Save answers** — write into `ml-project.yaml`. Never re-guess from chat.
3. **Fail if incomplete** — missing data path or inference mode → stop.
4. **Use templates only** — fill blanks; do not invent pipelines.
5. **Ask user only for real choices** — batch vs realtime, labels yes/no.

---

## Simple example

**Ask:** Detect anomalies in fryer temperature. No labels. Score once a day.

**Locked result (both people get this):**

| Decision | Locked value |
|---|---|
| Problem | Anomaly detection |
| Model | Isolation Forest |
| Metric | Score distribution + precision@k when labels appear later |
| Serve | Batch (daily) |
| Spec file | `ml-project.yaml` |

---

## How a run works

```text
User request
    → Ask missing questions (only real choices)
    → Update ml-project.yaml
    → Requirements gate (pass / fail)
    → Apply anomaly decision locks
    → Design / templates (no free-form inventing)
```

If the gate fails → ask again. Do not generate code.

---

## Current scope

| Area | Status |
|---|---|
| Anomaly detection | In progress (locked rules) |
| Classification | Next |
| Regression | Next |
| Databricks templates | Next |
| AWS / Azure adapters | Later |

---

## Repo layout

```text
README.md                 ← start here
docs/architecture.md      ← deterministic rules and gates
schemas/ml-project.yaml   ← canonical project specification
skills/                   ← AI skill playbooks
  orchestrator/
  requirements/
  ml/
    common/
    anamoly-detection/    ← anomaly first
```

---

## Read next

- [docs/architecture.md](docs/architecture.md) — locked models, metrics, required fields, pass/fail criteria.

---

## Consistency target

Same use case + same answers + same platform → same:

- problem type
- model family
- primary metric
- inference mode
- pipeline stages
- project folder layout

Allowed small differences: table names, thresholds, cluster size, project name.
