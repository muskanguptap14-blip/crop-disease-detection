"""Download the PlantVillage dataset or show manual-download instructions."""

import json
import os
import sys
from pathlib import Path

import kagglehub

# This makes direct commands such as "python src/download_data.py" work.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATA_DIR, ROOT


DATASET = "vipoooool/new-plant-diseases-dataset"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
PATHS_FILE = DATA_DIR / "paths.json"


def find_dataset_split(data_dir: Path, split_name: str) -> Path | None:
    """Find a nested train or valid directory, including common aliases."""
    split_names = {
        "train": {"train", "training"},
        "valid": {"valid", "validation", "val"},
        "validation": {"valid", "validation", "val"},
    }
    acceptable_names = split_names.get(split_name.lower(), {split_name.lower()})
    for current_dir, child_names, _ in os.walk(data_dir):
        child_names.sort(key=str.casefold)
        path = Path(current_dir)
        if path.name.lower() not in acceptable_names:
            continue
        for class_name in child_names:
            class_dir = path / class_name
            if any(
                item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS
                for item in class_dir.iterdir()
            ):
                return path
    return None


def find_kaggle_json() -> Path | None:
    """Return a Kaggle credential file at a standard Windows or Linux location."""
    possible = [
        Path.home() / ".kaggle" / "kaggle.json",
        Path("C:/Users") / Path.home().name / ".kaggle" / "kaggle.json",
    ]
    for path in possible:
        if path.is_file():
            return path
    return None


def has_kaggle_credentials() -> bool:
    """Return True if a Kaggle file or supported environment credential exists."""
    if find_kaggle_json() is not None:
        return True
    if os.environ.get("KAGGLE_API_TOKEN"):
        return True
    if os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"):
        return True
    return False


def dataset_is_ready(data_dir: Path) -> bool:
    """Check that at least one split contains class folders and images."""
    return (
        find_dataset_split(data_dir, "train") is not None
        and find_dataset_split(data_dir, "valid") is not None
    )


def print_manual_steps() -> None:
    """Explain browser download when Kaggle credentials are unavailable."""
    print("\nAutomatic Kaggle download is not available.")
    print("1. Open https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset")
    print("2. Sign in, click Download, and save the ZIP file.")
    print(f"3. Extract the ZIP contents inside: {DATA_DIR}")
    print("4. Ensure folders like 'Train', 'Valid', or 'train', 'valid' exist below data/raw.")
    print("5. Run: python src/download_data.py")
    print("\nAlternative Kaggle setup:")
    print("  1. Kaggle Account -> Settings -> API -> Create New Token")
    print("  2. Place kaggle.json in C:\\Users\\<your-name>\\.kaggle\\")
    print("  3. Run this script again.")


def download_with_kagglehub() -> Path:
    """Download and extract the dataset directly into data/raw."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("PlantVillage is approximately 2.7 GB; download may take several minutes.")
    dataset_path = kagglehub.dataset_download(
        DATASET,
        output_dir=str(DATA_DIR),
    )
    return Path(dataset_path)


def save_detected_paths(search_root: Path = DATA_DIR) -> tuple[Path | None, Path | None]:
    """Save detected train and valid directories for later scripts."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    train_dir = find_dataset_split(search_root, "train")
    valid_dir = find_dataset_split(search_root, "valid")
    if valid_dir is None:
        valid_dir = find_dataset_split(DATA_DIR, "validation")

    payload = {
        "train": str(train_dir) if train_dir else None,
        "valid": str(valid_dir) if valid_dir else None,
    }
    PATHS_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return train_dir, valid_dir


def main() -> None:
    if dataset_is_ready(DATA_DIR):
        train_dir, valid_dir = save_detected_paths()
        print("Dataset is already downloaded.")
        print(f"Train folder: {train_dir or 'not found'}")
        print(f"Valid folder: {valid_dir or 'not found'}")
        print(f"Saved paths: {PATHS_FILE}")
        return

    if not has_kaggle_credentials():
        print_manual_steps()
        return

    try:
        dataset_path = download_with_kagglehub()
    except Exception as error:
        raise RuntimeError(f"KaggleHub dataset download failed: {error}") from error

    search_roots = [dataset_path, DATA_DIR]
    for search_root in search_roots:
        train_dir = find_dataset_split(search_root, "train")
        valid_dir = find_dataset_split(search_root, "valid")
        if train_dir and valid_dir:
            train_dir, valid_dir = save_detected_paths(search_root)
            print("Download complete.")
            print(f"Train folder: {train_dir}")
            print(f"Valid folder: {valid_dir}")
            print(f"Saved paths: {PATHS_FILE}")
            return

    raise FileNotFoundError(
        f"Download returned {dataset_path}, but train/valid folders were not detected."
    )


if __name__ == "__main__":
    main()