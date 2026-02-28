import React from 'react';
import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <div style={{ minHeight: '100vh', background:'#faf5ff', fontFamily: "'Segoe UI', sans-serif" }}>

      {/* ── HERO SECTION ─────────────────────────────────────────────────── */}
      <div style={{
        background: 'linear-gradient(135deg,#667eea 0%,#764ba2 60%,#f43f8e 100%)',
        padding: '80px 20px 100px',
        textAlign: 'center',
        position: 'relative',
        overflow: 'hidden',
      }}>
        {/* Background blur circles */}
        <div style={{ position: 'absolute', top: -80, left: -80, width: 300, height: 300, borderRadius: '50%', background: 'rgba(255,255,255,0.07)', pointerEvents: 'none' }} />
        <div style={{ position: 'absolute', bottom: -60, right: -60, width: 250, height: 250, borderRadius: '50%', background: 'rgba(255,255,255,0.05)', pointerEvents: 'none' }} />

        {/* Logo */}
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 24 }}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="72" height="72">
            <defs>
              <linearGradient id="logobg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{stopColor:'rgba(255,255,255,0.3)', stopOpacity:1}} />
                <stop offset="100%" style={{stopColor:'rgba(255,255,255,0.1)', stopOpacity:1}} />
              </linearGradient>
            </defs>
            <rect x="2" y="2" width="60" height="60" rx="16" ry="16" fill="url(#logobg)" />
            <path d="M32 10 C32 10,34 24,38 28 C42 32,54 32,54 32 C54 32,42 32,38 36 C34 40,32 54,32 54 C32 54,30 40,26 36 C22 32,10 32,10 32 C10 32,22 32,26 28 C30 24,32 10,32 10 Z" fill="white" />
          </svg>
        </div>

        {/* Headline */}
        <h1 style={{
          fontSize: 'clamp(2rem, 5vw, 3.5rem)',
          fontWeight: 900,
          color: 'white',
          margin: '0 0 20px',
          lineHeight: 1.15,
          maxWidth: 700,
          marginLeft: 'auto',
          marginRight: 'auto',
        }}>
          Imagify Pro — AI Photo Tools
        </h1>

        <p style={{
          fontSize: 'clamp(1rem, 2vw, 1.2rem)',
          color: 'rgba(255,255,255,0.85)',
          maxWidth: 520,
          margin: '0 auto 40px',
          lineHeight: 1.7,
        }}>
          Enhance, animate and bring your photos to life with the power of AI — in seconds.
        </p>

        {/* CTA Button */}
        <Link to="/enhancement" style={{
          display: 'inline-block',
          background: 'white',
          color: '#764ba2',
          fontWeight: 800,
          fontSize: 17,
          padding: '16px 48px',
          borderRadius: 50,
          textDecoration: 'none',
          boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
          transition: 'all 0.2s',
          letterSpacing: '0.2px',
        }}>
          Get Started Now →
        </Link>

        
      </div>

      {/* ── FEATURES SECTION ─────────────────────────────────────────────── */}
      <div style={{ padding: '80px 20px', maxWidth: 1100, margin: '0 auto' }}>
        <h2 style={{ textAlign: 'center', fontSize: 32, fontWeight: 800, color: '#1f2937', marginBottom: 12 }}>
          What can Imagify Pro do?
        </h2>
        <p style={{ textAlign: 'center', color: '#6b7280', marginBottom: 56, fontSize: 16 }}>
          Three powerful AI tools in one place
        </p>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: 28,
        }}>
          {/* Enhancement Card */}
          <FeatureCard
            to="/enhancement"
            gradient="linear-gradient(135deg, #f59e0b, #ef4444)"
            
            title="Image Enhancement"
            description="Boost brightness, sharpness and clarity of any photo in real time using professional-grade AI sliders."
            bullets={['Live preview', 'Brightness control', 'Deblur & Clarity']}
          />

          {/* Animation Card */}
          <FeatureCard
            to="/animation"
            gradient="linear-gradient(135deg, #9333ea, #3b82f6)"
    
            title="Smile Animation"
            description="Upload a face photo and generate a realistic AI smile using Replicate's expression editor model."
            bullets={['Real AI smile', 'Photorealistic result', 'Download instantly']}
          />

          {/* Video Card */}
          <FeatureCard
            to="/video"
            gradient="linear-gradient(135deg, #10b981, #0ea5e9)"
            
            title="Video Generation"
            description="Turn a single photo into a 5-second MP4 video with eye blinking, smile and natural head movement."
            bullets={['Eye blinking', 'Head movement', 'MP4 download']}
          />
        </div>
      </div>

      {/* ── HOW IT WORKS ─────────────────────────────────────────────────── */}
      <div style={{ background: 'white', padding: '80px 20px' }}>
        <div style={{ maxWidth: 900, margin: '0 auto', textAlign: 'center' }}>
          <h2 style={{ fontSize: 32, fontWeight: 800, color: '#1f2937', marginBottom: 12 }}>
            How it works
          </h2>
          <p style={{ color: '#6b7280', marginBottom: 56, fontSize: 16 }}>
            Three simple steps to transform your photos
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 32 }}>
            {[
              { step: '01', title: 'Upload Photo', desc: 'Choose any photo from your device — JPG, PNG or WEBP supported.' },
              { step: '02', title: 'Choose Tool', desc: 'Pick Enhancement, Animation or Video Generation based on what you need.' },
              { step: '03', title: 'Download Result', desc: 'AI processes your photo and delivers the result in seconds. Download and share!' },
            ].map((s) => (
              <div key={s.step} style={{ textAlign: 'center' }}>
                <div style={{
                  width: 56, height: 56, borderRadius: '50%',
                  background: 'linear-gradient(135deg, #667eea, #764ba2)',
                  color: 'white', fontWeight: 900, fontSize: 16,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  margin: '0 auto 16px',
                  boxShadow: '0 4px 16px rgba(102,126,234,0.4)',
                }}>
                  {s.step}
                </div>
                <h3 style={{ fontSize: 18, fontWeight: 700, color: '#1f2937', marginBottom: 8 }}>{s.title}</h3>
                <p style={{ fontSize: 14, color: '#6b7280', lineHeight: 1.6, margin: 0 }}>{s.desc}</p>
              </div>
            ))}
          </div>

          {/* Final CTA */}
          <div style={{ marginTop: 64 }}>
            <Link to="/enhancement" style={{
              display: 'inline-block',
              background: 'linear-gradient(135deg, #667eea, #764ba2)',
              color: 'white', fontWeight: 800,
              fontSize: 16, padding: '14px 44px',
              borderRadius: 50, textDecoration: 'none',
              boxShadow: '0 4px 20px rgba(102,126,234,0.4)',
            }}>
              Try Imagify Pro Free →
            </Link>
          </div>
        </div>
      </div>

      {/* ── FOOTER ───────────────────────────────────────────────────────── */}
      <footer style={{
        background: '#1f2937',
        padding: '40px 20px',
        textAlign: 'center',
      }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 10, marginBottom: 20 }}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="32" height="32">
            <rect x="2" y="2" width="60" height="60" rx="14" ry="14" fill="url(#footerbg)" />
            <defs>
              <linearGradient id="footerbg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{stopColor:'#667eea', stopOpacity:1}} />
                <stop offset="100%" style={{stopColor:'#f43f8e', stopOpacity:1}} />
              </linearGradient>
            </defs>
            <path d="M32 10 C32 10,34 24,38 28 C42 32,54 32,54 32 C54 32,42 32,38 36 C34 40,32 54,32 54 C32 54,30 40,26 36 C22 32,10 32,10 32 C10 32,22 32,26 28 C30 24,32 10,32 10 Z" fill="white" />
          </svg>
          <span style={{ color: 'white', fontWeight: 800, fontSize: 18 }}>Imagify Pro</span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'center', gap: 24, marginBottom: 24, flexWrap: 'wrap' }}>
          {[
            { to: '/enhancement', label: 'Enhancement' },
            { to: '/animation', label: 'Animation' },
            { to: '/video', label: 'Video' },
          ].map((l) => (
            <Link key={l.to} to={l.to} style={{ color: '#9ca3af', textDecoration: 'none', fontSize: 14, fontWeight: 500 }}>
              {l.label}
            </Link>
          ))}
        </div>

        <p style={{ color: '#6b7280', fontSize: 13, margin: 0 }}>
          © 2026 Imagify Pro — All rights reserved
        </p>
      </footer>

    </div>
  );
}

