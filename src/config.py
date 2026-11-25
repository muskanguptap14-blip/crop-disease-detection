from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"
MODEL_PATH = ROOT / "models" / "crop_disease_model.keras"
CLASS_NAMES_PATH = ROOT / "models" / "class_names.json"
DISEASE_INFO_PATH = ROOT / "assets" / "disease_info.json"
OUTPUT_DIR = ROOT / "outputs"
AUDIO_DIR = OUTPUT_DIR / "audio"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS_HEAD = 5
EPOCHS_FINETUNE = 3
SEED = 42
USE_SUBSET = True
MAX_IMAGES_PER_CLASS = 300
CONFIDENCE_THRESHOLD = 0.60