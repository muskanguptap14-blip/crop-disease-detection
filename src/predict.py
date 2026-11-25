"""Load the trained CNN once and predict one uploaded leaf image."""

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    CLASS_NAMES_PATH,
    CONFIDENCE_THRESHOLD,
    MODEL_PATH,
)
from src.disease_info import load_disease_info
from src.preprocess import preprocess_image


def validate_image(image) -> None:
    """Check the uploaded image object and its basic dimensions."""
    if image is None:
        raise ValueError("Please upload an image.")
    array = np.asarray(image)
    if array.size == 0:
        raise ValueError("The uploaded image is empty.")
    if array.ndim not in (2, 3):
        raise ValueError("This file is not a readable image.")


_MODEL = None
_CLASS_NAMES = None


def load_model_once():
    """Load model and ordered class names only once per Python process."""
    global _MODEL, _CLASS_NAMES
    if _MODEL is None:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                "Model file not found. Run: python src/train.py"
            )
        _MODEL = tf.keras.models.load_model(MODEL_PATH)
    if _CLASS_NAMES is None:
        if not CLASS_NAMES_PATH.is_file():
            raise FileNotFoundError("Class names file not found.")
        _CLASS_NAMES = json.loads(
            CLASS_NAMES_PATH.read_text(encoding="utf-8")
        )
    return _MODEL, _CLASS_NAMES


def predict_image(
    image,
    threshold: float = CONFIDENCE_THRESHOLD,
    model_bundle=None,
) -> dict[str, Any]:
    """Return label, confidence, top three predictions, and healthy status."""
    validate_image(image)
    model, class_names = model_bundle or load_model_once()
    batch = preprocess_image(image)
    probabilities = model.predict(batch, verbose=0)[0]

    ranked = np.argsort(probabilities)[::-1]
    top_index = int(ranked[0])
    confidence = float(probabilities[top_index])
    top3 = [
        {
            "label": class_names[int(index)],
            "display_name": class_names[int(index)].replace("_", " "),
            "confidence": float(probabilities[int(index)]),
        }
        for index in ranked[:3]
    ]

    label = class_names[top_index]
    if confidence < threshold:
        display_name = "Not sure, please upload a clearer leaf photo"
    else:
        display_name = label.replace("_", " ")

    info = load_disease_info(label)
    is_healthy = "healthy" in label.lower()
    return {
        "label": label,
        "display_name": display_name,
        "confidence": confidence,
        "top3": top3,
        "is_healthy": is_healthy,
        "crop": info.get("crop", display_name.split()[0]),
    }