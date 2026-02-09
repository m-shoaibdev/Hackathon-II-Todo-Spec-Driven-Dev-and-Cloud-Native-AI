#!/usr/bin/env python3
"""
Entry point for the In-Memory Console Todo App.
Phase I implementation with Python 3.13+
"""

import sys
import io

def main():
    """
    Main entry point for the application.
    """
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    print("Welcome to the In-Memory Console Todo App!")
    print("Type 'help' for available commands or 'quit' to exit.")

    # Import and run the CLI interface
    from src.cli.console import run_cli
    run_cli()


if __name__ == "__main__":
    main()