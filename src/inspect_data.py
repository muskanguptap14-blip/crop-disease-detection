"""Count dataset classes and save two beginner-friendly dataset plots."""

import random
import sys
import json
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image

# This makes direct commands such as "python src/inspect_data.py" work.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATA_DIR, OUTPUT_DIR, SEED
from src.download_data import find_dataset_split


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def get_image_files(folder: Path) -> list[Path]:
    """Return image files below a dataset folder."""
    if not folder.is_dir():
        return []
    return [
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]


def find_class_folders() -> tuple[list[Path], str]:
    """Find train or valid class folders and return them with a label."""
    paths_file = DATA_DIR / "paths.json"
    if paths_file.is_file():
        paths = json.loads(paths_file.read_text(encoding="utf-8"))
        saved_split = paths.get("train")
        if saved_split:
            split = Path(saved_split)
            folders = sorted(
                [path for path in split.iterdir() if path.is_dir()],
                key=lambda path: path.name.lower(),
            )
            if folders:
                return folders, split.name

    for split_name in ("train", "valid", "validation"):
        split = find_dataset_split(DATA_DIR, split_name)
        if split:
            folders = sorted(
                [path for path in split.iterdir() if path.is_dir()],
                key=lambda path: path.name.lower(),
            )
            if folders:
                return folders, split.name

    # Some downloaded datasets have class folders directly under data/raw.
    folders = (
        sorted(
            [path for path in DATA_DIR.iterdir() if path.is_dir()],
            key=lambda path: path.name.lower(),
        )
        if DATA_DIR.is_dir()
        else []
    )
    folders = [folder for folder in folders if get_image_files(folder)]
    return folders, "data/raw"


def save_distribution_chart(class_counts: dict[str, int]) -> Path:
    """Save a readable horizontal bar chart."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "class_distribution.png"

    names = list(class_counts)
    counts = [class_counts[name] for name in names]
    figure_height = max(8, len(names) * 0.32)
    plt.figure(figsize=(12, figure_height))
    plt.barh(names, counts, color="#4CAF50")
    plt.xlabel("Number of images")
    plt.ylabel("Disease class")
    plt.title("PlantVillage class distribution")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def save_sample_grid(class_folders: list[Path]) -> Path:
    """Save 16 images in a 4x4 grid."""
    random.seed(SEED)
    selected: list[Path] = []

    shuffled_folders = class_folders.copy()
    random.shuffle(shuffled_folders)
    for folder in shuffled_folders:
        images = get_image_files(folder)
        if images:
            selected.append(random.choice(images))
        if len(selected) == 16:
            break

    if len(selected) < 16:
        all_images = [
            image
            for folder in class_folders
            for image in get_image_files(folder)
        ]
        random.shuffle(all_images)
        for image in all_images:
            if image not in selected:
                selected.append(image)
            if len(selected) == 16:
                break

    if not selected:
        raise FileNotFoundError(
            "No JPG, JPEG, or PNG images found below data/raw."
        )

    plt.figure(figsize=(12, 12))
    for index, image_path in enumerate(selected[:16], start=1):
        image = Image.open(image_path).convert("RGB")
        axis = plt.subplot(4, 4, index)
        axis.imshow(image)
        axis.set_title(image_path.parent.name, fontsize=8)
        axis.axis("off")

    plt.suptitle("PlantVillage sample images", fontsize=16)
    plt.tight_layout()
    output_path = OUTPUT_DIR / "sample_grid.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def main() -> None:
    class_folders, split_label = find_class_folders()
    if not class_folders:
        print("Dataset not found.")
        print(f"Download or extract the dataset into: {DATA_DIR}")
        print("Then run: python src/download_data.py")
        print("Or run: python src/inspect_data.py")
        return

    class_counts = {
        folder.name: len(get_image_files(folder))
        for folder in class_folders
    }

    print(f"Dataset split inspected: {split_label}")
    print(f"Number of classes: {len(class_folders)}")
    print(f"Total images: {sum(class_counts.values())}")
    for class_name, count in class_counts.items():
        print(f"{class_name}: {count}")

    chart_path = save_distribution_chart(class_counts)
    grid_path = save_sample_grid(class_folders)
    print(f"Saved class chart: {chart_path}")
    print(f"Saved sample grid: {grid_path}")


if __name__ == "__main__":
    main()
