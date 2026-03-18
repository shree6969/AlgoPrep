import type { Difficulty } from '../types'
import clsx from 'clsx'

interface Props {
  difficulty: Difficulty
  size?: 'sm' | 'md'
}

const colors: Record<Difficulty, string> = {
  Easy: 'text-accent-green bg-accent-green/10 border-accent-green/20',
  Medium: 'text-accent-yellow bg-accent-yellow/10 border-accent-yellow/20',
  Hard: 'text-accent-red bg-accent-red/10 border-accent-red/20',
}

export default function DifficultyBadge({ difficulty, size = 'sm' }: Props) {
  return (
    <span
      className={clsx(
        'badge border font-semibold',
        colors[difficulty],
        size === 'md' ? 'text-sm px-2.5 py-1' : 'text-xs px-2 py-0.5'
      )}
    >
      {difficulty}
    </span>
  )
}
