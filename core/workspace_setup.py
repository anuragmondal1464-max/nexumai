import os
from pathlib import Path

from core.ui import section, info, success, warn, error


def _persist_workspace(path: Path) -> bool:
    value = str(path)
    os.environ["NEXUM_WORKSPACE"] = value
    if os.name != "nt":
        return False
    script = "[Environment]::SetEnvironmentVariable('NEXUM_WORKSPACE',$env:NEXUM_WORKSPACE_VALUE,'User')"
    child_env = os.environ.copy()
    child_env["NEXUM_WORKSPACE_VALUE"] = value
    result = __import__("subprocess").run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        env=child_env,
        stdout=__import__("subprocess").DEVNULL,
        stderr=__import__("subprocess").PIPE,
        text=True,
        check=False,
    )
    return result.returncode == 0


def choose_workspace(first_run=False):
    if first_run:
        section("WORKSPACE SETUP")
        info("Choose the folder where NEXUM will create and manage your work.")
    else:
        section("CHANGE WORKSPACE")
        info("Choose a new folder for NEXUM projects and files.")

    selected = ""
    if os.name == "nt":
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            selected = filedialog.askdirectory(title="Choose NEXUM workspace") or ""
            root.destroy()
        except Exception:
            selected = ""

    if not selected:
        try:
            selected = input("  Workspace path (Enter for default D:\\AF): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if not selected:
            selected = str(Path.home() / "NEXUM")

    path = Path(selected).expanduser().resolve()
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        error(f"Could not create workspace: {exc}")
        return None

    if _persist_workspace(path):
        success(f"Workspace saved: {path}")
    else:
        warn(f"Workspace active for this session: {path}")
    return path
