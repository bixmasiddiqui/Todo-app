'use client'

import { useState, useRef, useEffect } from 'react'
import type { Task } from '@/types/task'
import { parseCommand, generateId, type ChatMessage } from '@/lib/chatbot'

interface ChatBotProps {
  tasks: Task[]
  onAddTask: (title: string) => Promise<void>
  onToggleTask: (taskId: string, completed: boolean) => Promise<void>
  onDeleteTask: (taskId: string) => Promise<void>
}

const INITIAL_MESSAGE: ChatMessage = {
  id: 'welcome',
  role: 'assistant',
  content: "Hey, adventurer! I'm your **AI Quest Assistant**. I can help you manage your quests using natural language.\n\nTry saying things like:\n- \"add Buy groceries\"\n- \"complete task 1\"\n- \"show my tasks\"\n\nType **help** for all commands!",
  timestamp: new Date(),
}

export default function ChatBot({ tasks, onAddTask, onToggleTask, onDeleteTask }: ChatBotProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([INITIAL_MESSAGE])
  const [input, setInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [unreadCount, setUnreadCount] = useState(0)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (isOpen) {
      setUnreadCount(0)
      inputRef.current?.focus()
    }
  }, [isOpen])

  const addMessage = (role: 'user' | 'assistant', content: string) => {
    const msg: ChatMessage = { id: generateId(), role, content, timestamp: new Date() }
    setMessages(prev => [...prev, msg])
    if (!isOpen && role === 'assistant') {
      setUnreadCount(prev => prev + 1)
    }
    return msg
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const trimmed = input.trim()
    if (!trimmed || isProcessing) return

    setInput('')
    addMessage('user', trimmed)
    setIsProcessing(true)

    // Small delay for natural feel
    await new Promise(r => setTimeout(r, 400 + Math.random() * 400))

    const { action, response } = parseCommand(trimmed, tasks)

    try {
      switch (action.type) {
        case 'add':
          if (action.payload) {
            await onAddTask(action.payload)
          }
          break
        case 'complete':
          if (action.taskId) {
            await onToggleTask(action.taskId, true)
          }
          break
        case 'uncomplete':
          if (action.taskId) {
            await onToggleTask(action.taskId, false)
          }
          break
        case 'delete':
          if (action.taskId) {
            await onDeleteTask(action.taskId)
          }
          break
      }
      addMessage('assistant', response)
    } catch {
      addMessage('assistant', "Oops! Something went wrong while processing that. Please try again.")
    }

    setIsProcessing(false)
  }

  const formatMessage = (content: string) => {
    // Simple markdown-like formatting
    return content
      .replace(/\*\*(.+?)\*\*/g, '<strong class="text-cyan-300">$1</strong>')
      .replace(/~~(.+?)~~/g, '<del class="text-green-500/40">$1</del>')
      .replace(/\n/g, '<br/>')
  }

  return (
    <>
      {/* Chat Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full flex items-center justify-center transition-all duration-300 ${
          isOpen
            ? 'bg-red-500/20 border border-red-500/50 hover:bg-red-500/30'
            : 'bg-gradient-to-br from-cyan-500/20 to-fuchsia-500/20 border border-cyan-500/50 hover:border-cyan-400 animate-pulse-glow'
        }`}
      >
        {isOpen ? (
          <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <>
            <svg className="w-7 h-7 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-fuchsia-500 text-white text-[10px] font-pixel flex items-center justify-center animate-scale-in">
                {unreadCount}
              </span>
            )}
          </>
        )}
      </button>

      {/* Chat Panel */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-50 w-[380px] max-w-[calc(100vw-3rem)] animate-scale-in">
          <div className="game-card rounded-2xl overflow-hidden flex flex-col" style={{ height: '500px' }}>
            {/* Header */}
            <div className="px-4 py-3 border-b border-cyan-500/20 bg-gradient-to-r from-cyan-500/10 to-fuchsia-500/10">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500/30 to-fuchsia-500/30 border border-cyan-500/40 flex items-center justify-center">
                  <span className="text-sm">&#x1F916;</span>
                </div>
                <div>
                  <h3 className="font-pixel text-[10px] text-cyan-400 tracking-wider">AI QUEST ASSISTANT</h3>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"></div>
                    <span className="text-[10px] text-green-400/70">Online</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3" style={{ scrollbarWidth: 'thin' }}>
              {messages.map(msg => (
                <div
                  key={msg.id}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-in`}
                >
                  <div
                    className={`max-w-[85%] px-3.5 py-2.5 rounded-xl text-sm leading-relaxed ${
                      msg.role === 'user'
                        ? 'bg-cyan-500/15 border border-cyan-500/25 text-cyan-100'
                        : 'bg-fuchsia-500/10 border border-fuchsia-500/20 text-fuchsia-100/90'
                    }`}
                  >
                    <div
                      dangerouslySetInnerHTML={{ __html: formatMessage(msg.content) }}
                    />
                    <div className={`text-[9px] mt-1.5 ${
                      msg.role === 'user' ? 'text-cyan-500/30' : 'text-fuchsia-500/30'
                    }`}>
                      {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>
              ))}

              {isProcessing && (
                <div className="flex justify-start animate-fade-in">
                  <div className="bg-fuchsia-500/10 border border-fuchsia-500/20 px-4 py-3 rounded-xl">
                    <div className="flex gap-1.5">
                      <div className="w-2 h-2 rounded-full bg-fuchsia-400/60 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 rounded-full bg-fuchsia-400/60 animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 rounded-full bg-fuchsia-400/60 animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="p-3 border-t border-cyan-500/20">
              <div className="flex gap-2">
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  placeholder="Type a command..."
                  className="flex-1 px-3 py-2.5 text-sm rounded-lg game-input"
                  disabled={isProcessing}
                />
                <button
                  type="submit"
                  disabled={!input.trim() || isProcessing}
                  className="px-3 py-2.5 rounded-lg btn-neon disabled:opacity-20"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}
