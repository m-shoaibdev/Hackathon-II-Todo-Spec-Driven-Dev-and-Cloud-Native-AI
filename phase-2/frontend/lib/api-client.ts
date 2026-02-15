/**
 * API client for making authenticated requests to the backend
 *
 * This module provides a centralized fetch wrapper that:
 * 1. Automatically attaches JWT tokens to requests
 * 2. Handles common error responses (401, 403, 404, 500)
 * 3. Provides type-safe request/response handling
 */

import { getAuthToken } from "./auth"

/**
 * Base API URL from environment variable
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

/**
 * API error class for structured error handling
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public response?: any
  ) {
    super(message)
    this.name = "ApiError"
  }
}

/**
 * Make an authenticated API request
 *
 * @param endpoint - API endpoint (e.g., "/api/user_123/tasks")
 * @param options - Fetch options (method, body, headers, etc.)
 * @returns Promise<T> - Parsed JSON response
 * @throws {ApiError} - If request fails or returns error status
 *
 * @example
 * ```typescript
 * const tasks = await apiRequest<Task[]>("/api/user_123/tasks")
 * const task = await apiRequest<Task>("/api/user_123/tasks", {
 *   method: "POST",
 *   body: JSON.stringify({ title: "New task" })
 * })
 * ```
 */
export async function apiRequest<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Get JWT token from localStorage
  const token = getAuthToken()

  // Build headers
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  }

  // Add Authorization header if token exists
  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }

  // Make request
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include", // Include cookies
  })

  // Handle error responses
  if (!response.ok) {
    let errorMessage = `Request failed with status ${response.status}`
    let errorData: any

    try {
      errorData = await response.json()
      errorMessage = errorData.detail || errorMessage
    } catch {
      // Response body is not JSON or empty
      errorMessage = response.statusText || errorMessage
    }

    // Handle 401 Unauthorized - redirect to login
    if (response.status === 401) {
      // Clear auth data
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user')
        // Redirect to login page
        window.location.href = '/login?error=session_expired'
      }
      throw new ApiError('Session expired. Please login again.', response.status, errorData)
    }

    // Handle 403 Forbidden - user_id mismatch or permission denied
    if (response.status === 403) {
      // This indicates a serious issue (user_id mismatch or tampering)
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user')
        // Redirect to login with error
        window.location.href = '/login?error=access_denied'
      }
      throw new ApiError('Access denied. Please login again.', response.status, errorData)
    }

    throw new ApiError(errorMessage, response.status, errorData)
  }

  // Handle empty responses (e.g., 204 No Content)
  if (response.status === 204 || response.headers.get("content-length") === "0") {
    return undefined as T
  }

  // Parse and return JSON response
  return response.json()
}

/**
 * GET request helper
 *
 * @param endpoint - API endpoint
 * @returns Promise<T> - Parsed JSON response
 */
export async function get<T = any>(endpoint: string): Promise<T> {
  return apiRequest<T>(endpoint, { method: "GET" })
}

/**
 * POST request helper
 *
 * @param endpoint - API endpoint
 * @param data - Request body data
 * @returns Promise<T> - Parsed JSON response
 */
export async function post<T = any>(endpoint: string, data?: any): Promise<T> {
  return apiRequest<T>(endpoint, {
    method: "POST",
    body: data ? JSON.stringify(data) : undefined,
  })
}

/**
 * PUT request helper
 *
 * @param endpoint - API endpoint
 * @param data - Request body data
 * @returns Promise<T> - Parsed JSON response
 */
export async function put<T = any>(endpoint: string, data?: any): Promise<T> {
  return apiRequest<T>(endpoint, {
    method: "PUT",
    body: data ? JSON.stringify(data) : undefined,
  })
}

/**
 * PATCH request helper
 *
 * @param endpoint - API endpoint
 * @param data - Request body data
 * @returns Promise<T> - Parsed JSON response
 */
export async function patch<T = any>(endpoint: string, data?: any): Promise<T> {
  return apiRequest<T>(endpoint, {
    method: "PATCH",
    body: data ? JSON.stringify(data) : undefined,
  })
}

/**
 * DELETE request helper
 *
 * @param endpoint - API endpoint
 * @returns Promise<void>
 */
export async function del(endpoint: string): Promise<void> {
  return apiRequest<void>(endpoint, { method: "DELETE" })
}
