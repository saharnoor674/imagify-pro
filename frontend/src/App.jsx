import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Enhancement from './pages/Enhancement';
import Animation from './pages/Animation';

export default function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh' }}>
        {/* Navigation Menu */}
        <nav style={{
          padding: '20px',
          background: 'linear-gradient(to right, #667eea 0%, #764ba2 100%)',
          color: 'white',
          display: 'flex',
          gap: '20px',
          alignItems: 'center'
        }}>
          <h1 style={{ margin: 0, fontSize: '24px' }}>Imagify Pro</h1>
          <Link to="/" style={{ color: 'white', textDecoration: 'none', fontWeight: 'bold' }}>
            Enhancement
          </Link>
          <Link to="/animation" style={{ color: 'white', textDecoration: 'none', fontWeight: 'bold' }}>
            Animation
          </Link>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<Enhancement />} />
          <Route path="/animation" element={<Animation />} />
        </Routes>
      </div>
    </Router>
  );
}