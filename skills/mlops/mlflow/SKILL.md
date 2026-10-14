---
name: mlflow
description: >-
  Configures MLflow experiment tracking, artifact logging, and model registry
  for MLOps projects. Use when the user mentions MLflow, experiment tracking,
  model registry, logging metrics/params, or registering a model version.
---

# MLflow Skill

## Purpose

Add **MLflow** to an ML/MLOps project in a deterministic way:

1. Ask fixed option menus (see [options.md](options.md)).
2. Write choices into the canonical `ml-project.yaml` under `mlflow:`.
3. Tell implementation / train code **what** to log and register.
4. Do not invent tracking settings outside the menus.

This skill is **platform-capable** (local file store, Databricks-hosted MLflow, remote tracking server).  
It does **not** replace the anomaly/classification ML design skills — it runs **after** ML design (or alongside platform mapping).

## When to invoke

Invoke when:

* User says MLflow / experiment tracking / model registry
* Orchestrator reaches platform mapping / register stage
* `platform.name` is `databricks` or `local` and tracking is unresolved
* Training is about to run and `mlflow.enabled` is not set

## Core rules

1. **Menus only** — use [options.md](options.md); mark `(recommended)`.
2. **One menu at a time** — save each answer before the next.
3. **Canonical spec** — write to `mlflow:` (+ `platform.mapping.model_registry`).
4. **Train/infer invariant** — log the **same** transform + model versions together.
5. **No silent register to Production** — staging/production requires user confirm.
6. **Do not generate full app code here** — update YAML + list required train hooks; template implements them.

---

## What MLflow must cover

| Capability | Always? | Spec fields |
|---|---|---|
| Experiment tracking | if `mlflow.enabled=true` | tracking_uri, experiment_name |
| Log params | yes when enabled | log_params |
| Log metrics | yes when enabled | log_metrics |
| Log artifacts (model, scaler, report) | yes when enabled | log_artifacts |
| Model registry | optional menu | register_model, registered_model_name, stage |
| Autolog | optional menu | autolog |

---

## Progressive ask order

Skip items already set in the project YAML.

| Step | Menu | YAML field |
|---|---|---|
| 1 | Enable MLflow? | `mlflow.enabled` |
| 2 | Tracking backend | `mlflow.tracking_uri_mode` (+ uri if custom) |
| 3 | Experiment naming | `mlflow.experiment_name` |
| 4 | What to log | `mlflow.log_params`, `log_metrics`, `log_artifacts`, `autolog` |
| 5 | Register model? | `mlflow.register_model` |
| 6 | Registered model name | `mlflow.registered_model_name` |
| 7 | Initial stage | `mlflow.model_stage` |
| 8 | Run naming | `mlflow.run_name_strategy` |

If Step 1 = `false`, stop and set `mlflow.enabled: false`. Do not ask the rest.

---

## Recommended defaults

Blackstraw platform is **Databricks**. Prefer Databricks MLflow.

```text
platform = databricks (standard)
  → tracking_uri_mode = databricks          (workspace MLflow)
  → register_model = true
  → experiment_name = /Shared/<project.name> or /Users/<user>/<project.name>
  → model_stage = staging                   (never production without confirm)

platform = local (demo only)
  → tracking_uri_mode = local_file          (./mlruns)
  → register_model = false
  → experiment_name = <project.name>

Always when enabled:
  → log_params = true
  → log_metrics = true
  → log_artifacts = true
  → autolog = false                         (explicit logging preferred for determinism)
```

---

## YAML shape to write

Write (or merge) this block into the project `ml-project.yaml`:

```yaml
mlflow:
  enabled: true
  tracking_uri_mode: local_file          # local_file | databricks | remote_uri
  tracking_uri: ./mlruns                 # used when local_file or remote_uri
  experiment_name: credit-card-fraud
  run_name_strategy: timestamped         # timestamped | model_metric | custom
  autolog: false
  log_params: true
  log_metrics: true
  log_artifacts: true
  register_model: false
  registered_model_name: null            # e.g. credit_card_anomaly
  model_stage: none                      # none | staging | production | archived
  tags:
    problem_type: anomaly_detection
    project: credit-card-fraud

platform:
  mapping:
    model_registry: mlflow               # when register_model true
```

Also record user picks under `requirements.user_decisions` / `business.decisions` if the project uses those sections.

---

## Required train / evaluate hooks (for implementation)

When `mlflow.enabled=true`, training code **must**:

```text
1. mlflow.set_tracking_uri(...)
2. mlflow.set_experiment(experiment_name)
3. with mlflow.start_run(run_name=...):
4.    log params (model id, contamination, split, seed, feature list)
5.    train + evaluate
6.    log metrics (primary + secondaries from ml_design)
7.    log artifacts: model.pkl, scaler/transform, train_report.json, ml-project.yaml snapshot
8.    if register_model:
         mlflow.sklearn.log_model(...) or generic pyfunc
         + register to registered_model_name
         + set stage only if user chose staging/production
```

**Never** fit preprocessors inside the logged inference path differently from training.  
Log transform + model as one logical version.

---

## Gate

### MLflow gate PASS when

* `mlflow.enabled` is true or false (explicit)
* If true: `tracking_uri_mode`, `experiment_name`, log flags set
* If `register_model=true`: `registered_model_name` set; stage ≠ `production` unless user confirmed

### FAIL → ask next missing menu; do not train with half config

---

## Interaction with other skills

| Skill | Relationship |
|---|---|
| Orchestrator | Calls this at platform mapping / before train |
| Requirements | May ask “Enable MLflow?” as part of MLOps menus |
| Anomaly (or other ML) | Owns model/metric menus; MLflow **logs** those choices |
| Common ML | Artifact association — MLflow run links model + transform |

---

## Example (local demo)

```text
Agent: Enable MLflow tracking?
1. true (recommended)
2. false

User: 1

Agent: Tracking backend?
1. local_file — ./mlruns (recommended for local)
2. databricks — Databricks workspace MLflow
3. remote_uri — custom tracking server

User: 1

Agent: Register the model in MLflow Model Registry?
1. false (recommended for first local run)
2. true

User: 1

→ writes mlflow: block into projects/<name>/ml-project.yaml
→ continue to train
```

---

## Out of scope

* Replacing Databricks Unity Catalog governance policy
* Designing the ML algorithm (use ML problem skill)
* Free-form experiment sprawl without `experiment_name` rules

## See also

* [options.md](options.md) — full menus
* `schemas/mlflow-options.yaml` — machine-readable menus
* `docs/architecture.md` — register stage in pipeline locks
