import { useState, useEffect } from 'react'

export type Theme = 'dark' | 'light'

function applyTheme(theme: Theme) {
  if (theme === 'light') {
    document.documentElement.classList.add('light')
  } else {
    document.documentElement.classList.remove('light')
  }
}

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(() => {
    const stored = localStorage.getItem('theme') as Theme | null
    return stored ?? 'dark'
  })

  useEffect(() => {
    applyTheme(theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  // Apply on mount (handles SSR / hydration)
  useEffect(() => {
    applyTheme(theme)
  }, [])

  const toggle = () => setTheme(t => (t === 'dark' ? 'light' : 'dark'))

  return { theme, toggle }
}
