import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getProblem, getSolution, executeProblem } from '../api'
import type { Problem, ExecutionResult, VizStep } from '../types'
import DifficultyBadge from '../components/DifficultyBadge'
import PatternBadge from '../components/PatternBadge'
import CodeEditor from '../components/CodeEditor'
import Visualizer from '../components/Visualizer'
import {
  ChevronLeft,
  ChevronDown,
  ChevronUp,
  Eye,
  EyeOff,
  Play,
  Lightbulb,
  Clock,
  MemoryStick,
  Building2,
  AlertCircle,
} from 'lucide-react'
import clsx from 'clsx'

const companyColors: Record<string, string> = {
  google: 'bg-blue-500/20 text-blue-300 border-blue-500/20',
  meta: 'bg-blue-700/20 text-blue-400 border-blue-700/20',
  amazon: 'bg-orange-500/20 text-orange-300 border-orange-500/20',
  apple: 'bg-gray-500/20 text-gray-300 border-gray-500/20',
  microsoft: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/20',
  anthropic: 'bg-purple-500/20 text-purple-300 border-purple-500/20',
  openai: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/20',
  netflix: 'bg-red-600/20 text-red-300 border-red-600/20',
  uber: 'bg-gray-600/20 text-gray-300 border-gray-600/20',
  airbnb: 'bg-pink-500/20 text-pink-300 border-pink-500/20',
  linkedin: 'bg-blue-600/20 text-blue-300 border-blue-600/20',
}

// Default inputs per problem
const DEFAULT_INPUTS: Record<string, Record<string, any>> = {
  'container-with-most-water': { height: [1, 8, 6, 2, 5, 4, 8, 3, 7] },
  'trapping-rain-water': { height: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1] },
  'minimum-window-substring': { s: 'ADOBECODEBANC', t: 'ABC' },
  'search-in-rotated-sorted-array': { nums: [4, 5, 6, 7, 0, 1, 2], target: 0 },
  'longest-increasing-subsequence': { nums: [10, 9, 2, 5, 3, 7, 101, 18] },
  'coin-change': { coins: [1, 2, 5], amount: 11 },
  'edit-distance': { word1: 'horse', word2: 'ros' },
  'largest-rectangle-in-histogram': { heights: [2, 1, 5, 6, 2, 3] },
  'merge-intervals': { intervals: [[1, 3], [2, 6], [8, 10], [15, 18]] },
  'n-queens': { n: 4 },
  'unique-paths': { m: 3, n: 7 },
}

function renderDescription(text: string) {
  // Simple markdown-like renderer
  return text.split('\n\n').map((para, i) => {
    if (para.startsWith('**') && para.endsWith('**')) {
      return (
        <p key={i} className="font-semibold text-text-primary mb-2">
          {para.slice(2, -2)}
        </p>
      )
    }
    const rendered = para
      .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong class="text-text-primary">$1</strong>')
      .replace(/\n/g, '<br/>')

    return (
      <p
        key={i}
        className="text-text-secondary text-sm leading-relaxed mb-3"
        dangerouslySetInnerHTML={{ __html: rendered }}
      />
    )
  })
}

