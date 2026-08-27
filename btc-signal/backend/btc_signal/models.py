from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class ModelArtifact:
    version: str
    feature_version: str
    training_end: str
    dataset_version: str


def baseline_classifier() -> Pipeline:
    return Pipeline([
        ('scale', StandardScaler()),
        ('classifier', CalibratedClassifierCV(LogisticRegression(max_iter=2000), method='sigmoid', cv=3)),
    ])


def entropy(probabilities: np.ndarray) -> float:
    p = np.clip(probabilities.astype(float), 1e-12, 1 - 1e-12)
    return float(-(p * np.log(p)).sum())
