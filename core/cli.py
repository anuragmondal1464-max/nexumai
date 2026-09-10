import os

import config
from core.agent import Agent
from core.setup import first_run_setup
from core.workspace_setup import choose_workspace
from core.ui import (
    banner, clear, prompt, info, success, error, warn, section, WHITE, DIM, BOLD
)

def _print_help():
    section("COMMANDS")
    print("  help     Show commands")
    print("  models   List models available to your API key")
    print("  model    Show the selected model")
    print("  memory   Show saved memory")
    print("  tasks    Show tasks")
    print("  clear    Clear the terminal")
    print("  exit     Close NEXUM")
    print("  quit     Close NEXUM")
    print()
    print(DIM + "  Anything else is sent to NEXUM as a natural-language request.")

def run_cli():
    key = first_run_setup()
    if not key:
        error("NEXUM cannot start without an API key.")
        return

    # First launch lets the user choose where NEXUM stores project work.
    if not os.getenv("NEXUM_WORKSPACE"):
        selected = choose_workspace(first_run=True)
        if selected:
            config.set_workspace(selected)

    try:
        agent = Agent(key)
    except Exception as exc:
        error(str(exc))
        return

    clear()
    banner()
    success(f"Ready  •  model: {agent.models.selected}")
    info(f"Workspace: {config.WORKSPACE_ROOT}")
    print()

    while True:
        try:
            text = prompt().strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not text:
            continue

        cmd = text.lower()
        if cmd in ("exit", "quit"):
            print(DIM + "Goodbye.")
            break
        if cmd == "help":
            _print_help()
            continue
        if cmd == "models":
            section("AVAILABLE MODELS")
            for model in agent.models.models:
                marker = "  * " if model == agent.models.selected else "    "
                print(marker + model)
            continue
        if cmd == "model":
            info(f"Selected model: {agent.models.selected}")
            continue
        if cmd in ("workspace", "change workspace"):
            selected = choose_workspace(first_run=False)
            if selected:
                config.set_workspace(selected)
                agent = Agent(key)
                success(f"Workspace changed to: {config.WORKSPACE_ROOT}")
            continue
        if cmd == "memory":
            section("MEMORY")
            print(agent.memory.list())
            continue
        if cmd == "tasks":
            section("TASKS")
            tasks = agent.tasks.list()
            if not tasks:
                print(DIM + "  No tasks.")
            for task in tasks:
                status = "✓" if task["status"] == "done" else "○"
                print(f"  {status} [{task['id']}] {task['title']}")
            continue
        if cmd == "clear":
            clear()
            banner()
            continue

        try:
            answer = agent.ask(text)
            print()
            print(WHITE + answer)
        except Exception as exc:
            error(f"NEXUM error: {exc}")
