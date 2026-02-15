'use client'

/**
 * New Task page - Create new task
 *
 * Protected route for creating tasks
 */

import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { createTask } from '@/services/task-service'
import TaskForm from '@/components/tasks/TaskForm'

export default function NewTaskPage() {
  const router = useRouter()
  const { user } = useAuth()

  /**
   * Handle task creation
   */
  async function handleSubmit(data: { title: string; description?: string }) {
    if (!user) {
      throw new Error('User not authenticated')
    }

    // Create task
    await createTask(user.id, data)

    // Redirect to dashboard
    router.push('/dashboard')
  }

  /**
   * Handle cancel
   */
  function handleCancel() {
    router.push('/dashboard')
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Page header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Create New Task</h1>
          <p className="text-gray-600 mt-2">
            Add a new task to your todo list
          </p>
        </div>

        {/* Task form */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <TaskForm
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            submitText="Create Task"
          />
        </div>
      </div>
    </div>
  )
}
