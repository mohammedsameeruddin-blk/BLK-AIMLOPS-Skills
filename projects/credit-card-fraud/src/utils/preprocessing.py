"""
Data loading and feature preprocessing for the anomaly detection skill.

Rules:
- Fit scaler only on training data; transform val/test.
- For unsupervised models, fit scaler on normal-class rows only.
- RobustScaler is used for all features (handles extreme-value outliers).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split

from utils.config import get


def load_dataset(cfg: dict) -> tuple[np.ndarray, np.ndarray | None, list[str]]:
    """
    Returns (X, y, feature_cols).
    y is None if target_column is not present in the CSV.
    """
    path = get(cfg, "data.path")
    target_col = get(cfg, "data.target_column")
    feature_spec = get(cfg, "data.feature_columns", "auto")

    df = pd.read_csv(path)

    if feature_spec == "auto":
        feature_cols = [c for c in df.columns if c != target_col]
    else:
        feature_cols = list(feature_spec)

    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Feature columns not found in CSV: {missing}")

    X = df[feature_cols].values.astype(float)

    y = None
    if target_col and target_col in df.columns:
        anomaly_value = get(cfg, "data.anomaly_value", 1)
        y = (df[target_col] == anomaly_value).astype(int).values

    return X, y, feature_cols


def split_data(
    X: np.ndarray,
    y: np.ndarray | None,
    cfg: dict,
) -> tuple:
    """
    Returns (X_train, X_val, X_test, y_train, y_val, y_test).
    y arrays are None when y is None.
    """
    test_size = get(cfg, "ml_design.training_strategy.test_size", 0.2)
    val_size  = get(cfg, "ml_design.training_strategy.val_size", 0.2)
    seed      = get(cfg, "ml_design.training_strategy.random_state", 42)
    stratify  = get(cfg, "ml_design.training_strategy.stratify", True) and y is not None

    stratify_arr = y if stratify else None

    X_tv, X_test, y_tv, y_test = train_test_split(
        X, y if y is not None else np.zeros(len(X)),
        test_size=test_size, stratify=stratify_arr, random_state=seed,
    )

    stratify_tv = y_tv if stratify else None
    X_train, X_val, y_train, y_val = train_test_split(
        X_tv, y_tv,
        test_size=val_size, stratify=stratify_tv, random_state=seed,
    )

    if y is None:
        y_train = y_val = y_test = None

    return X_train, X_val, X_test, y_train, y_val, y_test


def fit_scaler(X_train: np.ndarray, y_train: np.ndarray | None = None, normal_only: bool = False) -> RobustScaler:
    """Fit RobustScaler. If normal_only=True, fit on Class==0 rows only."""
    if normal_only and y_train is not None:
        X_fit = X_train[y_train == 0]
    else:
        X_fit = X_train
    scaler = RobustScaler()
    scaler.fit(X_fit)
    return scaler
