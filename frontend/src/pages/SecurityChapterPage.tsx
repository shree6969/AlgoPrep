import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Clock, ChevronDown, ChevronRight, BookOpen, Code2, ExternalLink, Lightbulb, Eye, EyeOff } from 'lucide-react'
import { getSecurityChapter } from '../api'
import type { SecurityChapter, SecurityChallenge } from '../types'
import SecurityContentRenderer from '../components/SecurityContentRenderer'
import CodeMirror from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'
import { oneDark } from '@codemirror/theme-one-dark'
import clsx from 'clsx'

const DIFFICULTY_STYLES: Record<string, string> = {
  Easy:   'bg-green-500/10 text-green-400 border-green-500/20',
  Medium: 'bg-accent-yellow/10 text-accent-yellow border-accent-yellow/20',
  Hard:   'bg-red-500/10 text-red-400 border-red-500/20',
}

function ChallengeCard({ challenge }: { challenge: SecurityChallenge }) {
  const [activeTab, setActiveTab] = useState<'problem' | 'starter' | 'solution'>('problem')
  const [showHints, setShowHints] = useState(false)
  const [showSolution, setShowSolution] = useState(false)

  return (
    <div className="border border-border rounded-xl overflow-hidden bg-bg-primary">
      {/* Header */}
      <div className="bg-bg-secondary px-5 py-4 border-b border-border">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Code2 size={14} className="text-accent-purple" />
              <span className="text-xs text-text-muted font-medium uppercase tracking-wide">Coding Challenge</span>
            </div>
            <h3 className="font-semibold text-text-primary">{challenge.title}</h3>
          </div>
          <span className={`text-xs px-2 py-1 rounded border font-medium ${DIFFICULTY_STYLES[challenge.difficulty]}`}>
            {challenge.difficulty}
          </span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-border">
        {(['problem', 'starter', 'solution'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => { setActiveTab(tab); if (tab === 'solution') setShowSolution(true) }}
            className={clsx(
              'px-4 py-2.5 text-sm font-medium transition-colors',
              activeTab === tab
                ? 'text-accent-blue border-b-2 border-accent-blue'
                : 'text-text-muted hover:text-text-secondary'
            )}
          >
            {tab === 'problem' ? 'Problem' : tab === 'starter' ? 'Starter Code' : 'Solution'}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="p-5">
        {activeTab === 'problem' && (
          <div className="space-y-4">
            <p className="text-sm text-text-secondary leading-relaxed">{challenge.description}</p>
            {challenge.context && (
              <div className="bg-bg-secondary rounded-lg p-4 border border-border">
                <p className="text-xs text-text-muted font-medium mb-2 uppercase tracking-wide">Context</p>
                <pre className="text-sm text-text-secondary whitespace-pre-wrap leading-relaxed font-mono text-xs">{challenge.context}</pre>
              </div>
            )}

            {/* Hints */}
            <div>
              <button
                onClick={() => setShowHints(!showHints)}
                className="flex items-center gap-2 text-accent-yellow text-sm hover:text-accent-yellow/80 transition-colors"
              >
                <Lightbulb size={14} />
                {showHints ? 'Hide hints' : `Show hints (${challenge.hints.length})`}
                {showHints ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
              </button>
              {showHints && (
                <ul className="mt-3 space-y-2 ml-2">
                  {challenge.hints.map((hint, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-text-secondary">
                      <span className="text-accent-yellow shrink-0 mt-0.5">→</span>
                      {hint}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}

        {activeTab === 'starter' && (
          <div className="rounded-lg overflow-hidden border border-border">
            <CodeMirror
              value={challenge.starter_code}
              extensions={[python()]}
              theme={oneDark}
              editable={false}
              basicSetup={{ lineNumbers: true, foldGutter: false }}
            />
          </div>
        )}

        {activeTab === 'solution' && (
          <div className="space-y-4">
            {!showSolution ? (
              <button
                onClick={() => setShowSolution(true)}
                className="flex items-center gap-2 text-sm text-text-muted border border-dashed border-border rounded-lg px-4 py-3 w-full justify-center hover:border-accent-blue/40 hover:text-text-secondary transition-colors"
              >
                <Eye size={14} />
                Reveal solution
              </button>
            ) : (
              <>
                <div className="rounded-lg overflow-hidden border border-border">
                  <CodeMirror
                    value={challenge.solution_code}
                    extensions={[python()]}
                    theme={oneDark}
                    editable={false}
                    basicSetup={{ lineNumbers: true, foldGutter: false }}
                  />
                </div>
                {challenge.solution_explanation && (
                  <div className="bg-green-500/5 border border-green-500/20 rounded-lg p-4">
                    <p className="text-xs font-medium text-green-400 mb-2 uppercase tracking-wide">Explanation</p>
                    <p className="text-sm text-text-secondary leading-relaxed">{challenge.solution_explanation}</p>
                  </div>
                )}
                <button
                  onClick={() => setShowSolution(false)}
                  className="flex items-center gap-1.5 text-xs text-text-muted hover:text-text-secondary transition-colors"
                >
                  <EyeOff size={12} /> Hide solution
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default function SecurityChapterPage() {
  const { chapterId } = useParams<{ chapterId: string }>()
  const [chapter, setChapter] = useState<SecurityChapter | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeSection, setActiveSection] = useState<string | null>(null)

  useEffect(() => {
    if (!chapterId) return
    setLoading(true)
    getSecurityChapter(chapterId)
      .then(ch => {
        setChapter(ch)
        if (ch.sections.length > 0) setActiveSection(ch.sections[0].id)
      })
      .finally(() => setLoading(false))
  }, [chapterId])

  if (loading) {
    return (
      <div className="max-w-screen-xl mx-auto px-4 py-10">
        <div className="space-y-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-24 bg-bg-secondary rounded-xl border border-border animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  if (!chapter) {
    return (
      <div className="max-w-screen-xl mx-auto px-4 py-10 text-center">
        <p className="text-text-muted">Chapter not found.</p>
        <Link to="/security" className="text-accent-blue text-sm mt-2 inline-block">← Back to Security</Link>
      </div>
    )
  }

  return (
    <div className="max-w-screen-xl mx-auto px-4 py-8">
      {/* Back nav */}
      <Link
        to="/security"
        className="inline-flex items-center gap-1.5 text-sm text-text-muted hover:text-text-primary mb-6 transition-colors"
      >
        <ArrowLeft size={14} />
        Security Engineering
      </Link>

      <div className="flex gap-8">
        {/* Sidebar TOC */}
        <aside className="hidden lg:block w-56 shrink-0">
          <div className="sticky top-20">
            <p className="text-xs text-text-muted font-medium uppercase tracking-wide mb-3">
              Chapter {chapter.chapter_num}
            </p>
            <nav className="space-y-1">
              {chapter.sections.map(section => (
                <button
                  key={section.id}
                  onClick={() => {
                    setActiveSection(section.id)
                    document.getElementById(`section-${section.id}`)?.scrollIntoView({ behavior: 'smooth' })
                  }}
                  className={clsx(
                    'w-full text-left text-xs px-3 py-2 rounded-lg transition-colors',
                    activeSection === section.id
                      ? 'bg-accent-blue/10 text-accent-blue'
                      : 'text-text-muted hover:text-text-secondary hover:bg-bg-tertiary'
                  )}
                >
                  {section.title}
                </button>
              ))}
              {chapter.challenges.length > 0 && (
                <button
                  onClick={() => document.getElementById('challenges')?.scrollIntoView({ behavior: 'smooth' })}
                  className="w-full text-left text-xs px-3 py-2 rounded-lg text-accent-purple hover:bg-accent-purple/10 transition-colors"
                >
                  Coding Challenges ({chapter.challenges.length})
                </button>
              )}
              {chapter.references.length > 0 && (
                <button
                  onClick={() => document.getElementById('references')?.scrollIntoView({ behavior: 'smooth' })}
                  className="w-full text-left text-xs px-3 py-2 rounded-lg text-text-muted hover:text-text-secondary hover:bg-bg-tertiary transition-colors"
                >
                  References
                </button>
              )}
            </nav>
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 min-w-0">
          {/* Chapter header */}
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs text-text-muted font-medium bg-bg-secondary border border-border px-2 py-0.5 rounded">
                Chapter {chapter.chapter_num}
              </span>
              <span className="flex items-center gap-1 text-xs text-text-muted">
                <Clock size={11} /> {chapter.estimated_minutes} min read
              </span>
            </div>
            <h1 className="text-2xl font-bold text-text-primary mb-1">{chapter.title}</h1>
            <p className="text-text-muted">{chapter.subtitle}</p>
            <p className="text-sm text-text-secondary mt-3 leading-relaxed max-w-2xl">{chapter.description}</p>

            {/* Tags */}
            <div className="flex flex-wrap gap-2 mt-4">
              {chapter.tags.map(tag => (
                <span key={tag} className="text-xs bg-bg-secondary border border-border px-2.5 py-1 rounded-full text-text-muted">
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {/* Sections */}
          <div className="space-y-10">
            {chapter.sections.map(section => (
              <section
                key={section.id}
                id={`section-${section.id}`}
                onMouseEnter={() => setActiveSection(section.id)}
              >
                <h2 className="text-xl font-semibold text-text-primary mb-4 pb-2 border-b border-border">
                  {section.title}
                </h2>
                <SecurityContentRenderer blocks={section.blocks} />
              </section>
            ))}
          </div>

          {/* Challenges */}
          {chapter.challenges.length > 0 && (
            <div id="challenges" className="mt-12">
              <div className="flex items-center gap-2 mb-6">
                <Code2 size={18} className="text-accent-purple" />
                <h2 className="text-xl font-semibold text-text-primary">Coding Challenges</h2>
                <span className="text-xs bg-accent-purple/10 text-accent-purple px-2 py-0.5 rounded font-medium">
                  {chapter.challenges.length}
                </span>
              </div>
              <div className="space-y-6">
                {chapter.challenges.map(challenge => (
                  <ChallengeCard key={challenge.id} challenge={challenge} />
                ))}
              </div>
            </div>
          )}

          {/* References */}
          {chapter.references.length > 0 && (
            <div id="references" className="mt-12 border-t border-border pt-8">
              <div className="flex items-center gap-2 mb-4">
                <BookOpen size={16} className="text-text-muted" />
                <h2 className="text-base font-semibold text-text-primary">References & Further Reading</h2>
              </div>
              <ul className="space-y-2">
                {chapter.references.map((ref, i) => (
                  <li key={i}>
                    <a
                      href={ref.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 text-sm text-accent-blue hover:underline"
                    >
                      <ExternalLink size={12} />
                      {ref.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
