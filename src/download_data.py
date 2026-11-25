"""Download the PlantVillage dataset or show manual-download instructions."""

import shutil
import subprocess
import sys
from pathlib import Path

# This makes direct commands such as "python src/download_data.py" work.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATA_DIR, ROOT


DATASET = "vipoooool/new-plant-diseases-dataset"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def find_dataset_split(data_dir: Path, split_name: str) -> Path | None:
    """Find a nested train or valid folder regardless of unzip nesting."""
    matches = [
        path
        for path in data_dir.rglob("*")
        if path.is_dir()
        and (
            path.name.lower() == split_name.lower()
            or path.name.lower() == "training"
            or path.name.lower() == "validation"
        )
    ]
    for path in matches:
        if any(folder.is_dir() for folder in path.iterdir()):
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


def dataset_is_ready(data_dir: Path) -> bool:
    """Check that at least one split contains class folders and images."""
    for split_name in ("train", "valid", "validation"):
        split = find_dataset_split(data_dir, split_name)
        if split:
            image_count = sum(
                1
                for path in split.rglob("*")
                if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
            )
            if image_count > 0:
                return True
    return False


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


def download_with_kaggle() -> bool:
    """Use the Kaggle command-line tool when kaggle.json is present."""
    credential = find_kaggle_json()
    if credential is None:
        return False

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    kaggle_command = shutil.which("kaggle")
    if kaggle_command is None:
        print("kaggle.json was found, but the Kaggle command is not on PATH.")
        print("Run: python -m pip install kaggle")
        return False

    command = [
        kaggle_command,
        "datasets",
        "download",
        "-d",
        DATASET,
        "-p",
        str(DATA_DIR),
        "--unzip",
    ]
    print("Downloading PlantVillage through the Kaggle API...")
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode == 0


def main() -> None:
    if dataset_is_ready(DATA_DIR):
        train_dir = find_dataset_split(DATA_DIR, "train")
        valid_dir = find_dataset_split(DATA_DIR, "valid")
        print("Dataset is already downloaded.")
        print(f"Train folder: {train_dir or 'not found'}")
        print(f"Valid folder: {valid_dir or 'not found'}")
        return

    if find_kaggle_json():
        if download_with_kaggle() and dataset_is_ready(DATA_DIR):
            print("Download complete.")
            print(f"Train folder: {find_dataset_split(DATA_DIR, 'train') or 'not found'}")
            print(f"Valid folder: {find_dataset_split(DATA_DIR, 'valid') or 'not found'}")
            return

    print_manual_steps()


if __name__ == "__main__":
    main()