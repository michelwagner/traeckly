import json
from pathlib import Path
import subprocess
import tkinter as tk
import re


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
        if 0 <= r < rows and 0 <= c < cols:
            grid[r][c] = {"title": title, "task": task}
    return grid

def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "rows": int(data.get("rows", 0)),
        "cols": int(data.get("cols", 0)),
        "tiles": data.get("tiles", []),
        "window_title": data.get("window_title", ""),
        "command": data.get("command", ""),
        "background": data.get("background", "#FFFFFF"),
        "background_active": data.get("background_active", "#FFB0B0"),
    }



def build_ui(config: dict):
    rows = config["rows"]
    cols = config["cols"]
    window_title = config["window_title"]
    command_template = config["command"]
    background = config["background"]
    background_active = config["background_active"]
    grid = load_grid(config)

    root = tk.Tk()
    root.title(window_title)

    # Make grid expandable
    for c in range(cols):
        root.grid_columnconfigure(c, weight=1)
    for r in range(rows):
        root.grid_rowconfigure(r, weight=1)

    # normalize colors for Tkinter
    bg = background
    bg_active = background_active

    buttons = []

    def on_click(clicked_btn, task):
        # replace non-printable characters (including whitespace) with '_'
        task_sanitized = re.sub(r'\W', '_', task) if task else task
        # compose and execute the command
        if task_sanitized and command_template:
            cmd = command_template.format(task_sanitized)
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
            title = cell["title"]
            task = cell["task"]
            btn = tk.Button(
                root,
                text=title or "",
                wraplength=120,
                bg=bg,
                activebackground=bg,
            )
            btn.config(command=lambda b=btn, t=task: on_click(b, t))
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
