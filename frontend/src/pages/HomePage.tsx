import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getPatterns, getProblems } from '../api'
import type { PatternInfo, ProblemListItem } from '../types'
import { Code2, BarChart2, Network, ChevronRight, Zap, Target, BookOpen } from 'lucide-react'

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

const patternGradients: Record<string, string> = {
  'Two Pointers': 'from-cyan-500/20 to-cyan-500/5 border-cyan-500/20',
  'Sliding Window': 'from-blue-500/20 to-blue-500/5 border-blue-500/20',
  'Binary Search': 'from-indigo-500/20 to-indigo-500/5 border-indigo-500/20',
  'Dynamic Programming 1D': 'from-purple-500/20 to-purple-500/5 border-purple-500/20',
  'Dynamic Programming 2D': 'from-violet-500/20 to-violet-500/5 border-violet-500/20',
  'Trees': 'from-green-500/20 to-green-500/5 border-green-500/20',
  'Graph Traversal': 'from-emerald-500/20 to-emerald-500/5 border-emerald-500/20',
  'Heap / Priority Queue': 'from-orange-500/20 to-orange-500/5 border-orange-500/20',
  'Backtracking': 'from-red-500/20 to-red-500/5 border-red-500/20',
  'Monotonic Stack': 'from-yellow-500/20 to-yellow-500/5 border-yellow-500/20',
  'Trie': 'from-pink-500/20 to-pink-500/5 border-pink-500/20',
  'Union Find': 'from-rose-500/20 to-rose-500/5 border-rose-500/20',
  'System Design Coding': 'from-sky-500/20 to-sky-500/5 border-sky-500/20',
  'Intervals': 'from-amber-500/20 to-amber-500/5 border-amber-500/20',
}

const companies = ['google', 'meta', 'amazon', 'apple', 'microsoft', 'anthropic', 'netflix', 'uber', 'airbnb']

export default function HomePage() {
  const [patterns, setPatterns] = useState<PatternInfo[]>([])
  const [problems, setProblems] = useState<ProblemListItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getPatterns(), getProblems()])
      .then(([pats, probs]) => {
        setPatterns(pats)
        setProblems(probs)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const diffCounts = {
    Easy: problems.filter((p) => p.difficulty === 'Easy').length,
    Medium: problems.filter((p) => p.difficulty === 'Medium').length,
    Hard: problems.filter((p) => p.difficulty === 'Hard').length,
  }

  return (
    <div className="max-w-screen-xl mx-auto px-6 py-12">
      {/* Hero */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 bg-accent-purple/10 text-accent-purple border border-accent-purple/20 rounded-full px-4 py-1.5 text-sm mb-6">
          <Zap size={14} />
          Built for L7/L8 System Design & Algorithms
        </div>
        <h1 className="text-5xl font-bold text-text-primary mb-4 leading-tight">
          Master{' '}
          <span className="bg-gradient-to-r from-accent-blue to-accent-purple bg-clip-text text-transparent">
            Algorithm Interviews
          </span>
        </h1>
        <p className="text-text-secondary text-xl max-w-2xl mx-auto mb-8">
          50+ curated problems with step-by-step visual explanations. Cover every pattern
          asked at top tech companies.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link to="/problems" className="btn btn-primary px-6 py-3 text-base">
            <BookOpen size={18} />
            Browse Problems
          </Link>
          <Link to="/patterns" className="btn btn-secondary px-6 py-3 text-base">
            <Network size={18} />
            Explore Patterns
          </Link>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-16">
        {[
          { label: 'Problems', value: problems.length, icon: <Code2 size={20} />, color: 'text-accent-blue' },
          { label: 'Patterns', value: patterns.length, icon: <Network size={20} />, color: 'text-accent-purple' },
          { label: 'Companies', value: companies.length, icon: <Target size={20} />, color: 'text-accent-green' },
          { label: 'Visualized', value: problems.filter((p) => p.viz_type !== 'none').length, icon: <BarChart2 size={20} />, color: 'text-accent-yellow' },
        ].map((stat) => (
          <div key={stat.label} className="card p-6 text-center">
            <div className={`${stat.color} flex justify-center mb-2`}>{stat.icon}</div>
            <div className="text-3xl font-bold text-text-primary mb-1">
              {loading ? '—' : stat.value}
            </div>
            <div className="text-text-muted text-sm">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Difficulty distribution */}
      {!loading && (
        <div className="card p-6 mb-16">
          <h2 className="text-lg font-semibold text-text-primary mb-4">Problem Distribution</h2>
          <div className="flex items-center gap-6">
            <div className="flex-1 h-3 rounded-full bg-bg-tertiary overflow-hidden flex">
              <div
                className="bg-accent-green h-full transition-all"
                style={{ width: `${(diffCounts.Easy / problems.length) * 100}%` }}
              />
              <div
                className="bg-accent-yellow h-full transition-all"
                style={{ width: `${(diffCounts.Medium / problems.length) * 100}%` }}
              />
              <div
                className="bg-accent-red h-full transition-all"
                style={{ width: `${(diffCounts.Hard / problems.length) * 100}%` }}
              />
            </div>
            <div className="flex items-center gap-4 text-sm flex-shrink-0">
              <span className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-accent-green" />
                <span className="text-text-muted">Easy</span>
                <span className="text-text-primary font-medium">{diffCounts.Easy}</span>
              </span>
              <span className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-accent-yellow" />
                <span className="text-text-muted">Medium</span>
                <span className="text-text-primary font-medium">{diffCounts.Medium}</span>
              </span>
              <span className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-accent-red" />
                <span className="text-text-muted">Hard</span>
                <span className="text-text-primary font-medium">{diffCounts.Hard}</span>
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Patterns grid */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-text-primary">Algorithm Patterns</h2>
          <Link to="/patterns" className="text-accent-blue text-sm hover:underline flex items-center gap-1">
            View all <ChevronRight size={14} />
          </Link>
        </div>

        {loading ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="card p-5 h-32 animate-pulse bg-bg-secondary" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {patterns.map((pattern) => (
              <Link
                key={pattern.name}
                to={`/problems?pattern=${encodeURIComponent(pattern.name)}`}
                className={`card p-5 bg-gradient-to-br border hover:scale-[1.02] transition-all group ${patternGradients[pattern.name] || 'from-bg-tertiary/40 to-bg-tertiary/10 border-border'}`}
              >
                <div className="text-2xl mb-3 font-mono opacity-70">
                  {patternIcons[pattern.name] || '◆'}
                </div>
                <h3 className="text-text-primary font-semibold text-sm leading-tight mb-1 group-hover:text-white">
                  {pattern.name}
                </h3>
                <div className="flex items-center justify-between mt-2">
                  <span className="text-text-muted text-xs">{pattern.count} problems</span>
                  <ChevronRight size={12} className="text-text-muted group-hover:text-text-secondary transition-colors" />
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Companies row */}
      <div className="mt-16 text-center">
        <p className="text-text-muted text-sm mb-4">Problems from top companies</p>
        <div className="flex flex-wrap justify-center gap-3">
          {companies.map((c) => (
            <Link
              key={c}
              to={`/problems?company=${c}`}
              className="capitalize text-sm px-4 py-2 rounded-full bg-bg-secondary border border-border text-text-secondary hover:text-text-primary hover:border-border-light transition-colors"
            >
              {c}
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
