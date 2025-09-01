# Automated Translation System for NTR Documentation

This system automatically translates documentation between English and Swedish using DeepL API, triggered by Git commits.

## Features

- **Bidirectional Translation**: Translates between any configured languages
- **Automatic Translation**: Translates changed files on every commit
- **Pull Request Workflow**: Creates PRs for review before merging
- **DeepL Integration**: Uses DeepL's high-quality translation API
- **Git Hooks**: Pre-commit hooks for seamless integration
- **Multi-language Support**: Supports translation between all configured languages
- **Preserves Formatting**: Maintains markdown structure and metadata
- **Logging**: Comprehensive logging for troubleshooting

## Quick Setup

### 1. Install Dependencies

```powershell
# Windows (PowerShell)
.\setup-translation.ps1 -Install

# Linux/Mac (Bash)
pip install -r requirements.txt
```

### 2. Configure DeepL API

Get a free API key from [DeepL Pro](https://www.deepl.com/pro-api) and set it as an environment variable:

```powershell
# Windows (PowerShell)
$env:DEEPL_API_KEY = "your-api-key-here"

# Linux/Mac (Bash)
export DEEPL_API_KEY="your-api-key-here"
```

### 3. Setup Git Hooks

```powershell
# Windows (PowerShell)
.\setup-translation.ps1 -Install

# Linux/Mac (Bash)
chmod +x .git/hooks/pre-commit
```

### 4. Test the System

```powershell
# Windows (PowerShell)
.\setup-translation.ps1 -Test

# Linux/Mac (Bash)
python translate.py --mode translate-file --source-file docs/en/overview.md --target-lang SV
```

## Usage

### Automatic Translation with Pull Requests (Recommended)

1. Make changes to English documentation files
2. Stage your changes: `git add .`
3. Commit: `git commit -m "Update documentation"`
4. The pre-commit hook automatically:
   - Creates a new branch for translations
   - Translates changes to Swedish
   - Commits translated files to the branch
   - Creates a pull request for review
5. Review the PR and merge when satisfied

### Manual Translation

```bash
# Translate a specific file
python translate.py --mode translate-file --source-file docs/en/overview.md --target-lang SV

# Translate between specific languages
python translate.py --mode translate-lang --from-lang en-se --to-lang sv-se

# Sync all files between all languages (bidirectional)
python translate.py --mode sync-all

# Translate changed files (git hook mode)
python translate.py --mode git-hook
```

## Configuration

### Translation Settings (`translation-config.json`)

```json
{
  "translation": {
    "provider": "deepl",
    "languages": {
      "bidirectional": true,
      "supported_languages": ["en-se", "sv-se"],
      "default_source": "en-se"
    },
    "translation_options": {
      "preserve_metadata": true,
      "preserve_links": true,
      "preserve_code_blocks": true
    }
  }
}
```

### Language Configuration (`help-config.json`)

The system uses your existing `help-config.json` to map files between languages:

```json
{
  "apps": {
    "ntr-app": {
      "locales": {
        "en-se": {
          "code": "en",
          "file_paths": {
            "overview": "docs/en/overview.md"
          }
        },
        "sv-se": {
          "code": "sv", 
          "file_paths": {
            "overview": "docs/sv/overview.md"
          }
        }
      }
    }
  }
}
```

## File Structure

```
ntr-test/
├── translate.py                 # Main translation script
├── setup-translation.ps1       # Setup script (Windows)
├── translation-config.json     # Translation settings
├── help-config.json           # Language mapping
├── requirements.txt           # Python dependencies
├── .git/hooks/
│   ├── pre-commit            # Git hook (Bash)
│   └── pre-commit.ps1        # Git hook (PowerShell)
└── docs/
    ├── en/                   # English documentation
    └── sv/                   # Swedish documentation
```

## How It Works

1. **Detection**: Git pre-commit hook detects changed markdown files
2. **Branch Creation**: Creates a new branch for translation changes
3. **Mapping**: System finds corresponding files in ALL other languages using `help-config.json`
4. **Translation**: DeepL API translates content while preserving structure
5. **Commit**: Translated files are committed to the translation branch
6. **Pull Request**: Creates a PR for review before merging
7. **Review**: Team reviews and approves the translations
8. **Merge**: PR is merged after approval

## Bidirectional Translation

The system now supports translation between any configured languages:

### Automatic Translation (Git Hook)
- When you change a file in ANY language, it automatically translates to ALL other languages
- Example: Change `docs/sv/overview.md` → translates to `docs/en/overview.md`
- Example: Change `docs/en/user-management.md` → translates to `docs/sv/user-management.md`

### Manual Translation Modes

#### 1. **translate-lang**: Translate between specific languages
```bash
# Swedish to English
python translate.py --mode translate-lang --from-lang sv-se --to-lang en-se

# English to Swedish
python translate.py --mode translate-lang --from-lang en-se --to-lang sv-se
```

#### 2. **sync-all**: Sync all languages with each other
```bash
# Translates all files between all configured languages
python translate.py --mode sync-all
```

#### 3. **translate-file**: Translate a specific file
```bash
# Translate any file to any language
python translate.py --mode translate-file --source-file docs/sv/overview.md --target-lang EN --source-lang SV
```

## Pull Request Workflow

### Automatic PR Creation

The system automatically creates pull requests for translation changes:

1. **Branch Creation**: Creates a branch named `auto-translate-YYYYMMDD-HHMMSS`
2. **Translation**: Translates all changed files to target languages
3. **Commit**: Commits translated files with descriptive messages
4. **PR Creation**: Creates a pull request with:
   - List of translated files
   - Translation details (provider, timestamp)
   - Review instructions
   - Manual PR creation instructions (if GitHub CLI not available)

### PR Review Process

1. **Review Content**: Check translated text for accuracy
2. **Verify Formatting**: Ensure markdown structure is preserved
3. **Test Links**: Verify all links work correctly
4. **Approve**: Approve the PR if satisfied
5. **Merge**: Merge the PR to integrate translations

### Manual PR Creation

If GitHub CLI is not available, the system creates a PR template file:
- File: `PR_TEMPLATE_{branch_name}.md`
- Contains title, body, and manual steps
- Follow the instructions to create the PR manually

## Troubleshooting

### Common Issues

**Translation not working:**
- Check if `DEEPL_API_KEY` environment variable is set
- Verify DeepL API key is valid and has credits
- Check `translation.log` for error messages

**Git hook not running:**
- Ensure hook files are executable: `chmod +x .git/hooks/pre-commit`
- Check if Python and dependencies are installed
- Verify `translate.py` exists in project root

**Files not being translated:**
- Check if files are in the correct paths defined in `help-config.json`
- Ensure files have `.md` extension
- Verify file paths match exactly

### Logs

Translation logs are saved to `translation.log`:

```bash
# View recent logs
tail -f translation.log

# Search for errors
grep "ERROR" translation.log
```

### Manual Testing

```bash
# Test translation with a sample file
python translate.py --mode translate-file --source-file docs/en/overview.md --target-lang SV

# Test git hook mode
python translate.py --mode git-hook

# Test full sync
python translate.py --mode sync-all
```

## Advanced Configuration

### Custom Translation Providers

To use a different translation service, modify `translate.py`:

```python
def translate_text(self, text: str, target_lang: str, source_lang: str = "EN") -> str:
    # Replace DeepL API call with your preferred service
    # Example: Google Translate, Azure Translator, etc.
    pass
```

### Custom File Patterns

Modify `translation-config.json` to include/exclude specific files:

```json
{
  "file_patterns": {
    "include": ["*.md", "*.txt"],
    "exclude": ["drafts/**", "archived/**"]
  }
}
```

### Batch Translation

For bulk translation of existing files:

```bash
# Translate all English files to Swedish
python translate.py --mode sync-all

# Translate specific sections
python translate.py --mode translate-file --source-file docs/en/user-management.md --target-lang SV
```

## API Limits and Costs

- **DeepL Free**: 500,000 characters/month
- **DeepL Pro**: Pay-per-use pricing
- **Rate Limits**: 25 requests/second for free tier

Monitor usage in your DeepL account dashboard.

## Support

For issues or questions:
1. Check `translation.log` for error messages
2. Verify configuration files are correct
3. Test with manual translation commands
4. Ensure all dependencies are installed

## Contributing

To extend the translation system:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This translation system is part of the NTR documentation project.
