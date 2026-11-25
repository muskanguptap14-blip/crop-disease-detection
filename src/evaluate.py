"""Evaluate the trained model and produce report plots."""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    CLASS_NAMES_PATH,
    MODEL_PATH,
    OUTPUT_DIR,
)
from src.data_loader import build_datasets


def main() -> None:
    if not MODEL_PATH.is_file():
        raise FileNotFoundError("Train the model first: python src/train.py")

    _, valid_ds, class_names = build_datasets()
    model = tf.keras.models.load_model(MODEL_PATH)
    probabilities = model.predict(valid_ds, verbose=1)
    predicted = np.argmax(probabilities, axis=1)

    actual = np.concatenate([labels.numpy() for _, labels in valid_ds])
    actual = np.argmax(actual, axis=1)

    accuracy = accuracy_score(actual, predicted)
    precision = precision_score(actual, predicted, average="macro", zero_division=0)
    recall = recall_score(actual, predicted, average="macro", zero_division=0)
    f1 = f1_score(actual, predicted, average="macro", zero_division=0)

    print("\nClassification report:")
    print(classification_report(actual, predicted, target_names=class_names, zero_division=0))
    print(f"\nAccuracy: {accuracy:.4%}")
    print(f"Macro precision: {precision:.4%}")
    print(f"Macro recall: {recall:.4%}")
    print(f"Macro F1: {f1:.4%}")

    matrix = confusion_matrix(actual, predicted)
    plt.figure(figsize=(16, 14))
    sns.heatmap(matrix, cmap="Blues", xticklabels=class_names, yticklabels=class_names)
    plt.xlabel("Predicted class")
    plt.ylabel("True class")
    plt.xticks(rotation=90, fontsize=7)
    plt.yticks(rotation=0, fontsize=7)
    plt.tight_layout()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=180)
    plt.close()

    confused = []
    for true_index in range(len(class_names)):
        for predicted_index in range(len(class_names)):
            if true_index != predicted_index and matrix[true_index, predicted_index] > 0:
                confused.append(
                    (int(matrix[true_index, predicted_index]),
                     class_names[true_index],
                     class_names[predicted_index])
                )
    confused.sort(reverse=True)

    print("\n5 most confused class pairs:")
    for count, true_name, predicted_name in confused[:5]:
        print(f"{true_name} -> {predicted_name}: {count} images")

    print("\nReport table:")
    print("Metric | Value")
    print("---|---")
    print(f"Accuracy | {accuracy:.4%}")
    print(f"Macro precision | {precision:.4%}")
    print(f"Macro recall | {recall:.4%}")
    print(f"Macro F1 | {f1:.4%}")
    print(f"Number of classes | {len(class_names)}")
    print(f"Saved confusion matrix | {OUTPUT_DIR / 'confusion_matrix.png'}")


if __name__ == "__main__":
    main()