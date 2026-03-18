export type Difficulty = 'Easy' | 'Medium' | 'Hard'
export type VizType = 'array' | 'tree' | 'graph' | 'grid' | 'none'
export type Pattern = string

export interface Example {
  input: string
  output: string
  explanation?: string
}

export interface Problem {
  id: string
  title: string
  difficulty: Difficulty
  pattern: Pattern
  companies: string[]
  description: string
  examples: Example[]
  constraints: string[]
  hints: string[]
  solution_code: string
  time_complexity: string
  space_complexity: string
  viz_type: VizType
}

export interface ProblemListItem {
  id: string
  title: string
  difficulty: Difficulty
  pattern: Pattern
  companies: string[]
  viz_type: VizType
  solved?: boolean
}

export interface VizStep {
  step_num: number
  description: string
  data: any
  highlights: Record<string, any>
  state: Record<string, any>
}

export interface ExecutionResult {
  steps: VizStep[]
  output: string
  passed: boolean
  runtime_ms: number
}

export interface PatternInfo {
  name: string
  count: number
  description: string
}

export interface CompanyInfo {
  name: string
  count: number
}
