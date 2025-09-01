# MkDocs Deployment Script for Windows
# This script helps build and serve the documentation

param(
    [switch]$Serve,
    [switch]$Build,
    [switch]$Install,
    [switch]$Clean
)

Write-Host "Training Management System Help - MkDocs Deployment Script" -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Green

# Function to check if Python is installed
function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
        return $false
    }
}

# Function to check if pip is available
function Test-Pip {
    try {
        $pipVersion = pip --version 2>&1
        Write-Host "✓ pip found: $pipVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "✗ pip not found. Please install pip." -ForegroundColor Red
        return $false
    }
}

# Function to install dependencies
function Install-Dependencies {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    try {
        pip install -r requirements.txt
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

# Function to build documentation
function Build-Documentation {
    Write-Host "Building documentation..." -ForegroundColor Yellow
    try {
        if ($Clean) {
            mkdocs build --clean
        } else {
            mkdocs build
        }
        Write-Host "✓ Documentation built successfully" -ForegroundColor Green
        Write-Host "Output directory: site/" -ForegroundColor Cyan
    }
    catch {
        Write-Host "✗ Failed to build documentation" -ForegroundColor Red
        exit 1
    }
}

# Function to serve documentation
function Serve-Documentation {
    Write-Host "Starting development server..." -ForegroundColor Yellow
    Write-Host "Documentation will be available at: http://127.0.0.1:8000" -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    try {
        mkdocs serve
    }
    catch {
        Write-Host "✗ Failed to start development server" -ForegroundColor Red
        exit 1
    }
}

# Main execution
if (-not (Test-Python)) {
    exit 1
}

if (-not (Test-Pip)) {
    exit 1
}

# Check if requirements.txt exists
if (-not (Test-Path "requirements.txt")) {
    Write-Host "✗ requirements.txt not found" -ForegroundColor Red
    exit 1
}

# Check if mkdocs.yml exists
if (-not (Test-Path "mkdocs.yml")) {
    Write-Host "✗ mkdocs.yml not found" -ForegroundColor Red
    exit 1
}

# Install dependencies if requested or if serving
if ($Install -or $Serve) {
    Install-Dependencies
}

# Build documentation if requested
if ($Build) {
    Build-Documentation
}

# Serve documentation if requested
if ($Serve) {
    Serve-Documentation
}

# If no specific action requested, show help
if (-not ($Serve -or $Build -or $Install)) {
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\deploy.ps1 -Serve     # Start development server"
    Write-Host "  .\deploy.ps1 -Build     # Build static site"
    Write-Host "  .\deploy.ps1 -Install   # Install dependencies"
    Write-Host "  .\deploy.ps1 -Clean     # Clean build (use with -Build)"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\deploy.ps1 -Serve -Install  # Install and serve"
    Write-Host "  .\deploy.ps1 -Build -Clean    # Clean build"
    Write-Host ""
}
