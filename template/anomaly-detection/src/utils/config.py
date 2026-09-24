"""
Load ml-project.yaml and apply CLI --set overrides.

CLI override syntax:  --set hyperparameters.lof.n_neighbors=100
                      --set ml_design.selected_algorithm.name=isolation_forest
                      --set data.path=my_data.csv
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml


def load(yaml_path: str | Path, overrides: list[str] | None = None) -> dict:
    """Return merged config: yaml base + any --set key=value overrides."""
    path = Path(yaml_path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    with open(path) as f:
        cfg = yaml.safe_load(f)

    if overrides:
        for override in overrides:
            _apply_override(cfg, override)

    return cfg


def _apply_override(cfg: dict, override: str) -> None:
    if "=" not in override:
        raise ValueError(f"--set override must be key=value, got: {override!r}")
    key_path, raw_value = override.split("=", 1)
    keys = key_path.strip().split(".")
    value = _coerce(raw_value.strip())

    node = cfg
    for k in keys[:-1]:
        if k not in node or not isinstance(node[k], dict):
            node[k] = {}
        node = node[k]
    node[keys[-1]] = value


def _coerce(value: str) -> Any:
    """Cast a string to int, float, bool, None, list, or leave as str."""
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() in ("null", "none", "~"):
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    # simple list: [a, b, c]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [_coerce(v.strip()) for v in inner.split(",") if v.strip()]
    return value


def get(cfg: dict, dot_path: str, default: Any = None) -> Any:
    """Safely read a nested value: get(cfg, 'ml_design.selected_algorithm.name')."""
    node = cfg
    for k in dot_path.split("."):
        if not isinstance(node, dict) or k not in node:
            return default
        node = node[k]
    return node
