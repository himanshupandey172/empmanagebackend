@echo off
cd %~dp0
"C:\Program Files\Git\git-bash.exe" -c "git status; exec bash"
pause