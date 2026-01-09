import sys
from fastapi.responses import JSONResponse 
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from .model_loader import load_model, predict as predict_image_model

app = FastAPI(title="SmartTrash AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictResponse(BaseModel):
    material: str
    bin: str
    tip: str
    color: str
    confidence: float

@app.on_event("startup")
def startup_event():
    load_model()

@app.post("/predict") 
async def predict_endpoint(file: UploadFile = File(...)):
    
    print(f"\n➡️ RICHIESTA RICEVUTA! File: {file.filename}", file=sys.stderr, flush=True)

    # ==========================================
    # 1. LEGGIAMO PRIMA IL FILE (CRUCIALE!)
    # ==========================================
    # Dobbiamo consumare lo stream di dati, altrimenti il browser
    # interpreterà il rifiuto immediato come un crash di rete.
    try:
        img_bytes = await file.read()
    except Exception as e:
         return JSONResponse(status_code=200, content={
             "error": "Errore upload", 
             "tip": "Riprova", 
             "material": "Errore", 
             "bin": "N/A", 
             "color": "red", 
             "confidence": 0.0
         })

    # ==========================================
    # 2. ORA FACCIAMO LA VALIDAZIONE
    # ==========================================
    filename = file.filename.lower()
    valid_extensions = ('.jpg', '.jpeg', '.png')
    
    if not filename.endswith(valid_extensions):
        msg = "Errore! Ricarica la pagina e invia una foto in .jpg o .png"
        print(f"❌ FILE RIFIUTATO: {filename}", file=sys.stderr)
        
        return JSONResponse(
            status_code=200, 
            content={
                "error": msg,            
                "material": "Formato Errato", 
                "bin": "N/A",
                "tip": msg,              
                "color": "red",          
                "confidence": 0.0
            }
        )
    # ==========================================

    try:
        # Passiamo i byte che ABBIAMO GIÀ LETTO (img_bytes)
        # Non usare più 'await file.read()' qui sotto perché l'abbiamo già fatto sopra!
        result = predict_image_model(img_bytes)
        
        # 🚨 PROTEZIONE ANTI-CRASH 🚨
        if result is None:
            print("❌ ERRORE GRAVE: La funzione predict ha restituito None!", file=sys.stderr)
            raise HTTPException(status_code=500, detail="Errore interno")

        if "error" in result:
             print(f"❌ ERRORE NEL MODELLO: {result['error']}", file=sys.stderr, flush=True)
             return JSONResponse(status_code=200, content={
                 "error": result["error"],
                 "material": "Errore",
                 "bin": "N/A",
                 "tip": result["error"],
                 "color": "red",
                 "confidence": 0.0
             })
             
        return result

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"❌ ERRORE GENERICO MAIN: {str(e)}", file=sys.stderr, flush=True)
        return JSONResponse(status_code=200, content={
             "error": str(e),
             "material": "Errore Server",
             "bin": "N/A",
             "tip": "Si è verificato un errore imprevisto.",
             "color": "red",
             "confidence": 0.0
        })