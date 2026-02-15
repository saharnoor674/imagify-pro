import React, { useState, useRef, useEffect } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [enh, setEnh] = useState(50);
  const [sharp, setSharp] = useState(50);
  const [clarity, setClarity] = useState(50);
  const [imageSrc, setImageSrc] = useState("");
  const [loading, setLoading] = useState(false);
  const fileRef = useRef();
  const debounceRef = useRef();

  useEffect(() => {
    if (!file) return;
    // debounce slider changes
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      sendImage();
    }, 300);
    return () => clearTimeout(debounceRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enh, sharp, clarity]);

  async function sendImage() {
    if (!file) return;
    setLoading(true);

    const form = new FormData();
    form.append("file", file);

    const url = `http://127.0.0.1:8000/api/enhance/?enh=${enh}&sharp=${sharp}&clarity=${clarity}`;
    try {
      const res = await fetch(url, { method: "POST", body: form });
      if (!res.ok) throw new Error("Enhance failed");
      const data = await res.json();
      setImageSrc("data:image/png;base64," + data.image);
    } catch (e) {
      console.error(e);
      alert("Could not reach backend. Start backend at http://127.0.0.1:8000/");
    } finally {
      setLoading(false);
    }
  }

  function onFileChange(e) {
    const f = e.target.files && e.target.files[0];
    setFile(f || null);
    setImageSrc("");
  }

  function download() {
    if (!imageSrc) return;
    const a = document.createElement("a");
    a.href = imageSrc;
    a.download = "enhanced_image.png";
    a.click();
  }

  return (
    <div className="container">
      <h2>Imagify Pro — Enhance Image</h2>

      <div className="row">
        <label>Image</label>
        <input ref={fileRef} type="file" accept="image/*" onChange={onFileChange} />
      </div>

      <div className="row">
        <label>Enhancement: {enh}</label>
        <input type="range" min="0" max="100" value={enh} onChange={(e) => setEnh(e.target.value)} />
      </div>

      <div className="row">
        <label>Sharpness: {sharp}</label>
        <input type="range" min="0" max="100" value={sharp} onChange={(e) => setSharp(e.target.value)} />
      </div>

      <div className="row">
        <label>Clarity: {clarity}</label>
        <input type="range" min="0" max="100" value={clarity} onChange={(e) => setClarity(e.target.value)} />
      </div>

      <div className="row actions">
        <button onClick={sendImage} disabled={!file || loading}>Enhance</button>
        <button onClick={download} disabled={!imageSrc}>Download</button>
      </div>

      <div className="result">
        {loading && <div className="spinner">Processing...</div>}
        {imageSrc && <img src={imageSrc} alt="Enhanced result" />}
      </div>
    </div>
  );
}
