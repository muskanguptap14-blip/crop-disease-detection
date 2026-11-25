# AI Crop Disease Detection System

An end-to-end CPU-friendly Streamlit application that identifies possible crop diseases from a leaf image. It uses OpenCV preprocessing, MobileNetV2 transfer learning, disease information, and text-to-speech.

## Architecture

```text
PlantVillage images
        |
        v
OpenCV preprocessing + augmentation
        |
        v
MobileNetV2 CNN transfer learning
        |
        v
Disease label + confidence + top 3
        |
        v
Streamlit UI + gTTS / pyttsx3 audio
```

## Setup

```powershell
cd C:\Users\muska\OneDrive\Desktop\college\crop-disease-detection
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
set $env:KAGGLE_API_TOKEN="your-token"
python src\download_data.py
python src\inspect_data.py
python src\train.py
python src\evaluate.py
python -m pytest -q
streamlit run app.py
```

The Kaggle token is not stored in this project. Kaggle also supports `kaggle.json` in `%USERPROFILE%\.kaggle\`.

## Project structure

```text
assets/            Disease information
data/raw/          Downloaded PlantVillage dataset
data/sample_images Demo validation images
models/            Saved model and class names
outputs/           Plots, reports, and audio
src/               Preprocessing, training, evaluation, prediction
tests/             pytest tests
app.py             Streamlit application
```

## CPU training

Subset mode limits training to 300 images per class. The Stage 1 head trains for 5 epochs, with optional fine-tuning for 3 epochs using `python src/train.py --finetune`.

## Limitations

PlantVillage contains mostly lab-style images. Real farm photographs may reduce accuracy. Predictions are possible diseases, not certified diagnoses. Consult a local agriculture officer before treatment.

## Viva summary

A user uploads a leaf photograph. OpenCV resizes and normalizes it, MobileNetV2 extracts features and predicts a class, Streamlit displays the result, and text-to-speech reads a short explanation. Transfer learning makes training practical on a CPU laptop.