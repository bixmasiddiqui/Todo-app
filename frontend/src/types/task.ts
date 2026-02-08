/**
 * Task type matching backend TaskResponse schema
 */
export interface Task {
  id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

/**
 * Task creation payload matching backend TaskCreate schema
 */
export interface TaskCreate {
  title: string
  description?: string
}

/**
 * Task update payload matching backend TaskUpdate schema
 */
export interface TaskUpdate {
  title?: string
  description?: string
  completed?: boolean
}
