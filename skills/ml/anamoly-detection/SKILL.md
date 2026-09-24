---
name: anomaly-detection
description: >-
  Interactive anomaly detection skill. Collects all user requirements via
  progressive menus, writes ml-project.yaml, then asks the user whether to
  run training. Use when the problem is anomaly detection, fraud, outlier,
  or suspicious event detection.
---

# Anomaly Detection Skill

## Purpose

Guide the user through every required decision, write their answers into
`template/anomaly-detection/ml-project.yaml`, then offer to run training.

**Important rules:**
- Show menus from [options.md](options.md) — do not invent options.
- Ask **one menu at a time** in the order below.
- Mark the recommended option on every menu.
- Save each answer into `ml-project.yaml` before asking the next question.
- After all required questions are answered, print a summary and ask:
  **"Ready to train? (yes / no)"**
- If yes → run `python src/train.py` from `template/anomaly-detection/`.
- If no → tell the user to edit `ml-project.yaml` and run manually.

---

## Step-by-step flow

### Phase 0 — Create the project folder (always first)

**Ask:**
```
What would you like to call this project? (e.g. credit-card-fraud, sensor-anomaly)
```

Once the user gives a name, run:
```bash
python new_project.py --name <project-name>
```

This creates `projects/<project-name>/` as a clean copy of the template.
All subsequent config writes and training commands use **that folder**, not the template.

Confirm to the user:
```
Created: projects/<project-name>/
I'll collect your requirements and fill in ml-project.yaml there.
```

---

### Phase 1 — Data & context (ask in order, skip if already known)

| Step | Question | Config field written |
|---|---|---|
| 1 | Data source type? | `data.source_type` |
| 2 | Path to your CSV / table? | `data.path` |
| 3 | Which column is the label (0 = normal, 1 = anomaly)? | `data.target_column` |
| 4 | What value means "anomaly" in that column? (default: 1) | `data.anomaly_value` |
| 5 | Anomaly labels available? (true / false / partial) | `anomaly_detection.labels.available` |
| 6 | Anomaly type? (point / contextual / collective) | `anomaly_detection.anomaly_type` |
| 7 | Entity grain — what are we flagging? | `anomaly_detection.entity` |
| 8 | Expected anomaly rate? | `anomaly_detection.expected_anomaly_frequency` |

### Phase 2 — ML design

| Step | Question | Config field written |
|---|---|---|
| 9  | Inference mode? (batch / near_realtime / realtime) | `inference.mode` |
| 10 | Inference frequency? (skip if realtime) | `inference.frequency` |
| 11 | Model? (show menu from options.md §7) | `ml_design.selected_algorithm.name` |
| 12 | Primary metric? (show menu from options.md §8) | `ml_design.validation_strategy.primary_metric` |
| 13 | Secondary metrics? (optional, multi-select) | `ml_design.validation_strategy.secondary_metrics` |
| 14 | Threshold strategy? | `ml_design.threshold_strategy.method` |
| 15 | Train/val split strategy? | `ml_design.training_strategy.split_strategy` |
| 16 | Feature strategy? | `ml_design.feature_strategy` |
| 17 | Explainability? | `ml_design.explainability.strategy` |

### Phase 3 — Operations (ask only if user wants to go further)

| Step | Question | Config field written |
|---|---|---|
| 18 | Action on alert? | `business.action_on_alert` |
| 19 | Monitoring level? | `monitoring.level` |
| 20 | Retraining trigger? | `retraining.trigger.type` |
| 21 | Platform? | `platform.name` |

> Phases 1 and 2 are **required** before training.
> Phase 3 is optional — ask: *"Do you want to configure operations settings
> (monitoring, retraining, platform)? Or skip to training?"*

---

## How to ask each menu (required format)

```
<Question text>

1. <id> — <label>  (recommended)
2. <id> — <label>
3. <id> — <label>
...

Reply with the number, the ID, or "use recommended".
```

One menu per message. Wait for the answer before asking the next.

---

## After all required questions are answered

