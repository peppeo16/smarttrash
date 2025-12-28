from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional
import os
import random

# Classi finali del progetto (5 bidoni)
POSSIBLE_BINS = ("PLASTICA", "CARTA", "VETRO", "UMIDO", "INDIFFERENZIATO")

# Cache del modello (lazy-load)
_model: Optional[object] = None

# Percorso modello (default) + override via env
# Esempio: export SMARTTRASH_MODEL_PATH="/path/al/modello.h5"
DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[2] / "model" / "saved_model.h5"
MODEL_PATH = Path(os.getenv("SMARTTRASH_MODEL_PATH", str(DEFAULT_MODEL_PATH)))


def get_model() -> Optional[object]:
    """
    Carica e ritorna il modello (lazy).
    Se non disponibile, ritorna None (il backend userà il mock).
    """
    global _model
    if _model is not None:
        return _model

    if not MODEL_PATH.exists():
        return None

    # TODO: scegliete UNO tra TensorFlow o PyTorch, non entrambi.
    # Qui assumo .h5 / Keras
    try:
        from tensorflow import keras  # import pesante: solo se serve
        _model = keras.models.load_model(str(MODEL_PATH))
        return _model
    except Exception:
        # Se il load fallisce, evitiamo di rompere il backend
        return None


def predict_mock(_: bytes) -> Dict:
    """Fallback: ritorna una classe casuale + confidence fissa (solo demo)."""
    bin_choice = random.choice(POSSIBLE_BINS)
    material_map = {
        "PLASTICA": "plastica",
        "CARTA": "carta",
        "VETRO": "vetro",
        "UMIDO": "umido",
        "INDIFFERENZIATO": "indifferenziato",
    }
    return {"material": material_map[bin_choice], "bin": bin_choice, "confidence": 0.80}


def predict(img_bytes: bytes) -> Dict:
    """
    Entry point usata dal backend.
    Se il modello non c'è -> mock.
    """
    model = get_model()
    if model is None:
        return predict_mock(img_bytes)

    # Qui sotto: implementazione reale MINIMA (da adattare al vostro training)
    # Assunzioni:
    # - input immagine 224x224 RGB
    # - output: probabilità per 5 classi in ordine POSSIBLE_BINS
    try:
        from PIL import Image
        import numpy as np

        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img = img.resize((224, 224))
        x = np.array(img, dtype=np.float32) / 255.0
        x = np.expand_dims(x, axis=0)

        preds = model.predict(x)[0]  # shape (5,)
        class_id = int(np.argmax(preds))
        confidence = float(preds[class_id])

        bin_choice = POSSIBLE_BINS[class_id]
        material_map = {
            "PLASTICA": "plastica",
            "CARTA": "carta",
            "VETRO": "vetro",
            "UMIDO": "umido",
            "INDIFFERENZIATO": "indifferenziato",
        }
        return {"material": material_map[bin_choice], "bin": bin_choice, "confidence": confidence}

    except Exception:
        # Se qualcosa va storto, NON crashiamo tutto: fallback mock
        return predict_mock(img_bytes)