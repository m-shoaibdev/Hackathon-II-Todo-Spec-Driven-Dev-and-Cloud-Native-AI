"""
In-memory data store for the Todo application.
Phase I implementation with in-memory storage only, no persistence.
"""

from typing import Dict, List, Optional
from src.models.todo import Todo


class InMemoryStore:
    """
    Manages todos in memory with basic CRUD operations.
    """

    def __init__(self):
        """
        Initialize an empty in-memory store with an auto-incrementing ID counter.
        """
        self.todos: Dict[int, Todo] = {}
        self._next_id = 1

    def add_todo(self, description: str) -> Todo:
        """
        Add a new todo to the store.

        Args:
            description (str): Description of the new todo

        Returns:
            Todo: The created Todo object
        """
        new_id = self._next_id
        self._next_id += 1

        todo = Todo(todo_id=new_id, description=description, completed=False)
        self.todos[new_id] = todo
        return todo

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """
        Get a specific todo by ID.

        Args:
            todo_id (int): ID of the todo to retrieve

        Returns:
            Todo: The Todo object if found, None otherwise
        """
        return self.todos.get(todo_id)

    def get_all_todos(self) -> List[Todo]:
        """
        Get all todos in the store.

        Returns:
            List[Todo]: List of all Todo objects
        """
        return list(self.todos.values())

    def update_todo(self, todo_id: int, description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Todo]:
        """
        Update an existing todo.

        Args:
            todo_id (int): ID of the todo to update
            description (Optional[str]): New description (if provided)
            completed (Optional[bool]): New completion status (if provided)

        Returns:
            Todo: Updated Todo object if successful, None if todo doesn't exist
        """
        if todo_id not in self.todos:
            return None

        todo = self.todos[todo_id]

        if description is not None:
            todo.update_description(description)

        if completed is not None:
            if completed:
                todo.mark_completed()
            else:
                todo.mark_incomplete()

        return todo

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo by ID.

        Args:
            todo_id (int): ID of the todo to delete

        Returns:
            bool: True if deletion was successful, False if todo didn't exist
        """
        if todo_id in self.todos:
            del self.todos[todo_id]
            return True
        return False

    def clear_all(self):
        """
        Clear all todos from the store.
        """
        self.todos.clear()
        self._next_id = 1

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new todo.

        Returns:
            int: The next available ID
        """
        return self._next_id