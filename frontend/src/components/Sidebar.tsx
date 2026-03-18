import { useState, useEffect } from 'react'
import { Search, X, ChevronDown, ChevronUp } from 'lucide-react'
import { getPatterns, getCompanies } from '../api'
import type { PatternInfo, CompanyInfo } from '../types'
import clsx from 'clsx'

interface Props {
  onFilterChange: (filters: {
    pattern?: string
    difficulty?: string
    company?: string
    search?: string
  }) => void
  activeFilters: {
    pattern?: string
    difficulty?: string
    company?: string
    search?: string
  }
}

const difficulties = ['Easy', 'Medium', 'Hard']

export default function Sidebar({ onFilterChange, activeFilters }: Props) {
  const [patterns, setPatterns] = useState<PatternInfo[]>([])
  const [companies, setCompanies] = useState<CompanyInfo[]>([])
  const [showAllCompanies, setShowAllCompanies] = useState(false)
  const [searchInput, setSearchInput] = useState(activeFilters.search || '')

  useEffect(() => {
    getPatterns().then(setPatterns).catch(console.error)
    getCompanies().then(setCompanies).catch(console.error)
  }, [])

  const handleSearch = (val: string) => {
    setSearchInput(val)
    onFilterChange({ ...activeFilters, search: val || undefined })
  }

  const handlePattern = (pattern: string) => {
    const newPattern = activeFilters.pattern === pattern ? undefined : pattern
    onFilterChange({ ...activeFilters, pattern: newPattern })
  }

  const handleDifficulty = (diff: string) => {
    const newDiff = activeFilters.difficulty === diff ? undefined : diff
    onFilterChange({ ...activeFilters, difficulty: newDiff })
  }

  const handleCompany = (company: string) => {
    const newCompany = activeFilters.company === company ? undefined : company
    onFilterChange({ ...activeFilters, company: newCompany })
  }

  const clearAll = () => {
    setSearchInput('')
    onFilterChange({})
  }

  const hasFilters = !!(
    activeFilters.pattern ||
    activeFilters.difficulty ||
    activeFilters.company ||
    activeFilters.search
  )

  const displayedCompanies = showAllCompanies ? companies : companies.slice(0, 8)

  return (
    <aside className="w-60 flex-shrink-0 bg-bg-secondary border-r border-border flex flex-col h-full overflow-y-auto">
      <div className="p-4 space-y-5">
        {/* Search */}
        <div>
          <div className="relative">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" />
            <input
              type="text"
              placeholder="Search problems..."
              value={searchInput}
              onChange={(e) => handleSearch(e.target.value)}
              className="input w-full pl-9 pr-3 py-2 text-sm"
            />
            {searchInput && (
              <button
                onClick={() => handleSearch('')}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-primary"
              >
                <X size={14} />
              </button>
            )}
          </div>
        </div>

        {/* Clear filters */}
        {hasFilters && (
          <button
            onClick={clearAll}
            className="text-xs text-accent-blue hover:underline flex items-center gap-1"
          >
            <X size={12} /> Clear all filters
          </button>
        )}

        {/* Difficulty */}
        <div>
          <h3 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">
            Difficulty
          </h3>
          <div className="space-y-1">
            {difficulties.map((diff) => {
              const isActive = activeFilters.difficulty === diff
              const color =
                diff === 'Easy'
                  ? 'text-accent-green'
                  : diff === 'Medium'
                  ? 'text-accent-yellow'
                  : 'text-accent-red'
              return (
                <button
                  key={diff}
                  onClick={() => handleDifficulty(diff)}
                  className={clsx(
                    'w-full text-left px-3 py-1.5 rounded-lg text-sm flex items-center justify-between transition-colors',
                    isActive
                      ? 'bg-bg-tertiary border border-border-light'
                      : 'hover:bg-bg-tertiary/60'
                  )}
                >
                  <span className={clsx(isActive ? color : 'text-text-secondary')}>{diff}</span>
                  {isActive && <X size={12} className="text-text-muted" />}
                </button>
              )
            })}
          </div>
        </div>

        {/* Patterns */}
        <div>
          <h3 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">
            Patterns
          </h3>
          <div className="space-y-0.5">
            {patterns.map((p) => {
              const isActive = activeFilters.pattern === p.name
              return (
                <button
                  key={p.name}
                  onClick={() => handlePattern(p.name)}
                  className={clsx(
                    'w-full text-left px-3 py-1.5 rounded-lg text-xs flex items-center justify-between transition-colors',
                    isActive
                      ? 'bg-accent-blue/10 text-accent-blue border border-accent-blue/20'
                      : 'text-text-secondary hover:bg-bg-tertiary/60 hover:text-text-primary'
                  )}
                >
                  <span className="truncate">{p.name}</span>
                  <span className="ml-2 text-text-muted flex-shrink-0">{p.count}</span>
                </button>
              )
            })}
          </div>
        </div>

        {/* Companies */}
        <div>
          <h3 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">
            Companies
          </h3>
          <div className="space-y-0.5">
            {displayedCompanies.map((c) => {
              const isActive = activeFilters.company === c.name
              return (
                <button
                  key={c.name}
                  onClick={() => handleCompany(c.name)}
                  className={clsx(
                    'w-full text-left px-3 py-1.5 rounded-lg text-xs flex items-center justify-between transition-colors capitalize',
                    isActive
                      ? 'bg-accent-purple/10 text-accent-purple border border-accent-purple/20'
                      : 'text-text-secondary hover:bg-bg-tertiary/60 hover:text-text-primary'
                  )}
                >
                  <span>{c.name}</span>
                  <span className="ml-2 text-text-muted">{c.count}</span>
                </button>
              )
            })}
          </div>
          {companies.length > 8 && (
            <button
              onClick={() => setShowAllCompanies(!showAllCompanies)}
              className="mt-2 text-xs text-accent-blue hover:underline flex items-center gap-1 px-3"
            >
              {showAllCompanies ? (
                <>
                  <ChevronUp size={12} /> Show less
                </>
              ) : (
                <>
                  <ChevronDown size={12} /> Show all ({companies.length})
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </aside>
  )
}
