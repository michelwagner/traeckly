import json
from pathlib import Path
import subprocess
import tkinter as tk
import re


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data


def parse_command(commands: list, tile: dict) -> str:
    """Look up a command by name from the tile and return the command string.

    Template parameters of the form {$(Key)} inside the command string
    are replaced with the corresponding value from the `tile` dict (or
    the empty string if the key does not exist).
    """
    command_name = tile.get("command", "")
    for cmd in commands:
        if cmd.get("name") == command_name:
            template = cmd.get("command", "") or ""

            # replace {$(...)} placeholders with tile values
            def _repl(match):
                key = match.group(1)
                val = tile.get(key, "")
                return str(val)

            return re.sub(r"\{\$\(([^)]+)\)\}", _repl, template)
    return ""


def sanitize(item: str) -> str:
    """Replace non-printable characters (including whitespace) with '_'."""
    return re.sub(r'\W', '_', item) if item else item


def load_grid(config: dict):
    rows = config["rows"]
    cols = config["cols"]
    tiles = config["tiles"]

    # Create an empty grid of titles and tasks
    grid = [[{"title": "", "task": ""} for _ in range(cols)] for _ in range(rows)]
    for t in tiles:
        r = int(t.get("row", 0))
        c = int(t.get("col", 0))
        title = str(t.get("title", ""))
        task = str(t.get("task", ""))
        task_sanitized = sanitize(task)
        
        command = str(t.get("command", ""))
        if 0 <= r < rows and 0 <= c < cols:
            grid[r][c] = {"title": title, "task": task_sanitized, "command": command}
    return grid


def build_ui(config: dict):
    rows = config["rows"]
    cols = config["cols"]
    window_title = config.get("window_title", "")
    commands = config.get("commands", [])
    background = config.get("background", "#FFFFFF")
    background_active = config.get("background_active", "#FFB0B0")
    grid = load_grid(config)

    root = tk.Tk()
    root.title(window_title)

    # Make grid expandable
    for c in range(cols):
        root.grid_columnconfigure(c, weight=1)
    for r in range(rows):
        root.grid_rowconfigure(r, weight=1)

    # colors for Tkinter
    bg = background
    bg_active = background_active

    buttons = []

    def on_click(clicked_btn, tile):
        # get command template from commands list via parse_command
        cmd = parse_command(commands, tile)

        if cmd:
            try:
                print(f"Running command: {cmd}")
                subprocess.run(cmd, shell=True)
            except Exception as e:
                print(f"Error running command: {e}")

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

    for r in range(rows):
        row_buttons = []
        for c in range(cols):
            cell = grid[r][c]
            title = cell.get("title", "")
            btn = tk.Button(
                root,
                text=title or "",
                wraplength=120,
                bg=bg,
                activebackground=bg,
            )
            btn.config(command=lambda b=btn, tile=cell: on_click(b, tile))
            btn.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
            row_buttons.append(btn)
        buttons.append(row_buttons)

    root.minsize(300, 200)
    return root


def main():
    cfg_path = Path(__file__).parent / "traeckly_gui.user.json"
    if not cfg_path.exists():
        print(f"Config file not found: {cfg_path}")
        return
    
    config = load_config(cfg_path)
    root = build_ui(config)
    root.mainloop()


if __name__ == "__main__":
    main()
