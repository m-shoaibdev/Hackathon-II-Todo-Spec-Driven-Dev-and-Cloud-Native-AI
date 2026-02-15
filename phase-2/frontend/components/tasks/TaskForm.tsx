'use client'

/**
 * TaskForm component - Reusable form for creating/editing tasks
 *
 * Features:
 * - Title input (required, 1-200 chars)
 * - Description textarea (optional, max 1000 chars)
 * - Client-side validation
 * - Loading and error states
 */

import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'
import { validateTaskTitle, validateTaskDescription } from '@/types/task'

interface TaskFormProps {
  /**
   * Initial values (for edit mode)
   */
  initialValues?: {
    title?: string
    description?: string
  }

  /**
   * Form submission handler
   */
  onSubmit: (data: { title: string; description?: string }) => Promise<void>

  /**
   * Cancel handler
   */
  onCancel?: () => void

  /**
   * Submit button text
   */
  submitText?: string

  /**
   * Whether form is in loading state
   */
  loading?: boolean
}

export default function TaskForm({
  initialValues,
  onSubmit,
  onCancel,
  submitText = 'Save Task',
  loading: externalLoading = false,
}: TaskFormProps) {
  const router = useRouter()

  // Form state
  const [title, setTitle] = useState(initialValues?.title || '')
  const [description, setDescription] = useState(initialValues?.description || '')

  // UI state
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Validation errors
  const [titleError, setTitleError] = useState<string | null>(null)
  const [descriptionError, setDescriptionError] = useState<string | null>(null)

  const isLoading = loading || externalLoading

  /**
   * Validate title on blur
   */
  function handleTitleBlur() {
    const error = validateTaskTitle(title)
    setTitleError(error || null)
  }

  /**
   * Validate description on blur
   */
  function handleDescriptionBlur() {
    const error = validateTaskDescription(description)
    setDescriptionError(error || null)
  }

  /**
   * Handle form submission
   */
  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)

    // Validate all fields
    const titleValidationError = validateTaskTitle(title)
    const descriptionValidationError = validateTaskDescription(description)

    setTitleError(titleValidationError || null)
    setDescriptionError(descriptionValidationError || null)

    if (titleValidationError || descriptionValidationError) {
      return
    }

    setLoading(true)

    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim() || undefined,
      })
    } catch (err: any) {
      console.error('Form submission error:', err)
      setError(err.message || 'Failed to save task')
    } finally {
      setLoading(false)
    }
  }

  /**
   * Handle cancel
   */
  function handleCancel() {
    if (onCancel) {
      onCancel()
    } else {
      router.back()
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Global error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Title field */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium mb-2">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value)
            setTitleError(null)
          }}
          onBlur={handleTitleBlur}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            titleError ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Enter task title"
          required
          disabled={isLoading}
          maxLength={200}
        />
        {titleError && (
          <p className="text-red-500 text-sm mt-1">{titleError}</p>
        )}
        <p className="text-gray-500 text-xs mt-1">
          {title.length}/200 characters
        </p>
      </div>

      {/* Description field */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium mb-2">
          Description (optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => {
            setDescription(e.target.value)
            setDescriptionError(null)
          }}
          onBlur={handleDescriptionBlur}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            descriptionError ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Enter task description (optional)"
          rows={4}
          disabled={isLoading}
          maxLength={1000}
        />
        {descriptionError && (
          <p className="text-red-500 text-sm mt-1">{descriptionError}</p>
        )}
        <p className="text-gray-500 text-xs mt-1">
          {description.length}/1000 characters
        </p>
      </div>

      {/* Form actions */}
      <div className="flex gap-4">
        <button
          type="submit"
          disabled={isLoading}
          className={`flex-1 px-6 py-3 text-white rounded-lg font-medium ${
            isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {isLoading ? 'Saving...' : submitText}
        </button>

        <button
          type="button"
          onClick={handleCancel}
          disabled={isLoading}
          className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
      </div>
    </form>
  )
}
