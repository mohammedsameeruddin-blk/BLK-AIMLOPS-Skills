# AI MLOps Skills Architecture (Deterministic)

## Purpose

Turn a natural-language ML request into a **standard, repeatable** project.

**Consistency target:** same answers → same design and process, with at most ~5–10% difference (names, thresholds, cluster size — not model family or pipeline shape).

**Current scope:** Anomaly detection only. Classification and regression come next, using the same pattern.

---

## The 5 deterministic rules

| # | Rule | Meaning |
|---|---|---|
| 1 | **Lock rules** | Decision tables choose model, metric, serve mode. No free pick. |
| 2 | **Save answers** | Every answer goes into `schemas/ml-project.yaml`. Downstream skills read the file, not the chat. |
| 3 | **Fail if incomplete** | Missing required fields → requirements gate **FAIL**. Stop. Do not invent. |
| 4 | **Use templates only** | Fill fixed pipeline templates. Do not invent new layouts. |
| 5 | **Ask only real choices** | Ask the user only when the choice is business-critical (e.g. labels yes/no, batch vs realtime). |

If a decision can be decided by a rule, the AI must not ask and must not invent.

---

## Simple example (anomaly)

**User:** “Detect anomalies in fryer temperature. No labels. Score once a day.”

| Step | What happens |
|---|---|
| Save | Answers written to `ml-project.yaml` |
| Gate | Required fields checked → PASS |
| Lock | Unlabeled anomaly → **Isolation Forest** |
| Metric | Unlabeled → score / expert review protocol |
| Serve | Daily → **batch** |
| Output | Same design for any person with the same answers |

**Wrong (non-deterministic):** Person A gets Isolation Forest, Person B gets Autoencoder.

**Right:** Both get Isolation Forest + batch + same pipeline stages.

---

## High-level flow

```text
User Request
     |
     v
Understand + identify problem (anomaly first)
     |
     v
Ask only missing REAL choices
     |
     v
Update schemas/ml-project.yaml
     |
     v
Requirements Gate  ---- FAIL ----> ask again / stop
     |
     PASS
     v
Apply anomaly LOCK tables (model, metric, serve)
     |
     v
Fill locked pipeline templates
     |
     v
(Platform adapter later — Databricks)
```

**Hard stop:** No implementation code until requirements gate PASSES and locks are applied.

---

## Canonical specification (single source of truth)

File: `schemas/ml-project.yaml`

- One project = one spec file.
- Skills may update owned sections.
- Skills must **not** create a second competing spec.
- Skills must **not** re-interpret the original chat once the field is saved.

After each user answer:

1. Write the value into the spec.
2. Set requirement state: `provided` / `derived` / `confirmed`.
3. Re-run completeness check.

---

## What to ask the user (anomaly only)

Ask only these **real choices**. Do not ask for model name or metric name — those are locked.

### Required user / derived fields (must be non-null to pass gate)

| Field in spec | Ask user? | Notes |
|---|---|---|
| `project.name` | Yes (or derive) | Short project name |
| `business.objective` | Yes | What decision changes |
| `project.problem_type` | Derive if clear | Must be `anomaly_detection` |
| `data.source.location` | Yes | Table / path / URI |
| `data.source.type` | Yes / derive | table, files, db, etc. |
| `anomaly_detection.definition.*` | Yes | What is normal vs abnormal + action |
| `anomaly_detection.entity.columns` | Yes if ambiguous | What entity (machine, line, sensor…) |
| `anomaly_detection.labels.available` | Yes | **true / false** |
| `inference.mode` | Yes | **batch / realtime** |
| `platform.name` | Yes if unknown | e.g. databricks |

### Conditional (required only when triggered)

| If… | Then also require |
|---|---|
| `labels.available = true` | `labels.column`, label meaning |
| `inference.mode = realtime` | `operational_requirements.latency` |
| `inference.mode = batch` | `inference.frequency` (e.g. daily, hourly) |
| timestamp matters for context | `data.timestamp.column` |

### Ask as fixed menus (do not free-pick outside the list)

- Algorithm → show **model menu** (recommended default marked)
- Primary metric → show **metric menu** (recommended default marked)
- Folder layout → fixed template only (no inventing)
- Inference transform fit → always **no** (`fit_allowed: false`)

---

## Requirements gate (pass / fail)

### PASS only if all are true

1. All required fields above are filled (non-null / non-empty).
2. All triggered conditional fields are filled.
3. No unresolved `requirements.conflicts`.
4. `anomaly_detection.definition` has observation, normal, abnormal, expected_action.
5. `anomaly_detection.labels.available` is explicitly true or false.
6. `inference.mode` is `batch` or `realtime`.
7. `data.source.location` is present.

### FAIL behavior

```text
FAIL
  → list missing fields in gates.requirements.blocking_reasons
  → ask the next highest-priority missing question
  → do NOT apply model locks as final
  → do NOT generate code or templates
```

Soft “looks complete” is not allowed. Gate is binary: **passed | failed**.

---

## Anomaly decision locks (fixed menus + recommended defaults)

Apply **after** requirements gate PASSES.  
**Show the user a fixed option menu** for model and metrics. Do not invent options.
Recommended defaults keep projects consistent; user choice is saved in the spec.

Full menus live in `skills/ml/anamoly-detection/options.md`.

