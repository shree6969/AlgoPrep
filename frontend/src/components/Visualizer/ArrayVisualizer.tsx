import { useMemo } from 'react'
import type { VizStep } from '../../types'

interface Props {
  step: VizStep
}

function getBarColor(index: number, highlights: Record<string, any>): string {
  if (highlights.found === index) return '#34d399'     // green - found
  if (highlights.result_idx === index) return '#34d399' // green - result
  if (highlights.left === index) return '#4f9eff'      // blue - left pointer
  if (highlights.right === index) return '#f87171'     // red - right pointer
  if (highlights.mid === index) return '#a78bfa'       // purple - mid
  if (highlights.current === index) return '#fbbf24'   // yellow - current
  if (highlights.moving === index) return '#fb923c'    // orange - moving
  if (highlights.filling === index) return '#38bdf8'   // light blue - filling
  if (highlights.popped === index) return '#f87171'    // red - popped
  if (highlights.active === index) return '#fbbf24'    // yellow

  if (Array.isArray(highlights.water_range) && highlights.water_range.includes(index))
    return '#1d4ed8'
  if (Array.isArray(highlights.window_range) && highlights.window_range.includes(index))
    return '#7c3aed'
  if (Array.isArray(highlights.sorted_half) && highlights.sorted_half.includes(index))
    return '#065f46'
  if (Array.isArray(highlights.stack_indices) && highlights.stack_indices.includes(index))
    return '#92400e'

  return '#2a2d3e'
}

function getLabelColor(index: number, highlights: Record<string, any>): string {
  if (highlights.left === index) return '#4f9eff'
  if (highlights.right === index) return '#f87171'
  if (highlights.mid === index) return '#a78bfa'
  if (highlights.current === index) return '#fbbf24'
  if (highlights.moving === index) return '#fb923c'
  return ''
}

function getPointerLabel(index: number, highlights: Record<string, any>): string {
  const labels: string[] = []
  if (highlights.left === index) labels.push('L')
  if (highlights.right === index) labels.push('R')
  if (highlights.mid === index) labels.push('M')
  if (highlights.current === index) labels.push('i')
  if (highlights.found === index) labels.push('✓')
  return labels.join(',')
}

export default function ArrayVisualizer({ step }: Props) {
  const { data, highlights } = step

  // Normalize data: could be an array or an object with 'nums' / 'dp' / 'height' field
  const arr: number[] = useMemo(() => {
    if (Array.isArray(data)) return data
    if (data && typeof data === 'object') {
      const candidate = data.nums || data.dp || data.height || data.heights
      if (Array.isArray(candidate)) return candidate
    }
    return []
  }, [data])

  if (!arr.length) {
    return (
      <div className="flex items-center justify-center h-full text-text-muted text-sm">
        No array data to visualize
      </div>
    )
  }

  const maxVal = Math.max(...arr.map((v) => Math.abs(v)), 1)
  const BOX_W = Math.max(28, Math.min(52, Math.floor(680 / arr.length) - 4))
  const MAX_H = 160
  const totalWidth = arr.length * (BOX_W + 4) + 8
  const svgH = MAX_H + 80

  // Check if we should render as histogram bars
  const isHistogram = !!(data && typeof data === 'object' && (data.heights || (data.height && highlights.water_range)))

  return (
    <div className="w-full overflow-x-auto p-4">
      <svg width={totalWidth} height={svgH} className="mx-auto">
        {arr.map((val, i) => {
          const x = i * (BOX_W + 4) + 4
          const barColor = getBarColor(i, highlights)
          const labelColor = getLabelColor(i, highlights)
          const pointerLabel = getPointerLabel(i, highlights)

          if (isHistogram) {
            // Histogram bar visualization
            const barH = Math.max(4, (Math.abs(val) / maxVal) * MAX_H)
            const y = MAX_H - barH + 10

            return (
              <g key={i}>
                <rect
                  x={x}
                  y={y}
                  width={BOX_W}
                  height={barH}
                  rx={3}
                  fill={barColor}
                  stroke="#3a3f5c"
                  strokeWidth={1}
                  style={{ transition: 'fill 0.3s ease' }}
                />
                <text
                  x={x + BOX_W / 2}
                  y={y - 4}
                  textAnchor="middle"
                  fontSize={10}
                  fill={labelColor || '#94a3b8'}
                >
                  {val}
                </text>
                {pointerLabel && (
                  <text
                    x={x + BOX_W / 2}
                    y={MAX_H + 30}
                    textAnchor="middle"
                    fontSize={11}
                    fontWeight="bold"
                    fill={labelColor || '#4f9eff'}
                  >
                    {pointerLabel}
                  </text>
                )}
                {/* Index */}
                <text
                  x={x + BOX_W / 2}
                  y={MAX_H + 50}
                  textAnchor="middle"
                  fontSize={9}
                  fill="#4a5568"
                >
                  {i}
                </text>
              </g>
            )
          }

          // Box visualization
          const BOX_H = 36
          const y = MAX_H / 2

          return (
            <g key={i}>
              <rect
                x={x}
                y={y}
                width={BOX_W}
                height={BOX_H}
                rx={4}
                fill={barColor}
                stroke="#3a3f5c"
                strokeWidth={barColor !== '#2a2d3e' ? 1.5 : 1}
                style={{ transition: 'fill 0.3s ease' }}
              />
              <text
                x={x + BOX_W / 2}
                y={y + BOX_H / 2 + 5}
                textAnchor="middle"
                fontSize={Math.min(13, BOX_W - 6)}
                fontWeight="500"
                fill={barColor !== '#2a2d3e' ? '#fff' : '#94a3b8'}
                fontFamily="monospace"
              >
                {val}
              </text>
              {/* Index */}
              <text
                x={x + BOX_W / 2}
                y={y + BOX_H + 14}
                textAnchor="middle"
                fontSize={9}
                fill="#4a5568"
              >
                {i}
              </text>
              {/* Pointer label above */}
              {pointerLabel && (
                <text
                  x={x + BOX_W / 2}
                  y={y - 8}
                  textAnchor="middle"
                  fontSize={11}
                  fontWeight="bold"
                  fill={labelColor || '#4f9eff'}
                >
                  {pointerLabel}
                </text>
              )}
            </g>
          )
        })}
      </svg>

      {/* State info */}
      {Object.keys(step.state).length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {Object.entries(step.state)
            .filter(([k]) => !['dp', 'window_counts', 'done', 'action'].includes(k))
            .slice(0, 6)
            .map(([k, v]) => (
              <div key={k} className="text-xs bg-bg-tertiary rounded px-2 py-1 border border-border">
                <span className="text-text-muted">{k}: </span>
                <span className="text-text-primary font-mono">{JSON.stringify(v)}</span>
              </div>
            ))}
        </div>
      )}
    </div>
  )
}