1. Print a **Configuration Summary** table:

```
=== Your Anomaly Detection Configuration ===

  Data path       : <value>
  Target column   : <value>
  Labels          : <value>
  Model           : <value>
  Primary metric  : <value>
  Threshold       : <value>
  Inference mode  : <value>
  Platform        : <value>
  ... (all filled fields)
```

2. Show the `ml-project.yaml` snippet that will be written.

3. Write all answers into `projects/<project-name>/ml-project.yaml`.

4. Ask:

```
Configuration saved to ml-project.yaml.

Ready to start training? (yes / no)
  yes — runs: python src/train.py  (may take a few minutes)
  no  — you can edit ml-project.yaml and run manually later
```

---

## If user says "yes" — run training

```bash
python projects/<project-name>/src/train.py
```

- Stream the output to the user.
- When training finishes, read `projects/<project-name>/artifacts/train_report.json`
  and print the test metrics.
- Tell the user:

```
Training complete.
Artifacts saved to projects/<project-name>/artifacts/

To score new data:
  python projects/<project-name>/src/predict.py --input <your_file.csv> --output scored.csv

To evaluate predictions:
  python projects/<project-name>/src/evaluate.py --predictions scored.csv --label-col <target_column>
```

---

## If user says "no" — give manual instructions

```
No problem. Your project is ready at projects/<project-name>/

When you're ready, run:
  python projects/<project-name>/src/train.py

Or override any config value on the fly:
  python projects/<project-name>/src/train.py --set ml_design.selected_algorithm.name=lightgbm
  python projects/<project-name>/src/train.py --set data.path=my_data.csv
```

---

## Model recommendation rules (from options.md)

```
labels.available == true
    → recommend lightgbm

labels.available == false AND tabular
    → recommend isolation_forest

labels.available == false AND time series / sequence
    → recommend lstm  (not yet in template — fall back to isolation_forest)

labels.available == false AND image/grid
    → recommend cnn   (not yet in template — fall back to autoencoder)
```

Always show the full model menu. User may override the recommendation.

---

## Metric recommendation rules

```
labels.available == true
    → recommend primary: pr_auc
    → offer also: f1, precision, recall, roc_auc

labels.available == false AND some known cases exist
    → recommend primary: precision_at_k

labels.available == false AND no eval labels
    → recommend primary: expert_review_hit_rate
    → require secondary: score_stability + anomaly_score_distribution
```

---

## What NOT to do

- Do not ask all menus at once.
- Do not invent model or metric IDs outside [options.md](options.md).
- Do not run `train.py` without explicit user confirmation ("yes").
- Do not skip writing `ml-project.yaml` before offering to train.
- Do not proceed to Phase 3 without asking the user first.

---

## Config fields written (canonical spec)

```yaml
project:
  name: <project.name>

data:
  path: <data.path>
  target_column: <data.target_column>
  anomaly_value: <data.anomaly_value>
  feature_columns: auto

anomaly_detection:
  anomaly_type: <anomaly_detection.anomaly_type>
  entity: <anomaly_detection.entity>
  labels:
    available: <anomaly_detection.labels.available>
  expected_anomaly_frequency: <anomaly_detection.expected_anomaly_frequency>

inference:
  mode: <inference.mode>
  frequency: <inference.frequency>

ml_design:
  selected_algorithm:
    name: <model>
    selection_reason: user_selected
  validation_strategy:
    primary_metric: <primary_metric>
    secondary_metrics: [<secondary_metrics>]
  threshold_strategy:
    method: <threshold_strategy>
  training_strategy:
    split_strategy: <split_strategy>
    test_size: 0.2
    val_size: 0.2
    random_state: 42
    stratify: true
  feature_strategy: <feature_strategy>
  explainability:
    strategy: <explainability>

requirements:
  user_decisions:
    - {id: model,            value: <model>,            source: user}
    - {id: primary_metric,   value: <primary_metric>,   source: user}
    - {id: inference_mode,   value: <inference_mode>,   source: user}
    - ... (one entry per user choice)
```
