import React, { useState, useRef } from 'react';

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
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file');
        return;
      }
      
      setSelectedImage(file);
      setError(null);
      setResultUrl(null);
      
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const generateSmile = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedImage);

      const response = await fetch('http://127.0.0.1:8000/api/animate/smile', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to generate smile');
      }

      // The response is an image file
      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setResultUrl(imageUrl);

    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    if (resultUrl) {
      URL.revokeObjectURL(resultUrl);
    }
    setResultUrl(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(to bottom right, #faf5ff, #eff6ff)', padding: '3rem 1rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#1f2937', marginBottom: '1rem' }}>
            Smile Effect
          </h1>
          <p style={{ color: '#6b7280' }}>
            Upload a face photo and add a smile effect (FREE VERSION)
          </p>
        </div>

        <div style={{ background: 'white', borderRadius: '1rem', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)', padding: '2rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
            
            <div>
              <h2 style={{ fontSize: '1.5rem', fontWeight: '600', color: '#1f2937', marginBottom: '1rem' }}>
                Upload Image
              </h2>
              
              <div
                style={{
                  border: '2px dashed #d1d5db',
                  borderRadius: '0.75rem',
                  padding: '2rem',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'border-color 0.2s'
                }}
                onClick={() => fileInputRef.current && fileInputRef.current.click()}
              >
                {previewUrl ? (
                  <img
                    src={previewUrl}
                    alt="Preview"
                    style={{ maxWidth: '100%', height: '256px', objectFit: 'contain', borderRadius: '0.5rem', margin: '0 auto' }}
                  />
                ) : (
                  <div style={{ padding: '3rem 0' }}>
                    <div style={{ margin: '0 auto', height: '3rem', width: '3rem', color: '#9ca3af', marginBottom: '1rem' }}>
                      <svg
                        style={{ width: '100%', height: '100%' }}
                        stroke="currentColor"
                        fill="none"
                        viewBox="0 0 48 48"
                      >
                        <path
                          d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </div>
                    <p style={{ marginTop: '1rem', color: '#6b7280' }}>
                      Click to upload or drag and drop
                    </p>
                    <p style={{ fontSize: '0.875rem', color: '#9ca3af', marginTop: '0.5rem' }}>
                      PNG, JPG, WEBP up to 10MB
                    </p>
                  </div>
                )}
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                style={{ display: 'none' }}
              />

              <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                <button
                  onClick={generateSmile}
                  disabled={!selectedImage || loading}
                  style={{
                    flex: 1,
                    background: loading || !selectedImage ? '#9ca3af' : 'linear-gradient(to right, #9333ea, #3b82f6)',
                    color: 'white',
                    padding: '0.75rem 1.5rem',
                    borderRadius: '0.5rem',
                    fontWeight: '600',
                    border: 'none',
                    cursor: loading || !selectedImage ? 'not-allowed' : 'pointer',
                    opacity: loading || !selectedImage ? 0.5 : 1,
                    transition: 'all 0.2s'
                  }}
                >
                  {loading ? 'Processing...' : 'Generate Smile'}
                </button>
                
                <button
                  onClick={reset}
                  style={{
                    padding: '0.75rem 1.5rem',
                    border: '2px solid #d1d5db',
                    borderRadius: '0.5rem',
                    fontWeight: '600',
                    background: 'white',
                    cursor: 'pointer',
                    transition: 'border-color 0.2s'
                  }}
                >
                  Reset
                </button>
              </div>

              {error && (
                <div style={{
                  background: '#fef2f2',
                  border: '1px solid #fecaca',
                  color: '#b91c1c',
                  padding: '0.75rem 1rem',
                  borderRadius: '0.5rem',
                  marginTop: '1rem'
                }}>
                  {error}
                </div>
              )}
            </div>

            <div>
              <h2 style={{ fontSize: '1.5rem', fontWeight: '600', color: '#1f2937', marginBottom: '1rem' }}>
                Result
              </h2>
              
              <div style={{
                border: '2px solid #e5e7eb',
                borderRadius: '0.75rem',
                padding: '2rem',
                minHeight: '400px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: '#f9fafb'
              }}>
                {resultUrl ? (
                  <div style={{ width: '100%' }}>
                    <img
                      src={resultUrl}
                      alt="Smile result"
                      style={{ width: '100%', height: '256px', objectFit: 'contain', borderRadius: '0.5rem', marginBottom: '1rem' }}
                    />
                    <a
                      href={resultUrl}
                      download="smile_result.jpg"
                      style={{
                        display: 'block',
                        width: '100%',
                        textAlign: 'center',
                        background: '#16a34a',
                        color: 'white',
                        padding: '0.75rem 1.5rem',
                        borderRadius: '0.5rem',
                        fontWeight: '600',
                        textDecoration: 'none',
                        transition: 'background 0.2s'
                      }}
                    >
                      Download Result
                    </a>
                  </div>
                ) : (
                  <div style={{ textAlign: 'center', color: '#9ca3af' }}>
                    <div style={{ margin: '0 auto', height: '4rem', width: '4rem', marginBottom: '1rem' }}>
                      <svg
                        style={{ width: '100%', height: '100%' }}
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                    </div>
                    <p>Your smile effect will appear here</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        <div style={{
          marginTop: '2rem',
          background: '#dbeafe',
          border: '1px solid #93c5fd',
          borderRadius: '0.5rem',
          padding: '1.5rem'
        }}>
          <h3 style={{ fontWeight: '600', color: '#1e3a8a', marginBottom: '0.5rem' }}>
            Free Version - Simple Smile Effect
          </h3>
          <p style={{ color: '#1e40af', fontSize: '0.875rem', lineHeight: '1.5', margin: 0 }}>
            This is a basic smile effect. For AI-powered realistic smile animations, you would need a paid service like Replicate or premium APIs. This free version uses simple image processing.
          </p>
        </div>
      </div>
    </div>
  );
}
