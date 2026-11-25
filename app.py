"""Streamlit interface for the AI Crop Disease Detection System."""

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.disease_info import load_disease_info
from src.predict import load_model_once, predict_image
from src.tts import build_spoken_script, speak

UI_STRINGS_PATH = PROJECT_ROOT / "assets" / "ui_strings.json"
ENGLISH_FALLBACK = {
    "language_name": "English",
    "title": "AI Crop Disease Detection System",
    "subtitle": "AMC Engineering College | Department of ISE",
    "about": "About",
    "how_to": "How to use",
    "supported": "Supported crops",
    "threshold": "Confidence threshold",
    "language": "Language",
    "upload": "Choose a crop leaf image",
    "detect": "Detect Disease",
    "analyzing": "Analyzing the leaf...",
    "healthy": "HEALTHY LEAF",
    "diseased": "DISEASED LEAF",
    "uncertain": "NOT SURE - CLEARER PHOTO NEEDED",
    "crop": "Crop",
    "confidence": "Confidence",
    "top3": "Top 3 predictions",
    "description": "Description",
    "symptoms": "Symptoms",
    "precautions": "Precautions",
    "treatment": "Treatment",
    "audio": "Audio explanation",
    "download": "Download audio",
    "too_large": "This image is larger than 20 MB. Please resize it and try again.",
    "corrupt": "The image is corrupted or cannot be opened.",
    "model_missing": "Model file not found. Run python src/train.py first.",
    "not_sure": "Not sure, please upload a clearer leaf photo.",
    "footer": "Team: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M | Guide: Prof. Tejashree",
}


def load_ui_strings() -> dict:
    if not UI_STRINGS_PATH.is_file():
        return {"en": ENGLISH_FALLBACK}
    strings = json.loads(UI_STRINGS_PATH.read_text(encoding="utf-8"))
    if "en" not in strings:
        raise ValueError(f"English UI strings are missing from {UI_STRINGS_PATH}")
    return strings


UI_STRINGS = load_ui_strings()

st.set_page_config(
    page_title=UI_STRINGS["en"].get("title", ENGLISH_FALLBACK["title"]),
    page_icon="🌿",
    layout="wide",
)


@st.cache_resource
def get_model_bundle():
    """Cache the model and ordered labels for this Streamlit process."""
    return load_model_once()


