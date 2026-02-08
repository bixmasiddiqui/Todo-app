/**
 * AI-Powered Chatbot Engine
 * Natural language command parser for todo management
 */
import type { Task } from '@/types/task'

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export interface ChatAction {
  type: 'add' | 'complete' | 'uncomplete' | 'delete' | 'list' | 'help' | 'greet' | 'none'
  payload?: string
  taskId?: string
}

const GREETINGS = ['hi', 'hello', 'hey', 'sup', 'yo', 'howdy', 'greetings', 'hola']
const THANKS = ['thanks', 'thank you', 'thx', 'ty', 'appreciate']

const GREETING_RESPONSES = [
  "Hey there, adventurer! Ready to manage your quests? Type **help** to see what I can do!",
  "Welcome back, hero! Need help with your quests? Just ask!",
  "Greetings, quest master! What shall we do today?",
  "Hello! I'm your AI quest assistant. Tell me what you need!",
]

const THANKS_RESPONSES = [
  "You're welcome! Happy questing!",
  "No problem, adventurer! Keep slaying those tasks!",
  "Anytime! That's what I'm here for.",
  "Glad I could help! Onwards to victory!",
]

const HELP_TEXT = `Here's what I can do:

**Add a quest:**
- "add Buy groceries"
- "create Walk the dog"
- "new task Study for exam"

**Complete a quest:**
- "complete Buy groceries"
- "done Walk the dog"
- "finish task 1"

**Undo completion:**
- "undo Buy groceries"
- "uncomplete task 2"

**Delete a quest:**
- "delete Buy groceries"
- "remove task 1"

**View quests:**
- "list" or "show tasks"
- "show completed"
- "show pending"

**Other:**
- "clear all completed"
- "how many tasks"
- "help"

Just type naturally - I'll figure out what you mean!`

function randomPick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)]
}

