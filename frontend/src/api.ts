import axios from 'axios'
import type { Problem, ProblemListItem, ExecutionResult, PatternInfo, CompanyInfo, SecurityChapter, SecurityChapterListItem } from './types'

const api = axios.create({ baseURL: '/api' })

export interface GetProblemsParams {
  pattern?: string
  difficulty?: string
  company?: string
  search?: string
  skip?: number
  limit?: number
}

export const getProblems = (params?: GetProblemsParams) =>
  api.get<ProblemListItem[]>('/problems', { params }).then((r) => r.data)

export const getProblem = (id: string) =>
  api.get<Problem>(`/problems/${id}`).then((r) => r.data)

export const getSolution = (id: string) =>
  api.get<{ id: string; solution_code: string }>(`/problems/${id}/solution`).then((r) => r.data)

export const executeProblem = (id: string, input: Record<string, any>) =>
  api.post<ExecutionResult>(`/problems/${id}/execute`, { input }).then((r) => r.data)

export const getPatterns = () =>
  api.get<PatternInfo[]>('/patterns').then((r) => r.data)

export const getCompanies = () =>
  api.get<CompanyInfo[]>('/companies').then((r) => r.data)

export const getSecurityChapters = () =>
  api.get<SecurityChapterListItem[]>('/security/chapters').then((r) => r.data)

export const getSecurityChapter = (id: string) =>
  api.get<SecurityChapter>(`/security/chapters/${id}`).then((r) => r.data)
