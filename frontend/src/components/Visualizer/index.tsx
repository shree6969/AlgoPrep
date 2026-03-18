import { useState, useEffect, useRef, useCallback } from 'react'
import type { VizStep, VizType } from '../../types'
import StepControls from './StepControls'
import ArrayVisualizer from './ArrayVisualizer'
import GridVisualizer from './GridVisualizer'
import TreeVisualizer from './TreeVisualizer'
import GraphVisualizer from './GraphVisualizer'

interface Props {
  steps: VizStep[]
  vizType: VizType
}

export default function Visualizer({ steps, vizType }: Props) {
  const [currentStep, setCurrentStep] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [speed, setSpeed] = useState(1)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const totalSteps = steps.length

  // Reset when steps change
  useEffect(() => {
    setCurrentStep(0)
    setIsPlaying(false)
  }, [steps])

  // Auto-play interval
  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= totalSteps - 1) {
            setIsPlaying(false)
            return prev
          }
          return prev + 1
        })
      }, 1000 / speed)
    } else {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [isPlaying, speed, totalSteps])

  const handlePrev = useCallback(() => {
    setCurrentStep((prev) => Math.max(0, prev - 1))
    setIsPlaying(false)
  }, [])

  const handleNext = useCallback(() => {
    setCurrentStep((prev) => Math.min(totalSteps - 1, prev + 1))
    setIsPlaying(false)
  }, [totalSteps])

  const handlePlayPause = useCallback(() => {
    if (currentStep >= totalSteps - 1) {
      setCurrentStep(0)
      setIsPlaying(true)
    } else {
      setIsPlaying((prev) => !prev)
    }
  }, [currentStep, totalSteps])

  const handleReset = useCallback(() => {
    setIsPlaying(false)
    setCurrentStep(0)
  }, [])

  if (!steps.length) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-text-muted p-8 text-center">
        <div className="text-5xl mb-4 opacity-30">▶</div>
        <h3 className="text-text-secondary font-semibold mb-1">No visualization yet</h3>
        <p className="text-sm">Configure inputs and click "Run Visualization" to see the algorithm in action.</p>
      </div>
    )
  }

  const step = steps[currentStep]

  const renderViz = () => {
    switch (vizType) {
      case 'array':
        return <ArrayVisualizer step={step} />
      case 'grid':
        return <GridVisualizer step={step} />
      case 'tree':
        return <TreeVisualizer step={step} />
      case 'graph':
        return <GraphVisualizer step={step} />
      default:
        return (
          <div className="flex items-center justify-center h-full text-text-muted text-sm p-6 text-center">
            <div>
              <div className="text-4xl mb-3">⚙</div>
              <p className="text-text-secondary font-medium mb-1">Algorithm Executed</p>
              <p>{step.description}</p>
              {step.state.result !== undefined && (
                <div className="mt-3 bg-bg-tertiary rounded-lg px-4 py-2 border border-border inline-block">
                  <span className="text-text-muted">Result: </span>
                  <span className="text-accent-green font-mono font-semibold">
                    {JSON.stringify(step.state.result)}
                  </span>
                </div>
              )}
            </div>
          </div>
        )
    }
  }

  return (
    <div className="flex flex-col h-full bg-bg-primary">
      {/* Viz area */}
      <div className="flex-1 overflow-auto min-h-0">
        {renderViz()}
      </div>

      {/* Controls */}
      <StepControls
        currentStep={currentStep}
        totalSteps={totalSteps}
        isPlaying={isPlaying}
        speed={speed}
        description={step.description}
        onPrev={handlePrev}
        onNext={handleNext}
        onPlayPause={handlePlayPause}
        onReset={handleReset}
        onSpeedChange={setSpeed}
      />
    </div>
  )
}
