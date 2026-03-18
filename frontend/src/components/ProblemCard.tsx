import { Link } from 'react-router-dom'
import type { ProblemListItem } from '../types'
import DifficultyBadge from './DifficultyBadge'
import PatternBadge from './PatternBadge'
import clsx from 'clsx'

interface Props {
  problem: ProblemListItem
  index: number
}

const companyColors: Record<string, string> = {
  google: 'bg-blue-500/20 text-blue-300',
  meta: 'bg-blue-700/20 text-blue-400',
  amazon: 'bg-orange-500/20 text-orange-300',
  apple: 'bg-gray-500/20 text-gray-300',
  microsoft: 'bg-cyan-500/20 text-cyan-300',
  anthropic: 'bg-purple-500/20 text-purple-300',
  openai: 'bg-emerald-500/20 text-emerald-300',
  netflix: 'bg-red-600/20 text-red-300',
  uber: 'bg-gray-600/20 text-gray-300',
  airbnb: 'bg-pink-500/20 text-pink-300',
  linkedin: 'bg-blue-600/20 text-blue-300',
  twitter: 'bg-sky-500/20 text-sky-300',
}

const vizTypeIcons: Record<string, string> = {
  array: '▤',
  tree: '⎇',
  graph: '⊕',
  grid: '⊞',
  none: '—',
}

export default function ProblemCard({ problem, index }: Props) {
  return (
    <Link
      to={`/problems/${problem.id}`}
      className={clsx(
        'flex items-center gap-4 px-4 py-3 border-b border-border',
        'hover:bg-bg-tertiary/50 transition-colors group'
      )}
    >
      {/* Index */}
      <span className="w-8 text-right text-text-muted text-xs font-mono flex-shrink-0">
        {index + 1}
      </span>

      {/* Title */}
      <div className="flex-1 min-w-0">
        <span className="text-text-primary group-hover:text-accent-blue transition-colors font-medium text-sm">
          {problem.title}
        </span>
      </div>

      {/* Difficulty */}
      <div className="hidden sm:block flex-shrink-0">
        <DifficultyBadge difficulty={problem.difficulty} />
      </div>

      {/* Pattern */}
      <div className="hidden md:block flex-shrink-0">
        <PatternBadge pattern={problem.pattern} />
      </div>

      {/* Companies */}
      <div className="hidden lg:flex items-center gap-1 flex-shrink-0 max-w-48">
        {problem.companies.slice(0, 3).map((company) => (
          <span
            key={company}
            className={clsx(
              'text-xs px-1.5 py-0.5 rounded font-medium',
              companyColors[company] || 'bg-bg-tertiary text-text-muted'
            )}
          >
            {company}
          </span>
        ))}
        {problem.companies.length > 3 && (
          <span className="text-xs text-text-muted">+{problem.companies.length - 3}</span>
        )}
      </div>

      {/* Viz type */}
      <div className="hidden xl:flex items-center gap-1 flex-shrink-0 w-16">
        <span className="text-text-muted text-sm font-mono">{vizTypeIcons[problem.viz_type]}</span>
        <span className="text-text-muted text-xs">{problem.viz_type}</span>
      </div>
    </Link>
  )
}
