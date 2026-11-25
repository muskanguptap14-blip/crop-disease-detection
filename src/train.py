"""Train a CPU-friendly MobileNetV2 crop disease classifier."""

import argparse
import json
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import tensorflow as tf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    CLASS_NAMES_PATH,
    EPOCHS_FINETUNE,
    EPOCHS_HEAD,
    MODEL_PATH,
    OUTPUT_DIR,
)
from src.data_loader import build_datasets


def build_model(number_of_classes: int) -> tf.keras.Model:
    """Build MobileNetV2 transfer-learning model."""
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = base_model(inputs, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(number_of_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model, base_model


def callbacks() -> list[tf.keras.callbacks.Callback]:
    """Create callbacks for reliable CPU training."""
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    return [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=2, restore_best_weights=True
        ),
        tf.keras.callbacks.ModelCheckpoint(
            str(MODEL_PATH),
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=1, min_lr=1e-6
        ),
    ]


def save_training_curves(history, finetune_history=None) -> None:
    """Save accuracy and loss curves for the final report."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    accuracy = list(history.history["accuracy"])
    val_accuracy = list(history.history["val_accuracy"])
    loss = list(history.history["loss"])
    val_loss = list(history.history["val_loss"])

    if finetune_history:
        accuracy += finetune_history.history["accuracy"]
        val_accuracy += finetune_history.history["val_accuracy"]
        loss += finetune_history.history["loss"]
        val_loss += finetune_history.history["val_loss"]

    epochs = range(1, len(accuracy) + 1)
    figure, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(epochs, accuracy, label="Training")
    axes[0].plot(epochs, val_accuracy, label="Validation")
    axes[0].set_title("Accuracy")
    axes[0].set_xlabel("Epoch")
    axes[0].legend()

    axes[1].plot(epochs, loss, label="Training")
    axes[1].plot(epochs, val_loss, label="Validation")
    axes[1].set_title("Loss")
    axes[1].set_xlabel("Epoch")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "training_curves.png", dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finetune", action="store_true")
    args = parser.parse_args()

    train_ds, valid_ds, class_names = build_datasets()
    model, base_model = build_model(len(class_names))
    start = time.time()

    print("Training subset head for 5 epochs on CPU.")
    history = model.fit(
        train_ds,
        validation_data=valid_ds,
        epochs=EPOCHS_HEAD,
        callbacks=callbacks(),
        verbose=1,
    )

    finetune_history = None
    if args.finetune:
        print("Fine-tuning the top 20 MobileNetV2 layers.")
        base_model.trainable = True
        for layer in base_model.layers[:-20]:
            layer.trainable = False
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )
        finetune_history = model.fit(
            train_ds,
            validation_data=valid_ds,
            epochs=EPOCHS_FINETUNE,
            callbacks=callbacks(),
            verbose=1,
        )

    model.save(MODEL_PATH)
    save_training_curves(history, finetune_history)
    elapsed_minutes = (time.time() - start) / 60
    evaluation = model.evaluate(valid_ds, verbose=0)
    print(f"Final validation loss: {evaluation[0]:.4f}")
    print(f"Final validation accuracy: {evaluation[1]:.4%}")
    print(f"Training time: {elapsed_minutes:.1f} minutes")
    print(f"Saved model: {MODEL_PATH}")
    print(f"Saved class names: {CLASS_NAMES_PATH}")


if __name__ == "__main__":
    main()