@echo off
start cmd /c "cd %~dp0 && conda activate todo2 && pyinstaller -y main.spec"