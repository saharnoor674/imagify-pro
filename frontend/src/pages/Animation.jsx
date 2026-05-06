import React, { useState, useRef } from 'react';
import API_BASE from '../config';

export default function Animation() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [resultUrl, setResultUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.type.startsWith('image/')) { setError('Please select an image file'); return; }
      setSelectedImage(file);
      setError(null);
      setResultUrl(null);
      const reader = new FileReader();
      reader.onloadend = () => setPreviewUrl(reader.result);
      reader.readAsDataURL(file);
    }
  };

  const generateSmile = async () => {
    if (!selectedImage) { setError('Please select an image first'); return; }
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', selectedImage);
      const response = await fetch(`${API_BASE}/api/animate/smile`, {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Failed to generate smile');
      const blob = await response.blob();
      setResultUrl(URL.createObjectURL(blob));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    if (resultUrl) URL.revokeObjectURL(resultUrl);
    setResultUrl(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(to bottom right, #faf5ff, #eff6ff)', padding: '20px 12px 60px', overflowX: 'hidden' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#1f2937', marginBottom: '1rem' }}>Smile Effect</h1>
          <p style={{ color: '#6b7280' }}>Upload a face photo and add a smile effect</p>
        </div>

        <div style={{ background: 'white', borderRadius: '1rem', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)', padding: '2rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '2rem' }}>

            {/* Upload */}
            <div>
              <h2 style={{ fontSize: '1.5rem', fontWeight: '600', color: '#1f2937', marginBottom: '1rem' }}>Upload Image</h2>
              <div
                style={{ border: '2px dashed #d1d5db', borderRadius: '0.75rem', padding: '2rem', textAlign: 'center', cursor: 'pointer', minHeight: '256px', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}
                onClick={() => fileInputRef.current && fileInputRef.current.click()}
              >
                {previewUrl ? (
                  <img src={previewUrl} alt="Preview" style={{ maxWidth: '100%', height: '256px', objectFit: 'contain', borderRadius: '0.5rem' }} />
                ) : (
                  <div style={{ padding: '2rem 0' }}>
                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}></div>
                    <p style={{ color: '#6b7280' }}>Click to upload or drag and drop</p>
                    <p style={{ fontSize: '0.875rem', color: '#9ca3af', marginTop: '0.5rem' }}>PNG, JPG, WEBP up to 10MB</p>
                  </div>
                )}
              </div>
              <input ref={fileInputRef} type="file" accept="image/*" onChange={handleImageSelect} style={{ display: 'none' }} />

              <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                <button onClick={generateSmile} disabled={!selectedImage || loading} style={{ flex: 1, background: loading || !selectedImage ? '#9ca3af' : 'linear-gradient(to right, #9333ea, #3b82f6)', color: 'white', padding: '0.75rem 1.5rem', borderRadius: '0.5rem', fontWeight: '600', border: 'none', cursor: loading || !selectedImage ? 'not-allowed' : 'pointer', opacity: loading || !selectedImage ? 0.5 : 1 }}>
                  {loading ? 'Processing...' : 'Generate Smile'}
                </button>
                <button onClick={reset} style={{ padding: '0.75rem 1.5rem', border: '2px solid #d1d5db', borderRadius: '0.5rem', fontWeight: '600', background: 'white', cursor: 'pointer' }}>
                  Reset
                </button>
              </div>

              {error && (
                <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#b91c1c', padding: '0.75rem 1rem', borderRadius: '0.5rem', marginTop: '1rem' }}>
                  {error}
                </div>
              )}
            </div>

            {/* Result */}
            <div>
              <h2 style={{ fontSize: '1.5rem', fontWeight: '600', color: '#1f2937', marginBottom: '1rem' }}>Result</h2>
              <div style={{ border: '2px solid #e5e7eb', borderRadius: '0.75rem', padding: '2rem', minHeight: '256px', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f9fafb' }}>
                {loading ? (
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ width: 48, height: 48, borderRadius: '50%', border: '4px solid #e9d5ff', borderTopColor: '#9333ea', animation: 'spin 1s linear infinite', margin: '0 auto 1rem' }} />
                    <p style={{ color: '#9333ea', fontWeight: 600 }}>Generating smile...</p>
                  </div>
                ) : resultUrl ? (
                  <div style={{ width: '100%' }}>
                    <img src={resultUrl} alt="Result" style={{ width: '100%', height: '256px', objectFit: 'contain', borderRadius: '0.5rem', marginBottom: '1rem' }} />
                    <a href={resultUrl} download="smile_result.jpg" style={{ display: 'block', width: '100%', textAlign: 'center', background: '#16a34a', color: 'white', padding: '0.75rem 1.5rem', borderRadius: '0.5rem', fontWeight: '600', textDecoration: 'none' }}>
                      Download Result
                    </a>
                  </div>
                ) : (
                  <div style={{ textAlign: 'center', color: '#9ca3af' }}>
                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}></div>
                    <p>Your smile effect will appear here</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}