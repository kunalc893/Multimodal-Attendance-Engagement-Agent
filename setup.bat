@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  where py >nul 2>nul
  if errorlevel 1 (
    python -m venv .venv
  ) else (
    py -3 -m venv .venv
  )
  if errorlevel 1 goto error
)
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto error
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
echo.
echo Setup complete. Run run_app.bat or press F5 in VS Code.
pause
exit /b 0
:error
echo Setup failed. Install Python 3.10 or newer and ensure the Python launcher or python command is on PATH.
pause
exit /b 1
