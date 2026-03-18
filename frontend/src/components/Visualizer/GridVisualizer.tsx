import type { VizStep } from '../../types'

interface Props {
  step: VizStep
}

function getCellStyle(val: any, row: number, col: number, highlights: Record<string, any>): string {
  const isResult =
    (highlights.result && Array.isArray(highlights.result) &&
      highlights.result[0] === row && highlights.result[1] === col)
  const isCurrent =
    highlights.current_row === row && highlights.current_col === col
  const isTop =
    highlights.top && highlights.top[0] === row && highlights.top[1] === col
  const isLeft =
    highlights.left && highlights.left[0] === row && highlights.left[1] === col
  const isDiag =
    highlights.diag && highlights.diag[0] === row && highlights.diag[1] === col
  const isBase = highlights.base === col && row === 0
  const isCurrentCol = highlights.current === col && !Array.isArray(highlights.current)
  const isSourceCol = highlights.source === col

  if (isResult) return 'bg-accent-green/30 border-accent-green text-accent-green font-bold'
  if (isCurrent) return 'bg-accent-yellow/30 border-accent-yellow text-accent-yellow font-bold'
  if (isTop) return 'bg-accent-blue/20 border-accent-blue/60 text-accent-blue'
  if (isLeft) return 'bg-accent-purple/20 border-accent-purple/60 text-accent-purple'
  if (isDiag) return 'bg-orange-400/20 border-orange-400/60 text-orange-300'
  if (isBase) return 'bg-accent-green/20 border-accent-green/40 text-accent-green'
  if (isCurrentCol) return 'bg-accent-yellow/20 border-accent-yellow/40 text-accent-yellow'
  if (isSourceCol) return 'bg-cyan-400/20 border-cyan-400/40 text-cyan-300'

  if (val === 0) return 'bg-bg-primary/60 border-border text-text-muted'
  if (val === -1) return 'bg-bg-primary/60 border-border text-text-muted'
  if (val === null || val === undefined) return 'bg-bg-primary/60 border-border text-text-muted'

  return 'bg-bg-tertiary border-border text-text-primary'
}

