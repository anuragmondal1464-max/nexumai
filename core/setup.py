import os
import subprocess
from pathlib import Path

from config import APP_DIR
from core.ui import section, info, success, error, warn

def _persist_windows_user_env(name, value):
    if os.name != "nt":
        return False
    child_env = os.environ.copy()
    child_env["NEXUM_SETUP_SECRET"] = value
    script = (
        "[Environment]::SetEnvironmentVariable("
        "'GROQ_API_KEY',$env:NEXUM_SETUP_SECRET,'User')"
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        env=child_env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    return result.returncode == 0

def first_run_setup():
    key = os.getenv("GROQ_API_KEY", "").strip()
    if key:
        return key

    section("FIRST-TIME SETUP")
    info("NEXUM needs your Groq API key to connect to its AI service.")
    info("The key will be saved as your Windows user environment variable.")
    print()
    try:
        key = input("  GROQ_API_KEY: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return ""

    if not key:
        error("No API key was entered.")
        return ""

    if os.name == "nt":
        if not _persist_windows_user_env("GROQ_API_KEY", key):
            warn("NEXUM could not persist the Windows environment variable.")
            warn("The key is still active for this session.")
        else:
            success("GROQ_API_KEY saved to your Windows user environment.")
            info("Future CMD windows will start NEXUM without asking again.")

    # Make it available immediately in the current process.
    os.environ["GROQ_API_KEY"] = key
    return key
