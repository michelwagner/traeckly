@echo off
set old_dir=%cd%
cd %~dp0

if exist .venv (call .venv\Scripts\activate.bat)
python.exe traeckly_gui.py %*
if exist .venv (call .venv\Scripts\deactivate.bat)

cd %old_dir%