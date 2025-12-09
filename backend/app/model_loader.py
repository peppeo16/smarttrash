# backend/app/model_loader.py

from typing import Dict
import random

POSSIBLE_BINS = ["PLASTICA", "CARTA", "VETRO", "UMIDO", "INDIFFERENZIATO"]

def predict_mock(img_bytes: bytes) -> Dict:
    """
    MOCK: ignora l'immagine e restituisce una predizione finta.
    Serve solo per testare il flusso end-to-end.
    """
    bin_choice = random.choice(POSSIBLE_BINS)

    # materiale "umano" da mostrare all'utente
    material_map = {
        "PLASTICA": "plastica",
        "CARTA": "carta",
        "VETRO": "vetro",
        "UMIDO": "umido",
        "INDIFFERENZIATO": "indifferenziato",
    }

    return {
        "material": material_map[bin_choice],
        "bin": bin_choice,
        "confidence": 0.80,  # valore finto
    }