### Lock A — Algorithm menu

Offer only:

`isolation_forest` | `one_class_svm` | `lof` | `autoencoder` | `cnn` | `lstm` | `lightgbm`

```text
labels.available == true (reliable)
    → recommend lightgbm
    → still show full menu; save user pick

labels.available == false + tabular
    → recommend isolation_forest

labels.available == false + sequence/time series
    → recommend lstm

labels.available == false + image/grid
    → recommend cnn
```

User must confirm or pick another **menu id**. Record in `ml_design.selected_algorithm`.

### Lock B — Metric menu

Offer only:

`precision` | `recall` | `f1` | `pr_auc` | `roc_auc` | `precision_at_k` |
`expert_review_hit_rate` | `score_stability` | `anomaly_score_distribution`

```text
labels.available == true
    → recommend primary: pr_auc
    → also offer: precision, recall, f1, roc_auc

labels.available == false + known incidents
    → recommend primary: precision_at_k

labels.available == false + no labels at all
    → recommend primary: expert_review_hit_rate
    → also require: score_stability (+ log score distribution)

Never optimize accuracy alone for anomaly/fraud.
```

User picks **one primary** (optional secondaries). Save to `ml_design.validation_strategy`.

### Lock C — Inference mode defaults

```text
User said daily / hourly / scheduled
    → inference.mode = batch

User said API / milliseconds / interactive app
    → inference.mode = realtime

If unclear → ASK (batch vs realtime). Do not guess.
```

### Lock D — Threshold

```text
supervised → threshold from validation (F1 or business cost if provided)
unsupervised → quantile threshold from training scores
               default contamination / expected rate from
               anomaly_detection.expected_anomaly_frequency
               if missing → ASK once, else default 0.01
```

### Lock E — Pipeline stages (fixed order)

Every anomaly project uses the same stages. Do not add/remove without a recorded exception.

```text
1. ingest
2. validate_schema_and_quality
3. features
4. fit_transforms_on_train_only
5. train
6. evaluate
7. register_model_and_transforms
8. infer (batch job or serving)
9. monitor (optional flag, but stage exists in template)
```

### Lock F — Train / infer transform rule

```text
Training: fit transforms → persist artifact → transform → train
Inference: load artifact → transform → predict
Inference: fit_allowed = false   (always)
```

---

## Fulfillment criteria (same results for everyone)

Two runs are considered **consistent** if they match on all of the following when inputs match:

| Must match | May differ slightly |
|---|---|
| `problem_type` | `project.name` |
| `selected_algorithm.name` | Exact threshold value |
| Primary metric | Cluster / compute size |
| `inference.mode` | Catalog / table path strings |
| Pipeline stage list and order | Column display names |
| Transform fit rule (`fit_allowed=false` on infer) | |
| Spec sections filled | |

**Target:** ≤ ~10% difference, only in the “may differ” column.

---

## Locked pipeline template shape (anomaly)

Do not invent a different layout. Fill this skeleton (platform adapter fills paths later):

```text
01_intake/       answers + charter from ml-project.yaml
02_data/         load + quality checks
03_features/     feature contract
04_train/        IsolationForest or LightGBM (from lock)
05_evaluate/     locked metrics + pass/fail vs baseline
06_register/     model + transformation versions
07_infer/        batch and/or realtime (from lock)
08_monitor/      drift / score / volume
09_ops/          job schedule / triggers
```

Code generation (when added) must copy this template and substitute values from the spec only.

---

## Gates summary

| Gate | Pass when |
|---|---|
| **Requirements** | Required + conditional fields filled; no conflicts |
| **ML design** | Locks A–D applied and written to spec |
| **Architecture** | Pipeline stages = Lock E; transform rule = Lock F |
| **Implementation** (later) | Generated from templates only; matches spec |
| **Validation** (later) | Checks pass against spec |

Failed gate → return to owning stage. No silent bypass.

---

## Human decision points only

Ask the user when:

1. Labels exist or not.
2. Batch vs realtime.
3. Entity / anomaly business definition is ambiguous.
4. Multiple entity columns are plausible.
5. A fallback away from the locked default model is requested.

Do **not** ask:

- “Which model do you prefer?” (use Lock A)
- “Which metric?” (use Lock B)
- “How should we structure folders?” (use template)

---

## Out of scope for this version

- Classification and regression locks (next)
- Full Databricks / AWS code generation
- Auto-picking exotic deep models by default

---

## Extensibility (later)

Same pattern for new problem types:

1. Add required fields for that problem.
2. Add Lock A/B tables for that problem.
3. Reuse same gates, spec file, and template stages.

```text
anomaly_detection   ← current
classification      ← next
regression          ← next
```

---

## Responsibility boundary

| Layer | Does | Does not |
|---|---|---|
| Orchestrator | Order, gates, routing | Pick algorithms |
| Requirements | Ask real choices, update spec | Generate code |
| Anomaly skill | Apply Lock A–D | Invent models outside table |
| Templates / platform (later) | Fill locked skeleton | Redesign pipeline |

---

## Bottom line

Determinism is not “smarter AI.”

It is:

```text
Locked questions
  + ml-project.yaml
  + pass/fail gate
  + locked model/metric/serve tables
  + fixed templates
```

Same answers → same anomaly project.
