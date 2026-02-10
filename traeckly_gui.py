import json
from pathlib import Path
import subprocess
import tkinter as tk
import re


def load_config(path: Path) -> dict:
    """Load and parse JSON configuration file.
    
    Args:
        path: Path to the JSON configuration file.
        
    Returns:
        Dictionary containing the parsed configuration.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    return data


def parse_command(commands: dict, tile: dict) -> str:
    """Look up a command by name from the tile and return the command string.

    Template parameters of the form {$(Key)} inside the command string
    are replaced with the corresponding value from the `tile` dict (or
    the empty string if the key does not exist). Returns empty string if
    the command name is missing or not found in commands.
    """
    command = ""
    try:
        template = commands[tile["command"]]

        # replace {$(...)} placeholders with tile values
        def _repl(match):
            key = match.group(1)
            val = tile.get(key, "")
            return str(val)

        command = re.sub(r"\{\$\(([^)]+)\)\}", _repl, template)
    except (KeyError, TypeError):
        pass
    return command


def wrap_text(text: str, max_chars: int = 15) -> str:
    """Wrap text at whitespace or dashes to fit approximately max_chars per line."""
    if not text or not text.strip() or len(text) <= max_chars:
        result = text
    else:
        words = text.replace('-', '- ').split()
        result = words[0]
        current_line_len = len(words[0])
        
        for word in words[1:]:
            if current_line_len + 1 + len(word) <= max_chars:
                result += ' ' + word
                current_line_len += 1 + len(word)
            else:
                result += '\n' + word
                current_line_len = len(word)
    
    return result


def configure_grid_layout(root: tk.Tk, rows: int, cols: int):
    """Make grid rows and columns expandable."""
    for c in range(cols):
        root.grid_columnconfigure(c, weight=1)
    for r in range(rows):
        root.grid_rowconfigure(r, weight=1)


def create_click_handler(commands: dict, buttons: list, bg: str, bg_active: str):
    """Create and return a click handler function for buttons."""
    def on_click(clicked_btn, tile):
        cmd = parse_command(commands, tile)

        if cmd:
            try:
                print(f"Running command: {cmd}")
                subprocess.run(cmd, shell=True)
            except Exception as e:
                print(f"Error running command: {e}")

            if not tile.get("pushbutton", False):
                # reset all buttons to normal background
                for row_buttons in buttons:
                    for b in row_buttons:
                        try:
                            b.config(bg=bg)
                        except Exception:
                            pass
                # set clicked button to active background
                try:
                    clicked_btn.config(bg=bg_active)
                except Exception:
                    pass
    
    return on_click


def create_button(root: tk.Tk, cell: dict, bg: str, font_size: int, on_click, row: int, col: int):
    """Create a button for a grid cell."""
    title = cell.get("title", "")
    wrapped_title = wrap_text(title, max_chars=20)
    btn = tk.Button(
        root,
        text=wrapped_title or "",
        bg=bg,
        font=("TkDefaultFont", font_size)
    )
    btn.config(command=lambda b=btn, tile=cell: on_click(b, tile))
    btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
    return btn


def build_ui(config: dict):
    """Build and configure the main GUI window with button grid.
    
    Creates a tkinter window with a grid of buttons based on the configuration.
    Each button can execute commands when clicked, with visual feedback for
    active tasks.
    
    Args:
        config: Configuration dictionary containing window settings, commands,
                colors, font-size, and grid layout.
                
    Returns:
        Configured tk.Tk root window ready to run.
    """
    window_title = config.get("window_title", "")
    commands = config.get("commands", [])
    background = config.get("background", "#FFFFFF")
    background_active = config.get("background_active", "#FFB0B0")
    font_size = config.get("font-size", 10)
    grid = config.get("grid", [[]])
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    root = tk.Tk()
    root.title(window_title)
    
    configure_grid_layout(root, rows, cols)

    buttons = []
    on_click = create_click_handler(commands, buttons, background, background_active)

    for r in range(rows):
        row_buttons = []
        for c in range(cols):
            btn = create_button(root, grid[r][c], background, font_size, on_click, r, c)
            row_buttons.append(btn)
        buttons.append(row_buttons)

    root.minsize(300, 200)
    return root


def main():
    """Main entry point for the Traeckly GUI application.
    
    Loads the user configuration file and starts the GUI event loop.
    """
    cfg_path = Path(__file__).parent / "traeckly_gui.user.json"
    if not cfg_path.exists():
        print(f"Config file not found: {cfg_path}")
        return
    
    config = load_config(cfg_path)
    root = build_ui(config)
    root.mainloop()


if __name__ == "__main__":
    main()
