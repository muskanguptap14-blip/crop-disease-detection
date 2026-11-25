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
    crop_part = class_name.split("___", maxsplit=1)[0]
    crop = crop_part.replace("_", " ").replace(",", "").strip().title()
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
    """Create both nine-language JSON resources from saved class names."""
    if not CLASS_NAMES_PATH.is_file():
        raise FileNotFoundError("Run python src/inspect_data.py first.")
    class_names = json.loads(CLASS_NAMES_PATH.read_text(encoding="utf-8"))
    from src.generate_localizations import generate_localization_files

    return generate_localization_files(class_names)


def load_disease_info(class_name: str, language: str = "en") -> dict:
    """Return localized information for one class or a safe fallback."""
    if not DISEASE_INFO_PATH.is_file():
        return generate_default_info(class_name)
    data = json.loads(DISEASE_INFO_PATH.read_text(encoding="utf-8"))
    entry = data.get(class_name, generate_default_info(class_name))
    translations = entry.get("translations", {})
    return translations.get(language, translations.get("en", entry))


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