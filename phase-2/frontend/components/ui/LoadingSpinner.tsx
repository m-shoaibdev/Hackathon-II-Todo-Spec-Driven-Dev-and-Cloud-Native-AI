/**
 * LoadingSpinner component - Display loading state
 *
 * Shows animated spinner for async operations
 */

interface LoadingSpinnerProps {
  /**
   * Optional message to display below spinner
   */
  message?: string

  /**
   * Size of spinner (small, medium, large)
   */
  size?: 'small' | 'medium' | 'large'

  /**
   * Whether to display as full-page overlay
   */
  fullPage?: boolean
}

export default function LoadingSpinner({
  message = 'Loading...',
  size = 'medium',
  fullPage = false,
}: LoadingSpinnerProps) {
  const sizeClasses = {
    small: 'h-6 w-6',
    medium: 'h-12 w-12',
    large: 'h-16 w-16',
  }

  const spinner = (
    <div className="text-center">
      <div
        className={`animate-spin rounded-full border-b-2 border-blue-600 mx-auto mb-4 ${sizeClasses[size]}`}
      ></div>
      {message && <p className="text-gray-600">{message}</p>}
    </div>
  )

  if (fullPage) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        {spinner}
      </div>
    )
  }

  return <div className="flex items-center justify-center p-8">{spinner}</div>
}
