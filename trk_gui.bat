@echo off
set old_dir=%cd%
cd %~dp0
python.exe traeckly_gui.py %*
cd %old_dir%