/**
 * Task type definitions
 *
 * These types match the Task entity managed by the backend API
 * and enforce the data contracts defined in the specification.
 */

/**
 * Task entity (managed by backend)
 */
export interface Task {
  /**
   * Unique task identifier (auto-increment)
   */
  id: number

  /**
   * Owner user ID (UUID reference to User.id)
   */
  userId: string

  /**
   * Task title (1-200 characters, required)
   */
  title: string

  /**
   * Task description (max 1000 characters, optional)
   */
  description: string | null

  /**
   * Completion status (default: false)
   */
  completed: boolean

  /**
   * Task creation timestamp
   */
  createdAt: Date

  /**
   * Last update timestamp
   */
  updatedAt: Date
}

/**
 * Request payload for creating a new task
 */
export interface CreateTaskRequest {
  /**
   * Task title (required, 1-200 characters)
   */
  title: string

  /**
   * Task description (optional, max 1000 characters)
   */
  description?: string
}

/**
 * Request payload for updating an existing task
 */
export interface UpdateTaskRequest {
  /**
   * Updated task title (optional, 1-200 characters)
   */
  title?: string

  /**
   * Updated task description (optional, max 1000 characters)
   */
  description?: string | null
}

/**
 * Task list filter options
 */
export interface TaskFilter {
  /**
   * Filter by completion status
   */
  completed?: boolean

  /**
   * Search query for title/description
   */
  search?: string

  /**
   * Sort order (newest first or oldest first)
   */
  sortOrder?: "asc" | "desc"
}

/**
 * Task API response wrapper
 */
export interface TaskListResponse {
  /**
   * Array of tasks
   */
  tasks: Task[]

  /**
   * Total count of tasks (may differ from tasks.length if paginated)
   */
  total: number
}

/**
 * Task form validation errors
 */
export interface TaskValidationErrors {
  /**
   * Title validation error message
   */
  title?: string

  /**
   * Description validation error message
   */
  description?: string

  /**
   * General form error message
   */
  form?: string
}

/**
 * Validate task title
 *
 * @param title - Task title to validate
 * @returns Error message if invalid, undefined if valid
 */
export function validateTaskTitle(title: string): string | undefined {
  if (!title || title.trim().length === 0) {
    return "Title is required"
  }
  if (title.length > 200) {
    return "Title must be 200 characters or less"
  }
  return undefined
}

/**
 * Validate task description
 *
 * @param description - Task description to validate
 * @returns Error message if invalid, undefined if valid
 */
export function validateTaskDescription(
  description: string | null | undefined
): string | undefined {
  if (description && description.length > 1000) {
    return "Description must be 1000 characters or less"
  }
  return undefined
}

/**
 * Validate task creation request
 *
 * @param request - Create task request payload
 * @returns Validation errors object (empty if valid)
 */
export function validateCreateTask(
  request: CreateTaskRequest
): TaskValidationErrors {
  const errors: TaskValidationErrors = {}

  const titleError = validateTaskTitle(request.title)
  if (titleError) {
    errors.title = titleError
  }

  const descriptionError = validateTaskDescription(request.description)
  if (descriptionError) {
    errors.description = descriptionError
  }

  return errors
}
