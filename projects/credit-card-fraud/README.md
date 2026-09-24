# Anomaly Detection Skill Template

A reusable, config-driven ML pipeline for anomaly / fraud detection on tabular data.

## Supported models

| ID | Model | Labels needed? |
|---|---|---|
| `lof` | Local Outlier Factor | No (unsupervised) |
| `isolation_forest` | Isolation Forest | No (unsupervised) |
| `lightgbm` | LightGBM classifier | Yes |
| `autoencoder` | Autoencoder (PyTorch) | No (unsupervised) |

---

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your project

Edit `ml-project.yaml`:

```yaml
project:
  name: my-fraud-detection

data:
  path: data/transactions.csv   # ← your CSV
  target_column: is_fraud       # ← label column (0=normal, 1=anomaly)
  anomaly_value: 1
  feature_columns: auto         # or list: [col1, col2, ...]

ml_design:
  selected_algorithm:
    name: lof                   # lof | isolation_forest | lightgbm | autoencoder
  validation_strategy:
    primary_metric: f1          # f1 | pr_auc | precision | recall | roc_auc
```

### 3. Train

```bash
python src/train.py
# or override config on the fly:
python src/train.py --set ml_design.selected_algorithm.name=isolation_forest
python src/train.py --set data.path=new_data.csv --set hyperparameters.lof.n_neighbors=100
```

### 4. Score a batch

```bash
python src/predict.py --input data/new_transactions.csv --output scored.csv
```

### 5. Evaluate (if ground-truth labels are available)

```bash
python src/evaluate.py --predictions scored.csv --label-col is_fraud
```

---

## Outputs

After training, `artifacts/` contains:

| File | Contents |
|---|---|
| `scaler.pkl` | Fitted RobustScaler |
| `model.pkl` | Fitted model object |
| `meta.json` | threshold, feature_cols, model_name, val metrics |
| `train_report.json` | Val + test metric summary |

---

## Config reference

```yaml
hyperparameters:
  lof:
    n_neighbors: 50          # higher = smoother boundary, slower
    contamination: auto      # "auto" or expected anomaly rate (float)

  isolation_forest:
    n_estimators: 100
    contamination: auto

  lightgbm:
    n_estimators: 300
    max_depth: 6
    learning_rate: 0.05
    scale_pos_weight: auto   # "auto" = n_normal/n_anomaly

  autoencoder:
    hidden_dims: [32, 16, 32]   # symmetric encoder-bottleneck-decoder
    epochs: 50
    batch_size: 256
    learning_rate: 0.001

ml_design:
  threshold_strategy:
    method: f1_maximization  # f1_maximization | percentile | fixed
    percentile: 99.0         # used when method=percentile
    fixed_value: null        # used when method=fixed
```

---

## File structure

```
template/anomaly-detection/
  ml-project.yaml      ← fill this in, then run train.py
  requirements.txt
  src/
    train.py           ← main training script
    predict.py         ← batch scoring
    evaluate.py        ← metric report
    models/
      lof.py
      isolation_forest.py
      lightgbm_model.py
      autoencoder.py
    utils/
      config.py        ← yaml loader + --set CLI overrides
      preprocessing.py ← data loading, splitting, scaling
      metrics.py       ← threshold tuning, F1/PR-AUC/ROC-AUC
  artifacts/           ← written by train.py (gitignored)
```
