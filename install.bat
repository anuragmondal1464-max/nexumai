@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo.
echo ============================================================
echo                         NEXUM v0.4
echo                    Installation Wizard
echo ============================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python was not found on PATH.
  echo Install Python 3.10+ and make sure "Add Python to PATH" is enabled.
  pause
  exit /b 1
)

python --version
if errorlevel 1 goto :error

for /f "delims=" %%S in ('python -c "import sysconfig; print(sysconfig.get_path('scripts'))"') do set "PY_SCRIPTS=%%S"

if not defined PY_SCRIPTS (
  echo ERROR: Could not determine the Python Scripts directory.
  goto :error
)

echo.
echo Python Scripts: %PY_SCRIPTS%
echo.
echo Removing stale NEXUM launchers from this Python installation...
python -m pip uninstall nexum nexum-local-assistant -y >nul 2>nul
if exist "%PY_SCRIPTS%\nexum.exe" del /f /q "%PY_SCRIPTS%\nexum.exe" >nul 2>nul
if exist "%PY_SCRIPTS%\nexum-script.py" del /f /q "%PY_SCRIPTS%\nexum-script.py" >nul 2>nul

python -m pip install --upgrade pip
if errorlevel 1 goto :error

python -m pip install -e .
if errorlevel 1 goto :error

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$p=[Environment]::GetEnvironmentVariable('Path','User'); $s='%PY_SCRIPTS%'; $parts=@($p -split ';' | Where-Object { $_ -and $_.Trim() -ne $s.Trim() }); [Environment]::SetEnvironmentVariable('Path', (($parts + $s) -join ';'), 'User')"

rem Make the command usable in THIS CMD too, not only future CMD windows.
set "PATH=%PY_SCRIPTS%;%PATH%"

echo.
echo Verifying NEXUM command:
where nexum
if errorlevel 1 (
  echo WARNING: NEXUM was installed but the command was not found.
  echo Try opening a NEW Command Prompt and type: nexum
) else (
  echo NEXUM command is ready.
)

echo.
echo ============================================================
echo Installation complete.
echo.
echo Open a NEW Command Prompt and type:
echo.
echo     nexum
echo.
echo First launch will ask for your API key and let you choose

echo the workspace folder for your projects.
echo ============================================================
echo.
pause
exit /b 0

:error
echo.
echo ERROR: NEXUM installation failed.
pause
exit /b 1
