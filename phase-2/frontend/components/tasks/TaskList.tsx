/**
 * TaskList component - Display list of tasks
 *
 * Maps array of tasks to TaskItem components
 */

import type { Task } from '@/types/task'
import TaskItem from './TaskItem'

interface TaskListProps {
  /**
   * Array of tasks to display
   */
  tasks: Task[]

  /**
   * Optional callback when task is clicked
   */
  onTaskClick?: (task: Task) => void

  /**
   * Optional callback when task completion is toggled
   */
  onToggleComplete?: (task: Task) => Promise<void>

  /**
   * Optional callback when task is deleted
   */
  onDelete?: (task: Task) => Promise<void>

  /**
   * Optional empty state message
   */
  emptyMessage?: string
}

export default function TaskList({
  tasks,
  onTaskClick,
  onToggleComplete,
  onDelete,
  emptyMessage = 'No tasks yet',
}: TaskListProps) {
  /**
   * Empty state
   */
  if (tasks.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-12 text-center">
        <div className="text-gray-400 mb-4">
          <svg
            className="mx-auto h-12 w-12"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          {emptyMessage}
        </h3>
        <p className="text-gray-500">
          Create your first task to get started!
        </p>
      </div>
    )
  }

  /**
   * Task list
   */
  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onClick={onTaskClick}
          onToggleComplete={onToggleComplete}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
