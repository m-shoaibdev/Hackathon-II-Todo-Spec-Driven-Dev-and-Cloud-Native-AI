/**
 * Task service for API operations
 *
 * Provides functions to interact with task endpoints
 */

import { get, post, put, patch, del } from '@/lib/api-client'
import type { Task, CreateTaskRequest, UpdateTaskRequest } from '@/types/task'

/**
 * Get all tasks for a user
 *
 * @param userId - User ID
 * @returns Promise<Task[]> - Array of tasks
 */
export async function getTasks(userId: string): Promise<Task[]> {
  return get<Task[]>(`/api/${userId}/tasks`)
}

/**
 * Get a specific task by ID
 *
 * @param userId - User ID
 * @param taskId - Task ID
 * @returns Promise<Task> - The requested task
 */
export async function getTask(userId: string, taskId: number): Promise<Task> {
  return get<Task>(`/api/${userId}/tasks/${taskId}`)
}

/**
 * Create a new task
 *
 * @param userId - User ID
 * @param data - Task creation data
 * @returns Promise<Task> - Newly created task
 */
export async function createTask(
  userId: string,
  data: CreateTaskRequest
): Promise<Task> {
  return post<Task>(`/api/${userId}/tasks`, data)
}

/**
 * Update an existing task
 *
 * @param userId - User ID
 * @param taskId - Task ID
 * @param data - Task update data
 * @returns Promise<Task> - Updated task
 */
export async function updateTask(
  userId: string,
  taskId: number,
  data: UpdateTaskRequest
): Promise<Task> {
  return put<Task>(`/api/${userId}/tasks/${taskId}`, data)
}

/**
 * Toggle task completion status
 *
 * @param userId - User ID
 * @param taskId - Task ID
 * @returns Promise<Task> - Task with toggled completion
 */
export async function toggleComplete(
  userId: string,
  taskId: number
): Promise<Task> {
  return patch<Task>(`/api/${userId}/tasks/${taskId}/complete`)
}

/**
 * Delete a task
 *
 * @param userId - User ID
 * @param taskId - Task ID
 * @returns Promise<void>
 */
export async function deleteTask(
  userId: string,
  taskId: number
): Promise<void> {
  return del(`/api/${userId}/tasks/${taskId}`)
}
