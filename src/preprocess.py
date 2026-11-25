"""Shared image preprocessing for training and Streamlit inference."""

import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import IMG_SIZE, OUTPUT_DIR


def preprocess_image(image_or_path) -> np.ndarray | tf.Tensor:
    """Read/resize/normalize images for both tf.data and single-image inference."""
    if tf.is_tensor(image_or_path):
        image = tf.cast(image_or_path, tf.float32)
        image = tf.image.resize(image, IMG_SIZE, method="area")
        return preprocess_input(image)

    if isinstance(image_or_path, (str, Path)):
        image = cv2.imread(str(image_or_path), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("The image could not be read.")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image = np.asarray(image_or_path)
        if image.ndim == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    image = cv2.resize(image, IMG_SIZE, interpolation=cv2.INTER_AREA)
    batch = np.expand_dims(image.astype(np.float32), axis=0)
    return preprocess_input(batch)


def save_original_processed(image_or_path, output_name: str = "original_processed.png") -> Path:
    """Save a slide-friendly original-versus-processed comparison."""
    if isinstance(image_or_path, (str, Path)):
        original = cv2.imread(str(image_or_path), cv2.IMREAD_COLOR)
        if original is not None:
            original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    else:
        original_rgb = np.asarray(image_or_path)
        if original_rgb.ndim == 2:
            original_rgb = cv2.cvtColor(original_rgb, cv2.COLOR_GRAY2RGB)
        elif original_rgb.shape[2] == 4:
            original_rgb = cv2.cvtColor(original_rgb, cv2.COLOR_RGBA2RGB)
        original = original_rgb
    if original is None:
        raise ValueError("The image could not be read.")

    processed = preprocess_image(image_or_path)[0]
    processed = np.clip((processed + 1.0) * 127.5, 0, 255).astype(np.uint8)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / output_name
    figure, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(original_rgb)
    axes[0].set_title("Original leaf image")
    axes[1].imshow(processed)
    axes[1].set_title("Processed 224 x 224 image")
    for axis in axes:
        axis.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path