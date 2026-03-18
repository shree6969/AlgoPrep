import { Play, Pause, SkipBack, SkipForward, RotateCcw } from 'lucide-react'
import clsx from 'clsx'

interface Props {
  currentStep: number
  totalSteps: number
  isPlaying: boolean
  speed: number
  description: string
  onPrev: () => void
  onNext: () => void
  onPlayPause: () => void
  onReset: () => void
  onSpeedChange: (speed: number) => void
}

export default function StepControls({
  currentStep,
  totalSteps,
  isPlaying,
  speed,
  description,
  onPrev,
  onNext,
  onPlayPause,
  onReset,
  onSpeedChange,
}: Props) {
  const progress = totalSteps > 1 ? (currentStep / (totalSteps - 1)) * 100 : 0

  return (
    <div className="flex flex-col gap-3 p-4 bg-bg-secondary border-t border-border">
      {/* Description */}
      <div className="min-h-[2.5rem] flex items-start gap-2">
        <span className="text-xs font-mono text-accent-blue flex-shrink-0 mt-0.5">
          [{currentStep + 1}/{totalSteps}]
        </span>
        <p className="text-sm text-text-secondary leading-relaxed flex-1">{description}</p>
      </div>

      {/* Progress bar */}
      <div className="relative h-1.5 bg-bg-tertiary rounded-full overflow-hidden">
        <div
          className="absolute left-0 top-0 h-full bg-gradient-to-r from-accent-blue to-accent-purple rounded-full transition-all duration-200"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Controls row */}
      <div className="flex items-center justify-between">
        {/* Left: navigation controls */}
        <div className="flex items-center gap-1">
          <button
            onClick={onReset}
            className="btn btn-ghost btn-sm p-2"
            title="Reset"
            disabled={currentStep === 0 && !isPlaying}
          >
            <RotateCcw size={14} />
          </button>
          <button
            onClick={onPrev}
            disabled={currentStep === 0}
            className={clsx(
              'btn btn-ghost btn-sm p-2',
              currentStep === 0 && 'opacity-40 cursor-not-allowed'
            )}
            title="Previous step"
          >
            <SkipBack size={14} />
          </button>
          <button
            onClick={onPlayPause}
            className="btn btn-primary btn-sm px-4 gap-1.5"
          >
            {isPlaying ? <Pause size={14} /> : <Play size={14} />}
            {isPlaying ? 'Pause' : 'Play'}
          </button>
          <button
            onClick={onNext}
            disabled={currentStep === totalSteps - 1}
            className={clsx(
              'btn btn-ghost btn-sm p-2',
              currentStep === totalSteps - 1 && 'opacity-40 cursor-not-allowed'
            )}
            title="Next step"
          >
            <SkipForward size={14} />
          </button>
        </div>

        {/* Right: speed control */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-text-muted">Speed</span>
          <input
            type="range"
            min="0.5"
            max="3"
            step="0.5"
            value={speed}
            onChange={(e) => onSpeedChange(parseFloat(e.target.value))}
            className="w-20 accent-accent-blue cursor-pointer"
          />
          <span className="text-xs text-text-secondary w-8">{speed}x</span>
        </div>
      </div>
    </div>
  )
}
