# SmartTrash AI – Backend (FastAPI)

## 1. Panoramica
Il backend espone una API REST costruita con **FastAPI**.
Il suo compito è ricevere un'immagine, elaborarla e restituire:
- materiale riconosciuto,
- categoria del bidone,
- confidenza della predizione.

---

## 2. Endpoint

### 2.1 `GET /health`
Serve a verificare che il backend sia attivo.

**Risposta esempio**
```json
{"status": "ok"}