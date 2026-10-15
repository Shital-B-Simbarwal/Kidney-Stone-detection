
import { useState } from 'react'
import './App.css'

function App() {
  const [selectedImage, setSelectedImage] = useState(null)
  const [preview, setPreview] = useState('')
  const [result, setResult] = useState(null)

  function handleImageChange(event) {
    const file = event.target.files?.[0]

    if (!file) return

    setSelectedImage(file)
    setPreview(URL.createObjectURL(file))
    setResult(null)
  }

  
async function handleAnalyze() {
  if (!selectedImage) return

  setResult({
    prediction: 'Analyzing...',
    message: 'Sending your image to the AI model...',
  })

  try {
    const formData = new FormData()
    formData.append('file', selectedImage)

    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Prediction failed')
    }

    setResult({
      prediction: data.prediction,
      message: `Stone probability: ${(data.stone_probability * 100).toFixed(2)}%. ${data.message}`,
    })
  } catch (error) {
    setResult({
      prediction: 'Analysis failed',
      message: error.message || 'Could not connect to the backend.',
    })
  }
}


  return (
    <main className="app">
      <header className="navbar">
        <a className="brand" href="#">
          <span className="brand-icon">K</span>
          KidneyScan
        </a>
        <span className="nav-label">AI Research Prototype</span>
      </header>

      <section className="hero">
        <div className="hero-badge">
          <span className="status-dot" />
          DEEP LEARNING · MEDICAL IMAGING
        </div>

        <h1>
          Kidney stone detection,
          <span> made simpler.</span>
        </h1>

        <p className="hero-description">
          Upload a kidney CT scan image to explore our AI-powered
          image classification prototype.
        </p>
      </section>

      <section className="workspace">
        <div className="upload-card">
          <div className="section-heading">
            <div>
              <span className="step-label">STEP 01</span>
              <h2>Upload your scan</h2>
            </div>
            <span className="file-tag">PNG · JPG · JPEG</span>
          </div>

          <label className="upload-area">
            {preview ? (
              <img
                className="scan-preview"
                src={preview}
                alt="Selected CT scan preview"
              />
            ) : (
              <div className="upload-placeholder">
                <div className="upload-icon">↑</div>
                <h3>Choose a CT scan image</h3>
                <p>Click here to browse an image from your device</p>
                <span className="browse-button">Browse files</span>
              </div>
            )}

            <input
              type="file"
              accept="image/png,image/jpeg,image/jpg"
              onChange={handleImageChange}
            />
          </label>

          {selectedImage && (
            <div className="selected-file">
              <span className="file-check">✓</span>
              <div className="file-details">
                <strong>{selectedImage.name}</strong>
                <span>
                  {(selectedImage.size / 1024 / 1024).toFixed(2)} MB
                </span>
              </div>
              <button
                className="remove-button"
                onClick={() => {
                  setSelectedImage(null)
                  setPreview('')
                  setResult(null)
                }}
                type="button"
              >
                Remove
              </button>
            </div>
          )}

          <button
            className="analyze-button"
            type="button"
            onClick={handleAnalyze}
            disabled={!selectedImage}
          >
            Analyze scan <span>→</span>
          </button>

          <p className="upload-note">
            For demonstration purposes only. Use appropriate, authorized
            images and avoid uploading identifiable patient information.
          </p>
        </div>

        <aside className="result-card">
          <span className="step-label">STEP 02</span>
          <h2>Analysis results</h2>
          <p className="result-intro">
            Your prediction information will appear here.
          </p>

          <div className="result-visual">
            <div className="scan-symbol">
              <span>◎</span>
            </div>
            <p>
              {result ? result.prediction : 'Awaiting scan'}
            </p>
            <span className="result-status">
             {result?.prediction === 'Analyzing...'
              ? 'ANALYZING'
              : result?.prediction === 'Analysis failed'
              ? 'ERROR'
              : result
              ? 'RESULT RECEIVED'
              : 'NO ANALYSIS YET'}
              </span>
          </div>

          {result ? (
            <p className="result-message">{result.message}</p>
          ) : (
            <div className="result-placeholder">
              <span>01</span>
              <p>Upload an image to begin the demo workflow.</p>
            </div>
          )}

          <div className="disclaimer">
            <strong>Important medical disclaimer</strong>
            <p>
              This is an educational prototype, not a medical device.
              Results are not a diagnosis and must not replace review by
              a qualified healthcare professional.
            </p>
          </div>
        </aside>
      </section>

      <footer className="footer">
        <span>KidneyScan · Academic Project</span>
        <span>Built for learning and research</span>
      </footer>
    </main>
  )
}

export default App
