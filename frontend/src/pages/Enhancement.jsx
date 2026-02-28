import React, { useState, useRef, useEffect } from "react";
import API_BASE from "../config";

export default function Enhancement() {
  const [file, setFile] = useState(null);
  const [enh, setEnh] = useState(50);
  const [sharp, setSharp] = useState(50);
  const [clarity, setClarity] = useState(50);
  const [originalSrc, setOriginalSrc] = useState("");
  const [enhancedSrc, setEnhancedSrc] = useState("");
  const [loading, setLoading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef();
  const debounceRef = useRef();

  useEffect(() => {
    if (!file) return;
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => sendImage(), 400);
    return () => clearTimeout(debounceRef.current);
  }, [enh, sharp, clarity]);

  async function sendImage() {
    if (!file) return;
    setLoading(true);
    const form = new FormData();
    form.append("file", file);
    const url = `${API_BASE}/api/enhance/?enh=${enh}&sharp=${sharp}&clarity=${clarity}`;
    try {
      const res = await fetch(url, { method: "POST", body: form });
      if (!res.ok) throw new Error("Enhance failed");
      const data = await res.json();
      setEnhancedSrc("data:image/png;base64," + data.image);
    } catch (e) {
      console.error(e);
      alert("Could not reach backend.");
    } finally {
      setLoading(false);
    }
  }

  function onFileChange(e) {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    setFile(f);
    setEnhancedSrc("");
    const reader = new FileReader();
    reader.onloadend = () => setOriginalSrc(reader.result);
    reader.readAsDataURL(f);
  }

  function onDrop(e) {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files[0];
    if (!f || !f.type.startsWith("image/")) return;
    setFile(f);
    setEnhancedSrc("");
    const reader = new FileReader();
    reader.onloadend = () => setOriginalSrc(reader.result);
    reader.readAsDataURL(f);
  }

  function download() {
    if (!enhancedSrc) return;
    const a = document.createElement("a");
    a.href = enhancedSrc;
    a.download = "enhanced_image.png";
    a.click();
  }

  function reset() {
    setFile(null);
    setOriginalSrc("");
    setEnhancedSrc("");
    setEnh(50);
    setSharp(50);
    setClarity(50);
    if (fileRef.current) fileRef.current.value = "";
  }

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(to bottom right, #faf5ff, #eff6ff)",
      padding: "40px 20px 60px",
      fontFamily: "'Segoe UI', sans-serif",
    }}>
      <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <h1 style={{ fontSize: "2.5rem", fontWeight: 900, color: "#1f2937", marginBottom: "0.5rem" }}>
            Image Enhancement
          </h1>
          <p style={{ color: "#6b7280", fontSize: 16, margin: 0 }}>
            Upload a photo and adjust sliders to enhance in real time
          </p>
        </div>

        <div style={{ background: "white", borderRadius: "1rem", boxShadow: "0 20px 25px -5px rgba(0,0,0,0.1)", padding: "2rem" }}>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "2rem", marginBottom: "2rem" }}>

            {/* Original */}
            <div>
              <h2 style={{ fontSize: "1.25rem", fontWeight: 600, color: "#1f2937", marginBottom: "1rem" }}>Original</h2>
              <div
                style={{
                  border: dragOver ? "2px solid #667eea" : "2px dashed #d1d5db",
                  borderRadius: "0.75rem", minHeight: "320px",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  cursor: "pointer", background: dragOver ? "#eef2ff" : "#f9fafb",
                  overflow: "hidden", transition: "all 0.2s",
                }}
                onClick={() => fileRef.current?.click()}
                onDrop={onDrop}
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
              >
                {originalSrc ? (
                  <img src={originalSrc} alt="Original" style={{ width: "100%", height: "320px", objectFit: "contain" }} />
                ) : (
                  <div style={{ textAlign: "center", padding: "2rem" }}>
                    <div style={{ fontSize: "3rem", marginBottom: "1rem" }}></div>
                    <p style={{ color: "#6b7280", fontWeight: 600, margin: "0 0 4px" }}>Click or drag & drop</p>
                    <p style={{ color: "#9ca3af", fontSize: "0.875rem", margin: 0 }}>PNG, JPG, WEBP up to 10MB</p>
                  </div>
                )}
              </div>
              <input ref={fileRef} type="file" accept="image/*" onChange={onFileChange} style={{ display: "none" }} />
            </div>

            {/* Enhanced */}
            <div>
              <h2 style={{ fontSize: "1.25rem", fontWeight: 600, color: "#1f2937", marginBottom: "1rem" }}>
                Enhanced {loading && <span style={{ fontSize: "0.75rem", color: "#9333ea", fontWeight: "normal" }}>— updating...</span>}
              </h2>
              <div style={{
                border: "2px solid #e5e7eb", borderRadius: "0.75rem",
                minHeight: "320px", display: "flex", alignItems: "center",
                justifyContent: "center", background: "#f9fafb", overflow: "hidden",
              }}>
                {loading ? (
                  <div style={{ textAlign: "center" }}>
                    <div style={{ width: 48, height: 48, borderRadius: "50%", border: "4px solid #e9d5ff", borderTopColor: "#9333ea", animation: "spin 1s linear infinite", margin: "0 auto 1rem" }} />
                    <p style={{ color: "#9333ea", fontWeight: 600, margin: 0 }}>Enhancing...</p>
                  </div>
                ) : enhancedSrc ? (
                  <img src={enhancedSrc} alt="Enhanced" style={{ width: "100%", height: "320px", objectFit: "contain" }} />
                ) : (
                  <div style={{ textAlign: "center", padding: "2rem" }}>
                    <div style={{ fontSize: "3rem", marginBottom: "1rem" }}></div>
                    <p style={{ color: "#6b7280", fontWeight: 600, margin: "0 0 4px" }}>Enhanced image will appear here</p>
                    <p style={{ color: "#9ca3af", fontSize: "0.875rem", margin: 0 }}>Upload an image and adjust sliders</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Sliders */}
          <div style={{ background: "#f9fafb", borderRadius: "0.75rem", padding: "1.5rem", marginBottom: "1.5rem", border: "1px solid #e5e7eb" }}>
            <h3 style={{ fontSize: "1rem", fontWeight: 700, color: "#374151", margin: "0 0 1.25rem" }}>
              Adjust Enhancement Settings
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
              <div>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
                  <label style={{ fontSize: "0.875rem", fontWeight: 600, color: "#374151" }}> Enhancement</label>
                  <span style={{ fontSize: "0.875rem", fontWeight: 700, color: "#f59e0b" }}>{enh}</span>
                </div>
                <input type="range" min="0" max="100" value={enh} onChange={(e) => setEnh(Number(e.target.value))} style={{ width: "100%", accentColor: "#f59e0b", cursor: "pointer" }} />
              </div>
              <div>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
                  <label style={{ fontSize: "0.875rem", fontWeight: 600, color: "#374151" }}> Sharpness</label>
                  <span style={{ fontSize: "0.875rem", fontWeight: 700, color: "#10b981" }}>{sharp}</span>
                </div>
                <input type="range" min="0" max="100" value={sharp} onChange={(e) => setSharp(Number(e.target.value))} style={{ width: "100%", accentColor: "#10b981", cursor: "pointer" }} />
              </div>
              <div>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
                  <label style={{ fontSize: "0.875rem", fontWeight: 600, color: "#374151" }}> Clarity</label>
                  <span style={{ fontSize: "0.875rem", fontWeight: 700, color: "#3b82f6" }}>{clarity}</span>
                </div>
                <input type="range" min="0" max="100" value={clarity} onChange={(e) => setClarity(Number(e.target.value))} style={{ width: "100%", accentColor: "#3b82f6", cursor: "pointer" }} />
              </div>
            </div>
          </div>

          {/* Buttons */}
          <div style={{ display: "flex", gap: "1rem" }}>
            <button onClick={download} disabled={!enhancedSrc} style={{ flex: 1, background: !enhancedSrc ? "#9ca3af" : "linear-gradient(to right, #9333ea, #3b82f6)", color: "white", padding: "0.75rem 1.5rem", borderRadius: "0.5rem", fontWeight: 600, border: "none", cursor: !enhancedSrc ? "not-allowed" : "pointer", opacity: !enhancedSrc ? 0.5 : 1, fontSize: "1rem" }}>
              ⬇ Download
            </button>
            <button onClick={reset} style={{ flex: 1, padding: "0.75rem 1.5rem", border: "2px solid #d1d5db", borderRadius: "0.5rem", fontWeight: 600, background: "white", cursor: "pointer", fontSize: "1rem", color: "#374151" }}>
              Reset
            </button>
          </div>
        </div>
      </div>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}