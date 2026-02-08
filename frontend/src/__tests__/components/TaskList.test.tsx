import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import TaskList from '@/components/TaskList'
import type { Task } from '@/types/task'

const mockTasks: Task[] = [
  {
    id: '1',
    title: 'Buy groceries',
    description: null,
    completed: false,
    created_at: '2026-02-08T10:00:00Z',
    updated_at: '2026-02-08T10:00:00Z',
  },
  {
    id: '2',
    title: 'Walk the dog',
    description: 'Around the park',
    completed: true,
    created_at: '2026-02-08T09:00:00Z',
    updated_at: '2026-02-08T09:30:00Z',
  },
]

describe('TaskList Component', () => {
  it('renders empty state when no tasks', () => {
    render(<TaskList tasks={[]} />)
    expect(screen.getByText('NO ACTIVE QUESTS')).toBeInTheDocument()
  })

  it('renders task titles', () => {
    render(<TaskList tasks={mockTasks} />)
    expect(screen.getByText('Buy groceries')).toBeInTheDocument()
    expect(screen.getByText('Walk the dog')).toBeInTheDocument()
  })

  it('shows completed tasks with DONE label', () => {
    render(<TaskList tasks={mockTasks} />)
    expect(screen.getByText('[DONE]')).toBeInTheDocument()
  })

  it('calls onTaskToggle when checkbox is clicked', () => {
    const mockToggle = vi.fn()
    render(<TaskList tasks={mockTasks} onTaskToggle={mockToggle} />)

    const checkboxes = screen.getAllByRole('button')
    // First checkbox toggles task 1 to completed
    fireEvent.click(checkboxes[0])
    expect(mockToggle).toHaveBeenCalledWith('1', true)
  })

  it('shows quest progress bar when tasks exist', () => {
    render(<TaskList tasks={mockTasks} />)
    expect(screen.getByText('QUEST PROGRESS')).toBeInTheDocument()
    expect(screen.getByText('1/2')).toBeInTheDocument()
  })

  it('shows rank badge', () => {
    render(<TaskList tasks={mockTasks} />)
    expect(screen.getByText(/RANK/)).toBeInTheDocument()
  })

  it('shows XP reward on completed tasks', () => {
    render(<TaskList tasks={mockTasks} />)
    expect(screen.getByText('+25 XP')).toBeInTheDocument()
  })
})
