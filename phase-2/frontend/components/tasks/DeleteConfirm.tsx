'use client'

/**
 * DeleteConfirm component - Confirmation dialog for task deletion
 *
 * Shows modal with confirm/cancel buttons and error handling
 */

import { useState } from 'react'

interface DeleteConfirmProps {
  /**
   * Task title to display in confirmation
   */
  taskTitle: string

  /**
   * Whether modal is open
   */
  isOpen: boolean

  /**
   * Callback when confirmed
   */
  onConfirm: () => Promise<void>

  /**
   * Callback when cancelled
   */
  onCancel: () => void
}

export default function DeleteConfirm({
  taskTitle,
  isOpen,
  onConfirm,
  onCancel,
}: DeleteConfirmProps) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  /**
   * Handle confirmation
   */
  async function handleConfirm() {
    setLoading(true)
    setError(null)

    try {
      await onConfirm()
    } catch (err: any) {
      console.error('Delete failed:', err)
      setError(err.message || 'Failed to delete task')
      setLoading(false)
    }
    // Don't set loading to false on success - modal will close
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        {/* Error message */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Warning icon */}
        <div className="flex items-center gap-4 mb-4">
          <div className="flex-shrink-0">
            <svg
              className="h-10 w-10 text-red-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>

          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900">
              Delete Task
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              Are you sure you want to delete this task? This action cannot be undone.
            </p>
          </div>
        </div>

        {/* Task title */}
        <div className="bg-gray-100 rounded p-3 mb-6">
          <p className="text-sm font-medium text-gray-900 truncate">
            {taskTitle}
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          <button
            type="button"
            onClick={onCancel}
            disabled={loading}
            className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Cancel
          </button>

          <button
            type="button"
            onClick={handleConfirm}
            disabled={loading}
            className={`flex-1 px-4 py-2 text-white rounded-lg font-medium ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-red-600 hover:bg-red-700'
            }`}
          >
            {loading ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
    </div>
  )
}
