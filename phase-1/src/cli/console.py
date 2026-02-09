"""
Console interface for the Todo application.
Provides the command-line interface for users to interact with the todo list.
Phase I implementation with in-memory storage only.
"""

from typing import Optional
from src.services.todo_service import TodoService
from src.datastore.in_memory_store import InMemoryStore
from src.parser.commands import CommandParser, CommandType, ParsedCommand


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

    def display_welcome(self):
        """
        Display welcome message and instructions.
        """
        print("=" * 50)
        print("Welcome to the In-Memory Console Todo App!")
        print("=" * 50)
        print("Type 'help' for available commands or 'quit' to exit.\n")

    def display_todo_list(self):
        """
        Display the current list of todos.
        """
        todos = self.service.get_all_todos()

        if not todos:
            print("Your todo list is empty. Add some tasks!")
            return

        print(f"\nYour todo list ({len(todos)} items):")
        print("-" * 40)
        for todo in todos:
            status = "✓" if todo.completed else "○"
            print(f"[{status}] {todo.id}: {todo.description}")
        print("-" * 40)

    def handle_add_command(self, description: str):
        """
        Handle adding a new todo.

        Args:
            description (str): Description of the new todo
        """
        try:
            todo = self.service.add_todo(description)
            print(f"Added todo: {todo.description} (ID: {todo.id})")
        except ValueError as e:
            print(f"Error: {e}")

    def handle_list_command(self):
        """
        Handle listing all todos.
        """
        self.display_todo_list()

    def handle_complete_command(self, todo_id: int):
        """
        Handle marking a todo as completed.

        Args:
            todo_id (int): ID of the todo to complete
        """
        if self.service.complete_todo(todo_id):
            print(f"Marked todo {todo_id} as completed.")
        else:
            print(f"Error: Todo with ID {todo_id} not found.")

    def handle_incomplete_command(self, todo_id: int):
        """
        Handle marking a todo as incomplete.

        Args:
            todo_id (int): ID of the todo to mark as incomplete
        """
        if self.service.incomplete_todo(todo_id):
            print(f"Marked todo {todo_id} as incomplete.")
        else:
            print(f"Error: Todo with ID {todo_id} not found.")

    def handle_delete_command(self, todo_id: int):
        """
        Handle deleting a todo.

        Args:
            todo_id (int): ID of the todo to delete
        """
        if self.service.delete_todo(todo_id):
            print(f"Deleted todo {todo_id}.")
        else:
            print(f"Error: Todo with ID {todo_id} not found.")

    def handle_clear_command(self):
        """
        Handle clearing all todos.
        """
        self.service.clear_all_todos()
        print("All todos cleared.")

    def handle_help_command(self):
        """
        Handle displaying help information.
        """
        print(self.parser.get_help_text())

    def handle_quit_command(self):
        """
        Handle quitting the application.
        """
        print("Goodbye! Thanks for using the Todo App.")
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
                print("Error: Please provide a description for the new todo.")
        elif cmd_type == CommandType.LIST:
            self.handle_list_command()
        elif cmd_type == CommandType.COMPLETE:
            if len(args) >= 1:
                self.handle_complete_command(args[0])
            else:
                print("Error: Please provide the ID of the todo to complete.")
        elif cmd_type == CommandType.INCOMPLETE:
            if len(args) >= 1:
                self.handle_incomplete_command(args[0])
            else:
                print("Error: Please provide the ID of the todo to mark as incomplete.")
        elif cmd_type == CommandType.DELETE:
            if len(args) >= 1:
                self.handle_delete_command(args[0])
            else:
                print("Error: Please provide the ID of the todo to delete.")
        elif cmd_type == CommandType.HELP:
            self.handle_help_command()
        elif cmd_type == CommandType.QUIT:
            self.handle_quit_command()
        elif cmd_type == CommandType.CLEAR:
            self.handle_clear_command()
        else:
            print(f"Unknown command type: {cmd_type}")

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
                    print("Invalid command. Type 'help' for available commands.")
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