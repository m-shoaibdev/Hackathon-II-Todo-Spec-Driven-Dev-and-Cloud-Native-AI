'use client'

/**
 * Dashboard page - Main task management interface
 *
 * Displays user's task list with loading and error states
 */

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'
import { getTasks, toggleComplete, deleteTask } from '@/services/task-service'
import type { Task } from '@/types/task'
import TaskList from '@/components/tasks/TaskList'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import ErrorMessage from '@/components/ui/ErrorMessage'

export default function DashboardPage() {
  const { user } = useAuth()

  // Task state
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  /**
   * Fetch tasks on mount and when user changes
   */
  useEffect(() => {
    if (user) {
      fetchTasks()
    }
  }, [user])

  /**
   * Fetch tasks from API
   */
  async function fetchTasks() {
    if (!user) return

    setLoading(true)
    setError(null)

    try {
      const data = await getTasks(user.id)
      setTasks(data)
    } catch (err: any) {
      console.error('Failed to fetch tasks:', err)
      setError(err.message || 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  /**
   * Handle task completion toggle
   */
  async function handleToggleComplete(task: Task) {
    if (!user) return

    // Optimistically update UI
    setTasks(prevTasks =>
      prevTasks.map(t =>
        t.id === task.id ? { ...t, completed: !t.completed } : t
      )
    )

    try {
      await toggleComplete(user.id, task.id)
      // Optionally refetch to ensure sync
      // await fetchTasks()
    } catch (err: any) {
      // Revert optimistic update on error
      setTasks(prevTasks =>
        prevTasks.map(t =>
          t.id === task.id ? { ...t, completed: task.completed } : t
        )
      )
      throw err // Re-throw for TaskItem to handle
    }
  }

  /**
   * Handle task deletion
   */
  async function handleDelete(task: Task) {
    if (!user) return

    // Optimistically remove from UI
    setTasks(prevTasks => prevTasks.filter(t => t.id !== task.id))

    try {
      await deleteTask(user.id, task.id)
    } catch (err: any) {
      // Revert deletion on error - add back to list
      setTasks(prevTasks => [...prevTasks, task].sort((a, b) =>
        new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      ))
      throw err // Re-throw for DeleteConfirm to handle
    }
  }

  /**
   * Loading state
   */
  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-3xl font-bold text-gray-900">My Tasks</h2>
        </div>
        <LoadingSpinner message="Loading tasks..." />
      </div>
    )
  }

  /**
   * Error state
   */
  if (error) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-3xl font-bold text-gray-900">My Tasks</h2>
        </div>
        <ErrorMessage
          title="Failed to load tasks"
          message={error}
          onRetry={fetchTasks}
        />
      </div>
    )
  }

  /**
   * Task list view
   */
  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Page header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">My Tasks</h2>
          <p className="text-sm text-gray-500 mt-1">
            {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
          </p>
        </div>
        <Link
          href="/tasks/new"
          className="px-4 sm:px-6 py-2 sm:py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 inline-flex items-center justify-center gap-2 text-sm sm:text-base"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          <span className="hidden sm:inline">New Task</span>
          <span className="sm:hidden">New</span>
        </Link>
      </div>

      {/* Task list */}
      <TaskList
        tasks={tasks}
        onToggleComplete={handleToggleComplete}
        onDelete={handleDelete}
        emptyMessage="No tasks yet. Create one to get started!"
      />
    </div>
  )
}
