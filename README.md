# NEXUM

**NEXUM — local agentic AI assistant for Windows.**

Chat with NEXUM from CMD, work with files/projects, research the web, calculate, manage memory/tasks, and use agent tools from one terminal.

## Quick Start

### Requirements
- Windows 10/11
- Python 3.10+
- AI API key
- Internet connection

### Install

1. Extract this folder.
2. Run **`install.bat`**.
3. Close CMD and open a **new** CMD.
4. Run:

```bat
nexum
```

On first launch, enter your API key if requested.

## Workspace

Default workspace:

```text
%USERPROFILE%\NEXUM
```

NEXUM can ask you to choose a different folder on first setup. You can change it later with:

```text
workspace
```

Or set it from CMD:

```bat
setx NEXUM_WORKSPACE "C:\Projects\NEXUM"
```

Restart CMD after using `setx`.

## Use NEXUM

After:

```text
nexum >
```

just ask for what you want:

```text
create a Python project called my_app
list the files in my workspace
research the latest Python release
calculate 18% of 9500
remember that this project uses Python 3.12
add finish the API integration to my tasks
```

NEXUM decides when its available tools are needed and performs supported actions inside the configured workspace.

## Security

- Keep your API key private.
- Never commit secrets to GitHub.
- File operations are workspace-restricted.
- Deleting/overwriting files requires confirmation.

## Troubleshooting

If `nexum` is not recognized, close CMD, open a new CMD, and run `nexum` again. If it still fails, run `install.bat` as Administrator and restart CMD.

## License

MIT License — see [`LICENSE`](LICENSE).
