/**
 * TaskItem component - Display individual task
 *
 * Shows task title, description, and completion status with edit and toggle actions
 */

import { useState } from 'react'
import Link from 'next/link'
import type { Task } from '@/types/task'
import DeleteConfirm from './DeleteConfirm'

interface TaskItemProps {
  /**
   * Task to display
   */
  task: Task

  /**
   * Optional callback when task is clicked
   */
  onClick?: (task: Task) => void

  /**
   * Optional callback when completion is toggled
   */
  onToggleComplete?: (task: Task) => Promise<void>

  /**
   * Optional callback when task is deleted
   */
  onDelete?: (task: Task) => Promise<void>
}

export default function TaskItem({ task, onClick, onToggleComplete, onDelete }: TaskItemProps) {
  const [isToggling, setIsToggling] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)

  /**
   * Format date for display
   */
  function formatDate(date: Date | string | null | undefined): string {
    if (!date) return 'N/A'

    const d = typeof date === 'string' ? new Date(date) : date

    // Check if date is valid
    if (isNaN(d.getTime())) return 'Invalid date'

    return d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  /**
   * Handle completion toggle
   */
  async function handleToggle(e: React.ChangeEvent<HTMLInputElement>) {
    e.stopPropagation()

    if (!onToggleComplete || isToggling) return

    setIsToggling(true)
    setError(null)

    try {
      await onToggleComplete(task)
    } catch (err: any) {
      console.error('Failed to toggle completion:', err)
      setError(err.message || 'Failed to update task')
      // Revert checkbox state
      e.target.checked = !e.target.checked
    } finally {
      setIsToggling(false)
    }
  }

  /**
   * Handle delete confirmation
   */
  async function handleDelete() {
    if (!onDelete) return

    await onDelete(task)
    setShowDeleteConfirm(false)
  }

  return (
    <div className="space-y-2">
      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-3 py-2 rounded text-sm">
          {error}
        </div>
      )}
      <div
        className={`bg-white rounded-lg shadow p-4 border-l-4 ${
          task.completed ? 'border-green-500' : 'border-blue-500'
        } ${onClick ? 'cursor-pointer hover:shadow-md transition-shadow' : ''}`}
        onClick={() => onClick?.(task)}
      >
        {/* Task header */}
        <div className="flex items-start gap-3 mb-2">
          {/* Completion checkbox */}
          {onToggleComplete && (
            <div className="pt-0.5">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={handleToggle}
                disabled={isToggling}
                onClick={(e) => e.stopPropagation()}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 focus:ring-2 disabled:opacity-50 cursor-pointer"
              />
            </div>
          )}

          {/* Title and actions */}
          <div className="flex items-start justify-between flex-1">
            <h3
              className={`text-lg font-semibold flex-1 ${
                task.completed ? 'text-gray-500 line-through' : 'text-gray-900'
              }`}
            >
              {task.title}
            </h3>

            <div className="flex items-center gap-2 ml-4">
              {/* Edit button */}
              <Link
                href={`/tasks/${task.id}/edit`}
                onClick={(e) => e.stopPropagation()}
                className="px-3 py-1 text-sm text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded border border-blue-200 hover:border-blue-300 transition-colors"
              >
                Edit
              </Link>

              {/* Delete button */}
              {onDelete && (
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation()
                    setShowDeleteConfirm(true)
                  }}
                  className="px-3 py-1 text-sm text-red-600 hover:text-red-700 hover:bg-red-50 rounded border border-red-200 hover:border-red-300 transition-colors"
                >
                  Delete
                </button>
              )}

              {/* Completion badge */}
              {task.completed && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  ✓ Completed
                </span>
              )}
            </div>
          </div>
        </div>

      {/* Task description */}
      {task.description && (
        <p
          className={`text-sm mb-3 ${
            task.completed ? 'text-gray-400' : 'text-gray-600'
          }`}
        >
          {task.description}
        </p>
      )}

        {/* Task metadata */}
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Created: {formatDate(task.createdAt)}</span>
          {task.updatedAt !== task.createdAt && (
            <span>Updated: {formatDate(task.updatedAt)}</span>
          )}
        </div>
      </div>

      {/* Delete confirmation modal */}
      <DeleteConfirm
        taskTitle={task.title}
        isOpen={showDeleteConfirm}
        onConfirm={handleDelete}
        onCancel={() => setShowDeleteConfirm(false)}
      />
    </div>
  )
}
