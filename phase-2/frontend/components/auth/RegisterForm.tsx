'use client'

/**
 * Registration form component
 *
 * Handles user registration with email/password validation
 * and error display.
 */

import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'
import { post } from '@/lib/api-client'
import { type RegisterRequest } from '@/types/user'

interface RegisterFormProps {
  /**
   * Callback invoked on successful registration
   */
  onSuccess?: () => void
}

export default function RegisterForm({ onSuccess }: RegisterFormProps) {
  const router = useRouter()

  // Form state
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  // UI state
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  // Validation errors
  const [emailError, setEmailError] = useState<string | null>(null)
  const [passwordError, setPasswordError] = useState<string | null>(null)
  const [confirmError, setConfirmError] = useState<string | null>(null)

  /**
   * Validate email format
   */
  function validateEmail(email: string): boolean {
    if (!email) {
      setEmailError('Email is required')
      return false
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      setEmailError('Please enter a valid email address')
      return false
    }
    setEmailError(null)
    return true
  }

  /**
   * Validate password requirements
   */
  function validatePassword(password: string): boolean {
    if (!password) {
      setPasswordError('Password is required')
      return false
    }
    if (password.length < 8) {
      setPasswordError('Password must be at least 8 characters')
      return false
    }
    setPasswordError(null)
    return true
  }

  /**
   * Validate password confirmation
   */
  function validateConfirmPassword(confirm: string): boolean {
    if (confirm !== password) {
      setConfirmError('Passwords do not match')
      return false
    }
    setConfirmError(null)
    return true
  }

  /**
   * Handle form submission
   */
  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)

    // Validate all fields
    const isEmailValid = validateEmail(email)
    const isPasswordValid = validatePassword(password)
    const isConfirmValid = validateConfirmPassword(confirmPassword)

    if (!isEmailValid || !isPasswordValid || !isConfirmValid) {
      return
    }

    setLoading(true)

    try {
      // Prepare request payload
      const request: RegisterRequest = {
        email,
        password,
        name: name.trim() || undefined,
      }

      // Call registration API
      const response = await post('/auth/register', request)

      // Store token in localStorage for API requests
      if (response.token) {
        localStorage.setItem('auth_token', response.token)
      }

      // Call success callback if provided
      if (onSuccess) {
        onSuccess()
      }

      // Redirect to dashboard
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.message || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 w-full max-w-md">
      {/* Global error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Name field (optional) */}
      <div>
        <label htmlFor="name" className="block text-sm font-medium mb-2">
          Name (optional)
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Your name"
          disabled={loading}
        />
      </div>

      {/* Email field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-2">
          Email <span className="text-red-500">*</span>
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value)
            setEmailError(null)
          }}
          onBlur={() => validateEmail(email)}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            emailError ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="you@example.com"
          required
          disabled={loading}
        />
        {emailError && (
          <p className="text-red-500 text-sm mt-1">{emailError}</p>
        )}
      </div>

      {/* Password field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium mb-2">
          Password <span className="text-red-500">*</span>
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value)
            setPasswordError(null)
          }}
          onBlur={() => validatePassword(password)}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            passwordError ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Minimum 8 characters"
          required
          disabled={loading}
        />
        {passwordError && (
          <p className="text-red-500 text-sm mt-1">{passwordError}</p>
        )}
      </div>

      {/* Confirm password field */}
      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium mb-2">
          Confirm Password <span className="text-red-500">*</span>
        </label>
        <input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => {
            setConfirmPassword(e.target.value)
            setConfirmError(null)
          }}
          onBlur={() => validateConfirmPassword(confirmPassword)}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            confirmError ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Re-enter password"
          required
          disabled={loading}
        />
        {confirmError && (
          <p className="text-red-500 text-sm mt-1">{confirmError}</p>
        )}
      </div>

      {/* Submit button */}
      <button
        type="submit"
        disabled={loading}
        className={`w-full px-6 py-3 text-white rounded-lg font-medium ${
          loading
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-green-600 hover:bg-green-700'
        }`}
      >
        {loading ? 'Creating account...' : 'Register'}
      </button>

      {/* Login link */}
      <p className="text-center text-sm text-gray-600">
        Already have an account?{' '}
        <a href="/login" className="text-blue-600 hover:text-blue-700 font-medium">
          Login
        </a>
      </p>
    </form>
  )
}
