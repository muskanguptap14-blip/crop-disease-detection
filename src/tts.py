"""Convert prediction information into downloadable browser audio."""

import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import AUDIO_DIR


SCRIPT_TEMPLATES = {
    "en": "The leaf may have {name}. Confidence is {confidence} percent. Symptoms: {symptoms}. Precautions: {precautions}.",
    "kn": "ಎಲೆಗೆ {name} ರೋಗ ಇರುವ ಸಾಧ್ಯತೆ ಇದೆ. ವಿಶ್ವಾಸ {confidence} ಪ್ರತಿಶತ. ಲಕ್ಷಣಗಳು: {symptoms}. ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು: {precautions}.",
    "hi": "पत्ती में {name} रोग हो सकता है। विश्वास {confidence} प्रतिशत है। लक्षण: {symptoms}। सावधानियाँ: {precautions}।",
    "ta": "இலையில் {name} நோய் இருக்கலாம். நம்பிக்கை {confidence} சதவீதம். அறிகுறிகள்: {symptoms}. முன்னெச்சரிக்கைகள்: {precautions}.",
    "te": "ఆకులో {name} వ్యాధి ఉండవచ్చు. నమ్మకం {confidence} శాతం. లక్షణాలు: {symptoms}. జాగ్రత్తలు: {precautions}.",
    "ml": "ഇലയിൽ {name} രോഗം ഉണ്ടാകാം. വിശ്വാസം {confidence} ശതമാനം. ലക്ഷണങ്ങൾ: {symptoms}. മുൻകരുതലുകൾ: {precautions}.",
    "mr": "पानावर {name} रोग असू शकतो. विश्वास {confidence} टक्के. लक्षणे: {symptoms}. काळजी: {precautions}.",
    "bn": "পাতায় {name} রোগ থাকতে পারে। বিশ্বাস {confidence} শতাংশ। লক্ষণ: {symptoms}। সতর্কতা: {precautions}।",
    "gu": "પાનમાં {name} રોગ હોઈ શકે છે. વિશ્વાસ {confidence} ટકા. લક્ષણો: {symptoms}. સાવચેતીઓ: {precautions}.",
}


def build_spoken_script(result: dict, info: dict, lang: str = "en") -> str:
    """Create a short spoken script in one of the supported languages."""
    template = SCRIPT_TEMPLATES.get(lang, SCRIPT_TEMPLATES["en"])
    return template.format(
        name=info.get("display_name", result["display_name"]),
        confidence=round(result["confidence"] * 100),
        symptoms=info.get("symptoms", ""),
        precautions=info.get("precautions", ""),
    )


def speak(text: str, lang: str = "en") -> dict:
    """Try gTTS, then pyttsx3, and always return a status instead of crashing."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"prediction_{uuid.uuid4().hex}"

    if lang not in SCRIPT_TEMPLATES:
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