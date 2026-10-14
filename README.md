# BLK AI MLOps Skills

Standard way for Blackstraw to build **ML / MLOps projects on Databricks**.

You describe a use case in chat → the agent asks guided multiple-choice questions → it writes a project config → you can train.

**Goal:** Same answers → almost the same project (about 5–10% difference max).

**Platform:** **Databricks only** (Unity Catalog, Jobs, MLflow on Databricks). No AWS / Azure / GCP adapters.

---

## How to use (start here)

### 1. Open this repo in Cursor

Work inside this folder so the agent can read `skills/` and `CLAUDE.md`.

### 2. Start a new chat and ask in plain English

Example:

```text
I want to build an anomaly detection MLOps pipeline for credit card transactions.
The output should identify suspicious transactions.
```

Or use the shortcut:

```text
/anomaly-detection
```

### 3. Answer the menus

The agent will ask **one question at a time**, for example:

- Project name  
- Where is the data? (Databricks table / CSV / …)  
- Labels?  
- Model? (Isolation Forest, LOF, …)  
- Metric? (F1, PR-AUC, Precision@K, …)  
- Batch or realtime?  
- MLflow tracking / registry?  

Reply with a **number**, an **id**, or `use recommended`.

You do **not** need to edit YAML by hand.

### 4. Review what was created

The agent creates:

```text
projects/<your-project-name>/
  ml-project.yaml     ← your answers (source of truth)
  src/train.py
  src/predict.py
  src/evaluate.py
  ...
```

### 5. Train (when the agent asks, or manually)

```bash
# from repo root — create a project (agent usually does this)
python new_project.py --name my-project

cd projects/my-project
uv sync                    # install deps

# set data.path in ml-project.yaml to your table export / CSV, then:
python src/train.py
python src/predict.py --input data/new_rows.csv --output scored.csv
```

On Databricks, point `data.path` / source at a **Unity Catalog table** or volume path as you configure the project.

---

## What happens behind the scenes

```text
Your request
    → Agent reads skills (orchestrator → anomaly → optional MLflow)
    → Asks fixed option menus (one at a time)
    → Writes projects/<name>/ml-project.yaml
    → Requirements gate (pass / fail)
    → Ready to train? → run train.py
```

Same picks → same model family, metrics, and layout.

---

## What you can choose (menus)

Full lists live in the skill files. Summary:

| Topic | Examples |
|---|---|
| Data | Databricks table, CSV/Parquet, streaming |
| Labels | yes / no / partial |
| Model | Isolation Forest, One-Class SVM, LOF, Autoencoder, CNN, LSTM, LightGBM |
| Metrics | precision, recall, F1, PR-AUC, ROC-AUC, Precision@K, … |
| Serve | batch / near-realtime / realtime |
| Ops | monitoring, retraining, alert action |
| MLflow | Databricks MLflow tracking, experiment name, register model, stage |

- Anomaly menus: [`skills/ml/anamoly-detection/options.md`](skills/ml/anamoly-detection/options.md)  
- MLflow menus: [`skills/mlops/mlflow/options.md`](skills/mlops/mlflow/options.md)

---

## Simple example

**You say:** Detect anomalies in credit card transactions. No labels. Score daily on Databricks.

**Typical locked result:**

| Decision | Value |
|---|---|
| Problem | Anomaly detection |
| Platform | Databricks |
| Model | Isolation Forest (recommended if unlabeled) |
| Metric | Precision@K (if some known cases) |
| Serve | Batch |
| Tracking | Databricks MLflow |
| Config | `projects/<name>/ml-project.yaml` |

---

## Repo layout

```text
README.md                      ← you are here
CLAUDE.md                      ← rules for the AI agent
docs/architecture.md           ← deterministic rules & gates
schemas/                       ← project + option schemas
skills/
  orchestrator/                ← starts every ML request
  requirements/                ← asks questions
  ml/anamoly-detection/        ← anomaly flow + menus
  mlops/mlflow/                ← MLflow menus on Databricks
template/anomaly-detection/    ← copied into each new project
projects/                      ← your generated projects
new_project.py                 ← bootstrap a project folder
```

---

## Current scope

| Area | Status |
|---|---|
| Anomaly detection (menus + template) | Ready to use |
| MLflow skill (Databricks tracking / registry menus) | Ready |
| Train / predict template | Ready (local or Databricks-compatible code) |
| MLflow wired inside `train.py` | Next |
| Classification / regression | Planned |
| Full Databricks Jobs / UC deploy automation | Planned |

---

## Rules (keeps everyone consistent)

1. **Fixed menus only** — no inventing models or metrics.  
2. **Save answers** in `ml-project.yaml` — don’t re-guess from chat.  
3. **Fail if incomplete** — missing data path / model / metric → stop.  
4. **Templates only** — fill blanks; don’t invent a new pipeline layout.  
5. **Databricks only** — platform is Databricks (not AWS / Azure / GCP).

---

## More detail

- [docs/architecture.md](docs/architecture.md) — gates, locks, fulfillment criteria  
- [skills/ml/anamoly-detection/SKILL.md](skills/ml/anamoly-detection/SKILL.md) — step-by-step anomaly flow  
- [skills/mlops/mlflow/SKILL.md](skills/mlops/mlflow/SKILL.md) — MLflow on Databricks  

---

## Consistency target

Same use case + same answers on Databricks → same:

- problem type, model family, primary metric  
- inference mode, pipeline stages, folder layout  

Allowed small differences: table names, thresholds, cluster size, project name.
