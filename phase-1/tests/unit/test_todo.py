"""
Unit tests for the Todo model in the Todo application.
Phase I implementation with in-memory storage only.
"""

import pytest
from src.models.todo import Todo


class TestTodo:
    """Test cases for the Todo model."""

    def test_create_todo(self):
        """Test creating a new Todo object."""
        todo = Todo(1, "Test task")
        assert todo.id == 1
        assert todo.description == "Test task"
        assert todo.completed is False

    def test_create_completed_todo(self):
        """Test creating a Todo object with completed status."""
        todo = Todo(1, "Test task", completed=True)
        assert todo.id == 1
        assert todo.description == "Test task"
        assert todo.completed is True

    def test_mark_completed(self):
        """Test marking a todo as completed."""
        todo = Todo(1, "Test task")
        assert todo.completed is False
        todo.mark_completed()
        assert todo.completed is True

    def test_mark_incomplete(self):
        """Test marking a todo as incomplete."""
        todo = Todo(1, "Test task", completed=True)
        assert todo.completed is True
        todo.mark_incomplete()
        assert todo.completed is False

    def test_update_description(self):
        """Test updating a todo's description."""
        todo = Todo(1, "Old description")
        assert todo.description == "Old description"
        todo.update_description("New description")
        assert todo.description == "New description"

    def test_str_representation(self):
        """Test string representation of a todo."""
        todo = Todo(1, "Test task")
        assert str(todo) == "[○] 1: Test task"

        todo.mark_completed()
        assert str(todo) == "[✓] 1: Test task"

    def test_repr_representation(self):
        """Test detailed representation of a todo."""
        todo = Todo(1, "Test task", completed=True)
        expected = "Todo(id=1, description='Test task', completed=True)"
        assert repr(todo) == expected