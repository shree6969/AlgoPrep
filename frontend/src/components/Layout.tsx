import { Outlet, NavLink } from 'react-router-dom'
import { Code2, BookOpen, Network, Menu, X, Zap, Shield } from 'lucide-react'
import { useState } from 'react'
import clsx from 'clsx'

export default function Layout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navLinks = [
    { to: '/problems', label: 'Problems', icon: <BookOpen size={16} /> },
    { to: '/patterns', label: 'Patterns', icon: <Network size={16} /> },
    { to: '/security', label: 'Security', icon: <Shield size={16} /> },
  ]

  return (
    <div className="flex flex-col min-h-screen">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-bg-secondary border-b border-border">
        <div className="max-w-screen-2xl mx-auto px-4 h-14 flex items-center justify-between">
          {/* Logo */}
          <NavLink to="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-blue to-accent-purple flex items-center justify-center">
              <Code2 size={16} className="text-white" />
            </div>
            <span className="font-bold text-lg text-text-primary">
              AlgoPrep
            </span>
            <span className="text-xs bg-accent-purple/20 text-accent-purple px-1.5 py-0.5 rounded font-medium">
              L7/L8
            </span>
          </NavLink>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  clsx(
                    'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-accent-blue/10 text-accent-blue'
                      : 'text-text-secondary hover:text-text-primary hover:bg-bg-tertiary'
                  )
                }
              >
                {link.icon}
                {link.label}
              </NavLink>
            ))}
          </div>

          {/* Right side */}
          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-1.5 text-xs text-text-muted bg-bg-tertiary px-3 py-1.5 rounded-lg border border-border">
              <Zap size={12} className="text-accent-yellow" />
              <span>L7/L8 Interview Prep</span>
            </div>

            {/* Mobile menu button */}
            <button
              className="md:hidden btn btn-ghost p-2"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-border bg-bg-secondary px-4 py-3 flex flex-col gap-1">
            {navLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                onClick={() => setMobileMenuOpen(false)}
                className={({ isActive }) =>
                  clsx(
                    'flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium',
                    isActive
                      ? 'bg-accent-blue/10 text-accent-blue'
                      : 'text-text-secondary hover:bg-bg-tertiary'
                  )
                }
              >
                {link.icon}
                {link.label}
              </NavLink>
            ))}
          </div>
        )}
      </nav>

      {/* Page content */}
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  )
}
