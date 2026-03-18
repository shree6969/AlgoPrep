import CodeMirror from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'
import { oneDark } from '@codemirror/theme-one-dark'
import { EditorView } from '@codemirror/view'

interface Props {
  value: string
  onChange?: (val: string) => void
  readOnly?: boolean
  height?: string
}

const customTheme = EditorView.theme({
  '&': {
    backgroundColor: '#0f1117 !important',
    fontSize: '13px',
    fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
  },
  '.cm-scroller': {
    fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
  },
  '.cm-content': {
    padding: '12px 0',
  },
  '.cm-gutters': {
    backgroundColor: '#0f1117 !important',
    borderRight: '1px solid #2a2d3e',
    color: '#4a5568',
  },
  '.cm-activeLineGutter': {
    backgroundColor: '#1a1d27 !important',
  },
  '.cm-activeLine': {
    backgroundColor: '#1a1d27 !important',
  },
  '.cm-cursor': {
    borderLeftColor: '#4f9eff',
  },
  '.cm-selectionBackground, ::selection': {
    backgroundColor: '#264f78 !important',
  },
})

export default function CodeEditor({ value, onChange, readOnly = false, height = '400px' }: Props) {
  return (
    <div className="rounded-lg overflow-hidden border border-border">
      <CodeMirror
        value={value}
        height={height}
        theme={oneDark}
        extensions={[python(), customTheme]}
        onChange={onChange}
        readOnly={readOnly}
        basicSetup={{
          lineNumbers: true,
          highlightActiveLineGutter: true,
          highlightSpecialChars: true,
          history: true,
          foldGutter: true,
          drawSelection: true,
          dropCursor: true,
          allowMultipleSelections: true,
          indentOnInput: true,
          syntaxHighlighting: true,
          bracketMatching: true,
          closeBrackets: true,
          autocompletion: !readOnly,
          rectangularSelection: true,
          crosshairCursor: false,
          highlightActiveLine: true,
          highlightSelectionMatches: true,
          closeBracketsKeymap: true,
          defaultKeymap: true,
          searchKeymap: true,
          historyKeymap: true,
          foldKeymap: true,
          completionKeymap: !readOnly,
          lintKeymap: true,
          tabSize: 4,
        }}
      />
    </div>
  )
}
