@echo off
set "VENV_DIR=%~dp0venv"
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Virtual environment not found. Run setup.bat first.
    exit /b 1
)
call "%VENV_DIR%\Scripts\activate"
"%VENV_DIR%\Scripts\python.exe" ai_research_agent.py
