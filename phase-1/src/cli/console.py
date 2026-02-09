"""
Console interface for the Todo application.
Provides the command-line interface for users to interact with the todo list.
Phase I implementation with in-memory storage only.
"""

from typing import Optional
from src.services.todo_service import TodoService
from src.datastore.in_memory_store import InMemoryStore
from src.parser.commands import CommandParser, CommandType, ParsedCommand
from src.cli.ui import (
    ascii_banner, bold, success, error, warning, info,
    draw_box, statistics, format_todo_item
)


class TodoConsole:
    """
    Handles the console interface for the todo application.
    """

    def __init__(self):
        """
        Initialize the console interface with required components.
        """
        self.store = InMemoryStore()
        self.service = TodoService(self.store)
        self.parser = CommandParser()
        self.running = True
        self._setup_readline()

    def _setup_readline(self):
        """Set up readline for command history and completion."""
        try:
            import readline
            # Enable autocomplete with arrow keys
            readline.parse_and_bind('tab: complete')
            readline.set_completer(self._completer)
        except ImportError:
            pass

    def _completer(self, text, state):
        """Tab completion for commands."""
        commands = [
            'add', 'list', 'complete', 'incomplete', 'delete',
            'clear', 'help', 'quit'
        ]
        options = [cmd for cmd in commands if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        return None

    def _confirm_action(self, prompt="Continue? (yes/no): "):
        """
        Ask user for confirmation.

        Args:
            prompt (str): Confirmation prompt

        Returns:
            bool: True if user confirms, False otherwise
        """
        while True:
            response = input(warning(prompt)).strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print(error("Please enter 'yes' or 'no'"))

    def display_welcome(self):
        """
        Display welcome message and instructions with ASCII banner.
        """
        print(ascii_banner())
        top, bottom = draw_box(width=60)
        print(top)
        print(f" {bold('Type help for commands or quit to exit')}")
        print(bottom)
        print()

    def display_todo_list(self):
        """
        Display the current list of todos with statistics.
        """
        todos = self.service.get_all_todos()

        if not todos:
            print(warning("Your todo list is empty. Add some tasks!"))
            return

        completed = sum(1 for todo in todos if todo.completed)
        pending = len(todos) - completed

        print(f"\n{bold('Your Todo List')}")
        print(statistics(len(todos), completed, pending))
        print("-" * 50)
        for todo in todos:
            print(format_todo_item(todo.id, todo.description, todo.completed))
        print("-" * 50)

    def handle_add_command(self, description: str):
        """
        Handle adding a new todo with success message.

        Args:
            description (str): Description of the new todo
        """
        try:
            todo = self.service.add_todo(description)
            print(success(f"[OK] Added todo: {todo.description} (ID: {todo.id})"))
        except ValueError as e:
            print(error(f"[ERROR] {e}"))

    def handle_list_command(self):
        """
        Handle listing all todos.
        """
        self.display_todo_list()

    def handle_complete_command(self, todo_id: int):
        """
        Handle marking a todo as completed with colored feedback.

        Args:
            todo_id (int): ID of the todo to complete
        """
        if self.service.complete_todo(todo_id):
            print(success(f"[OK] Marked todo {todo_id} as completed."))
        else:
            print(error(f"[ERROR] Todo with ID {todo_id} not found."))

    def handle_incomplete_command(self, todo_id: int):
        """
        Handle marking a todo as incomplete with colored feedback.

        Args:
            todo_id (int): ID of the todo to mark as incomplete
        """
        if self.service.incomplete_todo(todo_id):
            print(success(f"✓ Marked todo {todo_id} as incomplete."))
        else:
            print(error(f"✗ Error: Todo with ID {todo_id} not found."))

    def handle_delete_command(self, todo_id: int):
        """
        Handle deleting a todo with confirmation.

        Args:
            todo_id (int): ID of the todo to delete
        """
        todo = self.service.get_todo(todo_id)
        if not todo:
            print(error(f"✗ Error: Todo with ID {todo_id} not found."))
            return

        # Ask for confirmation
        if not self._confirm_action(f"Delete '{todo.description}'? (yes/no): "):
            print(info("Cancelled deletion."))
            return

        if self.service.delete_todo(todo_id):
            print(success(f"✓ Deleted todo {todo_id}."))
        else:
            print(error(f"✗ Error deleting todo {todo_id}."))

    def handle_clear_command(self):
        """
        Handle clearing all todos with confirmation.
        """
        todos_count = len(self.service.get_all_todos())
        if todos_count == 0:
            print(warning("No todos to clear."))
            return

        if not self._confirm_action(f"Delete all {todos_count} todos? (yes/no): "):
            print(info("Cancelled clearing todos."))
            return

        self.service.clear_all_todos()
        print(success("✓ All todos cleared."))

    def handle_help_command(self):
        """
        Handle displaying help information.
        """
        print(self.parser.get_help_text())

    def handle_quit_command(self):
        """
        Handle quitting the application.
        """
        print(success("✓ Goodbye! Thanks for using the Todo App."))
        self.running = False

    def execute_command(self, parsed_cmd: ParsedCommand):
        """
        Execute a parsed command.

        Args:
            parsed_cmd (ParsedCommand): The command to execute
        """
        cmd_type = parsed_cmd.cmd_type
        args = parsed_cmd.args

        if cmd_type == CommandType.ADD:
            if len(args) >= 1:
                self.handle_add_command(args[0])
            else:
                print(error("✗ Error: Please provide a description for the new todo."))
        elif cmd_type == CommandType.LIST:
            self.handle_list_command()
        elif cmd_type == CommandType.COMPLETE:
            if len(args) >= 1:
                try:
                    self.handle_complete_command(args[0])
                except (ValueError, TypeError):
                    print(error(f"✗ Error: Invalid ID '{args[0]}'. Please provide a valid number."))
            else:
                print(error("✗ Error: Please provide the ID of the todo to complete."))
        elif cmd_type == CommandType.INCOMPLETE:
            if len(args) >= 1:
                try:
                    self.handle_incomplete_command(args[0])
                except (ValueError, TypeError):
                    print(error(f"✗ Error: Invalid ID '{args[0]}'. Please provide a valid number."))
            else:
                print(error("✗ Error: Please provide the ID of the todo to mark as incomplete."))
        elif cmd_type == CommandType.DELETE:
            if len(args) >= 1:
                try:
                    self.handle_delete_command(args[0])
                except (ValueError, TypeError):
                    print(error(f"✗ Error: Invalid ID '{args[0]}'. Please provide a valid number."))
            else:
                print(error("✗ Error: Please provide the ID of the todo to delete."))
        elif cmd_type == CommandType.HELP:
            self.handle_help_command()
        elif cmd_type == CommandType.QUIT:
            self.handle_quit_command()
        elif cmd_type == CommandType.CLEAR:
            self.handle_clear_command()
        else:
            print(error(f"✗ Unknown command type: {cmd_type}"))

    def run(self):
        """
        Run the main command loop.
        """
        self.display_welcome()

        while self.running:
            try:
                user_input = input("\n> ").strip()
                if not user_input:
                    continue

                parsed_cmd = self.parser.parse(user_input)

                if parsed_cmd is None:
                    print(error("✗ Invalid command. Type 'help' for available commands."))
                    continue

                self.execute_command(parsed_cmd)
            except KeyboardInterrupt:
                print("\n\nReceived interrupt signal. Quitting...")
                break
            except EOFError:
                print("\n\nEnd of input. Quitting...")
                break


def run_cli():
    """
    Entry point to run the CLI interface.
    """
    console = TodoConsole()
    console.run()