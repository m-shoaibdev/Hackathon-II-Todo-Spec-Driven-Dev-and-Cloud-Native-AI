"""
Unit tests for the CommandParser in the Todo application.
Phase I implementation with in-memory storage only.
"""

import pytest
from src.parser.commands import CommandParser, CommandType, ParsedCommand


class TestCommandParser:
    """Test cases for the CommandParser."""

    def setup_method(self):
        """Set up a fresh parser for each test."""
        self.parser = CommandParser()

    def test_parse_add_command_with_explicit_keyword(self):
        """Test parsing an add command with explicit 'add' keyword."""
        result = self.parser.parse("add Buy groceries")

        assert result is not None
        assert result.cmd_type == CommandType.ADD
        assert result.args == ["buy groceries"]

    def test_parse_add_command_shortcut(self):
        """Test parsing an add command with shortcut 'a'."""
        result = self.parser.parse("a Finish report")

        assert result is not None
        assert result.cmd_type == CommandType.ADD
        assert result.args == ["finish report"]

    def test_parse_add_command_without_keyword(self):
        """Test parsing an add command without explicit keyword."""
        result = self.parser.parse("Clean the house")

        assert result is not None
        assert result.cmd_type == CommandType.ADD
        assert result.args == ["clean the house"]

    @pytest.mark.parametrize("variant", ["list", "ls", "l"])
    def test_parse_list_command_variants(self, variant):
        """Test parsing list command with all variants."""
        result = self.parser.parse(variant)

        assert result is not None
        assert result.cmd_type == CommandType.LIST
        assert result.args == []

    @pytest.mark.parametrize("variant,expected_args", [("complete 1", [1]), ("done 2", [2]), ("c 3", [3])])
    def test_parse_complete_command_variants(self, variant, expected_args):
        """Test parsing complete command with all variants."""
        result = self.parser.parse(variant)

        assert result is not None
        assert result.cmd_type == CommandType.COMPLETE
        assert result.args == expected_args

    @pytest.mark.parametrize("variant,expected_args", [("incomplete 1", [1]), ("undo 2", [2]), ("i 3", [3])])
    def test_parse_incomplete_command_variants(self, variant, expected_args):
        """Test parsing incomplete command with all variants."""
        result = self.parser.parse(variant)

        assert result is not None
        assert result.cmd_type == CommandType.INCOMPLETE
        assert result.args == expected_args

    @pytest.mark.parametrize("variant,expected_args", [("delete 1", [1]), ("del 2", [2]), ("d 3", [3])])
    def test_parse_delete_command_variants(self, variant, expected_args):
        """Test parsing delete command with all variants."""
        result = self.parser.parse(variant)

        assert result is not None
        assert result.cmd_type == CommandType.DELETE
        assert result.args == expected_args

    @pytest.mark.parametrize("variant", ["help", "?"])
    def test_parse_help_command_variants(self, variant):
        """Test parsing help command with all variants."""
        result = self.parser.parse(variant)

        assert result is not None
        assert result.cmd_type == CommandType.HELP
        assert result.args == []

    @pytest.mark.parametrize("variant", ["quit", "q", "exit"])
    def test_parse_quit_command_variants(self, variant):
        """Test parsing quit command with all variants."""
        result = self.parser.parse(variant)

        assert result is not None
        assert result.cmd_type == CommandType.QUIT
        assert result.args == []

    def test_parse_clear_command(self):
        """Test parsing clear command."""
        result = self.parser.parse("clear")

        assert result is not None
        assert result.cmd_type == CommandType.CLEAR
        assert result.args == []

    def test_parse_invalid_command(self):
        """Test parsing an invalid command treats it as add command."""
        result = self.parser.parse("invalidcommand")

        assert result is not None
        assert result.cmd_type == CommandType.ADD
        assert result.args == ["invalidcommand"]

    def test_parse_invalid_numeric_argument(self):
        """Test parsing a command with invalid numeric argument treats as add."""
        result = self.parser.parse("complete abc")

        assert result is not None
        assert result.cmd_type == CommandType.ADD
        assert result.args == ["complete abc"]

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        result = self.parser.parse("")

        assert result is None

    def test_parse_whitespace_only_input(self):
        """Test parsing whitespace-only input."""
        result = self.parser.parse("   ")

        assert result is None

    def test_case_insensitive_parsing(self):
        """Test that parsing is case insensitive."""
        result = self.parser.parse("ADD Buy groceries")

        assert result is not None
        assert result.cmd_type == CommandType.ADD
        assert result.args == ["buy groceries"]

        result = self.parser.parse("LIST")

        assert result is not None
        assert result.cmd_type == CommandType.LIST
        assert result.args == []

    def test_get_help_text(self):
        """Test getting help text."""
        help_text = self.parser.get_help_text()

        assert isinstance(help_text, str)
        assert len(help_text) > 0
        assert "help" in help_text.lower()
        assert "add" in help_text.lower()
        assert "list" in help_text.lower()