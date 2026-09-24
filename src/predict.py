"""
Batch scoring for credit card anomaly detection.

Usage:
  python src/predict.py --input creditcard_data.csv --output predictions.csv
  python src/predict.py --input new_transactions.csv --output scored.csv

Output CSV has the original columns plus:
  fraud_score   continuous anomaly score (higher = more suspicious)
  fraud_flag    1 if fraud_score >= threshold else 0
"""

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).parent.parent
ARTIFACT_DIR = ROOT / "artifacts"


def load_artifacts():
    scaler = joblib.load(ARTIFACT_DIR / "scaler.pkl")
    model  = joblib.load(ARTIFACT_DIR / "model.pkl")
    with open(ARTIFACT_DIR / "threshold.json") as f:
        meta = json.load(f)
    return scaler, model, meta


def score_batch(df: pd.DataFrame, scaler, model, meta) -> pd.DataFrame:
    feature_cols = meta["feature_cols"]
    threshold    = meta["threshold"]

    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Input is missing columns: {missing}")

    X = scaler.transform(df[feature_cols].values)

    scores = -model.decision_function(X)  # negate: higher = more anomalous

    result = df.copy()
    result["fraud_score"] = scores.round(6)
    result["fraud_flag"]  = (scores >= threshold).astype(int)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  required=True, help="Path to input CSV")
    parser.add_argument("--output", required=True, help="Path to write scored CSV")
    args = parser.parse_args()

    print(f"Loading artifacts from {ARTIFACT_DIR}/")
    scaler, model, meta = load_artifacts()
    print(f"  threshold={meta['threshold']:.4f}  n_neighbors={meta['n_neighbors']}")

    print(f"Reading {args.input}...")
    df = pd.read_csv(args.input)
    print(f"  {len(df):,} rows")

    result = score_batch(df, scaler, model, meta)

    flagged = result["fraud_flag"].sum()
    print(f"  Flagged as fraud: {flagged} ({flagged/len(result)*100:.3f}%)")

    result.to_csv(args.output, index=False)
    print(f"Predictions written to {args.output}")


if __name__ == "__main__":
    main()
