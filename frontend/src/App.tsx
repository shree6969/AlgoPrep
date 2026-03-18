import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import ProblemsPage from './pages/ProblemsPage'
import ProblemPage from './pages/ProblemPage'
import PatternsPage from './pages/PatternsPage'
import SecurityPage from './pages/SecurityPage'
import SecurityChapterPage from './pages/SecurityChapterPage'

export default function App() {
  return (
    <div className="min-h-screen bg-bg-primary text-text-primary">
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="problems" element={<ProblemsPage />} />
          <Route path="problems/:id" element={<ProblemPage />} />
          <Route path="patterns" element={<PatternsPage />} />
          <Route path="security" element={<SecurityPage />} />
          <Route path="security/:chapterId" element={<SecurityChapterPage />} />
        </Route>
      </Routes>
    </div>
  )
}
