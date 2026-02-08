import { describe, it, expect, vi, beforeEach } from 'vitest'
import { fetchTasks, createTask, updateTask, deleteTask } from '@/lib/api'

const mockTask = {
  id: '123e4567-e89b-12d3-a456-426614174000',
  title: 'Test task',
  description: null,
  completed: false,
  created_at: '2026-02-08T10:00:00Z',
  updated_at: '2026-02-08T10:00:00Z',
}

describe('API Client', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  describe('fetchTasks', () => {
    it('fetches all tasks successfully', async () => {
      const mockResponse = [mockTask]
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      })

      const tasks = await fetchTasks()
      expect(tasks).toEqual(mockResponse)
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/todos'),
        expect.objectContaining({ method: 'GET' })
      )
    })

    it('throws error on fetch failure', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        text: () => Promise.resolve('Internal Server Error'),
      })

      await expect(fetchTasks()).rejects.toThrow('Failed to fetch tasks')
    })
  })

  describe('createTask', () => {
    it('creates a task with correct request format', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockTask),
      })

      const result = await createTask({ title: 'Test task' })
      expect(result).toEqual(mockTask)
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/todos'),
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: 'Test task' }),
        })
      )
    })

    it('throws error with detail message on failure', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        text: () => Promise.resolve(JSON.stringify({ detail: 'Validation failed' })),
      })

      await expect(createTask({ title: '' })).rejects.toThrow('Validation failed')
    })

    it('throws generic error when detail is not a string', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        text: () => Promise.resolve(JSON.stringify({ detail: { msg: 'error' } })),
      })

      await expect(createTask({ title: 'x' })).rejects.toThrow('Failed to create task')
    })
  })

  describe('updateTask', () => {
    it('sends PATCH request with correct data', async () => {
      const updated = { ...mockTask, completed: true }
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(updated),
      })

      const result = await updateTask(mockTask.id, { completed: true })
      expect(result.completed).toBe(true)
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining(`/api/todos/${mockTask.id}`),
        expect.objectContaining({ method: 'PATCH' })
      )
    })

    it('throws error on update failure', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        text: () => Promise.resolve(JSON.stringify({ detail: 'Not found' })),
      })

      await expect(updateTask('bad-id', { completed: true })).rejects.toThrow('Not found')
    })
  })

  describe('deleteTask', () => {
    it('sends DELETE request', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
      })

      await deleteTask(mockTask.id)
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining(`/api/todos/${mockTask.id}`),
        expect.objectContaining({ method: 'DELETE' })
      )
    })

    it('does not parse response body on success (204)', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
      })

      await expect(deleteTask(mockTask.id)).resolves.toBeUndefined()
    })

    it('throws error on delete failure', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        text: () => Promise.resolve(JSON.stringify({ detail: 'Not found' })),
      })

      await expect(deleteTask('bad-id')).rejects.toThrow('Not found')
    })
  })
})
