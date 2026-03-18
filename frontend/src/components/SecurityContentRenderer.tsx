import type { SecurityBlock } from '../types'
import CodeMirror from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'
import { oneDark } from '@codemirror/theme-one-dark'

const LANG_MAP: Record<string, any> = {
  python: python(),
}

function CalloutBox({ kind, title, content }: { kind: string; title: string; content: string }) {
  const styles: Record<string, string> = {
    info:    'border-accent-blue/40 bg-accent-blue/5 text-accent-blue',
    warning: 'border-accent-yellow/40 bg-accent-yellow/5 text-accent-yellow',
    danger:  'border-red-500/40 bg-red-500/5 text-red-400',
    success: 'border-green-500/40 bg-green-500/5 text-green-400',
  }
  const icons: Record<string, string> = {
    info: 'ℹ', warning: '⚠', danger: '⛔', success: '✓',
  }
  return (
    <div className={`my-4 rounded-lg border p-4 ${styles[kind] ?? styles.info}`}>
      <div className="font-semibold mb-1 flex items-center gap-2">
        <span>{icons[kind] ?? icons.info}</span>
        {title}
      </div>
      <p className="text-text-secondary text-sm leading-relaxed">{content}</p>
    </div>
  )
}

function DiagramBlock({ title, content }: { title: string; content: string }) {
  return (
    <div className="my-4">
      {title && <p className="text-xs text-text-muted mb-2 font-medium uppercase tracking-wide">{title}</p>}
      <pre className="bg-bg-primary border border-border rounded-lg p-4 text-xs text-text-secondary overflow-x-auto leading-relaxed font-mono">
        {content}
      </pre>
    </div>
  )
}

export default function SecurityContentRenderer({ blocks }: { blocks: SecurityBlock[] }) {
  return (
    <div className="space-y-2">
      {blocks.map((block, i) => {
        switch (block.type) {
          case 'paragraph':
            return (
              <p key={i} className="text-text-secondary leading-relaxed text-sm">
                {block.content}
              </p>
            )

          case 'heading': {
            const Tag = `h${block.level ?? 3}` as keyof JSX.IntrinsicElements
            const sizes: Record<number, string> = { 2: 'text-xl', 3: 'text-lg', 4: 'text-base' }
            return (
              <Tag
                key={i}
                className={`font-semibold text-text-primary mt-6 mb-2 ${sizes[block.level ?? 3]}`}
              >
                {block.content}
              </Tag>
            )
          }

          case 'code':
            return (
              <div key={i} className="my-4">
                {block.title && (
                  <div className="bg-bg-primary border border-b-0 border-border rounded-t-lg px-4 py-2 flex items-center justify-between">
                    <span className="text-xs text-text-muted font-medium">{block.title}</span>
                    <span className="text-xs text-accent-blue">{block.language}</span>
                  </div>
                )}
                <div className={block.title ? 'rounded-b-lg overflow-hidden border border-border' : 'rounded-lg overflow-hidden border border-border'}>
                  <CodeMirror
                    value={block.content ?? ''}
                    extensions={LANG_MAP[block.language ?? 'python'] ? [LANG_MAP[block.language ?? 'python']] : []}
                    theme={oneDark}
                    editable={false}
                    basicSetup={{ lineNumbers: true, foldGutter: false }}
                  />
                </div>
              </div>
            )

          case 'bullets':
            return (
              <ul key={i} className="my-3 space-y-2 ml-4">
                {(block.items ?? []).map((item, j) => (
                  <li key={j} className="flex items-start gap-2 text-sm text-text-secondary">
                    <span className="text-accent-blue mt-1 shrink-0">▸</span>
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            )

          case 'callout':
            return (
              <CalloutBox
                key={i}
                kind={block.kind ?? 'info'}
                title={block.title ?? ''}
                content={block.content ?? ''}
              />
            )

          case 'diagram':
            return (
              <DiagramBlock key={i} title={block.title ?? ''} content={block.content ?? ''} />
            )

          default:
            return null
        }
      })}
    </div>
  )
}
