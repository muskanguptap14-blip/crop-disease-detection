"""Convert prediction information into downloadable browser audio."""

import sys
import uuid
import warnings
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import AUDIO_DIR


def build_spoken_script(result: dict, info: dict) -> str:
    """Create a short, friendly English or supported-language script."""
    return (
        f"The leaf appears to have {result['display_name']}. "
        f"Confidence is {result['confidence'] * 100:.0f} percent. "
        f"Symptoms are {info.get('symptoms', 'not available')}. "
        f"Precautions are {info.get('precautions', 'not available')}."
    )


def speak(text: str, lang: str = "en") -> dict:
    """Try gTTS, then pyttsx3, and always return a status instead of crashing."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"prediction_{uuid.uuid4().hex}"

    if lang == "kn":
        # Kannada support is prepared but needs reviewed translations.
        lang = "en"

    try:
        from gtts import gTTS
        path = AUDIO_DIR / f"{filename}.mp3"
        gTTS(text=text, lang=lang, slow=False).save(str(path))
        return {"path": path, "warning": None, "engine": "gTTS"}
    except Exception as internet_error:
        warning = f"Internet audio failed ({internet_error}); using offline voice."
        try:
            import pyttsx3
            path = AUDIO_DIR / f"{filename}.wav"
            engine = pyttsx3.init()
            engine.save_to_file(text, str(path))
            engine.runAndWait()
            if path.is_file():
                return {"path": path, "warning": warning, "engine": "pyttsx3"}
        except Exception as offline_error:
            warning = f"{warning} Offline voice also failed ({offline_error})."
            return {"path": None, "warning": warning, "engine": None}