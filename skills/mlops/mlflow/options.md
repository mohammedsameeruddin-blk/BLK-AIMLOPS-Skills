# MLflow options catalog

Fixed menus for the MLflow skill.
Agent must only offer these IDs — no free-form inventing.
Mark one option **(recommended)** when asking. Save picks under `mlflow:` in `ml-project.yaml`.

Ask **one menu at a time**. Skip if already set.

---

## 1. Enable MLflow

| id | label | recommended_when |
|---|---|---|
| true | Enable MLflow tracking | almost always for real projects |
| false | No MLflow (local files only) | quick throwaway / no tracking needed |

---

## 2. Tracking backend

Blackstraw standard is **Databricks MLflow**.

| id | label | tracking_uri | recommended_when |
|---|---|---|---|
| databricks | Databricks workspace MLflow | `databricks` | **always (recommended)** |
| local_file | Local file store (`./mlruns`) | `./mlruns` | laptop demo only |
| remote_uri | Custom tracking server URL | *(ask user for URL)* | rare / special case |

---

## 3. Experiment naming

| id | label | how to set experiment_name |
|---|---|---|
| project_name | Use project name | `<project.name>` |
| shared_folder | Shared folder style | `/Shared/<project.name>` (Databricks) |
| user_folder | User folder style | `/Users/<user>/<project.name>` (Databricks) |
| custom | Custom name | ask user for string |

**Recommended:** `project_name` on local; `shared_folder` or `user_folder` on Databricks.

---

## 4. Run naming

| id | label |
|---|---|
| timestamped | `<model>_<YYYYMMDD_HHMMSS>` (recommended) |
| model_metric | `<model>_<primary_metric>` |
| custom | User-provided run name |

---

## 5. Autolog

| id | label | recommended_when |
|---|---|---|
| false | Explicit log only (recommended — more deterministic) | default |
| true | Enable mlflow.autolog() | rapid prototyping |

---

## 6. What to log (multi-select allowed; defaults all true except noted)

| id | label | default |
|---|---|---|
| log_params | Log params (model, seed, split, features) | true |
| log_metrics | Log metrics (primary + secondary) | true |
| log_artifacts | Log model, scaler/transform, reports, yaml snapshot | true |

Ask once:

```text
What should MLflow log? (pick all that apply, or "all")
1. log_params (recommended)
2. log_metrics (recommended)
3. log_artifacts (recommended)
4. all (recommended default)
```

---

## 7. Register model

| id | label | recommended_when |
|---|---|---|
| false | Do not register (tracking only) | first local runs |
| true | Register to MLflow Model Registry | Databricks / shared envs |

---

## 8. Initial registry stage

Only if `register_model = true`.

| id | label | recommended_when |
|---|---|---|
| none | Registered, no stage alias | safe default |
| staging | Staging / Challenger | after metrics pass (recommended if registering) |
| production | Production / Champion | **only with explicit user confirm** |
| archived | Archived | rollback / retire |

---

## 9. Artifact flavors (what to log as model)

| id | label | recommended_when |
|---|---|---|
| sklearn | mlflow.sklearn | Isolation Forest, LOF, One-Class SVM, LightGBM-sklearn |
| pyfunc | mlflow.pyfunc (custom wrapper) | mixed pipeline / non-sklearn |
| pytorch | mlflow.pytorch | CNN / LSTM / Autoencoder (torch) |

**Recommended:** `sklearn` for classic anomaly models; `pytorch` for deep models; `pyfunc` if bundling scaler+model.

---

## 10. Tags (optional multi-select)

| id | label |
|---|---|
| problem_type | Tag ML problem type |
| model_id | Tag selected model menu id |
| dataset_version | Tag data version / path hash |
| git_commit | Tag git SHA if available |

**Recommended:** enable `problem_type` + `model_id`.

---

## Ask order

```text
1. enable
2. tracking_backend   (if enabled)
3. experiment_naming
4. run_naming
5. autolog
6. what_to_log
7. register_model
8. model_stage        (if register)
9. artifact_flavor
10. tags              (optional)
```
