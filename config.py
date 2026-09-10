import os
from pathlib import Path

APP_DIR = Path(os.getenv("USERPROFILE", str(Path.home()))) / ".nexum"
APP_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_WORKSPACE = Path.home() / "NEXUM"
WORKSPACE_ROOT = Path(os.getenv("NEXUM_WORKSPACE", str(DEFAULT_WORKSPACE))).expanduser()
MAX_TOOL_ROUNDS = int(os.getenv("NEXUM_MAX_TOOL_ROUNDS", "6"))
HISTORY_LIMIT = int(os.getenv("NEXUM_HISTORY_LIMIT", "16"))
FILE_SIZE_LIMIT = int(os.getenv("NEXUM_FILE_SIZE_LIMIT", str(2 * 1024 * 1024)))
MODEL_OVERRIDE = os.getenv("NEXUM_MODEL", "").strip()


def set_workspace(path):
    global WORKSPACE_ROOT
    WORKSPACE_ROOT = Path(path).expanduser().resolve()
    os.environ["NEXUM_WORKSPACE"] = str(WORKSPACE_ROOT)
    return WORKSPACE_ROOT


SYSTEM_PROMPT = """You are NEXUM, a local agentic AI assistant.
Your visible product identity is only NEXUM. Never describe yourself using an API provider's brand.
You can use tools for workspace files, public web research, memory, tasks, and arithmetic.
Never claim an action succeeded unless the tool result confirms success.
Workspace file operations must stay inside the configured workspace.
Deleting files and overwriting existing files require explicit confirmation.
Do not expose API keys or credentials.
Be concise, helpful, and honest."""
