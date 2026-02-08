import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import TaskInput from '@/components/TaskInput'

describe('TaskInput Component', () => {
  it('renders input field and button', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    expect(screen.getByPlaceholderText('Enter your quest...')).toBeInTheDocument()
    expect(screen.getByText('Accept Quest')).toBeInTheDocument()
  })

  it('calls onTaskCreate when form is submitted with valid input', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('Enter your quest...')
    fireEvent.change(input, { target: { value: 'Buy groceries' } })
    fireEvent.submit(input.closest('form')!)

    expect(mockOnCreate).toHaveBeenCalledWith('Buy groceries')
  })

  it('does not call onTaskCreate when input is empty', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('Enter your quest...')
    fireEvent.submit(input.closest('form')!)

    expect(mockOnCreate).not.toHaveBeenCalled()
  })

  it('trims whitespace from input', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('Enter your quest...')
    fireEvent.change(input, { target: { value: '  Buy groceries  ' } })
    fireEvent.submit(input.closest('form')!)

    expect(mockOnCreate).toHaveBeenCalledWith('Buy groceries')
  })

  it('clears input after successful submission', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('Enter your quest...') as HTMLInputElement
    fireEvent.change(input, { target: { value: 'Buy groceries' } })
    fireEvent.submit(input.closest('form')!)

    expect(input.value).toBe('')
  })

  it('shows error message for empty input submission', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('Enter your quest...')
    fireEvent.change(input, { target: { value: '   ' } })
    fireEvent.submit(input.closest('form')!)

    expect(screen.getByText('Quest description cannot be empty!')).toBeInTheDocument()
  })

  it('disables button when isLoading is true', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} isLoading={true} />)

    const button = screen.getByText('Adding...') as HTMLButtonElement
    expect(button.closest('button')).toBeDisabled()
  })

  it('shows character count when typing', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('Enter your quest...')
    fireEvent.change(input, { target: { value: 'Test' } })

    expect(screen.getByText('496')).toBeInTheDocument()
  })

  it('enforces maximum character limit', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('Enter your quest...') as HTMLInputElement
    expect(input.maxLength).toBe(500)
  })

  it('submits on Enter key press', () => {
    const mockOnCreate = vi.fn()
    render(<TaskInput onTaskCreate={mockOnCreate} />)

    const input = screen.getByPlaceholderText('Enter your quest...')
    fireEvent.change(input, { target: { value: 'My quest' } })
    fireEvent.submit(input.closest('form')!)

    expect(mockOnCreate).toHaveBeenCalledWith('My quest')
  })
})
