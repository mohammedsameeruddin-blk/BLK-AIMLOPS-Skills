"""
Train LOF anomaly detector on credit card data.

Artifacts written to ../artifacts/:
  scaler.pkl       RobustScaler fit on train set (all features)
  model.pkl        LocalOutlierFactor (novelty=True, fit on normal-only)
  threshold.json   Decision threshold maximizing F1 on validation set
  train_report.json  Full metric report
"""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import (
    f1_score, precision_score, recall_score,
    average_precision_score, roc_auc_score,
    precision_recall_curve,
)
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).parent.parent
DATA_PATH = ROOT / "creditcard_data.csv"
ARTIFACT_DIR = ROOT / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

RANDOM_STATE = 42
TEST_SIZE = 0.2
N_NEIGHBORS = 50          # tuned: higher k improves LOF fraud separation
CONTAMINATION = 0.00173   # expected fraud rate


def load_data():
    df = pd.read_csv(DATA_PATH)
    feature_cols = [c for c in df.columns if c != "Class"]
    X = df[feature_cols].values
    y = df["Class"].values
    return X, y, feature_cols


def scale_features(X_train, X_val, X_test):
    # RobustScaler on all features — handles outlier-heavy Amount/Time without distortion
    scaler = RobustScaler()
    X_train = scaler.fit_transform(X_train)
    X_val   = scaler.transform(X_val)
    X_test  = scaler.transform(X_test)
    return scaler, X_train, X_val, X_test


def find_best_threshold(scores, y_true):
    """Return (threshold, f1) that maximizes F1 on the given set."""
    precisions, recalls, thresholds = precision_recall_curve(y_true, scores)
    with np.errstate(invalid="ignore"):
        f1s = np.where(
            (precisions + recalls) == 0,
            0.0,
            2 * precisions * recalls / (precisions + recalls),
        )
    best_idx = int(np.argmax(f1s[:-1]))
    return float(thresholds[best_idx]), float(f1s[best_idx])


def compute_metrics(y_true, y_pred, scores):
    return {
        "f1":        round(f1_score(y_true, y_pred, zero_division=0), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall":    round(recall_score(y_true, y_pred, zero_division=0), 4),
        "pr_auc":    round(average_precision_score(y_true, scores), 4),
        "roc_auc":   round(roc_auc_score(y_true, scores), 4),
    }


def main():
    print("Loading data...")
    X, y, feature_cols = load_data()

    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.2, stratify=y_trainval, random_state=RANDOM_STATE
    )

    print(f"Train: {len(X_train):,}  Val: {len(X_val):,}  Test: {len(X_test):,}")
    print(f"Train fraud: {y_train.sum()}  Val fraud: {y_val.sum()}  Test fraud: {y_test.sum()}")

    scaler, X_train, X_val, X_test = scale_features(X_train, X_val, X_test)

    # Fit only on normal (Class=0) transactions — LOF learns the normal manifold
    X_train_normal = X_train[y_train == 0]
    print(f"Fitting LOF on {len(X_train_normal):,} normal transactions (n_neighbors={N_NEIGHBORS})...")
    model = LocalOutlierFactor(
        n_neighbors=N_NEIGHBORS,
        contamination=CONTAMINATION,
        novelty=True,
        n_jobs=-1,
    )
    model.fit(X_train_normal)

    # LOF decision_function: positive=inlier, negative=outlier → negate for fraud score
    val_scores = -model.decision_function(X_val)
    threshold, val_f1 = find_best_threshold(val_scores, y_val)
    print(f"Best threshold on val: {threshold:.4f}  →  F1={val_f1:.4f}")

    test_scores = -model.decision_function(X_test)
    y_pred_test = (test_scores >= threshold).astype(int)
    test_metrics = compute_metrics(y_test, y_pred_test, test_scores)
    print("\nTest metrics:")
    for k, v in test_metrics.items():
        print(f"  {k}: {v}")

    joblib.dump(scaler, ARTIFACT_DIR / "scaler.pkl")
    joblib.dump(model,  ARTIFACT_DIR / "model.pkl")

    threshold_data = {
        "threshold":     threshold,
        "val_f1":        round(val_f1, 4),
        "n_neighbors":   N_NEIGHBORS,
        "contamination": CONTAMINATION,
        "feature_cols":  feature_cols,
    }
    with open(ARTIFACT_DIR / "threshold.json", "w") as f:
        json.dump(threshold_data, f, indent=2)

    report = {"val": {"f1": round(val_f1, 4)}, "test": test_metrics}
    with open(ARTIFACT_DIR / "train_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nArtifacts saved to {ARTIFACT_DIR}/")


if __name__ == "__main__":
    main()
