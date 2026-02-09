#!/usr/bin/env python3
"""
Entry point for the In-Memory Console Todo App.
Phase I implementation with Python 3.13+
"""

def main():
    """
    Main entry point for the application.
    """
    print("Welcome to the In-Memory Console Todo App!")
    print("Type 'help' for available commands or 'quit' to exit.")

    # Import and run the CLI interface
    from src.cli.console import run_cli
    run_cli()


if __name__ == "__main__":
    main()