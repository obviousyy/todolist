@echo off
start cmd /c "cd %~dp0 && conda activate todo1 && pyinstaller -y main.spec"