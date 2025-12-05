from fastapi import FastAPI
from pydantic import BaseModel

# Istanza principale dell'app
app = FastAPI(title="SmartTrash AI Backend")


# Modello di risposta per /predict
class PredictResponse(BaseModel):
    material: str    # es. "plastica"
    bin: str         # es. "PLASTICA"
    confidence: float  # es. 0.92


# ENDPOINTS

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
async def predict_mock():
    # Mock temporaneo, poi lo sostituirete con il modello vero
    return {
        "material": "plastica",
        "bin": "PLASTICA",
        "confidence": 0.95,
    }