@echo off
setlocal

:: 1. Check if an installed identity executable exists outside this shim
for /f "tokens=*" %%i in ('where identity.exe 2^>nul') do (
    if /i not "%%~dpi"=="%~dp0" (
        "%%i" %*
        exit /b %ERRORLEVEL%
    )
)

:: 2. Check bundled python directory inside extension, repository src, or alt paths
set "BUNDLE_SRC=%~dp0..\python"
if exist "%BUNDLE_SRC%\identity_cli" (
    set "PYTHONPATH=%BUNDLE_SRC%;%PYTHONPATH%"
)
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
    python.exe -c "import faker, openpyxl, rich, typer" >nul 2>nul
    if %ERRORLEVEL% neq 0 (
        echo [Identity Generator] First-time setup: installing required dependencies (faker, openpyxl, rich, typer)...
        python.exe -m pip install --quiet faker openpyxl rich typer
    )
    python.exe -m identity_cli.cli %*
    exit /b %ERRORLEVEL%
)

:: 4. Fallback to py launcher
where py.exe >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py.exe -c "import faker, openpyxl, rich, typer" >nul 2>nul
    if %ERRORLEVEL% neq 0 (
        echo [Identity Generator] First-time setup: installing required dependencies (faker, openpyxl, rich, typer)...
        py.exe -m pip install --quiet faker openpyxl rich typer
    )
    py.exe -m identity_cli.cli %*
    exit /b %ERRORLEVEL%
)

echo [Identity Generator] Error: Python or identity executable could not be found.
echo Please ensure Python 3.10+ is installed on your system.
exit /b 1
