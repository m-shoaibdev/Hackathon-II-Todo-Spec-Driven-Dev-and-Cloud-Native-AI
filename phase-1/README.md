# In-Memory Console Todo App

A simple command-line todo application built with Python. This application stores todos in memory only and provides a CLI for managing tasks.

## Features

- Add new todo items
- View all todo items
- Mark items as completed/incomplete
- Delete specific todo items
- Clear all todo items
- Cross-platform command-line interface

## Prerequisites

- Python 3.13 or higher
- UV package manager (optional, but recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # Or if using uv:
   uv pip install -r requirements.txt
   ```

## Usage

Run the application using:
```bash
python main.py
```

Once running, you can use the following commands:

- `add <task>` or `a <task>` - Add a new todo item
- `list` or `ls` or `l` - List all todo items
- `complete <id>` or `done <id>` or `c <id>` - Mark item as completed
- `incomplete <id>` or `undo <id>` or `i <id>` - Mark item as incomplete
- `delete <id>` or `del <id>` or `d <id>` - Delete a todo item
- `clear` - Clear all todo items
- `help` or `?` - Show help message
- `quit` or `q` or `exit` - Quit the application

### Example Session

```
> add Buy groceries
Added todo: Buy groceries (ID: 1)

> add Finish project
Added todo: Finish project (ID: 2)

> list
Your todo list (2 items):
----------------------------------------
[○] 1: Buy groceries
[○] 2: Finish project
----------------------------------------

> complete 1
Marked todo 1 as completed.

> list
Your todo list (2 items):
----------------------------------------
[✓] 1: Buy groceries
[○] 2: Finish project
----------------------------------------

> quit
Goodbye! Thanks for using the Todo App.
```

## Project Structure

```
src/
├── main.py                     # Application entry point
├── cli/
│   └── console.py              # Input/output loop
├── parser/
│   └── commands.py             # Command parsing
├── services/
│   └── todo_service.py         # Business logic for todos
├── datastore/
│   └── in_memory_store.py      # In-memory storage for todos
└── models/
    └── todo.py                 # Todo entity model

tests/
├── unit/
│   ├── test_todo.py
│   ├── test_in_memory_store.py
│   ├── test_todo_service.py
│   └── test_command_parser.py
└── contract/
    └── test_cli_interface.py
```

## Running Tests

To run the unit tests:
```bash
python -m pytest tests/unit/
```

To run all tests:
```bash
python -m pytest tests/
```

## Limitations

- Todos are stored in memory only and will be lost when the application closes
- No data persistence
- Single-user application
- Console-based interface only

## License

This project is released under the MIT License.