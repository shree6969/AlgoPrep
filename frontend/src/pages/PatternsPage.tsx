import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getPatterns } from '../api'
import type { PatternInfo } from '../types'
import { ChevronRight } from 'lucide-react'

const patternIcons: Record<string, string> = {
  'Two Pointers': '⟺',
  'Sliding Window': '⊡',
  'Binary Search': '⌗',
  'Dynamic Programming 1D': 'Σ',
  'Dynamic Programming 2D': '⊞',
  'Trees': '⎇',
  'Graph Traversal': '⊕',
  'Heap / Priority Queue': '△',
  'Backtracking': '↺',
  'Monotonic Stack': '≡',
  'Trie': '⋮',
  'Union Find': '⊔',
  'System Design Coding': '⚙',
  'Intervals': '⊢',
}

const patternColors: Record<string, { bg: string; text: string; border: string }> = {
  'Two Pointers': { bg: 'bg-cyan-500/10', text: 'text-cyan-400', border: 'border-cyan-500/20' },
  'Sliding Window': { bg: 'bg-blue-500/10', text: 'text-blue-400', border: 'border-blue-500/20' },
  'Binary Search': { bg: 'bg-indigo-500/10', text: 'text-indigo-400', border: 'border-indigo-500/20' },
  'Dynamic Programming 1D': { bg: 'bg-purple-500/10', text: 'text-purple-400', border: 'border-purple-500/20' },
  'Dynamic Programming 2D': { bg: 'bg-violet-500/10', text: 'text-violet-400', border: 'border-violet-500/20' },
  'Trees': { bg: 'bg-green-500/10', text: 'text-green-400', border: 'border-green-500/20' },
  'Graph Traversal': { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/20' },
  'Heap / Priority Queue': { bg: 'bg-orange-500/10', text: 'text-orange-400', border: 'border-orange-500/20' },
  'Backtracking': { bg: 'bg-red-500/10', text: 'text-red-400', border: 'border-red-500/20' },
  'Monotonic Stack': { bg: 'bg-yellow-500/10', text: 'text-yellow-400', border: 'border-yellow-500/20' },
  'Trie': { bg: 'bg-pink-500/10', text: 'text-pink-400', border: 'border-pink-500/20' },
  'Union Find': { bg: 'bg-rose-500/10', text: 'text-rose-400', border: 'border-rose-500/20' },
  'System Design Coding': { bg: 'bg-sky-500/10', text: 'text-sky-400', border: 'border-sky-500/20' },
  'Intervals': { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/20' },
}

export default function PatternsPage() {
  const [patterns, setPatterns] = useState<PatternInfo[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getPatterns()
      .then(setPatterns)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="max-w-screen-xl mx-auto px-6 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-text-primary mb-2">Algorithm Patterns</h1>
        <p className="text-text-muted">
          Master these {patterns.length} fundamental patterns to solve any interview problem.
        </p>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 9 }).map((_, i) => (
            <div key={i} className="card p-6 h-40 animate-pulse" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {patterns.map((pattern) => {
            const colors = patternColors[pattern.name] || {
              bg: 'bg-bg-tertiary',
              text: 'text-text-secondary',
              border: 'border-border',
            }
            const icon = patternIcons[pattern.name] || '◆'

            return (
              <Link
                key={pattern.name}
                to={`/problems?pattern=${encodeURIComponent(pattern.name)}`}
                className={`card p-6 hover:scale-[1.02] transition-all group ${colors.bg} border ${colors.border}`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div
                    className={`text-3xl font-mono opacity-80 ${colors.text}`}
                  >
                    {icon}
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-text-muted bg-bg-tertiary px-2 py-0.5 rounded border border-border">
                      {pattern.count} problems
                    </span>
                    <ChevronRight
                      size={16}
                      className="text-text-muted group-hover:text-text-secondary transition-colors"
                    />
                  </div>
                </div>
                <h3 className={`font-bold text-lg mb-2 group-hover:text-white transition-colors ${colors.text}`}>
                  {pattern.name}
                </h3>
                <p className="text-text-muted text-sm leading-relaxed line-clamp-2">
                  {pattern.description}
                </p>
              </Link>
            )
          })}
        </div>
      )}
    </div>
  )
}
