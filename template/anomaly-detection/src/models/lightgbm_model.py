"""LightGBM supervised classifier — requires labels.available: true."""

from __future__ import annotations

import numpy as np

from utils.config import get


def train(X_train: np.ndarray, y_train: np.ndarray | None, cfg: dict):
    """
    Fit a binary LightGBM classifier.
    Returns (model, meta_dict).
    Raises ValueError if labels are unavailable.
    """
    if y_train is None or not np.any(y_train == 1):
        raise ValueError(
            "lightgbm requires labels.available: true and at least one anomaly in training data."
        )

    try:
        import lightgbm as lgb
    except ImportError:
        raise ImportError("lightgbm is not installed. Run: pip install lightgbm")

    hp = cfg.get("hyperparameters", {}).get("lightgbm", {})
    n_estimators  = int(hp.get("n_estimators", 300))
    max_depth     = int(hp.get("max_depth", 6))
    learning_rate = float(hp.get("learning_rate", 0.05))
    spw           = hp.get("scale_pos_weight", "auto")

    if spw == "auto":
        n_normal = int((y_train == 0).sum())
        n_fraud  = int((y_train == 1).sum())
        spw = n_normal / max(n_fraud, 1)

    print(f"  [LightGBM] n_estimators={n_estimators}  scale_pos_weight={spw:.1f}")

    model = lgb.LGBMClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        scale_pos_weight=spw,
        n_jobs=-1,
        verbose=-1,
    )
    model.fit(X_train, y_train)

    meta = {"n_estimators": n_estimators, "scale_pos_weight": spw}
    return model, meta


def get_scores(model, X: np.ndarray, meta: dict) -> np.ndarray:
    """Returns fraud probability — higher = more anomalous."""
    return model.predict_proba(X)[:, 1]
