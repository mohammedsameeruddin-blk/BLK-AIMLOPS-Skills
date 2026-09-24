"""
Evaluate a scored predictions CSV against ground-truth labels.

Usage:
  python src/evaluate.py --predictions predictions.csv

Requires a 'Class' column in the predictions file (ground truth).
Prints F1, precision, recall, PR-AUC, ROC-AUC and a confusion matrix.
"""

import argparse
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    f1_score, precision_score, recall_score,
    average_precision_score, roc_auc_score,
    confusion_matrix, classification_report,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True, help="Scored CSV from predict.py")
    args = parser.parse_args()

    df = pd.read_csv(args.predictions)

    required = {"Class", "fraud_flag", "fraud_score"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Predictions file missing columns: {missing}")

    y_true  = df["Class"].values
    y_pred  = df["fraud_flag"].values
    scores  = df["fraud_score"].values

    f1        = f1_score(y_true, y_pred, zero_division=0)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall    = recall_score(y_true, y_pred, zero_division=0)
    pr_auc    = average_precision_score(y_true, scores)
    roc_auc   = roc_auc_score(y_true, scores)

    print("\n=== Evaluation Report ===")
    print(f"  F1        : {f1:.4f}  ← primary metric")
    print(f"  Precision : {precision:.4f}")
    print(f"  Recall    : {recall:.4f}")
    print(f"  PR-AUC    : {pr_auc:.4f}")
    print(f"  ROC-AUC   : {roc_auc:.4f}")

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print(f"\n=== Confusion Matrix ===")
    print(f"  True Negatives  (legit  → legit)  : {tn:,}")
    print(f"  False Positives (legit  → fraud)  : {fp:,}")
    print(f"  False Negatives (fraud  → legit)  : {fn:,}")
    print(f"  True Positives  (fraud  → fraud)  : {tp:,}")

    print(f"\n=== Classification Report ===")
    print(classification_report(y_true, y_pred, target_names=["legit", "fraud"], zero_division=0))


if __name__ == "__main__":
    main()
