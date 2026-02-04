'use client'

import { useState } from 'react'
import type { Task } from '@/types/task'

interface TaskListProps {
  tasks: Task[]
  onTaskToggle?: (taskId: string, isCompleted: boolean) => void
  onTaskDelete?: (taskId: string) => void
  onTaskUpdate?: (taskId: string, description: string) => void
}

const MAX_LENGTH = 500

export default function TaskList({ tasks, onTaskToggle, onTaskDelete, onTaskUpdate }: TaskListProps) {
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editValue, setEditValue] = useState('')
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null)

  const completedCount = tasks.filter(t => t.is_completed).length
  const totalCount = tasks.length

  const startEdit = (task: Task) => {
    setEditingId(task.id)
    setEditValue(task.description)
  }

  const cancelEdit = () => {
    setEditingId(null)
    setEditValue('')
  }

  const saveEdit = (taskId: string) => {
    const trimmed = editValue.trim()
    if (trimmed && trimmed !== tasks.find(t => t.id === taskId)?.description) {
      onTaskUpdate?.(taskId, trimmed)
    }
    cancelEdit()
  }

  const handleKeyDown = (e: React.KeyboardEvent, taskId: string) => {
    if (e.key === 'Enter') {
      saveEdit(taskId)
    } else if (e.key === 'Escape') {
      cancelEdit()
    }
  }

  const handleDelete = (taskId: string) => {
    if (deleteConfirmId === taskId) {
      onTaskDelete?.(taskId)
      setDeleteConfirmId(null)
    } else {
      setDeleteConfirmId(taskId)
      // Auto-cancel after 3 seconds
      setTimeout(() => setDeleteConfirmId(null), 3000)
    }
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-16 animate-scale-in">
        <div className="mb-6">
          <svg className="w-24 h-24 mx-auto text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
          No tasks yet
        </h3>
        <p className="text-gray-500 dark:text-gray-400 max-w-sm mx-auto">
          Start your productive day by adding your first task above
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Progress bar */}
      {totalCount > 0 && (
        <div className="mb-6 animate-slide-in">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Progress
            </span>
            <span className="text-sm font-semibold text-indigo-600 dark:text-indigo-400">
              {completedCount} of {totalCount} completed
            </span>
          </div>
          <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-indigo-500 to-indigo-600 rounded-full smooth-transition"
              style={{ width: `${totalCount > 0 ? (completedCount / totalCount) * 100 : 0}%` }}
            />
          </div>
        </div>
      )}

      {/* Task list */}
      <div className="space-y-2">
        {tasks.map((task, index) => {
          const isEditing = editingId === task.id
          const isDeleteConfirm = deleteConfirmId === task.id

          return (
            <div
              key={task.id}
              className="group relative bg-white dark:bg-gray-800 rounded-xl p-4 shadow-soft hover:shadow-soft-lg smooth-transition hover-lift border border-gray-100 dark:border-gray-700 animate-slide-in"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className="flex items-start gap-3">
                {/* Checkbox */}
                <div className="flex-shrink-0 mt-1">
                  <button
                    onClick={() => onTaskToggle?.(task.id, !task.is_completed)}
                    className="relative w-5 h-5 rounded border-2 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    style={{
                      borderColor: task.is_completed ? 'rgb(99, 102, 241)' : 'rgb(209, 213, 219)',
                      backgroundColor: task.is_completed ? 'rgb(99, 102, 241)' : 'transparent'
                    }}
                  >
                    {task.is_completed && (
                      <svg className="w-4 h-4 text-white absolute inset-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </button>
                </div>

                {/* Task content */}
                <div className="flex-1 min-w-0">
                  {isEditing ? (
                    <div className="space-y-2">
                      <input
                        type="text"
                        value={editValue}
                        onChange={(e) => setEditValue(e.target.value)}
                        onKeyDown={(e) => handleKeyDown(e, task.id)}
                        className="w-full px-3 py-2 text-sm border-2 border-indigo-400 rounded-lg focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 dark:focus:ring-indigo-900 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100"
                        maxLength={MAX_LENGTH}
                        autoFocus
                      />
                      <div className="flex gap-2">
                        <button
                          onClick={() => saveEdit(task.id)}
                          disabled={!editValue.trim()}
                          className="px-3 py-1.5 text-xs font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg smooth-transition disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          Save
                        </button>
                        <button
                          onClick={cancelEdit}
                          className="px-3 py-1.5 text-xs font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg smooth-transition"
                        >
                          Cancel
                        </button>
                        <span className="text-xs text-gray-400 ml-auto self-center">
                          {MAX_LENGTH - editValue.length} chars left
                        </span>
                      </div>
                    </div>
                  ) : (
                    <p
                      className={`text-base leading-relaxed break-words smooth-transition ${
                        task.is_completed
                          ? 'text-gray-400 dark:text-gray-500 line-through'
                          : 'text-gray-800 dark:text-gray-200'
                      }`}
                      onDoubleClick={() => !task.is_completed && startEdit(task)}
                    >
                      {task.description}
                    </p>
                  )}

                  {/* Timestamp */}
                  <p className="text-xs text-gray-400 dark:text-gray-500 mt-1.5">
                    {new Date(task.created_at).toLocaleDateString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>

                {/* Action buttons */}
                {!isEditing && (
                  <div className="flex-shrink-0 flex gap-1 opacity-0 group-hover:opacity-100 smooth-transition">
                    {!task.is_completed && onTaskUpdate && (
                      <button
                        onClick={() => startEdit(task)}
                        className="p-2 text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 rounded-lg smooth-transition"
                        title="Edit task"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                    )}

                    <button
                      onClick={() => handleDelete(task.id)}
                      className={`p-2 rounded-lg smooth-transition ${
                        isDeleteConfirm
                          ? 'text-white bg-red-500 hover:bg-red-600'
                          : 'text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20'
                      }`}
                      title={isDeleteConfirm ? 'Click again to confirm' : 'Delete task'}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
