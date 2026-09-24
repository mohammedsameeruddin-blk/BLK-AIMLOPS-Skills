"""Isolation Forest — unsupervised anomaly detection."""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import IsolationForest

from utils.config import get


def train(X_train: np.ndarray, y_train: np.ndarray | None, cfg: dict):
    """
    Fit IsolationForest on all training rows (unsupervised).
    Returns (model, meta_dict).
    """
    hp = cfg.get("hyperparameters", {}).get("isolation_forest", {})
    n_estimators  = int(hp.get("n_estimators", 100))
    contamination = hp.get("contamination", "auto")
    seed          = int(hp.get("random_state", 42))
    if contamination != "auto":
        contamination = float(contamination)

    print(f"  [IsolationForest] n_estimators={n_estimators}  contamination={contamination}")

    model = IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        random_state=seed,
        n_jobs=-1,
    )
    model.fit(X_train)

    meta = {"n_estimators": n_estimators, "contamination": contamination}
    return model, meta


def get_scores(model, X: np.ndarray, meta: dict) -> np.ndarray:
    """Higher score = more anomalous."""
    return -model.decision_function(X)
