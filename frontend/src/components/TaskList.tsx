'use client'

import { useState } from 'react'
import type { Task } from '@/types/task'

interface TaskListProps {
  tasks: Task[]
  onTaskToggle?: (taskId: string, isCompleted: boolean) => void
  onTaskDelete?: (taskId: string) => void
  onTaskUpdate?: (taskId: string, title: string) => void
}

const MAX_LENGTH = 500

const RANK_LABELS = ['F', 'E', 'D', 'C', 'B', 'A', 'S', 'SS', 'SSS']

export default function TaskList({ tasks, onTaskToggle, onTaskDelete, onTaskUpdate }: TaskListProps) {
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editValue, setEditValue] = useState('')
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null)

  const completedCount = tasks.filter(t => t.completed).length
  const totalCount = tasks.length
  const progressPercent = totalCount > 0 ? (completedCount / totalCount) * 100 : 0

  const startEdit = (task: Task) => {
    setEditingId(task.id)
    setEditValue(task.title)
  }

  const cancelEdit = () => {
    setEditingId(null)
    setEditValue('')
  }

  const saveEdit = (taskId: string) => {
    const trimmed = editValue.trim()
    if (trimmed && trimmed !== tasks.find(t => t.id === taskId)?.title) {
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
      setTimeout(() => setDeleteConfirmId(null), 3000)
    }
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-16 animate-scale-in">
        <div className="mb-6 text-6xl animate-float">&#x2694;&#xFE0F;</div>
        <h3 className="font-pixel text-sm neon-text-cyan mb-3">
          NO ACTIVE QUESTS
        </h3>
        <p className="text-cyan-500/40 text-sm max-w-sm mx-auto">
          Begin your adventure by accepting your first quest above
        </p>
      </div>
    )
  }

  const getRankIndex = () => Math.min(Math.floor(progressPercent / 12), RANK_LABELS.length - 1)

  return (
    <div className="space-y-4">
      {/* Progress / Quest Completion Bar */}
      {totalCount > 0 && (
        <div className="mb-6 animate-slide-in">
          <div className="flex justify-between items-center mb-2">
            <div className="flex items-center gap-2">
              <span className="font-pixel text-[10px] text-fuchsia-400/80">QUEST PROGRESS</span>
              <span className={`font-pixel text-[10px] px-2 py-0.5 rounded border
                ${progressPercent === 100
                  ? 'text-yellow-400 border-yellow-500/40 bg-yellow-500/10'
                  : 'text-cyan-400 border-cyan-500/30 bg-cyan-500/10'
                }`}>
                RANK {RANK_LABELS[getRankIndex()]}
              </span>
            </div>
            <span className="font-pixel text-[10px] text-green-400/70">
              {completedCount}/{totalCount}
            </span>
          </div>
          <div className="xp-bar-track h-4 rounded-full overflow-hidden relative">
            <div
              className="xp-bar-fill h-full rounded-full"
              style={{ width: `${progressPercent}%` }}
            />
            {progressPercent === 100 && (
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="font-pixel text-[8px] text-white drop-shadow-lg">ALL QUESTS COMPLETE!</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Quest List */}
      <div className="space-y-2">
        {tasks.map((task, index) => {
          const isEditing = editingId === task.id
          const isDeleteConfirm = deleteConfirmId === task.id

          return (
            <div
              key={task.id}
              className={`group relative rounded-xl p-4 animate-slide-in
                ${task.completed ? 'quest-item-completed' : 'quest-item'}`}
              style={{ animationDelay: `${index * 60}ms` }}
            >
              <div className="flex items-start gap-3">
                {/* Game-style checkbox */}
                <div className="flex-shrink-0 mt-1">
                  <button
                    onClick={() => onTaskToggle?.(task.id, !task.completed)}
                    className={`game-checkbox rounded flex items-center justify-center
                      ${task.completed ? 'game-checkbox-checked' : ''}`}
                  >
                    {task.completed && (
                      <svg className="w-3 h-3 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </button>
                </div>

                {/* Quest content */}
                <div className="flex-1 min-w-0">
                  {isEditing ? (
                    <div className="space-y-2">
                      <input
                        type="text"
                        value={editValue}
                        onChange={(e) => setEditValue(e.target.value)}
                        onKeyDown={(e) => handleKeyDown(e, task.id)}
                        className="w-full px-3 py-2 text-sm rounded-lg game-input"
                        maxLength={MAX_LENGTH}
                        autoFocus
                      />
                      <div className="flex gap-2">
                        <button
                          onClick={() => saveEdit(task.id)}
                          disabled={!editValue.trim()}
                          className="px-3 py-1.5 text-xs font-pixel btn-neon rounded-lg disabled:opacity-30"
                        >
                          Save
                        </button>
                        <button
                          onClick={cancelEdit}
                          className="px-3 py-1.5 text-xs text-cyan-500/50 border border-cyan-500/20 rounded-lg hover:border-cyan-500/40 transition-all"
                        >
                          Cancel
                        </button>
                        <span className="font-pixel text-[10px] text-cyan-500/30 ml-auto self-center">
                          {MAX_LENGTH - editValue.length}
                        </span>
                      </div>
                    </div>
                  ) : (
                    <p
                      className={`text-base leading-relaxed break-words transition-all duration-300 ${
                        task.completed
                          ? 'text-green-400/40 line-through'
                          : 'text-cyan-100/90'
                      }`}
                      onDoubleClick={() => !task.completed && startEdit(task)}
                    >
                      {task.completed && (
                        <span className="font-pixel text-[10px] text-green-400/60 mr-2">[DONE]</span>
                      )}
                      {task.title}
                    </p>
                  )}

                  {/* Timestamp */}
                  <p className="text-[10px] text-cyan-500/25 mt-1.5 font-mono">
                    {new Date(task.created_at).toLocaleDateString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                    {task.completed && (
                      <span className="ml-2 text-green-500/30">+25 XP</span>
                    )}
                  </p>
                </div>

                {/* Action buttons */}
                {!isEditing && (
                  <div className="flex-shrink-0 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    {!task.completed && onTaskUpdate && (
                      <button
                        onClick={() => startEdit(task)}
                        className="p-2 text-cyan-500/30 hover:text-cyan-400 hover:bg-cyan-500/10 rounded-lg transition-all"
                        title="Edit quest"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                    )}

                    <button
                      onClick={() => handleDelete(task.id)}
                      className={`p-2 rounded-lg transition-all ${
                        isDeleteConfirm
                          ? 'text-red-400 bg-red-500/20 border border-red-500/40'
                          : 'text-red-500/30 hover:text-red-400 hover:bg-red-500/10'
                      }`}
                      title={isDeleteConfirm ? 'Click again to abandon quest' : 'Abandon quest'}
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
