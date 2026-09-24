"""
Anomaly Detection — Training Orchestrator

Usage:
  python src/train.py                                  # uses ml-project.yaml in repo root
  python src/train.py --config path/to/ml-project.yaml
  python src/train.py --set data.path=my_data.csv --set ml_design.selected_algorithm.name=lightgbm

What it does:
  1. Load config (yaml + CLI overrides)
  2. Load data, split into train / val / test
  3. Fit RobustScaler on training data
  4. Train the selected model
  5. Tune decision threshold on validation set
  6. Evaluate on test set
  7. Save artifacts to <project_root>/artifacts/
"""

import argparse
import json
import sys
from pathlib import Path

import joblib
import numpy as np

# allow `python src/train.py` from the project root
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

import utils.config as cfg_mod
from utils.preprocessing import load_dataset, split_data, fit_scaler
from utils.metrics import find_best_threshold, compute_all

ARTIFACT_DIR = ROOT / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

MODEL_REGISTRY = {
    "lof":              "models.lof",
    "isolation_forest": "models.isolation_forest",
    "lightgbm":         "models.lightgbm_model",
    "autoencoder":      "models.autoencoder",
}


def _import_model(name: str):
    import importlib
    module_path = MODEL_REGISTRY.get(name)
    if module_path is None:
        raise ValueError(f"Unknown model: {name!r}. Choose from: {list(MODEL_REGISTRY)}")
    return importlib.import_module(module_path)


def main(args):
    # ── 1. Config ─────────────────────────────────────────────────────────────
    config_path = args.config or (ROOT / "ml-project.yaml")
    cfg = cfg_mod.load(config_path, overrides=args.set)

    model_name = cfg_mod.get(cfg, "ml_design.selected_algorithm.name")
    if not model_name:
        print("ERROR: set ml_design.selected_algorithm.name in ml-project.yaml or via --set")
        sys.exit(1)

    primary_metric = cfg_mod.get(cfg, "ml_design.validation_strategy.primary_metric", "f1")
    print(f"\n{'='*60}")
    print(f"  Project : {cfg_mod.get(cfg, 'project.name', 'unnamed')}")
    print(f"  Model   : {model_name}")
    print(f"  Metric  : {primary_metric}")
    print(f"{'='*60}\n")

    # ── 2. Load + split data ──────────────────────────────────────────────────
    print("Loading data...")
    X, y, feature_cols = load_dataset(cfg)
    print(f"  {len(X):,} rows  {len(feature_cols)} features", end="")
    if y is not None:
        print(f"  anomalies: {y.sum():,} ({y.mean()*100:.3f}%)")
    else:
        print()

    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y, cfg)
    print(f"  Train: {len(X_train):,}  Val: {len(X_val):,}  Test: {len(X_test):,}")

    # ── 3. Scale ──────────────────────────────────────────────────────────────
    # unsupervised models: fit scaler on normal-only rows (avoids contamination)
    unsupervised = model_name in ("lof", "isolation_forest", "autoencoder")
    scaler = fit_scaler(X_train, y_train, normal_only=unsupervised)
    X_train_s = scaler.transform(X_train)
    X_val_s   = scaler.transform(X_val)
    X_test_s  = scaler.transform(X_test)

    # ── 4. Train ──────────────────────────────────────────────────────────────
    print(f"\nTraining [{model_name}]...")
    module = _import_model(model_name)
    model, model_meta = module.train(X_train_s, y_train, cfg)

    # ── 5. Threshold tuning ───────────────────────────────────────────────────
    val_scores = module.get_scores(model, X_val_s, model_meta)
    if y_val is not None:
        threshold, val_value = find_best_threshold(val_scores, y_val, cfg)
        print(f"\nVal threshold: {threshold:.4f}  {primary_metric}={val_value:.4f}")
    else:
        # No labels — use contamination-based percentile
        contamination = cfg_mod.get(cfg, f"hyperparameters.{model_name}.contamination", "auto")
        pct = 99.0 if contamination == "auto" else (1 - float(contamination)) * 100
        threshold = float(np.percentile(val_scores, pct))
        val_value = None
        print(f"\nVal threshold (percentile {100-pct:.1f}%): {threshold:.4f}")

    # ── 6. Test evaluation ────────────────────────────────────────────────────
    test_scores = module.get_scores(model, X_test_s, model_meta)
    y_pred_test = (test_scores >= threshold).astype(int)

    if y_test is not None:
        test_metrics = compute_all(y_test, y_pred_test, test_scores)
        print("\nTest metrics:")
        for k, v in test_metrics.items():
            marker = " ← primary" if k == primary_metric else ""
            print(f"  {k}: {v}{marker}")
    else:
        flagged = y_pred_test.sum()
        print(f"\nFlagged on test set: {flagged:,} ({flagged/len(y_pred_test)*100:.3f}%)")
        test_metrics = {"flagged": int(flagged)}

    # ── 7. Save artifacts ─────────────────────────────────────────────────────
    joblib.dump(scaler, ARTIFACT_DIR / "scaler.pkl")
    joblib.dump(model,  ARTIFACT_DIR / "model.pkl")

    artifact_meta = {
        "model_name":    model_name,
        "threshold":     threshold,
        "feature_cols":  feature_cols,
        "primary_metric": primary_metric,
        "val_metric":    {primary_metric: round(val_value, 4)} if val_value else None,
        "model_meta":    model_meta,
    }
    with open(ARTIFACT_DIR / "meta.json", "w") as f:
        json.dump(artifact_meta, f, indent=2)

    report = {
        "val":  {primary_metric: round(val_value, 4)} if val_value else None,
        "test": test_metrics,
    }
    with open(ARTIFACT_DIR / "train_report.json", "w") as f:
        json.dump(report, f, indent=2)

    # write decisions back to config
    decisions = cfg_mod.get(cfg, "requirements.user_decisions", [])
    for decision_id, value in [
        ("model", model_name),
        ("primary_metric", primary_metric),
        ("threshold_strategy", cfg_mod.get(cfg, "ml_design.threshold_strategy.method", "f1_maximization")),
    ]:
        if not any(d.get("id") == decision_id for d in decisions):
            decisions.append({"id": decision_id, "value": value, "source": "user"})
    cfg["requirements"]["user_decisions"] = decisions

    import yaml
    with open(config_path, "w") as f:
        yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)

    print(f"\nArtifacts saved → {ARTIFACT_DIR}/")
    print("  scaler.pkl  model.pkl  meta.json  train_report.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train anomaly detection model")
    parser.add_argument("--config", default=None, help="Path to ml-project.yaml")
    parser.add_argument(
        "--set", action="append", default=[], metavar="KEY=VALUE",
        help="Override a config value, e.g. --set data.path=my.csv",
    )
    main(parser.parse_args())
