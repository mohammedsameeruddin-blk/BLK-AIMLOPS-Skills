"""
Threshold tuning and metric computation.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    f1_score, precision_score, recall_score,
    average_precision_score, roc_auc_score,
    precision_recall_curve,
)

from utils.config import get


def find_best_threshold(scores: np.ndarray, y_true: np.ndarray, cfg: dict) -> tuple[float, float]:
    """
    Return (threshold, primary_metric_value) based on the strategy in cfg.

    Strategies:
      f1_maximization  — sweep PR curve, pick threshold with highest F1
      percentile       — flag the top N% as anomalies
      fixed            — use cfg threshold_strategy.fixed_value
    """
    strategy = get(cfg, "ml_design.threshold_strategy.method", "f1_maximization")

    if strategy == "fixed":
        t = float(get(cfg, "ml_design.threshold_strategy.fixed_value", 0.0))
        y_pred = (scores >= t).astype(int)
        value = _primary_value(y_true, y_pred, scores, cfg)
        return t, value

    if strategy == "percentile":
        pct = float(get(cfg, "ml_design.threshold_strategy.percentile", 99.0))
        t = float(np.percentile(scores, pct))
        y_pred = (scores >= t).astype(int)
        value = _primary_value(y_true, y_pred, scores, cfg)
        return t, value

    # default: f1_maximization
    precisions, recalls, thresholds = precision_recall_curve(y_true, scores)
    with np.errstate(invalid="ignore"):
        f1s = np.where(
            (precisions + recalls) == 0,
            0.0,
            2 * precisions * recalls / (precisions + recalls),
        )
    best_idx = int(np.argmax(f1s[:-1]))
    t = float(thresholds[best_idx])
    return t, float(f1s[best_idx])


def compute_all(y_true: np.ndarray, y_pred: np.ndarray, scores: np.ndarray) -> dict:
    return {
        "f1":        round(f1_score(y_true, y_pred, zero_division=0), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall":    round(recall_score(y_true, y_pred, zero_division=0), 4),
        "pr_auc":    round(average_precision_score(y_true, scores), 4),
        "roc_auc":   round(roc_auc_score(y_true, scores), 4),
    }


def _primary_value(y_true, y_pred, scores, cfg) -> float:
    primary = get(cfg, "ml_design.validation_strategy.primary_metric", "f1")
    m = compute_all(y_true, y_pred, scores)
    return m.get(primary, m["f1"])
