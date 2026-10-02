@echo off
setlocal

:: 1. Check if an installed identity executable exists outside this shim
for /f "tokens=*" %%i in ('where identity.exe 2^>nul') do (
    if /i not "%%~dpi"=="%~dp0" (
        "%%i" %*
        exit /b %ERRORLEVEL%
    )
)

:: 2. If running from repository or alongside src, ensure PYTHONPATH includes src
set "REPO_SRC=%~dp0..\..\src"
if exist "%REPO_SRC%\identity_cli" (
    set "PYTHONPATH=%REPO_SRC%;%PYTHONPATH%"
)
set "ALT_SRC=%~dp0..\src"
if exist "%ALT_SRC%\identity_cli" (
    set "PYTHONPATH=%ALT_SRC%;%PYTHONPATH%"
)

:: 3. Try running identity_cli via Python module
where python.exe >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python.exe -m identity_cli.cli %*
    exit /b %ERRORLEVEL%
)

:: 4. Fallback to py launcher
where py.exe >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py.exe -m identity_cli.cli %*
    exit /b %ERRORLEVEL%
)

echo [Identity Generator] Error: Python or identity executable could not be found.
echo Please ensure Python 3.10+ is installed on your system.
exit /b 1
