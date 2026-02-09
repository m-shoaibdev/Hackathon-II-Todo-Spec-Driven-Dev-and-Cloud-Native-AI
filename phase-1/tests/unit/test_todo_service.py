"""
Unit tests for the TodoService in the Todo application.
Phase I implementation with in-memory storage only.
"""

import pytest
from src.services.todo_service import TodoService
from src.datastore.in_memory_store import InMemoryStore
from src.models.todo import Todo


class TestTodoService:
    """Test cases for the TodoService."""

    def setup_method(self):
        """Set up a fresh service for each test."""
        self.store = InMemoryStore()
        self.service = TodoService(self.store)

    def test_add_todo_success(self):
        """Test successfully adding a new todo."""
        todo = self.service.add_todo("Test task")

        assert todo.id == 1
        assert todo.description == "Test task"
        assert todo.completed is False
        assert len(self.store.todos) == 1

    def test_add_todo_empty_description(self):
        """Test adding a todo with empty description raises error."""
        with pytest.raises(ValueError, match="Todo description cannot be empty"):
            self.service.add_todo("")

        with pytest.raises(ValueError, match="Todo description cannot be empty"):
            self.service.add_todo("   ")

    def test_get_todo_exists(self):
        """Test retrieving an existing todo."""
        added_todo = self.service.add_todo("Test task")

        retrieved_todo = self.service.get_todo(1)

        assert retrieved_todo is not None
        assert retrieved_todo.id == 1
        assert retrieved_todo.description == "Test task"

    def test_get_todo_not_exists(self):
        """Test retrieving a non-existent todo."""
        retrieved_todo = self.service.get_todo(999)

        assert retrieved_todo is None

    def test_get_all_todos_empty(self):
        """Test getting all todos when there are none."""
        todos = self.service.get_all_todos()

        assert len(todos) == 0

    def test_get_all_todos_with_items(self):
        """Test getting all todos when there are items."""
        self.service.add_todo("Task 1")
        self.service.add_todo("Task 2")

        todos = self.service.get_all_todos()

        assert len(todos) == 2
        ids = [todo.id for todo in todos]
        assert 1 in ids
        assert 2 in ids

    def test_update_todo_description(self):
        """Test updating a todo's description."""
        self.service.add_todo("Old task")

        result = self.service.update_todo(1, description="New task")

        assert result is True
        updated_todo = self.service.get_todo(1)
        assert updated_todo.description == "New task"

    def test_update_todo_completion(self):
        """Test updating a todo's completion status."""
        self.service.add_todo("Test task")

        result = self.service.update_todo(1, completed=True)

        assert result is True
        updated_todo = self.service.get_todo(1)
        assert updated_todo.completed is True

    def test_update_todo_both_fields(self):
        """Test updating both description and completion status."""
        self.service.add_todo("Old task")

        result = self.service.update_todo(1, description="New task", completed=True)

        assert result is True
        updated_todo = self.service.get_todo(1)
        assert updated_todo.description == "New task"
        assert updated_todo.completed is True

    def test_update_todo_not_exists(self):
        """Test updating a non-existent todo."""
        result = self.service.update_todo(999, description="New task")

        assert result is False

    def test_update_todo_empty_description(self):
        """Test updating a todo with empty description raises error."""
        self.service.add_todo("Test task")

        with pytest.raises(ValueError, match="Todo description cannot be empty"):
            self.service.update_todo(1, description="")

        with pytest.raises(ValueError, match="Todo description cannot be empty"):
            self.service.update_todo(1, description="   ")

    def test_complete_todo_exists(self):
        """Test completing an existing todo."""
        self.service.add_todo("Test task")

        result = self.service.complete_todo(1)

        assert result is True
        updated_todo = self.service.get_todo(1)
        assert updated_todo.completed is True

    def test_complete_todo_not_exists(self):
        """Test completing a non-existent todo."""
        result = self.service.complete_todo(999)

        assert result is False

    def test_incomplete_todo_exists(self):
        """Test marking an existing todo as incomplete."""
        self.service.add_todo("Test task")
        self.service.complete_todo(1)  # First mark as complete

        result = self.service.incomplete_todo(1)

        assert result is True
        updated_todo = self.service.get_todo(1)
        assert updated_todo.completed is False

    def test_incomplete_todo_not_exists(self):
        """Test marking a non-existent todo as incomplete."""
        result = self.service.incomplete_todo(999)

        assert result is False

    def test_delete_todo_exists(self):
        """Test deleting an existing todo."""
        self.service.add_todo("Test task")

        result = self.service.delete_todo(1)

        assert result is True
        assert self.service.get_todo(1) is None
        assert len(self.store.todos) == 0

    def test_delete_todo_not_exists(self):
        """Test deleting a non-existent todo."""
        result = self.service.delete_todo(999)

        assert result is False

    def test_clear_all_todos(self):
        """Test clearing all todos."""
        self.service.add_todo("Task 1")
        self.service.add_todo("Task 2")

        assert len(self.service.get_all_todos()) == 2

        self.service.clear_all_todos()

        assert len(self.service.get_all_todos()) == 0