st.markdown(
    """
    <style>
    .main { background-color: #f7fbf7; }
    .healthy { background-color:#d9f4df; color:#176b2c; padding:14px;
               border-radius:8px; text-align:center; font-weight:700; }
    .diseased { background-color:#fde1df; color:#a12a20; padding:14px;
                border-radius:8px; text-align:center; font-weight:700; }
    .low-confidence { background-color:#fff3cd; color:#7a5900; padding:14px;
                      border-radius:8px; text-align:center; font-weight:700; }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    language = st.selectbox(
        UI_STRINGS["en"].get("language", "Language"),
        options=list(UI_STRINGS),
        format_func=lambda code: UI_STRINGS[code].get("language_name", code),
    )
    ui = UI_STRINGS.get(language, UI_STRINGS["en"])

    st.header(ui.get("about", ENGLISH_FALLBACK["about"]))
    st.write(ui.get("about_text", "Upload a clear photo of a crop leaf."))
    st.header(ui.get("how_to", ENGLISH_FALLBACK["how_to"]))
    st.write(ui.get("step1", "1. Choose a JPG, JPEG, or PNG leaf image."))
    st.write(ui.get("step2", "2. Preview the image."))
    st.write(ui.get("step3", "3. Select Detect Disease."))
    st.header(ui.get("supported", ENGLISH_FALLBACK["supported"]))
    st.write(
        ui.get(
            "crop_list",
            "Apple, tomato, potato, grape, corn, pepper, peach and more.",
        )
    )
    threshold = st.slider(
        ui.get("threshold", ENGLISH_FALLBACK["threshold"]),
        min_value=0.40,
        max_value=0.90,
        value=0.60,
        step=0.05,
    )

st.title(ui.get("title", ENGLISH_FALLBACK["title"]))
st.caption(ui.get("subtitle", ENGLISH_FALLBACK["subtitle"]))

uploaded_file = st.file_uploader(
    ui.get("upload", ENGLISH_FALLBACK["upload"]),
    type=["jpg", "jpeg", "png"],
)

if uploaded_file is not None:
    if uploaded_file.size > 20 * 1024 * 1024:
        st.error(ui.get("too_large", ENGLISH_FALLBACK["too_large"]))
    else:
        try:
            image = Image.open(uploaded_file).convert("RGB")
        except Exception:
            st.error(ui.get("corrupt", ENGLISH_FALLBACK["corrupt"]))
            image = None

        if image is not None:
            st.image(image, caption="Uploaded leaf image", use_container_width=True)

            if st.button(ui.get("detect", ENGLISH_FALLBACK["detect"]), type="primary", use_container_width=True):
                try:
                    with st.spinner(ui.get("analyzing", ENGLISH_FALLBACK["analyzing"])):
                        st.session_state.pop("audio_result", None)
                        model_bundle = get_model_bundle()
                        result = predict_image(
                            image,
                            threshold=threshold,
                            model_bundle=model_bundle,
                        )
                        info = load_disease_info(result["label"], language)
                        st.session_state["prediction"] = result
                        st.session_state["disease_info"] = info
                except FileNotFoundError as error:
                    st.error(
                        ui.get("model_missing", ENGLISH_FALLBACK["model_missing"])
                        if "model" in str(error).lower()
                        else str(error)
                    )
                except Exception as error:
                    st.error(f"Prediction could not be completed: {error}")

            if "prediction" in st.session_state:
                result = st.session_state["prediction"]
                info = load_disease_info(result["label"], language)
                low_confidence = result["confidence"] < threshold

                if low_confidence:
                    st.markdown(
                        f'<div class="low-confidence">{ui.get("uncertain", ENGLISH_FALLBACK["uncertain"])}</div>',
                        unsafe_allow_html=True,
                    )
                    st.write(ui.get("not_sure", ENGLISH_FALLBACK["not_sure"]))
                elif result["is_healthy"]:
                    st.markdown(
                        f'<div class="healthy">{ui.get("healthy", ENGLISH_FALLBACK["healthy"])}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="diseased">{ui.get("diseased", ENGLISH_FALLBACK["diseased"])}</div>',
                        unsafe_allow_html=True,
                    )

                st.subheader(info.get("display_name", result["display_name"]))
                st.write(f"**{ui.get('crop', ENGLISH_FALLBACK['crop'])}:** {info.get('crop', result['crop'])}")
                st.progress(min(max(result["confidence"], 0.0), 1.0))
                st.write(f"**{ui.get('confidence', ENGLISH_FALLBACK['confidence'])}:** {result['confidence'] * 100:.1f}%")

                chart_data = pd.DataFrame(
                    {
                        "Prediction": [
                            load_disease_info(item["label"], language).get(
                                "display_name", item["display_name"]
                            )
                        ],
                        "Confidence": [
                            item["confidence"] * 100 for item in result["top3"]
                        ],
                    }
                ).set_index("Prediction")
                st.subheader(ui.get("top3", ENGLISH_FALLBACK["top3"]))
                st.bar_chart(chart_data)

                with st.expander(ui.get("description", ENGLISH_FALLBACK["description"])):
                    st.write(info["description"])
                with st.expander(ui.get("symptoms", ENGLISH_FALLBACK["symptoms"])):
                    st.write(info["symptoms"])
                with st.expander(ui.get("precautions", ENGLISH_FALLBACK["precautions"])):
                    st.write(info["precautions"])
                with st.expander(ui.get("treatment", ENGLISH_FALLBACK["treatment"])):
                    st.write(info["treatment"])

                if not low_confidence:
                    audio_key = f"{result['label']}:{language}:{result['confidence']:.5f}"
                    if st.session_state.get("audio_key") != audio_key:
                        spoken_text = build_spoken_script(result, info, language)
                        st.session_state["audio_result"] = speak(
                            spoken_text,
                            lang=language,
                        )
                        st.session_state["audio_key"] = audio_key
                    audio_result = st.session_state["audio_result"]
                    if audio_result["path"]:
                        st.subheader(ui.get("audio", ENGLISH_FALLBACK["audio"]))
                        st.audio(str(audio_result["path"]))
                        with open(audio_result["path"], "rb") as audio_file:
                            st.download_button(
                                ui.get("download", ENGLISH_FALLBACK["download"]),
                                data=audio_file,
                                file_name=audio_result["path"].name,
                                mime="audio/mpeg"
                                if audio_result["path"].suffix == ".mp3"
                                else "audio/wav",
                            )
                    if audio_result["warning"]:
                        st.warning(audio_result["warning"])

st.markdown("---")
st.caption(ui.get("footer", ENGLISH_FALLBACK["footer"]))
