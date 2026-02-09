"""
UI utilities for the Todo application.
Provides color support, formatting, and visual elements.
Phase I enhancement for better user experience.
"""

import sys


class Colors:
    """ANSI color codes for terminal output."""

    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Foreground colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    # Check if terminal supports colors
    @staticmethod
    def is_supported():
        """Check if terminal supports ANSI colors."""
        # Disable colors on Windows by default, or if NO_COLOR is set
        if sys.platform == 'win32':
            return False
        return True


class BoxChars:
    """Unicode box-drawing characters for borders."""

    TOP_LEFT = '╔'
    TOP_RIGHT = '╗'
    BOTTOM_LEFT = '└'
    BOTTOM_RIGHT = '┘'
    HORIZONTAL = '═'
    VERTICAL = '║'
    T_DOWN = '╦'
    T_UP = '╩'
    T_RIGHT = '╠'
    T_LEFT = '╣'
    CROSS = '╬'

    # ASCII fallback for environments without Unicode support
    ASCII_TOP_LEFT = '+'
    ASCII_TOP_RIGHT = '+'
    ASCII_BOTTOM_LEFT = '+'
    ASCII_BOTTOM_RIGHT = '+'
    ASCII_HORIZONTAL = '-'
    ASCII_VERTICAL = '|'


class StatusIndicators:
    """Status indicators for todos."""

    COMPLETE = '✓'
    PENDING = '○'
    COMPLETE_ASCII = 'X'
    PENDING_ASCII = '[ ]'


def colorize(text, color):
    """
    Apply color to text if colors are supported.

    Args:
        text (str): Text to colorize
        color (str): Color code from Colors class

    Returns:
        str: Colored text or plain text if colors not supported
    """
    if not Colors.is_supported():
        return text
    return f"{color}{text}{Colors.RESET}"


def success(text):
    """Format text as success message (green)."""
    return colorize(text, Colors.GREEN)


def error(text):
    """Format text as error message (red)."""
    return colorize(text, Colors.RED)


def warning(text):
    """Format text as warning message (yellow)."""
    return colorize(text, Colors.YELLOW)


def info(text):
    """Format text as info message (cyan)."""
    return colorize(text, Colors.CYAN)


def bold(text):
    """Format text as bold."""
    if not Colors.is_supported():
        return text
    return f"{Colors.BOLD}{text}{Colors.RESET}"


def draw_box(title="", width=50):
    """
    Draw a decorative box with optional title.

    Args:
        title (str): Optional title for the box
        width (int): Width of the box

    Returns:
        tuple: (top_line, bottom_line) for use in printing
    """
    if Colors.is_supported():
        top = BoxChars.TOP_LEFT + BoxChars.HORIZONTAL * (width - 2) + BoxChars.TOP_RIGHT
        bottom = BoxChars.BOTTOM_LEFT + BoxChars.HORIZONTAL * (width - 2) + BoxChars.BOTTOM_RIGHT
    else:
        top = BoxChars.ASCII_TOP_LEFT + BoxChars.ASCII_HORIZONTAL * (width - 2) + BoxChars.ASCII_TOP_RIGHT
        bottom = BoxChars.ASCII_BOTTOM_LEFT + BoxChars.ASCII_HORIZONTAL * (width - 2) + BoxChars.ASCII_BOTTOM_RIGHT

    return top, bottom


def draw_separator(width=50):
    """Draw a horizontal separator line."""
    if Colors.is_supported():
        return BoxChars.HORIZONTAL * width
    return BoxChars.ASCII_HORIZONTAL * width


def ascii_banner():
    """Return an ASCII art banner for the application."""
    banner = r"""
     _____ _ _              _____     _ _
    |_   _| | |            |_   _|__ | | |
      | | | | | ___   ___    | |/ _ \| | |
      | | | | |/ _ \ / _ \   | | (_) | | |
      | | | |_| (_) | (_) |  | |\___/|_|_|
      \_/ |_|\___/ \___/   \_/\_|

    Welcome to Todo App - Manage your tasks efficiently!
    """
    return banner


def statistics(total, completed, pending):
    """
    Format statistics display.

    Args:
        total (int): Total number of todos
        completed (int): Number of completed todos
        pending (int): Number of pending todos

    Returns:
        str: Formatted statistics
    """
    stats = f"Total: {total} | {success('✓ Completed: ' + str(completed))} | {warning('Pending: ' + str(pending))}"
    return stats


def format_todo_item(todo_id, description, completed):
    """
    Format a todo item for display.

    Args:
        todo_id (int): ID of the todo
        description (str): Description of the todo
        completed (bool): Whether the todo is completed

    Returns:
        str: Formatted todo item
    """
    status_icon = StatusIndicators.COMPLETE if completed else StatusIndicators.PENDING
    status_text = success(f"[{status_icon}]") if completed else warning(f"[{status_icon}]")
    return f"{status_text} {bold(str(todo_id))}: {description}"
