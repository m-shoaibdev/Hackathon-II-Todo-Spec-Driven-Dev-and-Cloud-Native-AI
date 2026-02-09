"""
Service layer for the Todo application.
Handles business logic and coordinates between models and data store.
Phase I implementation with in-memory storage only.
"""

from typing import List, Optional
from src.models.todo import Todo
from src.datastore.in_memory_store import InMemoryStore


class TodoService:
    """
    Provides business logic for todo operations.
    """

    def __init__(self, store: InMemoryStore):
        """
        Initialize the TodoService with a data store.

        Args:
            store (InMemoryStore): The data store to use
        """
        self.store = store

    def add_todo(self, description: str) -> Todo:
        """
        Add a new todo with the given description.

        Args:
            description (str): Description of the new todo

        Returns:
            Todo: The created Todo object
        """
        if not description or description.strip() == "":
            raise ValueError("Todo description cannot be empty")

        return self.store.add_todo(description.strip())

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """
        Get a specific todo by ID.

        Args:
            todo_id (int): ID of the todo to retrieve

        Returns:
            Todo: The Todo object if found, None otherwise
        """
        return self.store.get_todo(todo_id)

    def get_all_todos(self) -> List[Todo]:
        """
        Get all todos.

        Returns:
            List[Todo]: List of all Todo objects
        """
        return self.store.get_all_todos()

    def update_todo(self, todo_id: int, description: Optional[str] = None, completed: Optional[bool] = None) -> bool:
        """
        Update an existing todo.

        Args:
            todo_id (int): ID of the todo to update
            description (Optional[str]): New description (if provided)
            completed (Optional[bool]): New completion status (if provided)

        Returns:
            bool: True if update was successful, False if todo doesn't exist
        """
        if description is not None and (not description or description.strip() == ""):
            raise ValueError("Todo description cannot be empty")

        updated_todo = self.store.update_todo(
            todo_id,
            description.strip() if description else None,
            completed
        )
        return updated_todo is not None

    def complete_todo(self, todo_id: int) -> bool:
        """
        Mark a todo as completed.

        Args:
            todo_id (int): ID of the todo to mark as completed

        Returns:
            bool: True if successful, False if todo doesn't exist
        """
        return self.store.update_todo(todo_id, completed=True) is not None

    def incomplete_todo(self, todo_id: int) -> bool:
        """
        Mark a todo as incomplete.

        Args:
            todo_id (int): ID of the todo to mark as incomplete

        Returns:
            bool: True if successful, False if todo doesn't exist
        """
        return self.store.update_todo(todo_id, completed=False) is not None

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo by ID.

        Args:
            todo_id (int): ID of the todo to delete

        Returns:
            bool: True if deletion was successful, False if todo doesn't exist
        """
        return self.store.delete_todo(todo_id)

    def clear_all_todos(self):
        """
        Clear all todos from the store.
        """
        self.store.clear_all()