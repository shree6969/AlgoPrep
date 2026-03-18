import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Shield, Clock, BookOpen, Code2, ChevronRight, Lock, Server, Eye } from 'lucide-react'
import { getSecurityChapters } from '../api'
import type { SecurityChapterListItem } from '../types'

const TAG_COLORS: Record<string, string> = {
  foundations:       'bg-accent-purple/10 text-accent-purple',
  'threat-modeling': 'bg-red-500/10 text-red-400',
  'zero-trust':      'bg-accent-blue/10 text-accent-blue',
  'workload-identity':'bg-green-500/10 text-green-400',
  'aws-agentcore':   'bg-accent-yellow/10 text-accent-yellow',
  iam:               'bg-orange-500/10 text-orange-400',
  credentials:       'bg-pink-500/10 text-pink-400',
  'mcp-gateway':     'bg-accent-blue/10 text-accent-blue',
  pat:               'bg-purple-400/10 text-purple-400',
  oauth2:            'bg-green-500/10 text-green-400',
  oidc:              'bg-cyan-500/10 text-cyan-400',
  jwt:               'bg-accent-yellow/10 text-accent-yellow',
  authorization:     'bg-red-500/10 text-red-400',
  observability:     'bg-teal-500/10 text-teal-400',
  'audit-logging':   'bg-orange-500/10 text-orange-400',
}

const CHAPTER_ICONS = [Shield, Lock, Server, Code2, Eye, BookOpen]

export default function SecurityPage() {
  const [chapters, setChapters] = useState<SecurityChapterListItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getSecurityChapters()
      .then(setChapters)
      .finally(() => setLoading(false))
  }, [])

  const totalMinutes = chapters.reduce((s, c) => s + c.estimated_minutes, 0)
  const totalChallenges = chapters.reduce((s, c) => s + c.challenge_count, 0)

  return (
    <div className="max-w-screen-xl mx-auto px-4 py-10">
      {/* Header */}
      <div className="mb-10">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-red-500 to-accent-purple flex items-center justify-center">
            <Shield size={20} className="text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-text-primary">Security Engineering</h1>
            <p className="text-text-muted text-sm">Enterprise Agentic Platforms on Public Clouds</p>
          </div>
        </div>
        <p className="text-text-secondary max-w-2xl text-sm leading-relaxed mt-4">
          A comprehensive guide to securing enterprise AI agent platforms on AWS — covering workload
          identities, MCP Gateway authentication, OAuth 2.0/OIDC token flows, Okta Cross-App Access,
          multi-layer authorization, and observability. Includes architecture deep-dives, production
          code patterns, and hands-on coding challenges.
        </p>

        {/* Stats row */}
        {!loading && (
          <div className="flex items-center gap-6 mt-6">
            <div className="flex items-center gap-2 text-sm text-text-secondary">
              <BookOpen size={14} className="text-accent-blue" />
              <span>{chapters.length} chapters</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-text-secondary">
              <Clock size={14} className="text-accent-yellow" />
              <span>~{Math.round(totalMinutes / 60)}h {totalMinutes % 60}m total</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-text-secondary">
              <Code2 size={14} className="text-accent-purple" />
              <span>{totalChallenges} coding challenges</span>
            </div>
          </div>
        )}
      </div>

      {/* Chapter grid */}
      {loading ? (
        <div className="grid gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-32 bg-bg-secondary rounded-xl border border-border animate-pulse" />
          ))}
        </div>
      ) : (
        <div className="grid gap-4">
          {chapters.map((chapter, idx) => {
            const Icon = CHAPTER_ICONS[idx % CHAPTER_ICONS.length]
            return (
              <Link
                key={chapter.id}
                to={`/security/${chapter.id}`}
                className="group bg-bg-secondary border border-border rounded-xl p-5 hover:border-accent-blue/40 hover:bg-bg-secondary/80 transition-all"
              >
                <div className="flex items-start gap-4">
                  {/* Chapter number + icon */}
                  <div className="shrink-0 w-12 h-12 rounded-lg bg-gradient-to-br from-red-500/20 to-accent-purple/20 border border-red-500/20 flex flex-col items-center justify-center">
                    <Icon size={14} className="text-red-400 mb-0.5" />
                    <span className="text-xs font-bold text-text-muted">{String(chapter.chapter_num).padStart(2, '0')}</span>
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h2 className="font-semibold text-text-primary group-hover:text-accent-blue transition-colors">
                          {chapter.title}
                        </h2>
                        <p className="text-sm text-text-muted mt-0.5">{chapter.subtitle}</p>
                      </div>
                      <ChevronRight size={16} className="text-text-muted group-hover:text-accent-blue shrink-0 mt-1 transition-colors" />
                    </div>

                    <p className="text-sm text-text-secondary mt-2 leading-relaxed line-clamp-2">
                      {chapter.description}
                    </p>

                    <div className="flex items-center gap-4 mt-3">
                      {/* Tags */}
                      <div className="flex flex-wrap gap-1.5">
                        {chapter.tags.slice(0, 4).map(tag => (
                          <span
                            key={tag}
                            className={`text-xs px-2 py-0.5 rounded font-medium ${TAG_COLORS[tag] ?? 'bg-bg-tertiary text-text-muted'}`}
                          >
                            {tag}
                          </span>
                        ))}
                      </div>

                      {/* Meta */}
                      <div className="ml-auto flex items-center gap-3 shrink-0">
                        <span className="text-xs text-text-muted flex items-center gap-1">
                          <BookOpen size={11} />
                          {chapter.section_count} sections
                        </span>
                        <span className="text-xs text-text-muted flex items-center gap-1">
                          <Code2 size={11} />
                          {chapter.challenge_count} challenge{chapter.challenge_count !== 1 ? 's' : ''}
                        </span>
                        <span className="text-xs text-text-muted flex items-center gap-1">
                          <Clock size={11} />
                          {chapter.estimated_minutes}m
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </Link>
            )
          })}
        </div>
      )}
    </div>
  )
}
