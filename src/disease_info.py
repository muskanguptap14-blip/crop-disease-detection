"""Load and generate disease information from PlantVillage class names."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import CLASS_NAMES_PATH, DISEASE_INFO_PATH


def display_name_from_class(class_name: str) -> str:
    """Convert a folder name such as Tomato_Early_blight into readable text."""
    parts = class_name.replace("___", "_").replace("__", "_").split("_")
    return " ".join(part.capitalize() for part in parts)


def generate_default_info(class_name: str) -> dict:
    """Create clear, safe generic information for a dataset class."""
    display_name = display_name_from_class(class_name)
    crop = display_name.split()[0] if "_".strip() else "Crop"
    is_healthy = "healthy" in class_name.lower()

    return {
        "display_name": display_name,
        "crop": crop,
        "status": "healthy" if is_healthy else "diseased",
        "description": (
            f"This PlantVillage class represents {display_name}. "
            "The prediction is a possibility based on leaf appearance, not a laboratory diagnosis."
        ),
        "symptoms": (
            "Look for unusual spots, discoloration, leaf damage, or changes in texture. "
            "Compare the affected area with a clear healthy leaf."
        ),
        "precautions": (
            "Remove severely affected leaves if appropriate, avoid overhead watering, "
            "and prevent tools or soil from spreading disease between plants."
        ),
        "treatment": (
            "Keep the field clean and use an appropriate control method only after local confirmation. "
            "Consult an agriculture officer before applying fungicides or chemicals."
        ),
    }


def generate_disease_info() -> dict:
    """Create disease_info.json for every saved class name."""
    if not CLASS_NAMES_PATH.is_file():
        raise FileNotFoundError("Run training or create models/class_names.json first.")
    class_names = json.loads(CLASS_NAMES_PATH.read_text(encoding="utf-8"))
    existing = {}
    if DISEASE_INFO_PATH.is_file():
        existing = json.loads(DISEASE_INFO_PATH.read_text(encoding="utf-8"))

    result = {}
    for class_name in class_names:
        result[class_name] = existing.get(class_name, generate_default_info(class_name))

    DISEASE_INFO_PATH.parent.mkdir(parents=True, exist_ok=True)
    output = dict(result)
    output["_general_note"] = (
        "This app provides general educational guidance only. "
        "Consult a local agriculture officer for diagnosis and treatment."
    )
    DISEASE_INFO_PATH.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )
    return result


def load_disease_info(class_name: str) -> dict:
    """Return information for one class or a safe fallback."""
    if not DISEASE_INFO_PATH.is_file():
        return generate_default_info(class_name)
    data = json.loads(DISEASE_INFO_PATH.read_text(encoding="utf-8"))
    return data.get(class_name, generate_default_info(class_name))


def check_info_coverage() -> bool:
    """Verify that every model class has an information entry."""
    if not CLASS_NAMES_PATH.is_file() or not DISEASE_INFO_PATH.is_file():
        return False
    class_names = set(json.loads(CLASS_NAMES_PATH.read_text(encoding="utf-8")))
    data = json.loads(DISEASE_INFO_PATH.read_text(encoding="utf-8"))
    keys = set(data.keys()) - {"_general_note"}
    return class_names == keys


if __name__ == "__main__":
    generated = generate_disease_info()
    print(f"Generated disease information for {len(generated)} classes.")