"""
Anomaly Detection — Evaluation

Usage:
  python src/evaluate.py --predictions scored.csv

Expects scored.csv to have:
  - a ground-truth label column (default: 'Class', override with --label-col)
  - anomaly_score  (continuous score from predict.py)
  - anomaly_flag   (binary prediction from predict.py)
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    f1_score, precision_score, recall_score,
    average_precision_score, roc_auc_score,
    confusion_matrix, classification_report,
)

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def main(args):
    df = pd.read_csv(args.predictions)

    for col in [args.label_col, "anomaly_flag", "anomaly_score"]:
        if col not in df.columns:
            print(f"ERROR: column '{col}' not found in {args.predictions}")
            sys.exit(1)

    y_true  = df[args.label_col].values
    y_pred  = df["anomaly_flag"].values
    scores  = df["anomaly_score"].values

    f1        = f1_score(y_true, y_pred, zero_division=0)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall    = recall_score(y_true, y_pred, zero_division=0)
    pr_auc    = average_precision_score(y_true, scores)
    roc_auc   = roc_auc_score(y_true, scores)

    print("\n=== Evaluation Report ===")
    print(f"  F1        : {f1:.4f}")
    print(f"  Precision : {precision:.4f}")
    print(f"  Recall    : {recall:.4f}")
    print(f"  PR-AUC    : {pr_auc:.4f}")
    print(f"  ROC-AUC   : {roc_auc:.4f}")

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print(f"\n=== Confusion Matrix ===")
    print(f"  True Negatives  (normal  → normal)  : {tn:,}")
    print(f"  False Positives (normal  → anomaly) : {fp:,}")
    print(f"  False Negatives (anomaly → normal)  : {fn:,}")
    print(f"  True Positives  (anomaly → anomaly) : {tp:,}")

    print(f"\n=== Classification Report ===")
    print(classification_report(y_true, y_pred, target_names=["normal", "anomaly"], zero_division=0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate anomaly detection predictions")
    parser.add_argument("--predictions", required=True, help="Scored CSV from predict.py")
    parser.add_argument("--label-col",   default="Class", help="Ground-truth column (default: Class)")
    main(parser.parse_args())
