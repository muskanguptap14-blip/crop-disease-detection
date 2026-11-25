"""Verify that all project dependencies can be imported."""

import importlib
import importlib.metadata
import sys


LIBRARIES = [
    "tensorflow",
    "numpy",
    "pandas",
    "cv2",
    "PIL",
    "sklearn",
    "matplotlib",
    "seaborn",
    "streamlit",
    "gtts",
    "pyttsx3",
    "kaggle",
    "tqdm",
]


def main() -> None:
    print(f"Python: {sys.version.split()[0]}")
    for library in LIBRARIES:
        if library == "kaggle":
            version = importlib.metadata.version("kaggle")
            print(f"{library}: {version}")
            continue
        module = importlib.import_module(library)
        version = getattr(module, "__version__", "installed")
        print(f"{library}: {version}")
    print("Environment OK")


if __name__ == "__main__":
    main()
