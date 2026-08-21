/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'x10-green': '#00ff88',
        'x10-dark': '#0a0f0a',
        'x10-surface': '#0d1f0d',
        'x10-card': '#111c11',
        'x10-border': '#1a3a1a',
        'x10-amber': '#f59e0b',
        'x10-blue': '#3b82f6',
        'x10-red': '#ef4444',
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'monospace'],
        'sans': ['Space Grotesk', 'sans-serif'],
      },
      boxShadow: {
        'glow-green': '0 0 20px rgba(0, 255, 136, 0.3)',
        'glow-amber': '0 0 20px rgba(245, 158, 11, 0.3)',
      },
      backdropBlur: {
        'xs': '2px',
      }
    }
  },
  plugins: [],
}
