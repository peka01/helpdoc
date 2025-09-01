@echo off
REM Translation Setup Script for NTR Documentation (Batch version)
REM This script helps set up the automated translation system

setlocal enabledelayedexpansion

echo NTR Documentation Translation Setup
echo ===================================

if "%1"=="-Install" goto :install
if "%1"=="-Configure" goto :configure
if "%1"=="-Test" goto :test
if "%1"=="-Help" goto :help
goto :help

:install
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    exit /b 1
)
echo Dependencies installed successfully

echo Setting up Git hooks...
if not exist ".git\hooks" (
    echo Git repository not found
    exit /b 1
)

if exist "pre-commit.ps1" (
    copy "pre-commit.ps1" ".git\hooks\pre-commit" >nul
    echo PowerShell pre-commit hook installed
) else if exist ".git\hooks\pre-commit" (
    echo Bash pre-commit hook already installed
) else (
    echo Pre-commit hook file not found
    exit /b 1
)
goto :end

:configure
echo Configuring translation settings...

if "%DEEPL_API_KEY%"=="" (
    echo DeepL API key not found in environment variables.
    echo To get a free API key, visit: https://www.deepl.com/pro-api
    set /p setkey="Would you like to set the DeepL API key now? (y/n): "
    if /i "!setkey!"=="y" (
        set /p apikey="Enter your DeepL API key: "
        set DEEPL_API_KEY=!apikey!
        echo API key set for current session.
        echo To make it permanent, add DEEPL_API_KEY to your environment variables.
    )
) else (
    echo DeepL API key found
)

if exist "translation-config.json" (
    echo Translation configuration found
) else (
    echo Translation configuration not found
    exit /b 1
)

if exist "help-config.json" (
    echo Help configuration found
) else (
    echo Help configuration not found
    exit /b 1
)
goto :end

:test
echo Testing translation system...

if not exist "translate.py" (
    echo Translation script not found
    exit /b 1
)

if exist "docs\en\overview.md" (
    echo Testing translation with docs\en\overview.md...
    python translate.py --mode translate-file --source-file docs\en\overview.md --target-lang SV --source-lang EN
    if errorlevel 1 (
        echo Translation test failed
        exit /b 1
    ) else (
        echo Translation test successful
    )
) else (
    echo Test file not found: docs\en\overview.md
    exit /b 1
)
goto :end

:help
echo.
echo Usage:
echo   setup-translation.bat -Install     # Install dependencies and setup hooks
echo   setup-translation.bat -Configure   # Configure translation settings
echo   setup-translation.bat -Test        # Test translation system
echo   setup-translation.bat -Help        # Show this help
echo.
echo Examples:
echo   setup-translation.bat -Install -Configure  # Full setup
echo.
goto :end

:end
if "%1"=="-Install" (
    echo.
    echo Translation setup completed successfully!
    echo.
    echo Next steps:
    echo 1. Set your DeepL API key as environment variable: DEEPL_API_KEY
    echo 2. Make changes to English documentation files
    echo 3. Commit changes - translations will happen automatically
    echo 4. Check translation.log for any issues
)
if "%1"=="-Configure" (
    echo.
    echo Configuration completed successfully!
)
if "%1"=="-Test" (
    echo.
    echo Test completed successfully!
)
exit /b 0
