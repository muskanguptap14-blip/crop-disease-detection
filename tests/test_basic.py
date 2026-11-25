"""Small tests for preprocessing and project integration."""

import json
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocess import preprocess_image
from src.config import CLASS_NAMES_PATH, DISEASE_INFO_PATH, MODEL_PATH
from src.disease_info import check_info_coverage


def test_preprocess_shape_and_range():
    image = np.full((300, 300, 3), 128, dtype=np.uint8)
    batch = preprocess_image(image)
    assert batch.shape == (1, 224, 224, 3)
    assert float(batch.min()) >= -1.0
    assert float(batch.max()) <= 1.0


def test_class_names_match_model_output_size():
    if not CLASS_NAMES_PATH.is_file():
        return
    class_names = json.loads(CLASS_NAMES_PATH.read_text(encoding="utf-8"))
    assert len(class_names) >= 2
    if MODEL_PATH.is_file():
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH)
        assert model.output_shape[-1] == len(class_names)


def test_disease_info_covers_all_classes():
    if not CLASS_NAMES_PATH.is_file():
        return
    assert check_info_coverage()


def test_predict_result_keys_exist():
    expected = {"label", "display_name", "confidence", "top3", "is_healthy", "crop"}
    if not MODEL_PATH.is_file():
        return
    from src.predict import predict_image
    image = np.full((224, 224, 3), 128, dtype=np.uint8)
    result = predict_image(image)
    assert expected.issubset(result.keys())