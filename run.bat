@echo off
REM Run the Transparency Dashboard

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run the dashboard
uv run dashboard
