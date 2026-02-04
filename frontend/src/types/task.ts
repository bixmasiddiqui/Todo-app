/**
 * Task type matching backend TaskResponse schema
 */
export interface Task {
  id: string
  description: string
  is_completed: boolean
  created_at: string
  updated_at: string
}

/**
 * Task creation payload matching backend TaskCreate schema
 */
export interface TaskCreate {
  description: string
}

/**
 * Task update payload matching backend TaskUpdate schema
 */
export interface TaskUpdate {
  description?: string
  is_completed?: boolean
}
