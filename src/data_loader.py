"""Create CPU-friendly TensorFlow data pipelines."""

import json
import random
import sys
from pathlib import Path

import tensorflow as tf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    BATCH_SIZE,
    CLASS_NAMES_PATH,
    IMG_SIZE,
    MAX_IMAGES_PER_CLASS,
    SEED,
    USE_SUBSET,
)
from src.preprocess import preprocess_image


def load_split_paths() -> tuple[Path, Path]:
    """Load train/valid paths from the downloader's JSON file."""
    paths_file = PROJECT_ROOT / "data" / "raw" / "paths.json"
    if not paths_file.is_file():
        raise FileNotFoundError("Run python src/download_data.py first.")
    paths = json.loads(paths_file.read_text(encoding="utf-8"))
    train_dir = Path(paths["train"]) if paths.get("train") else None
    valid_dir = Path(paths["valid"]) if paths.get("valid") else None
    if not train_dir or not train_dir.is_dir() or not valid_dir or not valid_dir.is_dir():
        raise FileNotFoundError("Train or valid folder is missing. Re-run download_data.py.")
    return train_dir, valid_dir


def make_train_subset(train_dir: Path) -> Path:
    """Create a temporary subset directory if subset mode is enabled."""
    if not USE_SUBSET:
        return train_dir

    subset_dir = PROJECT_ROOT / "data" / "raw" / "subset_train"
    subset_dir.mkdir(parents=True, exist_ok=True)
    random.seed(SEED)
    image_extensions = {".jpg", ".jpeg", ".png"}

    for class_dir in sorted(folder for folder in train_dir.iterdir() if folder.is_dir()):
        target_dir = subset_dir / class_dir.name
        target_dir.mkdir(parents=True, exist_ok=True)
        existing_images = [
            path
            for path in target_dir.iterdir()
            if path.is_file() and path.suffix.lower() in image_extensions
        ]
        missing_count = MAX_IMAGES_PER_CLASS - len(existing_images)
        if missing_count <= 0:
            continue
        images = [
            path for path in class_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in image_extensions
        ]
        random.shuffle(images)
        existing_names = {path.name for path in existing_images}
        copied_count = 0
        for source in images:
            if source.name in existing_names:
                continue
            target = target_dir / source.name
            if not target.exists():
                target.write_bytes(source.read_bytes())
                copied_count += 1
            if copied_count >= missing_count:
                break
    return subset_dir


def build_datasets():
    """Build augmented training and clean validation datasets."""
    train_dir, valid_dir = load_split_paths()
    train_dir = make_train_subset(train_dir)

    augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.08),
        tf.keras.layers.RandomZoom(0.10),
        tf.keras.layers.RandomBrightness(0.10),
    ], name="training_augmentation")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        labels="inferred",
        label_mode="categorical",
        batch_size=BATCH_SIZE,
        image_size=IMG_SIZE,
        shuffle=True,
        seed=SEED,
    )

    class_names = train_ds.class_names
    CLASS_NAMES_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLASS_NAMES_PATH.write_text(json.dumps(class_names, indent=2), encoding="utf-8")

    valid_ds = tf.keras.utils.image_dataset_from_directory(
        valid_dir,
        labels="inferred",
        label_mode="categorical",
        batch_size=BATCH_SIZE,
        image_size=IMG_SIZE,
        shuffle=False,
        seed=SEED,
        class_names=class_names,
    )

    def prepare_train(image, label):
        image = augmentation(image)
        return preprocess_image(image), label

    def prepare_valid(image, label):
        return preprocess_image(image), label

    train_ds = (
        train_ds
        .map(prepare_train, num_parallel_calls=tf.data.AUTOTUNE)
        .prefetch(tf.data.AUTOTUNE)
    )
    valid_ds = (
        valid_ds
        .map(prepare_valid, num_parallel_calls=tf.data.AUTOTUNE)
        .prefetch(tf.data.AUTOTUNE)
    )
    return train_ds, valid_ds, class_names