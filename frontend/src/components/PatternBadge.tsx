import type { Pattern } from '../types'
import clsx from 'clsx'

interface Props {
  pattern: Pattern
  size?: 'sm' | 'md'
}

const patternColors: Record<string, string> = {
  'Two Pointers': 'text-cyan-400 bg-cyan-400/10 border-cyan-400/20',
  'Sliding Window': 'text-blue-400 bg-blue-400/10 border-blue-400/20',
  'Binary Search': 'text-indigo-400 bg-indigo-400/10 border-indigo-400/20',
  'Dynamic Programming 1D': 'text-purple-400 bg-purple-400/10 border-purple-400/20',
  'Dynamic Programming 2D': 'text-violet-400 bg-violet-400/10 border-violet-400/20',
  'Trees': 'text-green-400 bg-green-400/10 border-green-400/20',
  'Graph Traversal': 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
  'Heap / Priority Queue': 'text-orange-400 bg-orange-400/10 border-orange-400/20',
  'Backtracking': 'text-red-400 bg-red-400/10 border-red-400/20',
  'Monotonic Stack': 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20',
  'Trie': 'text-pink-400 bg-pink-400/10 border-pink-400/20',
  'Union Find': 'text-rose-400 bg-rose-400/10 border-rose-400/20',
  'System Design Coding': 'text-sky-400 bg-sky-400/10 border-sky-400/20',
  'Intervals': 'text-amber-400 bg-amber-400/10 border-amber-400/20',
}

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

export default function PatternBadge({ pattern, size = 'sm' }: Props) {
  const colorClass = patternColors[pattern] || 'text-text-secondary bg-bg-tertiary border-border'
  const icon = patternIcons[pattern] || '◆'

  return (
    <span
      className={clsx(
        'badge border gap-1',
        colorClass,
        size === 'md' ? 'text-sm px-2.5 py-1' : 'text-xs px-2 py-0.5'
      )}
    >
      <span className="font-mono">{icon}</span>
      {pattern}
    </span>
  )
}
