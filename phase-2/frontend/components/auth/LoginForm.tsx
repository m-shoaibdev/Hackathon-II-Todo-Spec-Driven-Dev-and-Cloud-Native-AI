'use client'

/**
 * Login form component
 *
 * Handles user authentication with email/password
 * and JWT token storage.
 */

import { useState, FormEvent } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { type LoginRequest } from '@/types/user'

interface LoginFormProps {
  /**
   * Callback invoked on successful login
   */
  onSuccess?: () => void
}

export default function LoginForm({ onSuccess }: LoginFormProps) {
  const { login } = useAuth()

  // Form state
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  // UI state
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  /**
   * Handle form submission
   */
  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)

    // Basic validation
    if (!email || !password) {
      setError('Please enter both email and password')
      return
    }

    setLoading(true)

    try {
      // Prepare request payload
      const request: LoginRequest = {
        email,
        password,
      }

      // Call login via AuthContext (handles token storage and redirect)
      await login(request)

      // Call success callback if provided
      if (onSuccess) {
        onSuccess()
      }
    } catch (err: any) {
      setError(err.message || 'Invalid email or password')
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

      {/* Email field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-2">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="you@example.com"
          required
          disabled={loading}
        />
      </div>

      {/* Password field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium mb-2">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Your password"
          required
          disabled={loading}
        />
      </div>

      {/* Submit button */}
      <button
        type="submit"
        disabled={loading}
        className={`w-full px-6 py-3 text-white rounded-lg font-medium ${
          loading
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700'
        }`}
      >
        {loading ? 'Logging in...' : 'Login'}
      </button>

      {/* Registration link */}
      <p className="text-center text-sm text-gray-600">
        Don't have an account?{' '}
        <a href="/register" className="text-blue-600 hover:text-blue-700 font-medium">
          Register
        </a>
      </p>
    </form>
  )
}
