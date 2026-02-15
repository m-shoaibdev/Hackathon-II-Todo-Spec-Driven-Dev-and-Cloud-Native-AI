'use client'

/**
 * Authentication context for app-wide auth state management
 *
 * Provides:
 * - Current user information
 * - Authentication status
 * - Login/logout/register functions
 */

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import { post } from '@/lib/api-client'
import type { User, RegisterRequest, LoginRequest } from '@/types/user'

interface AuthContextType {
  /**
   * Currently authenticated user (null if not authenticated)
   */
  user: User | null

  /**
   * Whether auth state is being loaded
   */
  loading: boolean

  /**
   * Register a new user account
   */
  register: (request: RegisterRequest) => Promise<void>

  /**
   * Login with email and password
   */
  login: (request: LoginRequest) => Promise<void>

  /**
   * Logout the current user
   */
  logout: () => void

  /**
   * Refresh user data from localStorage
   */
  refreshUser: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  /**
   * Load user from localStorage on mount
   */
  useEffect(() => {
    try {
      const token = localStorage.getItem('auth_token')
      const userJson = localStorage.getItem('user')

      if (token && userJson) {
        const userData = JSON.parse(userJson)
        setUser(userData)
      }
    } catch (error) {
      console.error('Failed to load user:', error)
      // Clear invalid data
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Register a new user
   */
  const register = async (request: RegisterRequest) => {
    try {
      const response = await post('/auth/register', request)

      // Store token and user
      if (response.token) {
        localStorage.setItem('auth_token', response.token)
      }
      if (response.user) {
        localStorage.setItem('user', JSON.stringify(response.user))
        setUser(response.user)
      }

      // Redirect to dashboard
      router.push('/dashboard')
    } catch (error) {
      throw error // Re-throw for form to handle
    }
  }

  /**
   * Login existing user
   */
  const login = async (request: LoginRequest) => {
    try {
      const response = await post('/auth/login', request)

      // Store token and user
      if (response.token) {
        localStorage.setItem('auth_token', response.token)
      }
      if (response.user) {
        localStorage.setItem('user', JSON.stringify(response.user))
        setUser(response.user)
      }

      // Redirect to dashboard
      router.push('/dashboard')
    } catch (error) {
      throw error // Re-throw for form to handle
    }
  }

  /**
   * Logout current user
   */
  const logout = () => {
    // Clear storage
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')

    // Clear state
    setUser(null)

    // Redirect to home
    router.push('/')
  }

  /**
   * Refresh user data from localStorage
   */
  const refreshUser = () => {
    try {
      const userJson = localStorage.getItem('user')
      if (userJson) {
        const userData = JSON.parse(userJson)
        setUser(userData)
      }
    } catch (error) {
      console.error('Failed to refresh user:', error)
    }
  }

  const value: AuthContextType = {
    user,
    loading,
    register,
    login,
    logout,
    refreshUser,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

/**
 * Hook to access auth context
 *
 * @throws Error if used outside AuthProvider
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }

  return context
}
