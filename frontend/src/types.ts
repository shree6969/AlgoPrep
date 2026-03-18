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

// Security Engineering Module

export interface SecurityCodeSnippet {
  language: string
  title: string
  content: string
}

export interface SecurityBlock {
  type: 'paragraph' | 'heading' | 'code' | 'bullets' | 'callout' | 'diagram'
  content?: string
  level?: number
  items?: string[]
  kind?: 'info' | 'warning' | 'danger' | 'success'
  title?: string
  language?: string
}

export interface SecuritySection {
  id: string
  title: string
  blocks: SecurityBlock[]
}

export interface SecurityChallenge {
  id: string
  title: string
  difficulty: Difficulty
  description: string
  context: string
  starter_code: string
  solution_code: string
  solution_explanation: string
  hints: string[]
}

export interface SecurityReference {
  title: string
  url: string
}

export interface SecurityChapter {
  id: string
  chapter_num: number
  title: string
  subtitle: string
  description: string
  tags: string[]
  estimated_minutes: number
  sections: SecuritySection[]
  challenges: SecurityChallenge[]
  references: SecurityReference[]
}

export interface SecurityChapterListItem {
  id: string
  chapter_num: number
  title: string
  subtitle: string
  description: string
  tags: string[]
  estimated_minutes: number
  section_count: number
  challenge_count: number
}
