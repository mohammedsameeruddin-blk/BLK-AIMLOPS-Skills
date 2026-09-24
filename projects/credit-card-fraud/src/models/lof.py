"""Local Outlier Factor — novelty detection (fit on normal-only)."""

from __future__ import annotations

import numpy as np
from sklearn.neighbors import LocalOutlierFactor

from utils.config import get


def train(X_train: np.ndarray, y_train: np.ndarray | None, cfg: dict):
    """
    Fit LOF on normal (Class=0) rows only.
    Returns (model, meta_dict).
    """
    hp = cfg.get("hyperparameters", {}).get("lof", {})
    n_neighbors   = int(hp.get("n_neighbors", 50))
    contamination = hp.get("contamination", "auto")
    if contamination != "auto":
        contamination = float(contamination)

    X_fit = X_train[y_train == 0] if y_train is not None else X_train
    print(f"  [LOF] fitting on {len(X_fit):,} normal rows  n_neighbors={n_neighbors}")

    model = LocalOutlierFactor(
        n_neighbors=n_neighbors,
        contamination=contamination,
        novelty=True,
        n_jobs=-1,
    )
    model.fit(X_fit)

    meta = {"n_neighbors": n_neighbors, "contamination": contamination}
    return model, meta


def get_scores(model, X: np.ndarray, meta: dict) -> np.ndarray:
    """Higher score = more anomalous."""
    return -model.decision_function(X)
