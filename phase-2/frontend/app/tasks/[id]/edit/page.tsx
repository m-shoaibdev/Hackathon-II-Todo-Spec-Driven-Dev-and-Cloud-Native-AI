'use client'

/**
 * Edit Task page - Update existing task
 *
 * Protected route for editing tasks
 */

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { getTask, updateTask } from '@/services/task-service'
import type { Task } from '@/types/task'
import TaskForm from '@/components/tasks/TaskForm'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import ErrorMessage from '@/components/ui/ErrorMessage'

export default function EditTaskPage() {
  const router = useRouter()
  const params = useParams()
  const { user } = useAuth()

  const taskId = parseInt(params.id as string)

  // Task state
  const [task, setTask] = useState<Task | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  /**
   * Fetch task on mount
   */
  useEffect(() => {
    if (user && taskId) {
      fetchTask()
    }
  }, [user, taskId])

  /**
   * Fetch task from API
   */
  async function fetchTask() {
    if (!user) return

    setLoading(true)
    setError(null)

    try {
      const data = await getTask(user.id, taskId)
      setTask(data)
    } catch (err: any) {
      console.error('Failed to fetch task:', err)
      setError(err.message || 'Failed to load task')
    } finally {
      setLoading(false)
    }
  }

  /**
   * Handle task update
   */
  async function handleSubmit(data: { title: string; description?: string }) {
    if (!user) {
      throw new Error('User not authenticated')
    }

    // Update task
    await updateTask(user.id, taskId, data)

    // Redirect to dashboard
    router.push('/dashboard')
  }

  /**
   * Handle cancel
   */
  function handleCancel() {
    router.push('/dashboard')
  }

  /**
   * Loading state
   */
  if (loading) {
    return <LoadingSpinner message="Loading task..." fullPage />
  }

  /**
   * Error state
   */
  if (error || !task) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
          <ErrorMessage
            title="Failed to load task"
            message={error || 'Task not found'}
            onRetry={fetchTask}
          />
        </div>
      </div>
    )
  }

  /**
   * Edit form
   */
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Page header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Edit Task</h1>
          <p className="text-gray-600 mt-2">
            Update task details
          </p>
        </div>

        {/* Task form */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <TaskForm
            initialValues={{
              title: task.title,
              description: task.description || undefined,
            }}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            submitText="Update Task"
          />
        </div>
      </div>
    </div>
  )
}
