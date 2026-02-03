import json
from pathlib import Path
import subprocess
import tkinter as tk


def load_grid(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = int(data.get("rows", 0))
    cols = int(data.get("cols", 0))
    tiles = data.get("tiles", [])
    window_title = data.get("window_title", "Grid App")
    command_template = data.get("command", "")

    # color settings (may be "rgb(r,g,b)" or hex)
    background = data.get("background", "#A9A9A9")
    background_active = data.get("background_active", "#D3D3D3")

    # Create an empty grid of titles and tasks
    grid = [[{"title": "", "task": ""} for _ in range(cols)] for _ in range(rows)]
    for t in tiles:
        r = int(t.get("row", 0))
        c = int(t.get("col", 0))
        title = str(t.get("title", ""))
        task = str(t.get("task", ""))
        if 0 <= r < rows and 0 <= c < cols:
            grid[r][c] = {"title": title, "task": task}
    return window_title, rows, cols, grid, background, background_active, command_template


def _rgb_to_hex(color: str) -> str:
    """Convert "rgb(r,g,b)" or "r,g,b" or hex to hex string for Tkinter."""
    if not isinstance(color, str):
        return "#A9A9A9"
    s = color.strip()
    if s.startswith("#"):
        return s
    if s.lower().startswith("rgb"):
        try:
            inside = s[s.find("(") + 1:s.find(")")]
            parts = [int(p.strip()) for p in inside.split(",")]
            return "#{:02X}{:02X}{:02X}".format(*parts)
        except Exception:
            return "#A9A9A9"
    # try comma separated
    if "," in s:
        try:
            parts = [int(p.strip()) for p in s.split(",")]
            return "#{:02X}{:02X}{:02X}".format(*parts)
        except Exception:
            return "#A9A9A9"
    return s


def build_ui(cfg_path: Path):
    window_title, rows, cols, grid, background, background_active, command_template = load_grid(cfg_path)

    root = tk.Tk()
    root.title(window_title)

    # Make grid expandable
    for c in range(cols):
        root.grid_columnconfigure(c, weight=1)
    for r in range(rows):
        root.grid_rowconfigure(r, weight=1)

    # normalize colors for Tkinter
    bg = _rgb_to_hex(background)
    bg_active = _rgb_to_hex(background_active)

    buttons = []

    def on_click(clicked_btn, task):
        # compose and execute the command
        if task and command_template:
            cmd = command_template.format(task)
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
    cfg = Path(__file__).parent / "traeckly_gui.user.json"
    if not cfg.exists():
        print(f"Config file not found: {cfg}")
        return
    root = build_ui(cfg)
    root.mainloop()


if __name__ == "__main__":
    main()
