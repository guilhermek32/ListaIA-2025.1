"""Utility functions for data processing."""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional


def load_csv(filepath: str, **kwargs) -> pd.DataFrame:
    """Load CSV file into pandas DataFrame."""
    return pd.read_csv(filepath, **kwargs)


def save_csv(df: pd.DataFrame, filepath: str, **kwargs) -> None:
    """Save DataFrame to CSV file."""
    df.to_csv(filepath, index=False, **kwargs)


def normalize_array(arr: np.ndarray) -> np.ndarray:
    """Normalize numpy array to [0, 1] range."""
    min_val = np.min(arr)
    max_val = np.max(arr)
    if max_val - min_val == 0:
        return np.zeros_like(arr)
    return (arr - min_val) / (max_val - min_val)


def calculate_statistics(data: np.ndarray) -> Dict[str, float]:
    """Calculate basic statistics for numpy array."""
    return {
        "mean": float(np.mean(data)),
        "median": float(np.median(data)),
        "std": float(np.std(data)),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
    }