function findTaskByQuery(tasks: Task[], query: string): Task | undefined {
  const lower = query.toLowerCase().trim()

  // Try exact title match first
  const exact = tasks.find(t => t.title.toLowerCase() === lower)
  if (exact) return exact

  // Try "task N" pattern (1-indexed)
  const numMatch = lower.match(/^(?:task\s+)?#?(\d+)$/)
  if (numMatch) {
    const index = parseInt(numMatch[1], 10) - 1
    if (index >= 0 && index < tasks.length) return tasks[index]
  }

  // Try partial match
  const partial = tasks.find(t => t.title.toLowerCase().includes(lower))
  if (partial) return partial

  // Try fuzzy: any word overlap
  const queryWords = lower.split(/\s+/)
  let bestMatch: Task | undefined
  let bestScore = 0
  for (const task of tasks) {
    const titleWords = task.title.toLowerCase().split(/\s+/)
    const score = queryWords.filter(w => titleWords.some(tw => tw.includes(w))).length
    if (score > bestScore) {
      bestScore = score
      bestMatch = task
    }
  }
  if (bestScore > 0) return bestMatch

  return undefined
}

export function parseCommand(input: string, tasks: Task[]): { action: ChatAction; response: string } {
  const trimmed = input.trim()
  const lower = trimmed.toLowerCase()

  // Empty input
  if (!trimmed) {
    return {
      action: { type: 'none' },
      response: "I didn't catch that. Type **help** to see what I can do!",
    }
  }

  // Greetings
  if (GREETINGS.some(g => lower === g || lower.startsWith(g + ' ') || lower.startsWith(g + '!'))) {
    return {
      action: { type: 'greet' },
      response: randomPick(GREETING_RESPONSES),
    }
  }

  // Thanks
  if (THANKS.some(t => lower.includes(t))) {
    return {
      action: { type: 'none' },
      response: randomPick(THANKS_RESPONSES),
    }
  }

  // Help
  if (lower === 'help' || lower === '?' || lower === 'commands' || lower.includes('what can you do')) {
    return {
      action: { type: 'help' },
      response: HELP_TEXT,
    }
  }

  // Count tasks
  if (lower.includes('how many') || lower === 'count' || lower === 'stats') {
    const total = tasks.length
    const done = tasks.filter(t => t.completed).length
    const pending = total - done
    return {
      action: { type: 'none' },
      response: `You have **${total}** quests total: **${pending}** pending, **${done}** completed. ${done > 0 ? `That's +${done * 25} XP earned!` : 'Start completing quests to earn XP!'}`,
    }
  }

  // List tasks
  if (lower === 'list' || lower === 'show' || lower === 'tasks' || lower === 'show tasks' ||
      lower === 'my tasks' || lower === 'show all' || lower === 'list all' || lower === 'all tasks') {
    return {
      action: { type: 'list' },
      response: formatTaskList(tasks, 'all'),
    }
  }

  if (lower === 'show completed' || lower === 'completed' || lower === 'done tasks' || lower === 'finished') {
    return {
      action: { type: 'list' },
      response: formatTaskList(tasks, 'completed'),
    }
  }

  if (lower === 'show pending' || lower === 'pending' || lower === 'todo' || lower === 'remaining' || lower === 'active') {
    return {
      action: { type: 'list' },
      response: formatTaskList(tasks, 'pending'),
    }
  }

  // Clear completed
  if (lower === 'clear completed' || lower === 'clear all completed' || lower === 'remove completed') {
    const completed = tasks.filter(t => t.completed)
    if (completed.length === 0) {
      return { action: { type: 'none' }, response: "No completed quests to clear!" }
    }
    return {
      action: { type: 'none' },
      response: `There are **${completed.length}** completed quests. Delete them individually with "delete [task name]".`,
    }
  }

  // Add task
  const addMatch = lower.match(/^(?:add|create|new|new task|add task|create task|make)\s+(.+)$/i)
  if (addMatch) {
    const title = trimmed.slice(trimmed.indexOf(addMatch[1]!))
    return {
      action: { type: 'add', payload: title },
      response: `Quest accepted: **"${title}"**! Get it done, adventurer!`,
    }
  }

  // Complete task
  const completeMatch = lower.match(/^(?:complete|done|finish|check|mark done|mark complete|mark as done|mark as complete)\s+(.+)$/i)
  if (completeMatch) {
    const query = completeMatch[1]!
    const task = findTaskByQuery(tasks, query)
    if (!task) {
      return { action: { type: 'none' }, response: `Couldn't find a quest matching "${query}". Try "list" to see your quests.` }
    }
    if (task.completed) {
      return { action: { type: 'none' }, response: `**"${task.title}"** is already completed! +25 XP already earned.` }
    }
    return {
      action: { type: 'complete', taskId: task.id },
      response: `Quest complete: **"${task.title}"**! +25 XP earned!`,
    }
  }

  // Uncomplete task
  const undoMatch = lower.match(/^(?:undo|uncomplete|uncheck|reopen|mark incomplete|mark as incomplete)\s+(.+)$/i)
  if (undoMatch) {
    const query = undoMatch[1]!
    const task = findTaskByQuery(tasks, query)
    if (!task) {
      return { action: { type: 'none' }, response: `Couldn't find a quest matching "${query}". Try "list" to see your quests.` }
    }
    if (!task.completed) {
      return { action: { type: 'none' }, response: `**"${task.title}"** is already active!` }
    }
    return {
      action: { type: 'uncomplete', taskId: task.id },
      response: `Quest reopened: **"${task.title}"**. Back to the grind!`,
    }
  }

  // Delete task
  const deleteMatch = lower.match(/^(?:delete|remove|drop|discard|abandon|trash)\s+(.+)$/i)
  if (deleteMatch) {
    const query = deleteMatch[1]!
    const task = findTaskByQuery(tasks, query)
    if (!task) {
      return { action: { type: 'none' }, response: `Couldn't find a quest matching "${query}". Try "list" to see your quests.` }
    }
    return {
      action: { type: 'delete', taskId: task.id },
      response: `Quest abandoned: **"${task.title}"**. It has been removed from your quest log.`,
    }
  }

  // Fallback: if input looks like a task, suggest adding it
  if (trimmed.length > 2 && !lower.includes('?')) {
    return {
      action: { type: 'none' },
      response: `I'm not sure what you mean. Did you want to:\n- **Add** a quest? Try: "add ${trimmed}"\n- See **help**? Type: "help"`,
    }
  }

  return {
    action: { type: 'none' },
    response: "I didn't understand that. Type **help** to see what I can do!",
  }
}

function formatTaskList(tasks: Task[], filter: 'all' | 'completed' | 'pending'): string {
  let filtered = tasks
  if (filter === 'completed') filtered = tasks.filter(t => t.completed)
  if (filter === 'pending') filtered = tasks.filter(t => !t.completed)

  if (filtered.length === 0) {
    if (filter === 'completed') return "No completed quests yet. Keep going!"
    if (filter === 'pending') return "All quests completed! You're a legend!"
    return "No quests in your log. Add one with: \"add [quest name]\""
  }

  const label = filter === 'all' ? 'All Quests' : filter === 'completed' ? 'Completed Quests' : 'Pending Quests'
  const lines = filtered.map((t, i) => {
    const status = t.completed ? '~~' + t.title + '~~' : t.title
    const icon = t.completed ? '[DONE]' : `#${i + 1}`
    return `${icon} ${status}`
  })

  return `**${label}** (${filtered.length}):\n${lines.join('\n')}`
}

export function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 7)
}