export default function GridVisualizer({ step }: Props) {
  const { data, highlights } = step

  // Extract the 2D grid
  let grid: any[][] | null = null
  let word1 = ''
  let word2 = ''
  let coins: number[] = []

  if (Array.isArray(data)) {
    if (Array.isArray(data[0])) {
      grid = data as any[][]
    } else {
      // 1D dp array — render as single row
      grid = [data]
    }
  } else if (data && typeof data === 'object') {
    if (data.dp) {
      if (Array.isArray(data.dp[0])) {
        grid = data.dp
        word1 = data.word1 || ''
        word2 = data.word2 || ''
      } else {
        grid = [data.dp]
        coins = data.coins || []
      }
    } else if (data.board) {
      grid = data.board
    }
  }

  if (!grid) {
    return (
      <div className="flex items-center justify-center h-full text-text-muted text-sm">
        No grid data to visualize
      </div>
    )
  }

  const rows = grid.length
  const cols = grid[0]?.length || 0

  if (rows === 0 || cols === 0) {
    return (
      <div className="flex items-center justify-center h-full text-text-muted text-sm">
        Empty grid
      </div>
    )
  }

  // Determine cell size
  const maxDim = Math.max(rows, cols)
  const CELL_SIZE = maxDim <= 8 ? 44 : maxDim <= 12 ? 34 : 26

  const isBoard = data?.board !== undefined
  // N-queens board rendering
  if (isBoard) {
    const n = data.n || rows
    return (
      <div className="p-4 overflow-auto">
        <div className="inline-block">
          {grid.map((row, r) => (
            <div key={r} className="flex">
              {(Array.isArray(row) ? row : []).map((cell: any, c: number) => {
                const isLight = (r + c) % 2 === 0
                const isConflict =
                  highlights.conflict &&
                  highlights.conflict[0] === r &&
                  highlights.conflict[1] === c
                const isPlaced =
                  (highlights.placed &&
                    highlights.placed[0] === r &&
                    highlights.placed[1] === c) ||
                  cell === 1
                const isRemoved =
                  highlights.removed &&
                  highlights.removed[0] === r &&
                  highlights.removed[1] === c

                return (
                  <div
                    key={c}
                    style={{ width: CELL_SIZE, height: CELL_SIZE }}
                    className={`flex items-center justify-center text-lg border border-border/30 transition-colors duration-200 ${
                      isConflict
                        ? 'bg-red-900/40'
                        : isRemoved
                        ? 'bg-orange-900/30'
                        : isPlaced
                        ? isLight
                          ? 'bg-accent-green/20'
                          : 'bg-accent-green/30'
                        : isLight
                        ? 'bg-bg-tertiary/40'
                        : 'bg-bg-secondary'
                    }`}
                  >
                    {cell === 1 ? '♛' : cell === 0 ? '✗' : ''}
                  </div>
                )
              })}
            </div>
          ))}
        </div>
        {/* State info */}
        <div className="mt-3 flex flex-wrap gap-2">
          {step.state.solutions !== undefined && (
            <div className="text-xs bg-bg-tertiary rounded px-2 py-1 border border-border">
              <span className="text-text-muted">Solutions found: </span>
              <span className="text-accent-green font-mono">{step.state.solutions}</span>
            </div>
          )}
          {step.state.action && (
            <div className="text-xs bg-bg-tertiary rounded px-2 py-1 border border-border">
              <span className="text-text-muted">Action: </span>
              <span className="text-accent-yellow font-mono">{step.state.action}</span>
            </div>
          )}
        </div>
      </div>
    )
  }

  // DP table rendering
  const hasColHeaders = word2.length > 0
  const hasRowHeaders = word1.length > 0
  const is1D = rows === 1

  return (
    <div className="p-4 overflow-auto">
      {/* Column headers (word2) */}
      {hasColHeaders && (
        <div className="flex mb-1" style={{ paddingLeft: hasRowHeaders ? CELL_SIZE + 4 : 0 }}>
          <div style={{ width: CELL_SIZE }} />
          {word2.split('').map((ch, j) => (
            <div
              key={j}
              style={{ width: CELL_SIZE }}
              className="text-center text-xs text-accent-blue font-mono font-semibold"
            >
              {ch}
            </div>
          ))}
        </div>
      )}

      {grid.map((row, r) => (
        <div key={r} className="flex items-center mb-0.5">
          {/* Row header (word1) */}
          {hasRowHeaders && (
            <div
              style={{ width: CELL_SIZE }}
              className="text-center text-xs text-accent-purple font-mono font-semibold mr-1"
            >
              {r > 0 ? word1[r - 1] : ''}
            </div>
          )}

          {/* Cells */}
          {(Array.isArray(row) ? row : [row]).map((cell: any, c: number) => {
            const displayVal = cell === null || cell === undefined ? '' : String(cell)
            const cellClass = getCellStyle(cell, r, c, highlights)

            return (
              <div
                key={c}
                style={{ width: CELL_SIZE, height: CELL_SIZE }}
                className={`flex items-center justify-center text-xs font-mono border rounded transition-all duration-200 mx-px ${cellClass}`}
                title={`[${r}][${c}] = ${displayVal}`}
              >
                {displayVal === '-1' ? '∞' : displayVal}
              </div>
            )
          })}
        </div>
      ))}

      {/* 1D dp: show coins legend */}
      {is1D && coins.length > 0 && (
        <div className="mt-3 flex items-center gap-2">
          <span className="text-xs text-text-muted">Coins:</span>
          {coins.map((c, i) => (
            <span key={i} className="text-xs bg-bg-tertiary border border-border px-2 py-0.5 rounded font-mono">
              {c}
            </span>
          ))}
        </div>
      )}

      {/* Legend */}
      <div className="mt-3 flex flex-wrap gap-2 text-xs">
        {highlights.current_row !== undefined && (
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded bg-accent-yellow/30 border border-accent-yellow" />
            <span className="text-text-muted">Current cell</span>
          </div>
        )}
        {highlights.top && (
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded bg-accent-blue/20 border border-accent-blue/60" />
            <span className="text-text-muted">Top (dp[i-1][j])</span>
          </div>
        )}
        {highlights.left && (
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded bg-accent-purple/20 border border-accent-purple/60" />
            <span className="text-text-muted">Left (dp[i][j-1])</span>
          </div>
        )}
        {highlights.diag && (
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded bg-orange-400/20 border border-orange-400/60" />
            <span className="text-text-muted">Diag (dp[i-1][j-1])</span>
          </div>
        )}
      </div>

      {/* State info */}
      {Object.keys(step.state).length > 0 && (
        <div className="mt-2 flex flex-wrap gap-2">
          {Object.entries(step.state)
            .filter(([k]) => !['dp', 'done'].includes(k))
            .slice(0, 5)
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
