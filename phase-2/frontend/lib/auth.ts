/**
 * Better Auth configuration for JWT-based authentication
 *
 * Phase II: Simplified approach using localStorage
 * Tokens managed by backend, Better Auth used for client utilities
 */

import { createAuthClient } from "better-auth/client"

/**
 * Better Auth client instance
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL || "http://localhost:3000",
})

/**
 * Get the current user from localStorage
 *
 * @returns User object if authenticated, null otherwise
 */
export function getCurrentUser() {
  try {
    if (typeof window === 'undefined') return null

    const userJson = localStorage.getItem('user')
    if (!userJson) return null

    return JSON.parse(userJson)
  } catch (error) {
    console.error("Failed to get current user:", error)
    return null
  }
}

/**
 * Check if user is authenticated
 *
 * @returns boolean - True if user has valid session
 */
export function isAuthenticated(): boolean {
  const user = getCurrentUser()
  const token = getAuthToken()
  return user !== null && token !== null
}

/**
 * Sign out the current user
 *
 * Clears the session and JWT token from localStorage
 */
export function signOut(): void {
  try {
    if (typeof window === 'undefined') return

    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
  } catch (error) {
    console.error("Failed to sign out:", error)
    throw error
  }
}

/**
 * Get JWT token from localStorage for API requests
 *
 * @returns string | null - JWT token if authenticated
 */
export function getAuthToken(): string | null {
  try {
    if (typeof window === 'undefined') return null

    const token = localStorage.getItem('auth_token')

    // TODO Phase III: Add token refresh logic
    // - Decode JWT to check expiry
    // - If token expires in < 5 minutes, refresh it
    // - Implement refresh token rotation

    return token
  } catch (error) {
    console.error("Failed to get auth token:", error)
    return null
  }
}
