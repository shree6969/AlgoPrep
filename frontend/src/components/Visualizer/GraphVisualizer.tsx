import type { VizStep } from '../../types'

interface Props {
  step: VizStep
}

export default function GraphVisualizer({ step }: Props) {
  // Simple placeholder for graph visualization
  // For a full implementation, D3 force layout would be used
  const { data } = step

  return (
    <div className="flex flex-col items-center justify-center h-full p-6 text-center">
      <div className="text-5xl mb-4">⊕</div>
      <h3 className="text-text-primary font-semibold mb-2">Graph Visualization</h3>
      <p className="text-text-muted text-sm max-w-xs">
        {step.description || 'Graph algorithm running...'}
      </p>

      {/* State info */}
      {Object.keys(step.state).length > 0 && (
        <div className="mt-4 flex flex-wrap gap-2 justify-center max-w-md">
          {Object.entries(step.state)
            .filter(([k]) => !['done'].includes(k))
            .slice(0, 6)
            .map(([k, v]) => (
              <div key={k} className="text-xs bg-bg-tertiary rounded px-2 py-1 border border-border">
                <span className="text-text-muted">{k}: </span>
                <span className="text-text-primary font-mono">
                  {typeof v === 'object' ? JSON.stringify(v) : String(v)}
                </span>
              </div>
            ))}
        </div>
      )}

      {data && (
        <div className="mt-4 text-xs text-text-muted font-mono bg-bg-tertiary p-3 rounded-lg border border-border max-w-sm w-full text-left">
          <div className="text-text-secondary mb-1 font-sans">Step data:</div>
          <pre className="whitespace-pre-wrap break-all text-xs">
            {JSON.stringify(data, null, 2).slice(0, 300)}
          </pre>
        </div>
      )}
    </div>
  )
}
