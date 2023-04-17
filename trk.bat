@echo off
set old_dir=%cd%
cd %~dp0
python.exe traeckly.py %*
cd %old_dir%