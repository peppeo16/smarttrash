# backend/app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from .model_loader import predict_mock  # poi useremo il modello vero

# Istanza principale dell'app
app = FastAPI(title="SmartTrash AI Backend")

# Abilito CORS (così il frontend può chiamare il backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # per sviluppo va bene così
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modello di risposta per /predict
class PredictResponse(BaseModel):
    material: str                 # es. "plastica"
    bin: Literal[
        "PLASTICA", "CARTA", "VETRO", "UMIDO", "INDIFFERENZIATO"
    ]                             # una delle 5 categorie
    confidence: float             # es. 0.92

# ENDPOINTS

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
async def predict(file: UploadFile = File(...)):
    """
    Riceve un'immagine e restituisce la predizione.
    Per ora usa una funzione MOCK in model_loader.py.
    """

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Formato file non supportato")

    # Leggo i byte del file (l'immagine vera e propria)
    img_bytes = await file.read()

    # Chiamo la funzione mock (poi qui useremo il modello vero)
    result = predict_mock(img_bytes)

    return result