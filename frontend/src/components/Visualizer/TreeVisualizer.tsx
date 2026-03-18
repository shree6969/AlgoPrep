import type { VizStep } from '../../types'

interface Props {
  step: VizStep
}

// Simple manual tree layout for visualization
// Data format: adjacency map {nodeId: {val, left?, right?, ...}}
// or flat array in level-order

function buildTreeFromArray(arr: (number | null)[]): TreeNode | null {
  if (!arr || arr.length === 0 || arr[0] === null) return null

  const root: TreeNode = { id: 0, val: arr[0] as number, children: [] }
  const queue: TreeNode[] = [root]
  let i = 1

  while (queue.length > 0 && i < arr.length) {
    const node = queue.shift()!
    if (i < arr.length && arr[i] !== null) {
      const left: TreeNode = { id: i, val: arr[i] as number, children: [] }
      node.children.push({ ...left, side: 'left' })
      queue.push(left)
    } else {
      node.children.push(null as any)
    }
    i++
    if (i < arr.length && arr[i] !== null) {
      const right: TreeNode = { id: i, val: arr[i] as number, children: [] }
      node.children.push({ ...right, side: 'right' })
      queue.push(right)
    }
    i++
  }
  return root
}

interface TreeNode {
  id: number
  val: number
  children: (TreeNode | null)[]
  side?: 'left' | 'right'
  x?: number
  y?: number
}

function assignPositions(
  node: TreeNode | null,
  depth: number,
  left: number,
  right: number,
  positions: Map<number, { x: number; y: number }>
): void {
  if (!node) return
  const x = (left + right) / 2
  const y = depth * 70 + 40
  positions.set(node.id, { x, y })
  const mid = (left + right) / 2
  if (node.children[0]) assignPositions(node.children[0], depth + 1, left, mid, positions)
  if (node.children[1]) assignPositions(node.children[1], depth + 1, mid, right, positions)
}

function collectEdges(
  node: TreeNode | null,
  positions: Map<number, { x: number; y: number }>,
  edges: { x1: number; y1: number; x2: number; y2: number }[]
): void {
  if (!node) return
  const pos = positions.get(node.id)
  if (!pos) return
  for (const child of node.children) {
    if (child) {
      const childPos = positions.get(child.id)
      if (childPos) {
        edges.push({ x1: pos.x, y1: pos.y, x2: childPos.x, y2: childPos.y })
        collectEdges(child, positions, edges)
      }
    }
  }
}

function collectNodes(
  node: TreeNode | null,
  positions: Map<number, { x: number; y: number }>,
  nodes: { id: number; val: number; x: number; y: number }[]
): void {
  if (!node) return
  const pos = positions.get(node.id)
  if (pos) {
    nodes.push({ id: node.id, val: node.val, x: pos.x, y: pos.y })
  }
  for (const child of node.children) {
    collectNodes(child, positions, nodes)
  }
}

export default function TreeVisualizer({ step }: Props) {
  const { data, highlights } = step

  // Parse tree data
  let arr: (number | null)[] = []

  if (Array.isArray(data)) {
    arr = data
  } else if (data && typeof data === 'object') {
    if (Array.isArray(data.tree)) arr = data.tree
    else if (Array.isArray(data.nodes)) arr = data.nodes
  }

  if (!arr.length) {
    return (
      <div className="flex items-center justify-center h-full text-text-muted text-sm p-8">
        <div className="text-center">
          <div className="text-4xl mb-3">⎇</div>
          <p>Tree visualization</p>
          <p className="text-xs mt-1">Run the algorithm to see the tree.</p>
        </div>
      </div>
    )
  }

  const root = buildTreeFromArray(arr)
  if (!root) {
    return (
      <div className="flex items-center justify-center h-full text-text-muted text-sm">
        Empty tree
      </div>
    )
  }

  const depth = Math.ceil(Math.log2(arr.length + 1))
  const W = Math.max(400, (2 ** depth) * 50)
  const H = depth * 70 + 80

  const positions = new Map<number, { x: number; y: number }>()
  assignPositions(root, 0, 0, W, positions)

  const edges: { x1: number; y1: number; x2: number; y2: number }[] = []
  collectEdges(root, positions, edges)

  const nodes: { id: number; val: number; x: number; y: number }[] = []
  collectNodes(root, positions, nodes)

  const activeNodes: Set<number> = new Set(
    [highlights.active, highlights.current, highlights.placed, highlights.found]
      .filter((v) => typeof v === 'number')
  )

  return (
    <div className="w-full overflow-auto p-4">
      <svg width={W} height={H} className="mx-auto">
        {/* Edges */}
        {edges.map((e, i) => (
          <line
            key={i}
            x1={e.x1}
            y1={e.y1}
            x2={e.x2}
            y2={e.y2}
            stroke="#3a3f5c"
            strokeWidth={1.5}
          />
        ))}

        {/* Nodes */}
        {nodes.map((n) => {
          const isActive = activeNodes.has(n.id)
          const isResult = highlights.result_idx === n.id
          return (
            <g key={n.id}>
              <circle
                cx={n.x}
                cy={n.y}
                r={20}
                fill={
                  isResult
                    ? '#065f46'
                    : isActive
                    ? '#1e3a5f'
                    : '#22263a'
                }
                stroke={
                  isResult
                    ? '#34d399'
                    : isActive
                    ? '#4f9eff'
                    : '#3a3f5c'
                }
                strokeWidth={isActive || isResult ? 2 : 1.5}
                style={{ transition: 'all 0.3s ease' }}
              />
              <text
                x={n.x}
                y={n.y + 5}
                textAnchor="middle"
                fontSize={12}
                fontWeight="500"
                fill={isActive || isResult ? '#fff' : '#94a3b8'}
                fontFamily="monospace"
              >
                {n.val}
              </text>
            </g>
          )
        })}
      </svg>
    </div>
  )
}
