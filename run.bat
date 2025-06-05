@echo off
if not exist venv (
    echo Virtual environment not found. Run setup.bat first.
    exit /b 1
)
call venv\Scripts\activate
python ai_research_agent.py
