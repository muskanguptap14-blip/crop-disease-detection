"""Streamlit interface for the AI Crop Disease Detection System."""

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


st.set_page_config(
    page_title="AI Crop Disease Detection System",
    page_icon="🌿",
    layout="wide",
)


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


st.title("AI Crop Disease Detection System")
st.caption("AMC Engineering College | Department of ISE")


with st.sidebar:
    st.header("About")
    st.write(
        "Upload a clear photo of a crop leaf. The CNN compares it with "
        "PlantVillage disease patterns and returns a possible result."
    )
    st.header("How to use")
    st.write("1. Choose a JPG, JPEG, or PNG leaf image.")
    st.write("2. Preview the image.")
    st.write("3. Select Detect Disease.")
    st.header("Supported crops")
    st.write("Apple, tomato, potato, grape, corn, pepper, peach, blueberry, cherry and more.")
    threshold = st.slider(
        "Confidence threshold",
        min_value=0.40,
        max_value=0.90,
        value=0.60,
        step=0.05,
    )
    language = st.selectbox(
        "Audio language",
        options=["English", "Kannada (coming soon)"],
    )


uploaded_file = st.file_uploader(
    "Choose a crop leaf image",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file is not None:
    if uploaded_file.size > 20 * 1024 * 1024:
        st.error("This image is larger than 20 MB. Please resize it and try again.")
    else:
        try:
            image = Image.open(uploaded_file).convert("RGB")
        except Exception:
            st.error("The image is corrupted or cannot be opened.")
            image = None

        if image is not None:
            st.image(image, caption="Uploaded leaf image", use_container_width=True)

            if st.button("Detect Disease", type="primary", use_container_width=True):
                try:
                    with st.spinner("Analyzing the leaf..."):
                        result = predict_image(image, threshold=threshold)
                        info = load_disease_info(result["label"])
                        st.session_state["prediction"] = result
                        st.session_state["disease_info"] = info
                except FileNotFoundError as error:
                    st.error(str(error))
                except Exception as error:
                    st.error(f"Prediction could not be completed: {error}")

            if "prediction" in st.session_state:
                result = st.session_state["prediction"]
                info = st.session_state["disease_info"]
                low_confidence = result["display_name"].startswith("Not sure")

                if low_confidence:
                    st.markdown(
                        '<div class="low-confidence">NOT SURE - CLEARER PHOTO NEEDED</div>',
                        unsafe_allow_html=True,
                    )
                    st.write(result["display_name"])
                elif result["is_healthy"]:
                    st.markdown(
                        '<div class="healthy">HEALTHY LEAF</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        '<div class="diseased">DISEASED LEAF</div>',
                        unsafe_allow_html=True,
                    )

                st.subheader(result["display_name"])
                st.write(f"**Crop:** {result['crop']}")
                st.progress(min(max(result["confidence"], 0.0), 1.0))
                st.write(f"**Confidence:** {result['confidence'] * 100:.1f}%")

                chart_data = pd.DataFrame(
                    {
                        "Prediction": [
                            item["display_name"] for item in result["top3"]
                        ],
                        "Confidence": [
                            item["confidence"] * 100 for item in result["top3"]
                        ],
                    }
                ).set_index("Prediction")
                st.subheader("Top 3 predictions")
                st.bar_chart(chart_data)

                with st.expander("Description"):
                    st.write(info["description"])
                with st.expander("Symptoms"):
                    st.write(info["symptoms"])
                with st.expander("Precautions"):
                    st.write(info["precautions"])
                with st.expander("Treatment"):
                    st.write(info["treatment"])

                if not low_confidence:
                    audio_lang = "en"
                    spoken_text = build_spoken_script(result, info)
                    audio_result = speak(spoken_text, lang=audio_lang)
                    if audio_result["path"]:
                        st.subheader("Audio explanation")
                        st.audio(str(audio_result["path"]))
                        with open(audio_result["path"], "rb") as audio_file:
                            st.download_button(
                                "Download audio",
                                data=audio_file,
                                file_name=audio_result["path"].name,
                                mime="audio/mpeg"
                                if audio_result["path"].suffix == ".mp3"
                                else "audio/wav",
                            )
                    if audio_result["warning"]:
                        st.warning(audio_result["warning"])

st.markdown("---")
st.caption(
    "Team: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M "
    "| Guide: Prof. Tejashree"
)
