/**
 * User type definitions
 *
 * These types match the User entity managed by Better Auth
 * and referenced by the backend API.
 */

/**
 * User entity (managed by Better Auth)
 */
export interface User {
  /**
   * Unique user identifier (UUID from Better Auth)
   */
  id: string

  /**
   * User email address (unique, validated)
   */
  email: string

  /**
   * User display name (optional)
   */
  name?: string | null

  /**
   * Account creation timestamp
   */
  createdAt: Date
}

/**
 * User registration request payload
 */
export interface RegisterRequest {
  /**
   * Email address (required, must be valid email format)
   */
  email: string

  /**
   * Password (required, minimum 8 characters)
   */
  password: string

  /**
   * Display name (optional)
   */
  name?: string
}

/**
 * User login request payload
 */
export interface LoginRequest {
  /**
   * Email address
   */
  email: string

  /**
   * Password
   */
  password: string
}

/**
 * Authentication response from backend
 */
export interface AuthResponse {
  /**
   * User information
   */
  user: User

  /**
   * JWT access token
   */
  token: string

  /**
   * Token expiration timestamp
   */
  expiresAt: Date
}

/**
 * Better Auth session type
 */
export interface Session {
  /**
   * Authenticated user
   */
  user: User

  /**
   * Session token (JWT)
   */
  token: string

  /**
   * Session expiration timestamp
   */
  expiresAt: Date
}
