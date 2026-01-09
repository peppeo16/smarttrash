import { useState } from 'react'
import { Camera, Upload, RefreshCw, CheckCircle, AlertTriangle, HelpCircle, XCircle } from 'lucide-react' // <--- 1. AGGIUNTO XCircle
import './App.css'

function App() {
  const [image, setImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setImage(imageUrl);
      setSelectedFile(file);
      setResult(null); 
    }
  };

  const analyzeImage = async () => {
    if (!selectedFile) {
      alert("Nessun file selezionato!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      // Assicurati che l'URL sia corretto (se sei in locale usa localhost)
      const response = await fetch("https://smarttrash-ai.onrender.com/predict", {
        method: "POST",
        body: formData,
      });

      // Se il server è esploso (500) o non trovato (404)
      if (!response.ok) throw new Error("Errore di connessione col server");

      const data = await response.json();
      console.log("Dati Backend:", data);

      // --- 2. LOGICA DI GESTIONE ERRORE ---
      // Se il Python ci ha mandato un errore (es. formato sbagliato)
      if (data.error) {
          setResult({
              isError: true, // Flag speciale per dire "è un errore, non una predizione"
              label: data.material, // "Formato Errato"
              tip: data.tip,        // "Ricarica la pagina..."
              color: "#ef4444"      // Rosso
          });
          return; // Usciamo dalla funzione, non calcoliamo confidenza
      }

      // --- LOGICA DI SICUREZZA (Solo se non ci sono errori) ---
      const confidenceValue = data.confidence; 
      const isLowConfidence = confidenceValue < 0.60;

      setResult({
        isError: false,
        label: data.material,
        confidence: (confidenceValue * 100).toFixed(1) + "%",
        bin: data.bin,
        color: data.color,
        tip: data.tip,
        isLowConfidence: isLowConfidence 
      });

    } catch (error) {
      console.error(error);
      // Fallback per errori di rete veri (internet staccato, server spento)
      setResult({
          isError: true,
          label: "Errore Tecnico",
          tip: "Impossibile contattare il server. Controlla la connessione.",
          color: "#ef4444"
      });
    } finally {
      setLoading(false);
    }
  };

  const resetApp = () => {
    setImage(null);
    setSelectedFile(null);
    setResult(null);
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>🌱 SmartTrash AI</h1>
      </header>

      <main className="main-content">
        
        {/* SEZIONE 1: Caricamento */}
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
                <>
                  <input type="file" id="file-upload" accept="image/*" onChange={handleImageUpload} hidden />
                  <label htmlFor="file-upload" className="btn btn-secondary">
                    <Upload size={20} /> Carica Foto
                  </label>
                  <button className="btn btn-primary" onClick={() => document.getElementById('file-upload').click()}>
                    <Camera size={20} /> Scatta Foto
                  </button>
                </>
              ) : (
                !loading && (
                  <button className="btn btn-analyze" onClick={analyzeImage}>
                    Analizza Rifiuto ✨
                  </button>
                )
              )}
            </div>
            {loading && <div className="loader">🧠 Analisi in corso...</div>}
          </>
        )}

        {/* SEZIONE 2: RISULTATO */}
        {result && (
          <div className="result-card" style={{ 
            borderColor: result.color 
          }}>
            
            <div className="result-header" style={{ backgroundColor: result.color }}>
              {/* 3. LOGICA ICONE: Errore -> Incerto -> Sicuro */}
              {result.isError ? (
                 <XCircle size={32} color="white" />
              ) : result.isLowConfidence ? (
                <HelpCircle size={32} color="white" />
              ) : (
                <CheckCircle size={32} color="white" />
              )}
              
              <h2>{result.label}</h2>
            </div>
            
            <div className="result-body">
              
              {/* CASO A: ERRORE (File sbagliato o crash) */}
              {result.isError ? (
                  <div className="error-box">
                      <p style={{fontSize: '1.1rem', fontWeight: 'bold'}}>{result.tip}</p>
                      <br/>
                      <small>Prova a caricare un file .jpg o .png</small>
                  </div>

              /* CASO B: BASSA CONFIDENZA */
              ) : result.isLowConfidence ? (
                <div className="low-confidence-msg">
                  <p>Ho trovato <strong>{result.label}</strong>, ma la sicurezza è solo del <strong>{result.confidence}</strong>.</p>
                  <hr />
                  <p>⚠️ <strong>Consigli per una foto migliore:</strong></p>
                  <ul style={{textAlign: 'left', margin: '10px 0'}}>
                    <li>Avvicinati all'oggetto</li>
                    <li>Usa uno sfondo neutro</li>
                  </ul>
                </div>

              /* CASO C: RISULTATO NORMALE */
              ) : (
                <>
                  <p className="confidence">Sicurezza IA: <strong>{result.confidence}</strong></p>
                  
                  <div className="bin-info">
                    <span>Buttalo nel bidone:</span>
                    <strong style={{ color: result.color, fontSize: '1.2rem' }}>{result.bin}</strong>
                  </div>

                  <div className="tip-box">
                    <AlertTriangle size={18} color="#e67e22" />
                    <p>{result.tip}</p>
                  </div>
                </>
              )}

              <button className="btn btn-secondary" onClick={resetApp}>
                <RefreshCw size={18} /> {result.isError ? "Riprova" : "Analizza un altro"}
              </button>
            </div>
          </div>
        )}

      </main>
    </div>
  )
}

export default App