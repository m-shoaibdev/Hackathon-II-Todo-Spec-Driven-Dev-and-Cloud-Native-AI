"""
Contract tests for the CLI interface in the Todo application.
Phase I implementation with in-memory storage only.
"""

import io
import sys
from unittest.mock import patch, MagicMock
import pytest
from src.cli.console import TodoConsole


class TestTodoConsole:
    """Test cases for the TodoConsole."""

    def setup_method(self):
        """Set up a fresh console for each test."""
        self.console = TodoConsole()

    def test_display_welcome(self):
        """Test the welcome message display."""
        # Capture printed output
        with patch('builtins.print') as mock_print:
            self.console.display_welcome()

            # Check that print was called with expected messages
            assert mock_print.call_count >= 2  # At least welcome and instruction messages

    def test_display_todo_list_empty(self):
        """Test displaying an empty todo list."""
        with patch('builtins.print') as mock_print:
            self.console.display_todo_list()

            # Check that appropriate message for empty list was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            empty_message_found = any("empty" in text.lower() for text in printed_texts)
            assert empty_message_found

    def test_display_todo_list_with_items(self):
        """Test displaying a todo list with items."""
        # Add a todo
        self.console.service.add_todo("Test task")

        with patch('builtins.print') as mock_print:
            self.console.display_todo_list()

            # Check that the todo was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            task_found = any("test task" in text.lower() for text in printed_texts)
            assert task_found

    def test_handle_add_command_success(self):
        """Test handling an add command successfully."""
        with patch('builtins.print') as mock_print:
            self.console.handle_add_command("New test task")

            # Check that the success message was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            success_message_found = any("added todo" in text.lower() for text in printed_texts)
            assert success_message_found

    def test_handle_add_command_empty_description(self):
        """Test handling an add command with empty description."""
        with patch('builtins.print') as mock_print:
            self.console.handle_add_command("")

            # Check that the error message was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            error_message_found = any("error" in text.lower() and "cannot be empty" in text.lower() for text in printed_texts)
            assert error_message_found

    def test_handle_list_command(self):
        """Test handling a list command."""
        # Add a todo first
        self.console.service.add_todo("Test task")

        with patch.object(self.console, 'display_todo_list') as mock_display:
            self.console.handle_list_command()

            # Check that display_todo_list was called
            mock_display.assert_called_once()

    def test_handle_complete_command_success(self):
        """Test handling a complete command successfully."""
        # Add a todo first
        todo = self.console.service.add_todo("Test task")

        with patch('builtins.print') as mock_print:
            self.console.handle_complete_command(todo.id)

            # Check that the success message was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            success_message_found = any("marked" in text.lower() and "completed" in text.lower() for text in printed_texts)
            assert success_message_found

    def test_handle_complete_command_not_found(self):
        """Test handling a complete command for non-existent todo."""
        with patch('builtins.print') as mock_print:
            self.console.handle_complete_command(999)

            # Check that the error message was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            error_message_found = any("not found" in text.lower() for text in printed_texts)
            assert error_message_found

    def test_handle_incomplete_command_success(self):
        """Test handling an incomplete command successfully."""
        # Add and complete a todo first
        todo = self.console.service.add_todo("Test task")
        self.console.service.complete_todo(todo.id)

        with patch('builtins.print') as mock_print:
            self.console.handle_incomplete_command(todo.id)

            # Check that the success message was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            success_message_found = any("marked" in text.lower() and "incomplete" in text.lower() for text in printed_texts)
            assert success_message_found

    def test_handle_delete_command_success(self):
        """Test handling a delete command successfully."""
        # Add a todo first
        todo = self.console.service.add_todo("Test task")

        with patch('builtins.print') as mock_print:
            self.console.handle_delete_command(todo.id)

            # Check that the success message was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            success_message_found = any("deleted" in text.lower() for text in printed_texts)
            assert success_message_found

    def test_handle_delete_command_not_found(self):
        """Test handling a delete command for non-existent todo."""
        with patch('builtins.print') as mock_print:
            self.console.handle_delete_command(999)

            # Check that the error message was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            error_message_found = any("not found" in text.lower() for text in printed_texts)
            assert error_message_found

    def test_handle_clear_command(self):
        """Test handling a clear command."""
        # Add some todos first
        self.console.service.add_todo("Test task 1")
        self.console.service.add_todo("Test task 2")

        with patch('builtins.print') as mock_print:
            self.console.handle_clear_command()

            # Check that the success message was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            success_message_found = any("cleared" in text.lower() for text in printed_texts)
            assert success_message_found

            # Check that all todos were cleared
            assert len(self.console.service.get_all_todos()) == 0

    def test_handle_help_command(self):
        """Test handling a help command."""
        with patch('builtins.print') as mock_print:
            self.console.handle_help_command()

            # Check that help text was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            help_content_found = any(any(keyword in text.lower() for keyword in ['add', 'list', 'complete', 'delete', 'help', 'quit']) for text in printed_texts)
            assert help_content_found

    def test_execute_command_add(self):
        """Test executing an add command."""
        with patch.object(self.console, 'handle_add_command') as mock_handler:
            parsed_cmd = MagicMock()
            parsed_cmd.cmd_type = self.console.parser.parse("add Test task").cmd_type
            parsed_cmd.args = ["test task"]

            self.console.execute_command(parsed_cmd)

            # Check that the appropriate handler was called
            mock_handler.assert_called_once_with("test task")

    def test_execute_command_unknown(self):
        """Test executing an unknown command type."""
        with patch('builtins.print') as mock_print:
            # Create a fake command type
            from src.parser.commands import CommandType
            parsed_cmd = MagicMock()
            parsed_cmd.cmd_type = "UNKNOWN_TYPE"
            parsed_cmd.args = []

            self.console.execute_command(parsed_cmd)

            # Check that an error message was printed
            printed_texts = [call[0][0] if call[0] else "" for call in mock_print.call_args_list if call[0]]
            error_message_found = any("unknown command type" in text.lower() for text in printed_texts)
            assert error_message_found