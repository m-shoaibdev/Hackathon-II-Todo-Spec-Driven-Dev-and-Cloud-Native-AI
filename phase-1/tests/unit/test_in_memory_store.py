"""
Unit tests for the InMemoryStore in the Todo application.
Phase I implementation with in-memory storage only.
"""

import pytest
from src.datastore.in_memory_store import InMemoryStore
from src.models.todo import Todo


class TestInMemoryStore:
    """Test cases for the InMemoryStore."""

    def test_initial_state(self):
        """Test initial state of the store."""
        store = InMemoryStore()
        assert len(store.todos) == 0
        assert store._next_id == 1

    def test_add_todo(self):
        """Test adding a new todo."""
        store = InMemoryStore()
        todo = store.add_todo("Test task")

        assert todo.id == 1
        assert todo.description == "Test task"
        assert todo.completed is False
        assert len(store.todos) == 1
        assert store.todos[1] == todo
        assert store._next_id == 2

    def test_get_todo_exists(self):
        """Test retrieving an existing todo."""
        store = InMemoryStore()
        added_todo = store.add_todo("Test task")
        retrieved_todo = store.get_todo(1)

        assert retrieved_todo is not None
        assert retrieved_todo.id == 1
        assert retrieved_todo.description == "Test task"

    def test_get_todo_not_exists(self):
        """Test retrieving a non-existent todo."""
        store = InMemoryStore()
        todo = store.get_todo(999)

        assert todo is None

    def test_get_all_todos_empty(self):
        """Test getting all todos when the store is empty."""
        store = InMemoryStore()
        todos = store.get_all_todos()

        assert len(todos) == 0

    def test_get_all_todos_with_items(self):
        """Test getting all todos when the store has items."""
        store = InMemoryStore()
        store.add_todo("Task 1")
        store.add_todo("Task 2")
        store.add_todo("Task 3")

        todos = store.get_all_todos()

        assert len(todos) == 3
        descriptions = [todo.description for todo in todos]
        assert "Task 1" in descriptions
        assert "Task 2" in descriptions
        assert "Task 3" in descriptions

    def test_update_todo_description(self):
        """Test updating a todo's description."""
        store = InMemoryStore()
        todo = store.add_todo("Old task")

        updated = store.update_todo(1, description="New task")

        assert updated is not None
        assert updated.id == 1
        assert updated.description == "New task"
        assert store.todos[1].description == "New task"

    def test_update_todo_completion(self):
        """Test updating a todo's completion status."""
        store = InMemoryStore()
        todo = store.add_todo("Test task")

        updated = store.update_todo(1, completed=True)

        assert updated is not None
        assert updated.id == 1
        assert updated.completed is True
        assert store.todos[1].completed is True

    def test_update_todo_both_fields(self):
        """Test updating both description and completion status."""
        store = InMemoryStore()
        todo = store.add_todo("Old task")

        updated = store.update_todo(1, description="New task", completed=True)

        assert updated is not None
        assert updated.id == 1
        assert updated.description == "New task"
        assert updated.completed is True

    def test_update_todo_not_exists(self):
        """Test updating a non-existent todo."""
        store = InMemoryStore()
        result = store.update_todo(999, description="New task")

        assert result is None

    def test_delete_todo_exists(self):
        """Test deleting an existing todo."""
        store = InMemoryStore()
        store.add_todo("Test task")

        result = store.delete_todo(1)

        assert result is True
        assert len(store.todos) == 0
        assert store.get_todo(1) is None

    def test_delete_todo_not_exists(self):
        """Test deleting a non-existent todo."""
        store = InMemoryStore()
        result = store.delete_todo(999)

        assert result is False

    def test_clear_all(self):
        """Test clearing all todos."""
        store = InMemoryStore()
        store.add_todo("Task 1")
        store.add_todo("Task 2")

        assert len(store.todos) == 2

        store.clear_all()

        assert len(store.todos) == 0
        assert store._next_id == 1  # Reset to 1 after clearing

    def test_get_next_id(self):
        """Test getting the next available ID."""
        store = InMemoryStore()

        assert store.get_next_id() == 1

        store.add_todo("Task 1")

        assert store.get_next_id() == 2