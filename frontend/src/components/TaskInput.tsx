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
      setError('Task description cannot be empty')
      return
    }

    if (trimmed.length > MAX_LENGTH) {
      setError(`Task description must be ${MAX_LENGTH} characters or less`)
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
    <div className="mb-8 animate-slide-in">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="relative">
          <input
            type="text"
            value={description}
            onChange={handleChange}
            placeholder="What needs to be done?"
            className={`w-full px-5 py-4 text-base sm:text-lg rounded-xl shadow-soft hover-lift smooth-transition
              ${error
                ? 'border-2 border-red-400 focus:border-red-500 focus:ring-4 focus:ring-red-100 animate-shake'
                : 'border border-gray-200 dark:border-gray-700 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 dark:focus:ring-indigo-900'
              }
              bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
              placeholder:text-gray-400 dark:placeholder:text-gray-500
              disabled:opacity-50 disabled:cursor-not-allowed
              outline-none`}
            disabled={isLoading}
            maxLength={MAX_LENGTH}
            autoFocus
          />

          {/* Character count */}
          {description.length > 0 && (
            <div className={`absolute right-4 top-1/2 -translate-y-1/2 text-xs font-medium smooth-transition
              ${isNearLimit
                ? 'text-orange-500 dark:text-orange-400'
                : 'text-gray-400 dark:text-gray-500'
              }`}>
              {remainingChars}
            </div>
          )}
        </div>

        {/* Error message */}
        {error && (
          <div className="flex items-center gap-2 text-sm text-red-600 dark:text-red-400 animate-scale-in">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        )}

        {/* Action buttons */}
        <div className="flex gap-3">
          <button
            type="submit"
            disabled={isLoading || !isValid}
            className="flex-1 sm:flex-none px-8 py-3.5 rounded-xl font-semibold text-white
              bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-700 hover:to-indigo-600
              shadow-soft hover:shadow-soft-lg hover-lift smooth-transition
              disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none
              focus:outline-none focus:ring-4 focus:ring-indigo-300 dark:focus:ring-indigo-900
              active:scale-95"
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Adding...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Add Task
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
              className="px-4 py-3.5 rounded-xl font-medium text-gray-600 dark:text-gray-400
                bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700
                smooth-transition hover-lift shadow-soft
                focus:outline-none focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-600
                animate-scale-in"
            >
              Clear
            </button>
          )}
        </div>

        {/* Helpful hint */}
        {!description && !error && (
          <p className="text-sm text-gray-500 dark:text-gray-400 animate-fade-in">
            Press <kbd className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono">Enter</kbd> to add
          </p>
        )}
      </form>
    </div>
  )
}
