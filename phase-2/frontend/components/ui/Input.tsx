/**
 * Input component - Reusable input with validation states
 *
 * Provides consistent input styling across the application
 * with validation states and error messages
 */

import { InputHTMLAttributes, ReactNode } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  /**
   * Input label
   */
  label?: string

  /**
   * Error message
   */
  error?: string

  /**
   * Helper text
   */
  helperText?: string

  /**
   * Whether field is required
   */
  required?: boolean

  /**
   * Full width input
   */
  fullWidth?: boolean

  /**
   * Icon to display before input
   */
  startIcon?: ReactNode

  /**
   * Icon to display after input
   */
  endIcon?: ReactNode
}

export default function Input({
  label,
  error,
  helperText,
  required = false,
  fullWidth = false,
  startIcon,
  endIcon,
  className = '',
  id,
  ...props
}: InputProps) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-')

  // Base input styles
  const baseStyles = 'px-4 py-2 border rounded-lg transition-colors focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed'

  // Validation styles
  const validationStyles = error
    ? 'border-red-500 focus:ring-red-500'
    : 'border-gray-300'

  // Width styles
  const widthStyles = fullWidth ? 'w-full' : ''

  // Icon padding
  const iconPadding = startIcon ? 'pl-10' : endIcon ? 'pr-10' : ''

  // Combine styles
  const inputClasses = `${baseStyles} ${validationStyles} ${widthStyles} ${iconPadding} ${className}`.trim()

  return (
    <div className={fullWidth ? 'w-full' : ''}>
      {/* Label */}
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      {/* Input container */}
      <div className="relative">
        {/* Start icon */}
        {startIcon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
            {startIcon}
          </div>
        )}

        {/* Input */}
        <input
          id={inputId}
          className={inputClasses}
          required={required}
          {...props}
        />

        {/* End icon */}
        {endIcon && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-gray-400">
            {endIcon}
          </div>
        )}
      </div>

      {/* Error message */}
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}

      {/* Helper text */}
      {!error && helperText && (
        <p className="mt-1 text-sm text-gray-500">{helperText}</p>
      )}
    </div>
  )
}
