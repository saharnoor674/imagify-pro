import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Landing from './pages/Landing';
import Enhancement from './pages/Enhancement';
import Animation from './pages/Animation';
import Video from './pages/Video';

export default function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh' }}>
        <NavBar />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/enhancement" element={<Enhancement />} />
          <Route path="/animation" element={<Animation />} />
          <Route path="/video" element={<Video />} />
        </Routes>
      </div>
    </Router>
  );
}

function NavBar() {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  const links = [
    { to: "/enhancement", label: "Enhancement" },
    { to: "/animation", label: "Animation" },
    { to: "/video", label: "Video" },
  ];

  return (
    <>
      <nav style={{
        padding: '0 16px',
        height: 56,
        background: 'linear-gradient(to right, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        boxShadow: '0 2px 16px rgba(102,126,234,0.25)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
      }}>
        {/* Logo */}
        <Link to="/" onClick={() => setMenuOpen(false)} style={{ display: 'flex', alignItems: 'center', gap: 8, textDecoration: 'none', flexShrink: 0 }}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="30" height="30">
            <defs>
              <linearGradient id="navbg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{stopColor:'rgba(255,255,255,0.3)', stopOpacity:1}} />
                <stop offset="100%" style={{stopColor:'rgba(255,255,255,0.1)', stopOpacity:1}} />
              </linearGradient>
            </defs>
            <rect x="2" y="2" width="60" height="60" rx="14" ry="14" fill="url(#navbg)" />
            <path d="M32 10 C32 10,34 24,38 28 C42 32,54 32,54 32 C54 32,42 32,38 36 C34 40,32 54,32 54 C32 54,30 40,26 36 C22 32,10 32,10 32 C10 32,22 32,26 28 C30 24,32 10,32 10 Z" fill="white" />
          </svg>
          <span style={{ color: 'white', fontWeight: 800, fontSize: 16, whiteSpace: 'nowrap' }}>
            Imagify Pro
          </span>
        </Link>

        {/* Desktop links */}
        <div className="desktop-links" style={{ marginLeft: 'auto', display: 'flex', gap: 6 }}>
          {links.map((link) => {
            const isActive = location.pathname === link.to;
            return (
              <Link key={link.to} to={link.to} style={{
                color: 'white', textDecoration: 'none',
                fontWeight: isActive ? 700 : 500,
                fontSize: 13,
                padding: '5px 12px',
                borderRadius: 20,
                background: isActive ? 'rgba(255,255,255,0.22)' : 'transparent',
                border: '1px solid rgba(255,255,255,0.3)',
                whiteSpace: 'nowrap',
              }}>
                {link.label}
              </Link>
            );
          })}
        </div>

        {/* Hamburger button - mobile only */}
        <button
          className="hamburger"
          onClick={() => setMenuOpen(!menuOpen)}
          style={{
            display: 'none',
            marginLeft: 'auto',
            background: 'rgba(255,255,255,0.2)',
            border: '1px solid rgba(255,255,255,0.3)',
            borderRadius: 8,
            padding: '6px 10px',
            cursor: 'pointer',
            flexDirection: 'column',
            gap: 4,
          }}
        >
          <span style={{ display: 'block', width: 20, height: 2, background: 'white', borderRadius: 2 }} />
          <span style={{ display: 'block', width: 20, height: 2, background: 'white', borderRadius: 2 }} />
          <span style={{ display: 'block', width: 20, height: 2, background: 'white', borderRadius: 2 }} />
        </button>
      </nav>

      {/* Mobile dropdown menu */}
      {menuOpen && (
        <div style={{
          position: 'sticky',
          top: 56,
          zIndex: 99,
          background: 'linear-gradient(to right, #667eea 0%, #764ba2 100%)',
          display: 'flex',
          flexDirection: 'column',
          padding: '8px 16px 16px',
          gap: 8,
          boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
        }}>
          {links.map((link) => {
            const isActive = location.pathname === link.to;
            return (
              <Link
                key={link.to}
                to={link.to}
                onClick={() => setMenuOpen(false)}
                style={{
                  color: 'white',
                  textDecoration: 'none',
                  fontWeight: isActive ? 700 : 500,
                  fontSize: 15,
                  padding: '10px 16px',
                  borderRadius: 12,
                  background: isActive ? 'rgba(255,255,255,0.22)' : 'rgba(255,255,255,0.1)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  textAlign: 'center',
                }}
              >
                {link.label}
              </Link>
            );
          })}
        </div>
      )}

      <style>{`
        @media (max-width: 520px) {
          .desktop-links { display: none !important; }
          .hamburger { display: flex !important; }
        }
      `}</style>
    </>
  );
}