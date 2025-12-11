# backend/app/model_loader.py

from typing import Dict
import random

# 🔹 In futuro useremo anche queste librerie per il modello vero:
# import numpy as np
# from PIL import Image
# from io import BytesIO
# import tensorflow as tf
# from pathlib import Path

# Classi finali del progetto (i 5 bidoni)
POSSIBLE_BINS = ["PLASTICA", "CARTA", "VETRO", "UMIDO", "INDIFFERENZIATO"]

# Qui in futuro salveremo il modello caricato
_model = None


def get_model():
    """
    Restituisce il modello di classificazione.

    Adesso:
      - il modello reale non esiste ancora
      - quindi usiamo un placeholder (MOCK_MODEL)

    In futuro:
      - caricheremo il modello da backend/model/saved_model
      - lo salveremo in _model
      - lo riuseremo per le richieste successive
    """
    global _model

    if _model is None:
        # TODO (futuro):
        #   1) calcolare il path della cartella saved_model:
        #      model_path = Path(__file__).resolve().parent.parent / "model" / "saved_model"
        #   2) caricare il modello con:
        #      _model = tf.keras.models.load_model(model_path)
        print("⚠️ get_model() sta usando un MODELLO MOCK.")
        _model = "MOCK_MODEL"

    return _model


def predict_mock(img_bytes: bytes) -> Dict:
    """
    Versione MOCK della predizione.
    Ignora l'immagine e restituisce un bidone a caso.

    Serve per:
      - sviluppare il backend
      - testare l'integrazione col frontend
      - mostrare il flusso end-to-end anche senza il modello AI reale
    """
    bin_choice = random.choice(POSSIBLE_BINS)

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
        "confidence": 0.80,  # valore fisso, perché è solo un mock
    }


def predict_real(img_bytes: bytes) -> Dict:
    """
    Versione FUTURA della predizione.

    Obiettivo finale:
      usare il modello addestrato da Nicole per classificare davvero l'immagine.

    Passi che implementeremo quando il modello sarà pronto:

      1. Caricare (o recuperare) il modello:
         model = get_model()

      2. Convertire i byte in immagine:
         # img = Image.open(BytesIO(img_bytes)).convert("RGB")

      3. Ridimensionare l'immagine alla dimensione di input del modello
         (es. 224x224 — questo ce lo dirà Nicole):
         # img = img.resize((224, 224))

      4. Convertire in array numpy e normalizzare:
         # img_array = np.array(img) / 255.0
         # img_array = np.expand_dims(img_array, axis=0)  # shape: (1, H, W, 3)

      5. Fare la predizione:
         # preds = model.predict(img_array)[0]   # vettore di probabilità

      6. Trovare la classe con confidenza massima:
         # class_id = int(np.argmax(preds))
         # confidence = float(preds[class_id])

      7. Mappare class_id su uno dei 5 bidoni:
         # class_to_bin = {
         #     0: "PLASTICA",
         #     1: "CARTA",
         #     2: "VETRO",
         #     3: "UMIDO",
         #     4: "INDIFFERENZIATO",
         # }
         # bin_choice = class_to_bin[class_id]

      8. Costruire la risposta finale:
         # material_map = {
         #     "PLASTICA": "plastica",
         #     "CARTA": "carta",
         #     "VETRO": "vetro",
         #     "UMIDO": "umido",
         #     "INDIFFERENZIATO": "indifferenziato",
         # }
         #
         # return {
         #     "material": material_map[bin_choice],
         #     "bin": bin_choice,
         #     "confidence": confidence,
         # }

    NOTA:
      Adesso NON abbiamo ancora:
        - il modello addestrato
        - le librerie installate (tensorflow, numpy, pillow)
        - l'ordine definitivo delle classi

      Quindi, per non rompere il backend, per ora questa funzione
      usa semplicemente il MOCK.

      Quando Nicole ci darà:
        - il modello salvato,
        - input size,
        - normalizzazione,
        - ordine delle classi,
      potremo togliere il mock e implementare davvero i passaggi sopra.
    """
    # Per ora, continuiamo a usare il mock, così l'API funziona.
    return predict_mock(img_bytes)