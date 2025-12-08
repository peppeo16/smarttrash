import { useState } from 'react'
import { Camera, Upload, RefreshCw, CheckCircle, AlertTriangle } from 'lucide-react'
import './App.css'

function App() {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setImage(imageUrl);
      setResult(null); 
    }
  };

  // Funzione FINTA (Mock) per testare la grafica
  const simulateAI = () => {
    setLoading(true);
    
    // Facciamo finta di aspettare 2 secondi (come se il server pensasse)
    setTimeout(() => {
      // Simuliamo una risposta casuale
      const fakeResponses = [
        { label: "Plastica", confidence: "94%", bin: "Giallo", color: "#f1c40f", tip: "Schiacciala bene!" },
        { label: "Carta", confidence: "88%", bin: "Blu", color: "#3498db", tip: "Niente scontrini qui!" },
        { label: "Vetro", confidence: "92%", bin: "Verde", color: "#2ecc71", tip: "Togli il tappo!" }
      ];
      
      const randomResponse = fakeResponses[Math.floor(Math.random() * fakeResponses.length)];
      
      setResult(randomResponse);
      setLoading(false);
    }, 2000);
  };

  const resetApp = () => {
    setImage(null);
    setResult(null);
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>🌱 SmartTrash AI</h1>
      </header>

      <main className="main-content">
        
        {/* SEZIONE 1: Caricamento (Visibile se NON c'è risultato) */}
        {!result && (
          <>
            <div className="image-preview">
              {image ? (
                <img src={image} alt="Preview" className="uploaded-image" />
              ) : (
                <div className="placeholder">
                  <Upload size={48} color="#bdc3c7" />
                  <p>Carica una foto del rifiuto</p>
                </div>
              )}
            </div>

            <div className="controls">
              {!image ? (
                // Se non c'è immagine, mostra tasti caricamento
                <>
                  <input type="file" id="file-upload" accept="image/*" onChange={handleImageUpload} hidden />
                  <label htmlFor="file-upload" className="btn btn-secondary">
                    <Upload size={20} /> Carica
                  </label>
                  <button className="btn btn-primary" onClick={() => alert("Usa 'Carica' per ora!")}>
                    <Camera size={20} /> Scatta
                  </button>
                </>
              ) : (
                // Se c'è immagine, mostra tasto Analizza
                !loading && (
                  <button className="btn btn-analyze" onClick={simulateAI}>
                    Analizza Rifiuto ✨
                  </button>
                )
              )}
            </div>
            
            {loading && <div className="loader">🧠 L'AI sta pensando...</div>}
          </>
        )}

        {/* SEZIONE 2: Risultato (Visibile SOLO se c'è risultato) */}
        {result && (
          <div className="result-card" style={{ borderColor: result.color }}>
            <div className="result-header" style={{ backgroundColor: result.color }}>
              <CheckCircle size={32} color="white" />
              <h2>{result.label}</h2>
            </div>
            
            <div className="result-body">
              <p className="confidence">Sicurezza: <strong>{result.confidence}</strong></p>
              
              <div className="bin-info">
                <span>Buttalo nel bidone:</span>
                <strong style={{ color: result.color, fontSize: '1.2rem' }}>{result.bin}</strong>
              </div>

              <div className="tip-box">
                <AlertTriangle size={18} color="#e67e22" />
                <p>{result.tip}</p>
              </div>

              <button className="btn btn-secondary" onClick={resetApp}>
                <RefreshCw size={18} /> Analizza un altro
              </button>
            </div>
          </div>
        )}

      </main>
    </div>
  )
}

export default App