'use client'

import { useEffect, useState } from 'react'
import TaskInput from '@/components/TaskInput'
import TaskList from '@/components/TaskList'
import ChatBot from '@/components/ChatBot'
import { fetchTasks, createTask, updateTask, deleteTask } from '@/lib/api'
import type { Task } from '@/types/task'

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [initialLoad, setInitialLoad] = useState(true)
  const [showLevelUp, setShowLevelUp] = useState(false)

  const completedCount = tasks.filter(t => t.completed).length
  const totalCount = tasks.length
  const xp = completedCount * 25
  const level = Math.floor(xp / 100) + 1
  const xpInLevel = xp % 100

  useEffect(() => {
    loadTasks()
  }, [])

  const loadTasks = async () => {
    try {
      setError(null)
      const fetchedTasks = await fetchTasks()
      setTasks(fetchedTasks)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks')
    } finally {
      setInitialLoad(false)
    }
  }

  const handleTaskCreate = async (title: string) => {
    try {
      setIsLoading(true)
      setError(null)
      const newTask = await createTask({ title })
      setTasks([newTask, ...tasks])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task')
    } finally {
      setIsLoading(false)
    }
  }

  const handleTaskToggle = async (taskId: string, completed: boolean) => {
    try {
      setError(null)
      const prevCompleted = tasks.filter(t => t.completed).length
      setTasks(
        tasks.map((task) =>
          task.id === taskId ? { ...task, completed } : task
        )
      )
      await updateTask(taskId, { completed })

      if (completed) {
        const newXp = (prevCompleted + 1) * 25
        const newLevel = Math.floor(newXp / 100) + 1
        const oldLevel = Math.floor(prevCompleted * 25 / 100) + 1
        if (newLevel > oldLevel) {
          setShowLevelUp(true)
          setTimeout(() => setShowLevelUp(false), 2000)
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task')
      loadTasks()
    }
  }

  const handleTaskUpdate = async (taskId: string, title: string) => {
    try {
      setError(null)
      setTasks(
        tasks.map((task) =>
          task.id === taskId ? { ...task, title } : task
        )
      )
      await updateTask(taskId, { title })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task')
      loadTasks()
    }
  }

  const handleTaskDelete = async (taskId: string) => {
    try {
      setError(null)
      setTasks(tasks.filter((task) => task.id !== taskId))
      await deleteTask(taskId)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task')
      loadTasks()
    }
  }

  return (
    <main className="min-h-screen relative z-10 py-6 sm:py-10 scanline-overlay">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Header - Game Title */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="inline-block mb-4 animate-float">
            <div className="text-5xl sm:text-6xl mb-2">&#x1F3AE;</div>
          </div>
          <h1 className="font-pixel text-2xl sm:text-3xl neon-text-cyan mb-3 tracking-wider">
            QUEST LOG
          </h1>
          <p className="text-sm text-cyan-300/60 font-pixel tracking-wide">
            Level up your productivity
          </p>
        </div>

        {/* Stats Bar */}
        <div className="game-card rounded-xl p-4 mb-6 animate-slide-in">
          <div className="flex items-center justify-between gap-4 flex-wrap">
            {/* Level Badge */}
            <div className={`flex items-center gap-3 ${showLevelUp ? 'animate-level-up' : ''}`}>
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-yellow-500/20 to-orange-500/20 border border-yellow-500/40 flex items-center justify-center">
                <span className="font-pixel text-yellow-400 text-sm">LV</span>
              </div>
              <div>
                <div className="font-pixel text-yellow-400 text-lg">{level}</div>
                <div className="text-xs text-yellow-500/60">LEVEL</div>
              </div>
            </div>

            {/* XP Bar */}
            <div className="flex-1 min-w-[150px]">
              <div className="flex justify-between items-center mb-1">
                <span className="font-pixel text-[10px] text-green-400/80">XP</span>
                <span className="font-pixel text-[10px] text-green-400/60">{xpInLevel}/100</span>
              </div>
              <div className="xp-bar-track h-3 rounded-full overflow-hidden">
                <div
                  className="xp-bar-fill h-full rounded-full"
                  style={{ width: `${xpInLevel}%` }}
                />
              </div>
            </div>

            {/* Quest Stats */}
            <div className="flex gap-4">
              <div className="text-center">
                <div className="font-pixel text-cyan-400 text-lg">{totalCount}</div>
                <div className="text-[10px] text-cyan-500/60 font-pixel">QUESTS</div>
              </div>
              <div className="text-center">
                <div className="font-pixel text-green-400 text-lg">{completedCount}</div>
                <div className="text-[10px] text-green-500/60 font-pixel">DONE</div>
              </div>
            </div>
          </div>
        </div>

        {/* Level Up Notification */}
        {showLevelUp && (
          <div className="fixed top-8 left-1/2 -translate-x-1/2 z-50 animate-scale-in">
            <div className="game-card rounded-xl px-8 py-4 neon-border-green">
              <div className="font-pixel text-green-400 text-center">
                <div className="text-lg mb-1">LEVEL UP!</div>
                <div className="text-xs text-green-300/70">Level {level} reached</div>
              </div>
            </div>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="mb-6 p-4 rounded-xl border border-red-500/40 bg-red-900/20 animate-shake">
            <div className="flex items-start gap-3">
              <span className="text-red-400 font-pixel text-xs mt-0.5">ERROR</span>
              <p className="text-sm text-red-300 flex-1">{error}</p>
              <button
                onClick={() => setError(null)}
                className="text-red-400 hover:text-red-300 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        )}

        {/* Main Game Panel */}
        <div className="game-card rounded-2xl p-6 sm:p-8 animate-pulse-glow">
          {/* Section Title */}
          <div className="flex items-center gap-2 mb-6">
            <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></div>
            <span className="font-pixel text-[10px] text-cyan-400/70 tracking-widest">NEW QUEST</span>
            <div className="flex-1 h-px bg-gradient-to-r from-cyan-500/30 to-transparent"></div>
          </div>

          <TaskInput onTaskCreate={handleTaskCreate} isLoading={isLoading} />

          {/* Quest List Section */}
          <div className="flex items-center gap-2 mb-4 mt-2">
            <div className="w-2 h-2 rounded-full bg-fuchsia-400 animate-pulse"></div>
            <span className="font-pixel text-[10px] text-fuchsia-400/70 tracking-widest">ACTIVE QUESTS</span>
            <div className="flex-1 h-px bg-gradient-to-r from-fuchsia-500/30 to-transparent"></div>
          </div>

          {initialLoad ? (
            <div className="flex flex-col justify-center items-center py-16">
              <div className="relative w-16 h-16 mb-4">
                <div className="absolute inset-0 rounded-full border-2 border-cyan-500/20"></div>
                <div className="absolute inset-0 rounded-full border-2 border-cyan-400 border-t-transparent animate-spin"></div>
                <div className="absolute inset-2 rounded-full border-2 border-fuchsia-400 border-b-transparent animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
              </div>
              <span className="font-pixel text-[10px] text-cyan-400/60 animate-pulse">LOADING...</span>
            </div>
          ) : (
            <TaskList
              tasks={tasks}
              onTaskToggle={handleTaskToggle}
              onTaskDelete={handleTaskDelete}
              onTaskUpdate={handleTaskUpdate}
            />
          )}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center animate-fade-in">
          <p className="font-pixel text-[8px] text-cyan-500/30 tracking-widest">
            QUEST LOG v3.0 // NEXT.JS + FASTAPI + AI CHATBOT
          </p>
          <p className="text-[10px] text-cyan-500/20 mt-2">
            Double-click quests to edit // Click chat icon for AI assistant
          </p>
        </div>
      </div>

      {/* AI Chatbot */}
      <ChatBot
        tasks={tasks}
        onAddTask={handleTaskCreate}
        onToggleTask={handleTaskToggle}
        onDeleteTask={handleTaskDelete}
      />
    </main>
  )
}
