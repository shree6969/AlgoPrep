import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import ProblemsPage from './pages/ProblemsPage'
import ProblemPage from './pages/ProblemPage'
import PatternsPage from './pages/PatternsPage'

export default function App() {
  return (
    <div className="min-h-screen bg-bg-primary text-text-primary">
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="problems" element={<ProblemsPage />} />
          <Route path="problems/:id" element={<ProblemPage />} />
          <Route path="patterns" element={<PatternsPage />} />
        </Route>
      </Routes>
    </div>
  )
}
