"""
Todo model for the In-Memory Console Todo App.
Phase I implementation with in-memory storage only.
"""

import datetime
from typing import Optional


class Todo:
    """
    Represents a single todo item with properties like id, description, and completion status.
    """

    def __init__(self, todo_id: int, description: str, completed: bool = False):
        """
        Initialize a Todo object.

        Args:
            todo_id (int): Unique identifier for the todo
            description (str): Description of the todo
            completed (bool): Whether the todo is completed, defaults to False
        """
        self.id = todo_id
        self.description = description
        self.completed = completed
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def mark_completed(self):
        """
        Mark the todo as completed.
        """
        self.completed = True
        self.updated_at = datetime.datetime.now()

    def mark_incomplete(self):
        """
        Mark the todo as incomplete.
        """
        self.completed = False
        self.updated_at = datetime.datetime.now()

    def update_description(self, new_description: str):
        """
        Update the todo description.

        Args:
            new_description (str): New description for the todo
        """
        self.description = new_description
        self.updated_at = datetime.datetime.now()

    def __str__(self):
        """
        String representation of the todo.
        """
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}: {self.description}"

    def __repr__(self):
        """
        Detailed representation of the todo.
        """
        return f"Todo(id={self.id}, description='{self.description}', completed={self.completed})"