function FeatureCard({ to, gradient, icon, title, description, bullets }) {
  return (
    <div style={{
      background: 'white',
      borderRadius: 20,
      overflow: 'hidden',
      boxShadow: '0 8px 32px rgba(0,0,0,0.08)',
      border: '1px solid#f3f4f6',
      transition: 'transform 0.2s, box-shadow 0.2s',
    }}>
      {/* Color top bar */}
      <div style={{ height: 6, background: gradient }} />

      <div style={{ padding: '28px 28px 24px' }}>
        <div style={{ fontSize: 36, marginBottom: 14 }}>{icon}</div>
        <h3 style={{ fontSize: 20, fontWeight: 800, color: '#1f2937', marginBottom: 10 }}>{title}</h3>
        <p style={{ fontSize: 14, color: '#6b7280', lineHeight: 1.65, marginBottom: 20 }}>{description}</p>

        {/* Bullets */}
        <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 24px', display: 'flex', flexDirection: 'column', gap: 6 }}>
          {bullets.map((b) => (
            <li key={b} style={{ fontSize: 13, color: '#374151', display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ color: '#9333ea', fontWeight: 700 }}>✓</span> {b}
            </li>
          ))}
        </ul>

        <Link to={to} style={{
          display: 'block', textAlign: 'center',
          background: gradient,
          color: 'white', fontWeight: 700,
          fontSize: 14, padding: '10px 0',
          borderRadius: 10, textDecoration: 'none',
        }}>
          Try Now →
        </Link>
      </div>
    </div>
  );
}