# Translation Setup Script for NTR Documentation
# This script helps set up the automated translation system

param(
    [switch]$Install,
    [switch]$Configure,
    [switch]$Test,
    [switch]$Help
)

Write-Host "NTR Documentation Translation Setup" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

function Show-Help {
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\setup-translation.ps1 -Install     # Install dependencies and setup hooks"
    Write-Host "  .\setup-translation.ps1 -Configure   # Configure translation settings"
    Write-Host "  .\setup-translation.ps1 -Test        # Test translation system"
    Write-Host "  .\setup-translation.ps1 -Help        # Show this help"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\setup-translation.ps1 -Install -Configure  # Full setup"
    Write-Host ""
}

function Install-Dependencies {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    
    try {
        pip install -r requirements.txt
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        Write-Host "Please ensure Python and pip are installed and try again." -ForegroundColor Yellow
        return $false
    }
    return $true
}

function Setup-GitHooks {
    Write-Host "Setting up Git hooks..." -ForegroundColor Yellow
    
    $hooksDir = ".git\hooks"
    if (-not (Test-Path $hooksDir)) {
        Write-Host "✗ Git repository not found. Please run this script from a git repository." -ForegroundColor Red
        return $false
    }
    
    # Copy the pre-commit hook
    $preCommitHook = "$hooksDir\pre-commit"
    if (Test-Path "pre-commit.ps1") {
        Copy-Item "pre-commit.ps1" $preCommitHook -Force
        Write-Host "✓ PowerShell pre-commit hook installed" -ForegroundColor Green
    } elseif (Test-Path ".git\hooks\pre-commit") {
        Write-Host "✓ Bash pre-commit hook already installed" -ForegroundColor Green
    } else {
        Write-Host "✗ Pre-commit hook file not found" -ForegroundColor Red
        return $false
    }
    
    return $true
}

function Configure-Translation {
    Write-Host "Configuring translation settings..." -ForegroundColor Yellow
    
    # Check if DeepL API key is set
    $deeplKey = $env:DEEPL_API_KEY
    if (-not $deeplKey) {
        Write-Host "DeepL API key not found in environment variables." -ForegroundColor Yellow
        Write-Host "To get a free API key, visit: https://www.deepl.com/pro-api" -ForegroundColor Cyan
        
        $setKey = Read-Host "Would you like to set the DeepL API key now? (y/n)"
        if ($setKey -eq 'y' -or $setKey -eq 'Y') {
            $newKey = Read-Host "Enter your DeepL API key" -AsSecureString
            $env:DEEPL_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($newKey))
            
            Write-Host "API key set for current session." -ForegroundColor Green
            Write-Host "To make it permanent, add DEEPL_API_KEY to your environment variables." -ForegroundColor Yellow
        }
    } else {
        Write-Host "✓ DeepL API key found" -ForegroundColor Green
    }
    
    # Check configuration files
    if (Test-Path "translation-config.json") {
        Write-Host "✓ Translation configuration found" -ForegroundColor Green
    } else {
        Write-Host "✗ Translation configuration not found" -ForegroundColor Red
        return $false
    }
    
    if (Test-Path "help-config.json") {
        Write-Host "✓ Help configuration found" -ForegroundColor Green
    } else {
        Write-Host "✗ Help configuration not found" -ForegroundColor Red
        return $false
    }
    
    return $true
}

function Test-Translation {
    Write-Host "Testing translation system..." -ForegroundColor Yellow
    
    # Check if Python script exists
    if (-not (Test-Path "translate.py")) {
        Write-Host "✗ Translation script not found" -ForegroundColor Red
        return $false
    }
    
    # Test with a sample file
    $testFile = "docs\en\overview.md"
    if (Test-Path $testFile) {
        Write-Host "Testing translation with $testFile..." -ForegroundColor Cyan
        
        try {
            python translate.py --mode translate-file --source-file $testFile --target-lang SV --source-lang EN
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Translation test successful" -ForegroundColor Green
                return $true
            } else {
                Write-Host "✗ Translation test failed" -ForegroundColor Red
                return $false
            }
        } catch {
            Write-Host "✗ Translation test failed: $($_.Exception.Message)" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "✗ Test file not found: $testFile" -ForegroundColor Red
        return $false
    }
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

$success = $true

if ($Install) {
    $success = $success -and (Install-Dependencies)
    $success = $success -and (Setup-GitHooks)
}

if ($Configure) {
    $success = $success -and (Configure-Translation)
}

if ($Test) {
    $success = $success -and (Test-Translation)
}

# If no specific action requested, show help
if (-not ($Install -or $Configure -or $Test)) {
    Show-Help
    exit 0
}

if ($success) {
    Write-Host ""
    Write-Host "✓ Translation setup completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Set your DeepL API key as environment variable: DEEPL_API_KEY" -ForegroundColor Cyan
    Write-Host "2. Make changes to English documentation files" -ForegroundColor Cyan
    Write-Host "3. Commit changes - translations will happen automatically" -ForegroundColor Cyan
    Write-Host "4. Check translation.log for any issues" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "✗ Translation setup failed. Please check the errors above." -ForegroundColor Red
    exit 1
}
