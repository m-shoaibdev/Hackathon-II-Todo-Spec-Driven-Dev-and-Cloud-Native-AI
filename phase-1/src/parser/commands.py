"""
Command parser for the Todo application CLI.
Parses user input into structured commands for the service layer.
Phase I implementation with in-memory storage only.
"""

from enum import Enum
from typing import NamedTuple, Optional
import re


class CommandType(Enum):
    """
    Types of commands supported by the CLI.
    """
    ADD = "add"
    LIST = "list"
    COMPLETE = "complete"
    INCOMPLETE = "incomplete"
    DELETE = "delete"
    HELP = "help"
    QUIT = "quit"
    CLEAR = "clear"


class ParsedCommand(NamedTuple):
    """
    Represents a parsed command with its type and arguments.
    """
    cmd_type: CommandType
    args: list


class CommandParser:
    """
    Parses user input strings into structured commands.
    """

    def __init__(self):
        """
        Initialize the command parser with supported command patterns.
        """
        self.command_patterns = {
            r'^(?:add|a)\s+(.+)$': CommandType.ADD,
            r'^(?:list|ls|l)$': CommandType.LIST,
            r'^(?:complete|done|c)\s+(\d+)$': CommandType.COMPLETE,
            r'^(?:incomplete|undo|i)\s+(\d+)$': CommandType.INCOMPLETE,
            r'^(?:delete|del|d)\s+(\d+)$': CommandType.DELETE,
            r'^(?:help|\?)$': CommandType.HELP,
            r'^(?:quit|q|exit)$': CommandType.QUIT,
            r'^(?:clear)$': CommandType.CLEAR,
        }

    def parse(self, input_str: str) -> Optional[ParsedCommand]:
        """
        Parse a user input string into a structured command.

        Args:
            input_str (str): Raw user input

        Returns:
            ParsedCommand: Structured command with type and arguments, or None if invalid
        """
        if not input_str or not input_str.strip():
            return None

        input_str = input_str.strip().lower()

        for pattern, cmd_type in self.command_patterns.items():
            match = re.match(pattern, input_str)
            if match:
                args = list(match.groups())
                # Convert numeric arguments to integers
                if cmd_type in [CommandType.COMPLETE, CommandType.INCOMPLETE, CommandType.DELETE]:
                    try:
                        args = [int(arg) for arg in args]
                    except ValueError:
                        return None  # Invalid numeric argument
                return ParsedCommand(cmd_type, args)

        # If no pattern matched, it might be an add command without explicit 'add' keyword
        if input_str and not input_str.startswith(tuple(CommandType.__members__.keys())) and not input_str.startswith(('?', 'quit', 'q', 'exit', 'help')):
            # Treat the entire string as an add command
            return ParsedCommand(CommandType.ADD, [input_str])

        return None

    def get_help_text(self) -> str:
        """
        Get help text describing all available commands.

        Returns:
            str: Formatted help text
        """
        return """
Available Commands:
  add <task> | a <task>    - Add a new todo item
  list | ls | l            - List all todo items
  complete <id> | done <id> | c <id>  - Mark item as completed
  incomplete <id> | undo <id> | i <id>  - Mark item as incomplete
  delete <id> | del <id> | d <id>  - Delete a todo item
  clear                    - Clear all todo items
  help | ?                 - Show this help message
  quit | q | exit          - Quit the application
        """.strip()