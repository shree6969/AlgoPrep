import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { getProblems } from '../api'
import type { ProblemListItem } from '../types'
import ProblemCard from '../components/ProblemCard'
import Sidebar from '../components/Sidebar'
import { SlidersHorizontal, X } from 'lucide-react'
import clsx from 'clsx'

interface Filters {
  pattern?: string
  difficulty?: string
  company?: string
  search?: string
}

export default function ProblemsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [problems, setProblems] = useState<ProblemListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const getFiltersFromParams = (): Filters => ({
    pattern: searchParams.get('pattern') || undefined,
    difficulty: searchParams.get('difficulty') || undefined,
    company: searchParams.get('company') || undefined,
    search: searchParams.get('search') || undefined,
  })

  const [filters, setFilters] = useState<Filters>(getFiltersFromParams)

  useEffect(() => {
    setLoading(true)
    getProblems(filters)
      .then(setProblems)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [filters])

  const handleFilterChange = (newFilters: Filters) => {
    setFilters(newFilters)
    // Sync to URL
    const params: Record<string, string> = {}
    if (newFilters.pattern) params.pattern = newFilters.pattern
    if (newFilters.difficulty) params.difficulty = newFilters.difficulty
    if (newFilters.company) params.company = newFilters.company
    if (newFilters.search) params.search = newFilters.search
    setSearchParams(params)
  }

  const activeFilterCount = Object.values(filters).filter(Boolean).length

  return (
    <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
      {/* Sidebar */}
      <div
        className={clsx(
          'transition-all duration-200 overflow-hidden flex-shrink-0',
          sidebarOpen ? 'w-60' : 'w-0'
        )}
      >
        {sidebarOpen && (
          <Sidebar onFilterChange={handleFilterChange} activeFilters={filters} />
        )}
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-border bg-bg-secondary flex-shrink-0">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className={clsx(
              'btn btn-ghost btn-sm p-2 gap-1.5',
              activeFilterCount > 0 && !sidebarOpen && 'text-accent-blue'
            )}
            title="Toggle filters"
          >
            <SlidersHorizontal size={16} />
            {activeFilterCount > 0 && !sidebarOpen && (
              <span className="text-xs font-semibold">{activeFilterCount}</span>
            )}
          </button>

          <div className="flex-1">
            <span className="text-text-primary font-semibold">Problems</span>
            {!loading && (
              <span className="ml-2 text-text-muted text-sm">({problems.length})</span>
            )}
          </div>

          {/* Active filter pills */}
          <div className="flex items-center gap-2 flex-wrap">
            {filters.pattern && (
              <span className="text-xs bg-accent-blue/10 text-accent-blue border border-accent-blue/20 px-2 py-0.5 rounded-full flex items-center gap-1">
                {filters.pattern}
                <button onClick={() => handleFilterChange({ ...filters, pattern: undefined })}>
                  <X size={10} />
                </button>
              </span>
            )}
            {filters.difficulty && (
              <span className="text-xs bg-accent-yellow/10 text-accent-yellow border border-accent-yellow/20 px-2 py-0.5 rounded-full flex items-center gap-1">
                {filters.difficulty}
                <button onClick={() => handleFilterChange({ ...filters, difficulty: undefined })}>
                  <X size={10} />
                </button>
              </span>
            )}
            {filters.company && (
              <span className="text-xs bg-accent-purple/10 text-accent-purple border border-accent-purple/20 px-2 py-0.5 rounded-full flex items-center gap-1 capitalize">
                {filters.company}
                <button onClick={() => handleFilterChange({ ...filters, company: undefined })}>
                  <X size={10} />
                </button>
              </span>
            )}
          </div>
        </div>

        {/* Table header */}
        <div className="flex items-center gap-4 px-4 py-2 border-b border-border bg-bg-secondary/50 text-xs text-text-muted flex-shrink-0">
          <span className="w-8 text-right">#</span>
          <span className="flex-1">Title</span>
          <span className="hidden sm:block w-20">Difficulty</span>
          <span className="hidden md:block w-40">Pattern</span>
          <span className="hidden lg:block w-48">Companies</span>
          <span className="hidden xl:block w-20">Viz</span>
        </div>

        {/* Problems list */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="space-y-0">
              {Array.from({ length: 12 }).map((_, i) => (
                <div
                  key={i}
                  className="flex items-center gap-4 px-4 py-3 border-b border-border animate-pulse"
                >
                  <div className="w-8 h-3 bg-bg-tertiary rounded" />
                  <div className="flex-1 h-3 bg-bg-tertiary rounded" />
                  <div className="hidden sm:block w-16 h-4 bg-bg-tertiary rounded" />
                  <div className="hidden md:block w-28 h-4 bg-bg-tertiary rounded" />
                </div>
              ))}
            </div>
          ) : problems.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-text-muted py-20">
              <div className="text-4xl mb-3">🔍</div>
              <p className="text-text-secondary font-medium">No problems found</p>
              <p className="text-sm mt-1">Try adjusting your filters</p>
            </div>
          ) : (
            <div>
              {problems.map((problem, index) => (
                <ProblemCard key={problem.id} problem={problem} index={index} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
