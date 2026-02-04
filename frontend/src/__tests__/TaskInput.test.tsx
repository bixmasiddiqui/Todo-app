import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import TaskInput from '@/components/TaskInput'

describe('TaskInput Component', () => {
  it('renders input field and button', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    expect(screen.getByPlaceholderText('What needs to be done?')).toBeInTheDocument()
    expect(screen.getByText('Add Task')).toBeInTheDocument()
  })

  it('calls onTaskCreate when form is submitted with valid input', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('What needs to be done?')
    const button = screen.getByText('Add Task')

    fireEvent.change(input, { target: { value: 'Buy groceries' } })
    fireEvent.click(button)

    expect(mockOnCreate).toHaveBeenCalledWith('Buy groceries')
  })

  it('does not call onTaskCreate when input is empty', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const button = screen.getByText('Add Task')
    fireEvent.click(button)

    expect(mockOnCreate).not.toHaveBeenCalled()
  })

  it('trims whitespace from input', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('What needs to be done?')
    fireEvent.change(input, { target: { value: '  Buy groceries  ' } })
    fireEvent.submit(input.closest('form')!)

    expect(mockOnCreate).toHaveBeenCalledWith('Buy groceries')
  })

  it('clears input after successful submission', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('What needs to be done?') as HTMLInputElement
    fireEvent.change(input, { target: { value: 'Buy groceries' } })
    fireEvent.submit(input.closest('form')!)

    expect(input.value).toBe('')
  })

  it('shows error message for empty input submission', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('What needs to be done?')
    const button = screen.getByText('Add Task')

    // Try to submit empty
    fireEvent.change(input, { target: { value: '' } })
    fireEvent.click(button)

    expect(screen.getByText('Task description cannot be empty')).toBeInTheDocument()
  })

  it('disables button when isLoading is true', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} isLoading={true} />)

    const button = screen.getByText('Adding...') as HTMLButtonElement
    expect(button).toBeDisabled()
  })

  it('shows character count when typing', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('What needs to be done?')
    fireEvent.change(input, { target: { value: 'Test' } })

    // Should show remaining characters (500 - 4 = 496)
    expect(screen.getByText('496')).toBeInTheDocument()
  })

  it('enforces maximum character limit', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('What needs to be done?') as HTMLInputElement

    // Maximum is 500 characters
    expect(input.maxLength).toBe(500)
  })
})