export default function ProblemPage() {
  const { id } = useParams<{ id: string }>()
  const [problem, setProblem] = useState<Problem | null>(null)
  const [loading, setLoading] = useState(true)
  const [showSolution, setShowSolution] = useState(false)
  const [solutionCode, setSolutionCode] = useState('')
  const [userCode, setUserCode] = useState('# Write your solution here\n')
  const [showHints, setShowHints] = useState(false)
  const [executing, setExecuting] = useState(false)
  const [executionResult, setExecutionResult] = useState<ExecutionResult | null>(null)
  const [executionError, setExecutionError] = useState('')
  const [inputJson, setInputJson] = useState('')
  const [steps, setSteps] = useState<VizStep[]>([])
  const [descExpanded, setDescExpanded] = useState(true)
  const [examplesExpanded, setExamplesExpanded] = useState(true)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    setExecutionResult(null)
    setSteps([])
    setShowSolution(false)

    getProblem(id)
      .then((p) => {
        setProblem(p)
        setInputJson(JSON.stringify(DEFAULT_INPUTS[id] || {}, null, 2))
        setUserCode(`# ${p.title}\n# Pattern: ${p.pattern}\n# Time: ${p.time_complexity} | Space: ${p.space_complexity}\n\ndef solution():\n    pass\n`)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [id])

  const handleShowSolution = async () => {
    if (!id) return
    if (!solutionCode) {
      const data = await getSolution(id)
      setSolutionCode(data.solution_code)
    }
    setShowSolution(!showSolution)
  }

  const handleRun = async () => {
    if (!id) return
    setExecuting(true)
    setExecutionError('')
    try {
      let input: Record<string, any> = {}
      try {
        input = JSON.parse(inputJson)
      } catch {
        setExecutionError('Invalid JSON input')
        return
      }
      const result = await executeProblem(id, input)
      setExecutionResult(result)
      setSteps(result.steps)
    } catch (e: any) {
      setExecutionError(e?.response?.data?.detail || 'Execution failed')
    } finally {
      setExecuting(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-3.5rem)]">
        <div className="animate-spin w-8 h-8 border-2 border-accent-blue border-t-transparent rounded-full" />
      </div>
    )
  }

  if (!problem) {
    return (
      <div className="flex flex-col items-center justify-center h-[calc(100vh-3.5rem)] text-text-muted">
        <div className="text-4xl mb-3">404</div>
        <p className="text-text-secondary mb-4">Problem not found</p>
        <Link to="/problems" className="btn btn-primary">Back to Problems</Link>
      </div>
    )
  }

  return (
    <div className="h-[calc(100vh-3.5rem)] flex overflow-hidden">
      {/* LEFT PANEL: Problem description */}
      <div className="w-[38%] min-w-[320px] flex flex-col border-r border-border overflow-hidden">
        {/* Problem header */}
        <div className="flex-shrink-0 p-4 border-b border-border bg-bg-secondary">
          <Link
            to="/problems"
            className="inline-flex items-center gap-1 text-text-muted text-xs hover:text-text-secondary mb-3 transition-colors"
          >
            <ChevronLeft size={14} /> Problems
          </Link>
          <h1 className="text-xl font-bold text-text-primary mb-2">{problem.title}</h1>
          <div className="flex items-center flex-wrap gap-2">
            <DifficultyBadge difficulty={problem.difficulty} size="md" />
            <PatternBadge pattern={problem.pattern} size="md" />
          </div>
          {/* Complexity */}
          <div className="flex items-center gap-4 mt-3 text-xs text-text-muted">
            <span className="flex items-center gap-1">
              <Clock size={11} /> {problem.time_complexity}
            </span>
            <span className="flex items-center gap-1">
              <MemoryStick size={11} /> {problem.space_complexity}
            </span>
          </div>
          {/* Companies */}
          <div className="flex items-center flex-wrap gap-1.5 mt-3">
            <Building2 size={12} className="text-text-muted" />
            {problem.companies.map((c) => (
              <span
                key={c}
                className={clsx(
                  'text-xs px-2 py-0.5 rounded-full border capitalize font-medium',
                  companyColors[c] || 'bg-bg-tertiary text-text-muted border-border'
                )}
              >
                {c}
              </span>
            ))}
          </div>
        </div>

        {/* Scrollable content */}
        <div className="flex-1 overflow-y-auto">
          {/* Description */}
          <div className="border-b border-border">
            <button
              onClick={() => setDescExpanded(!descExpanded)}
              className="w-full flex items-center justify-between px-4 py-3 text-sm font-semibold text-text-primary hover:bg-bg-tertiary/40 transition-colors"
            >
              Description
              {descExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>
            {descExpanded && (
              <div className="px-4 pb-4 prose-dark">
                <style>{`.inline-code { background: #22263a; color: #4f9eff; padding: 0.1em 0.3em; border-radius: 3px; font-family: monospace; font-size: 0.85em; }`}</style>
                {renderDescription(problem.description)}
              </div>
            )}
          </div>

          {/* Examples */}
          <div className="border-b border-border">
            <button
              onClick={() => setExamplesExpanded(!examplesExpanded)}
              className="w-full flex items-center justify-between px-4 py-3 text-sm font-semibold text-text-primary hover:bg-bg-tertiary/40 transition-colors"
            >
              Examples
              {examplesExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>
            {examplesExpanded && (
              <div className="px-4 pb-4 space-y-3">
                {problem.examples.map((ex, i) => (
                  <div key={i} className="bg-bg-tertiary rounded-lg p-3 border border-border">
                    <div className="text-xs text-text-muted mb-1 font-semibold">Example {i + 1}</div>
                    <div className="font-mono text-xs space-y-1">
                      <div>
                        <span className="text-text-muted">Input: </span>
                        <span className="text-text-primary">{ex.input}</span>
                      </div>
                      <div>
                        <span className="text-text-muted">Output: </span>
                        <span className="text-accent-green">{ex.output}</span>
                      </div>
                      {ex.explanation && (
                        <div className="text-text-muted text-xs mt-1 pt-1 border-t border-border leading-relaxed">
                          {ex.explanation}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Constraints */}
          <div className="border-b border-border px-4 py-3">
            <h3 className="text-sm font-semibold text-text-primary mb-2">Constraints</h3>
            <ul className="space-y-1">
              {problem.constraints.map((c, i) => (
                <li key={i} className="text-xs text-text-muted font-mono flex items-start gap-1.5">
                  <span className="text-accent-blue mt-0.5">•</span>
                  {c}
                </li>
              ))}
            </ul>
          </div>

          {/* Hints */}
          <div className="px-4 py-3">
            <button
              onClick={() => setShowHints(!showHints)}
              className="flex items-center gap-2 text-sm text-text-secondary hover:text-text-primary transition-colors"
            >
              <Lightbulb size={14} className="text-accent-yellow" />
              {showHints ? 'Hide Hints' : `Show Hints (${problem.hints.length})`}
            </button>
            {showHints && (
              <div className="mt-3 space-y-2">
                {problem.hints.map((h, i) => (
                  <div
                    key={i}
                    className="text-xs text-text-secondary bg-accent-yellow/5 border border-accent-yellow/20 rounded-lg p-2.5"
                  >
                    <span className="text-accent-yellow font-medium">Hint {i + 1}: </span>
                    {h}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* MIDDLE PANEL: Code editor + input */}
      <div className="w-[32%] min-w-[280px] flex flex-col border-r border-border overflow-hidden bg-bg-primary">
        {/* Editor toolbar */}
        <div className="flex-shrink-0 flex items-center justify-between px-3 py-2 bg-bg-secondary border-b border-border">
          <span className="text-xs font-medium text-text-secondary">
            {showSolution ? 'Solution' : 'Your Code'} — Python
          </span>
          <button
            onClick={handleShowSolution}
            className="btn btn-ghost btn-sm gap-1.5 text-xs"
          >
            {showSolution ? <EyeOff size={13} /> : <Eye size={13} />}
            {showSolution ? 'Hide Solution' : 'Show Solution'}
          </button>
        </div>

        {/* Code editor */}
        <div className="flex-1 overflow-hidden min-h-0">
          <CodeEditor
            value={showSolution ? solutionCode : userCode}
            onChange={showSolution ? undefined : setUserCode}
            readOnly={showSolution}
            height="100%"
          />
        </div>

        {/* Input section */}
        <div className="flex-shrink-0 border-t border-border bg-bg-secondary">
          <div className="px-3 pt-3 pb-1">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-medium text-text-secondary">Test Input (JSON)</span>
              {executionResult && (
                <span className={clsx(
                  'text-xs px-2 py-0.5 rounded border',
                  executionResult.passed
                    ? 'text-accent-green bg-accent-green/10 border-accent-green/20'
                    : 'text-accent-red bg-accent-red/10 border-accent-red/20'
                )}>
                  {executionResult.passed ? '✓ Passed' : '✗ Failed'} · {executionResult.runtime_ms.toFixed(1)}ms
                </span>
              )}
            </div>
            <textarea
              value={inputJson}
              onChange={(e) => setInputJson(e.target.value)}
              rows={4}
              className="w-full input text-xs font-mono resize-none leading-relaxed"
              placeholder='{"nums": [1, 2, 3]}'
            />
          </div>

          {executionError && (
            <div className="px-3 pb-2 flex items-start gap-1.5 text-xs text-accent-red">
              <AlertCircle size={12} className="mt-0.5 flex-shrink-0" />
              {executionError}
            </div>
          )}

          {executionResult && (
            <div className="px-3 pb-2">
              <div className="text-xs bg-bg-tertiary rounded p-2 border border-border font-mono">
                <span className="text-text-muted">Output: </span>
                <span className="text-accent-green">{executionResult.output}</span>
              </div>
            </div>
          )}

          <div className="px-3 pb-3">
            <button
              onClick={handleRun}
              disabled={executing}
              className="btn btn-primary w-full gap-2 text-sm"
            >
              {executing ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Running...
                </>
              ) : (
                <>
                  <Play size={14} />
                  Run Visualization
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* RIGHT PANEL: Visualization */}
      <div className="flex-1 flex flex-col overflow-hidden bg-bg-primary min-w-[280px]">
        {/* Viz header */}
        <div className="flex-shrink-0 px-4 py-2.5 bg-bg-secondary border-b border-border flex items-center justify-between">
          <span className="text-xs font-medium text-text-secondary">
            Visualization
            {problem.viz_type !== 'none' && (
              <span className="ml-2 text-text-muted">· {problem.viz_type}</span>
            )}
          </span>
          {steps.length > 0 && (
            <span className="text-xs text-text-muted">{steps.length} steps</span>
          )}
        </div>

        {/* Visualizer */}
        <div className="flex-1 overflow-hidden min-h-0">
          <Visualizer steps={steps} vizType={problem.viz_type} />
        </div>
      </div>
    </div>
  )
}
