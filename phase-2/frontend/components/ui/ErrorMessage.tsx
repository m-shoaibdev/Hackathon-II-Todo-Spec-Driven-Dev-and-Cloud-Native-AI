/**
 * ErrorMessage component - Display error state
 *
 * Shows error message with optional retry action
 */

interface ErrorMessageProps {
  /**
   * Error message to display
   */
  message: string

  /**
   * Optional title (defaults to "Error")
   */
  title?: string

  /**
   * Optional retry callback
   */
  onRetry?: () => void

  /**
   * Whether to display as full-page
   */
  fullPage?: boolean
}

export default function ErrorMessage({
  message,
  title = 'Error',
  onRetry,
  fullPage = false,
}: ErrorMessageProps) {
  const content = (
    <div className="bg-red-50 border border-red-200 rounded-lg p-6">
      <div className="flex items-start">
        {/* Error icon */}
        <div className="flex-shrink-0">
          <svg
            className="h-6 w-6 text-red-600"
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

        {/* Error content */}
        <div className="ml-3 flex-1">
          <h3 className="text-sm font-medium text-red-800">{title}</h3>
          <div className="mt-2 text-sm text-red-700">
            <p>{message}</p>
          </div>

          {/* Retry button */}
          {onRetry && (
            <div className="mt-4">
              <button
                type="button"
                onClick={onRetry}
                className="inline-flex items-center px-4 py-2 border border-red-300 text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Try again
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )

  if (fullPage) {
    return (
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="max-w-md w-full">{content}</div>
      </div>
    )
  }

  return content
}
