/**
 * API client for backend communication
 */
import type { Task, TaskCreate, TaskUpdate } from '@/types/task'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://bismaimran-todo-app.hf.space'

/**
 * Fetch all tasks
 */
export async function fetchTasks(): Promise<Task[]> {
  const response = await fetch(`${API_URL}/api/todos`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch tasks: ${response.status}`)
  }

  return response.json()
}

/**
 * Create a new task
 */
export async function createTask(taskData: TaskCreate): Promise<Task> {
  const response = await fetch(`${API_URL}/api/todos`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(taskData),
  })

  if (!response.ok) {
    const text = await response.text()
    let message = 'Failed to create task'
    try {
      const err = JSON.parse(text)
      message = typeof err.detail === 'string' ? err.detail : message
    } catch {}
    throw new Error(message)
  }

  return response.json()
}

/**
 * Update a task
 */
export async function updateTask(
  taskId: string,
  taskData: TaskUpdate
): Promise<Task> {
  const response = await fetch(`${API_URL}/api/todos/${taskId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(taskData),
  })

  if (!response.ok) {
    const text = await response.text()
    let message = 'Failed to update task'
    try {
      const err = JSON.parse(text)
      message = typeof err.detail === 'string' ? err.detail : message
    } catch {}
    throw new Error(message)
  }

  return response.json()
}

/**
 * Delete a task (returns 204 No Content)
 */
export async function deleteTask(taskId: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/todos/${taskId}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    const text = await response.text()
    let message = 'Failed to delete task'
    try {
      const err = JSON.parse(text)
      message = typeof err.detail === 'string' ? err.detail : message
    } catch {}
    throw new Error(message)
  }
}
