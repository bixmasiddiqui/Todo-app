'use client'

import { useEffect, useState } from 'react'
import TaskInput from '@/components/TaskInput'
import TaskList from '@/components/TaskList'
import { fetchTasks, createTask, updateTask, deleteTask } from '@/lib/api'
import type { Task } from '@/types/task'

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [initialLoad, setInitialLoad] = useState(true)

  // Fetch tasks on mount
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

  const handleTaskCreate = async (description: string) => {
    try {
      setIsLoading(true)
      setError(null)
      const newTask = await createTask({ description })
      setTasks([newTask, ...tasks])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task')
    } finally {
      setIsLoading(false)
    }
  }

  const handleTaskToggle = async (taskId: string, isCompleted: boolean) => {
    try {
      setError(null)
      // Optimistic update
      setTasks(
        tasks.map((task) =>
          task.id === taskId ? { ...task, is_completed: isCompleted } : task
        )
      )
      await updateTask(taskId, { is_completed: isCompleted })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task')
      // Rollback on error
      loadTasks()
    }
  }

  const handleTaskUpdate = async (taskId: string, description: string) => {
    try {
      setError(null)
      // Optimistic update
      setTasks(
        tasks.map((task) =>
          task.id === taskId ? { ...task, description } : task
        )
      )
      await updateTask(taskId, { description })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task')
      // Rollback on error
      loadTasks()
    }
  }

  const handleTaskDelete = async (taskId: string) => {
    try {
      setError(null)
      // Optimistic update
      setTasks(tasks.filter((task) => task.id !== taskId))
      await deleteTask(taskId)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task')
      // Rollback on error
      loadTasks()
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-8 sm:py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8 sm:mb-12 animate-fade-in">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-indigo-600 shadow-lg flex items-center justify-center">
              <svg className="w-7 h-7 sm:w-8 sm:h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-gray-900 via-indigo-900 to-gray-900 dark:from-white dark:via-indigo-200 dark:to-white bg-clip-text text-transparent mb-3">
            Task Master
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-sm sm:text-base max-w-md mx-auto">
            Organize your day, accomplish your goals
          </p>
        </div>

        {/* Error message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 rounded-lg animate-shake">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <div className="flex-1">
                <p className="text-sm font-medium text-red-800 dark:text-red-200">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="text-red-400 hover:text-red-600 dark:text-red-500 dark:hover:text-red-300 smooth-transition"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        )}

        {/* Main card */}
        <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm shadow-2xl rounded-2xl sm:rounded-3xl p-6 sm:p-8 border border-gray-200/50 dark:border-gray-700/50">
          <TaskInput onTaskCreate={handleTaskCreate} isLoading={isLoading} />

          {initialLoad ? (
            <div className="flex justify-center items-center py-12">
              <div className="relative">
                <div className="w-12 h-12 rounded-full border-4 border-gray-200 dark:border-gray-700"></div>
                <div className="w-12 h-12 rounded-full border-4 border-indigo-600 border-t-transparent animate-spin absolute top-0 left-0"></div>
              </div>
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
        <div className="mt-8 text-center text-sm text-gray-500 dark:text-gray-400 animate-fade-in">
          <p>
            Built with ❤️ using Next.js, FastAPI & PostgreSQL
          </p>
          <p className="mt-1 text-xs">
            Double-click tasks to edit • Click delete twice to confirm
          </p>
        </div>
      </div>
    </main>
  )
}
