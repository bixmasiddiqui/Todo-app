'use client'

import { useState } from 'react'

interface TaskInputProps {
  onTaskCreate: (description: string) => void
  isLoading?: boolean
}

const MAX_LENGTH = 500

export default function TaskInput({ onTaskCreate, isLoading = false }: TaskInputProps) {
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')

  const remainingChars = MAX_LENGTH - description.length
  const isValid = description.trim().length > 0
  const isNearLimit = remainingChars < 50

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    const trimmed = description.trim()

    if (!trimmed) {
      setError('Quest description cannot be empty!')
      return
    }

    if (trimmed.length > MAX_LENGTH) {
      setError(`Quest description must be ${MAX_LENGTH} characters or less`)
      return
    }

    onTaskCreate(trimmed)
    setDescription('')
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDescription(e.target.value)
    if (error) setError('')
  }

  return (
    <div className="mb-6 animate-slide-in">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="relative">
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-cyan-500/40">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <input
            type="text"
            value={description}
            onChange={handleChange}
            placeholder="Enter your quest..."
            className={`w-full pl-12 pr-16 py-4 text-base rounded-xl game-input font-medium
              ${error ? 'border-red-500/50 animate-shake' : ''}
              disabled:opacity-30 disabled:cursor-not-allowed`}
            disabled={isLoading}
            maxLength={MAX_LENGTH}
            autoFocus
          />

          {description.length > 0 && (
            <div className={`absolute right-4 top-1/2 -translate-y-1/2 font-pixel text-[10px]
              ${isNearLimit ? 'text-orange-400' : 'text-cyan-500/30'}`}>
              {remainingChars}
            </div>
          )}
        </div>

        {error && (
          <div className="flex items-center gap-2 text-sm text-red-400 animate-scale-in">
            <span className="font-pixel text-[10px]">!</span>
            {error}
          </div>
        )}

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={isLoading || !isValid}
            className="flex-1 sm:flex-none px-8 py-3.5 rounded-xl font-pixel text-xs btn-neon"
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Adding...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Accept Quest
              </span>
            )}
          </button>

          {description.length > 0 && (
            <button
              type="button"
              onClick={() => {
                setDescription('')
                setError('')
              }}
              className="px-4 py-3.5 rounded-xl text-xs text-cyan-500/50 border border-cyan-500/20 hover:border-cyan-500/40 hover:text-cyan-400 transition-all animate-scale-in"
            >
              Clear
            </button>
          )}
        </div>

        {!description && !error && (
          <p className="text-xs text-cyan-500/30 animate-fade-in">
            Press <kbd className="px-2 py-0.5 bg-cyan-500/10 border border-cyan-500/20 rounded text-[10px] font-pixel">ENTER</kbd> to accept quest
          </p>
        )}
      </form>
    </div>
  )
}
