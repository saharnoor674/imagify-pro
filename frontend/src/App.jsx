import React from 'react';
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
  const isLanding = location.pathname === '/';

  const links = [
    { to: "/enhancement", label: "Enhancement" },
    { to: "/animation", label: "Animation" },
    { to: "/video", label: "Video" },
  ];

  return (
    <nav style={{
      padding: '0 32px',
      height: 62,
      background: 'linear-gradient(to right, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      boxShadow: '0 2px 16px rgba(102,126,234,0.25)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
    }}>

      {/* Logo + Brand */}
      <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: 10, textDecoration: 'none', marginRight: 24 }}>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="36" height="36">
          <defs>
            <linearGradient id="navbg" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style={{stopColor:'rgba(255,255,255,0.3)', stopOpacity:1}} />
              <stop offset="100%" style={{stopColor:'rgba(255,255,255,0.1)', stopOpacity:1}} />
            </linearGradient>
          </defs>
          <rect x="2" y="2" width="60" height="60" rx="14" ry="14" fill="url(#navbg)" />
          <path d="M32 10 C32 10,34 24,38 28 C42 32,54 32,54 32 C54 32,42 32,38 36 C34 40,32 54,32 54 C32 54,30 40,26 36 C22 32,10 32,10 32 C10 32,22 32,26 28 C30 24,32 10,32 10 Z" fill="white" />
        </svg>
        <span style={{ color: 'white', fontWeight: 800, fontSize: 18, letterSpacing: '-0.3px' }}>
          Imagify Pro
        </span>
      </Link>

      {/* Divider */}
      <div style={{ width: 1, height: 24, background: 'rgba(255,255,255,0.2)', marginRight: 8 }} />

      {/* Nav links — hide on landing page */}
      {!isLanding && links.map((link) => {
        const isActive = location.pathname === link.to;
        return (
          <Link key={link.to} to={link.to} style={{
            color: 'white', textDecoration: 'none',
            fontWeight: isActive ? 700 : 500, fontSize: 14,
            padding: '6px 18px', borderRadius: 20,
            background: isActive ? 'rgba(255,255,255,0.22)' : 'transparent',
            border: isActive ? '1px solid rgba(255,255,255,0.35)' : '1px solid transparent',
            transition: 'all 0.2s',
          }}>
            {link.label}
          </Link>
        );
      })}

      {/* On landing page show nav links on right */}
      {isLanding && (
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
          {links.map((link) => (
            <Link key={link.to} to={link.to} style={{
              color: 'white', textDecoration: 'none',
              fontWeight: 500, fontSize: 14,
              padding: '6px 18px', borderRadius: 20,
              border: '1px solid rgba(255,255,255,0.3)',
              transition: 'all 0.2s',
            }}>
              {link.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
}