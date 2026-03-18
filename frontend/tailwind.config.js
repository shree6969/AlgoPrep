/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        bg: {
          primary:   'rgb(var(--bg-primary)   / <alpha-value>)',
          secondary: 'rgb(var(--bg-secondary) / <alpha-value>)',
          tertiary:  'rgb(var(--bg-tertiary)  / <alpha-value>)',
        },
        border: {
          DEFAULT: 'rgb(var(--border)       / <alpha-value>)',
          light:   'rgb(var(--border-light) / <alpha-value>)',
        },
        accent: {
          blue:   'rgb(var(--accent-blue)   / <alpha-value>)',
          purple: 'rgb(var(--accent-purple) / <alpha-value>)',
          green:  'rgb(var(--accent-green)  / <alpha-value>)',
          yellow: 'rgb(var(--accent-yellow) / <alpha-value>)',
          red:    'rgb(var(--accent-red)    / <alpha-value>)',
          orange: 'rgb(var(--accent-orange) / <alpha-value>)',
        },
        text: {
          primary:   'rgb(var(--text-primary)   / <alpha-value>)',
          secondary: 'rgb(var(--text-secondary) / <alpha-value>)',
          muted:     'rgb(var(--text-muted)     / <alpha-value>)',
        },
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.2s ease-in-out',
        'slide-up': 'slideUp 0.2s ease-out',
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(8px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
