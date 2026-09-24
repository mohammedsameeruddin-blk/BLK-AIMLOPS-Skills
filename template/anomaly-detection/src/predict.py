"""
Anomaly Detection — Batch Scoring

Usage:
  python src/predict.py --input new_data.csv --output scored.csv
  python src/predict.py --input new_data.csv --output scored.csv --config ml-project.yaml

Output CSV = input CSV + two columns:
  anomaly_score   continuous score (higher = more suspicious)
  anomaly_flag    1 if anomaly_score >= threshold else 0
"""

import argparse
import json
import sys
from pathlib import Path

import joblib
import importlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

import utils.config as cfg_mod

ARTIFACT_DIR = ROOT / "artifacts"

MODEL_REGISTRY = {
    "lof":              "models.lof",
    "isolation_forest": "models.isolation_forest",
    "lightgbm":         "models.lightgbm_model",
    "autoencoder":      "models.autoencoder",
}


def main(args):
    # ── Load artifacts ────────────────────────────────────────────────────────
    meta_path = ARTIFACT_DIR / "meta.json"
    if not meta_path.exists():
        print(f"ERROR: artifacts not found at {ARTIFACT_DIR}. Run train.py first.")
        sys.exit(1)

    with open(meta_path) as f:
        meta = json.load(f)

    scaler      = joblib.load(ARTIFACT_DIR / "scaler.pkl")
    model_obj   = joblib.load(ARTIFACT_DIR / "model.pkl")
    model_name  = meta["model_name"]
    threshold   = meta["threshold"]
    feature_cols = meta["feature_cols"]
    model_meta  = meta["model_meta"]

    module = importlib.import_module(MODEL_REGISTRY[model_name])
    print(f"Model: {model_name}  threshold={threshold:.4f}")

    # ── Load input ────────────────────────────────────────────────────────────
    df = pd.read_csv(args.input)
    print(f"Input: {args.input}  ({len(df):,} rows)")

    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        print(f"ERROR: input CSV missing columns: {missing}")
        sys.exit(1)

    X = scaler.transform(df[feature_cols].values.astype(float))
    scores = module.get_scores(model_obj, X, model_meta)

    df["anomaly_score"] = scores.round(6)
    df["anomaly_flag"]  = (scores >= threshold).astype(int)

    flagged = int(df["anomaly_flag"].sum())
    print(f"Flagged: {flagged:,} ({flagged/len(df)*100:.3f}%)")

    df.to_csv(args.output, index=False)
    print(f"Saved → {args.output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch anomaly scoring")
    parser.add_argument("--input",  required=True, help="Input CSV path")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument("--config", default=None,  help="ml-project.yaml (optional)")
    main(parser.parse_args())
