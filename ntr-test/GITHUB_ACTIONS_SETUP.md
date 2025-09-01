# GitHub Actions Translation Setup

This guide explains how to set up automatic translation PRs using GitHub Actions.

## Overview

The GitHub Action workflow will automatically:
1. Detect when documentation files are updated in any language
2. Translate the changes to all other configured languages
3. Create a pull request with the title "Translation needed - content update"
4. Include all translated files for review

## Setup Requirements

### 1. Repository Secrets

You need to add the following secrets to your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:

**DEEPL_API_KEY**
- Your DeepL API key for translation services
- Get one from: https://www.deepl.com/pro-api

**GITHUB_TOKEN** (usually auto-configured)
- Used for creating pull requests
- Should be automatically available in GitHub Actions

### 2. File Structure

Ensure your documentation follows this structure:
```
docs/
├── en/
│   ├── overview.md
│   ├── subscriptions.md
│   └── ...
├── sv/
│   ├── overview.md
│   ├── subscriptions.md
│   └── ...
└── ...
```

### 3. Configuration File

Make sure your `help-config.json` file is properly configured with:
- Language configurations for all supported languages
- File path mappings for each language
- DeepL API configuration

## How It Works

1. **Trigger**: The workflow triggers when any `.md` file in the `docs/` directory is pushed to the `main` branch
2. **Detection**: It detects which files were changed in the last commit
3. **Translation**: Runs bidirectional translation between all configured languages
4. **PR Creation**: Creates a new branch with translations and opens a PR

## Workflow Steps

1. **Checkout**: Gets the repository code
2. **Setup**: Installs Python and dependencies
3. **GitHub CLI**: Installs GitHub CLI for PR creation
4. **Translation**: Runs the translation script
5. **Commit**: Commits translation changes to a new branch
6. **PR**: Creates a pull request for review

## Testing the Setup

To test if the workflow is working:

1. Make a small change to any documentation file in `docs/en/` or `docs/sv/`
2. Commit and push the change to the `main` branch
3. Check the Actions tab in your repository
4. You should see a new workflow run
5. If successful, a new PR titled "Translation needed - content update" will be created

## Troubleshooting

### Workflow Not Triggering
- Ensure files are in the `docs/` directory
- Check that the workflow file is in `.github/workflows/`
- Verify the branch name is `main`

### Translation Fails
- Check that `DEEPL_API_KEY` secret is set
- Verify your `help-config.json` is properly configured
- Check the workflow logs for specific error messages

### PR Not Created
- Ensure `GITHUB_TOKEN` has sufficient permissions
- Check that GitHub CLI is properly installed
- Verify the repository has pull request creation enabled

## Manual Testing

You can test the translation script locally:

```bash
# Test the GitHub Actions mode
python translate.py --mode github-actions

# Test sync all languages
python translate.py --mode sync-all

# Test specific file translation
python translate.py --mode translate-file --source-file docs/en/subscriptions.md --target-lang SV
```

## Configuration

The workflow uses these key files:
- `.github/workflows/auto-translate.yml` - GitHub Action workflow
- `translate.py` - Translation script
- `help-config.json` - Language and file configuration
- `requirements.txt` - Python dependencies
