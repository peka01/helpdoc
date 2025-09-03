# StackEdit Integration Guide

This guide explains how to use the StackEdit integration features in your NTR Help Documentation repository.

## What is StackEdit?

[StackEdit](https://stackedit.io/app#) is a powerful, free, open-source Markdown editor that provides:

- **Real-time preview** of Markdown content
- **GitHub integration** for direct repository access
- **Cloud storage** support (Google Drive, Dropbox, OneDrive)
- **Multiple export formats** (HTML, PDF, Markdown)
- **Advanced Markdown features** (MathJax, Mermaid diagrams, etc.)
- **Collaborative editing** capabilities

## Integration Options

### 1. Embedded Editor in Documentation

The StackEdit editor is now embedded in your documentation at `/stackedit-editor/`. Users can:

- Access the editor directly from your documentation
- Write and preview Markdown in real-time
- Save content to various cloud services
- Export to different formats

**Access**: Navigate to **Tools → StackEdit Editor** in your documentation navigation.

### 2. Standalone Full-Screen Editor

A standalone HTML file (`stackedit-standalone.html`) provides a full-screen editing experience:

- Full-screen StackEdit interface
- Custom header with navigation back to docs
- Responsive design for all devices
- Direct access without going through MkDocs

**Usage**: Open `stackedit-standalone.html` in any web browser.

### 3. Python Integration Script

A Python script (`stackedit_integration.py`) provides command-line integration:

- Open StackEdit with specific files
- Create new Markdown files
- Manage favorites and recent files
- Sync with GitHub repository
- Batch operations

## Quick Start

### Option A: Use Embedded Editor

1. Navigate to your documentation site
2. Go to **Tools → StackEdit Editor**
3. Start writing Markdown in the embedded editor
4. Use the toolbar to save, export, or manage files

### Option B: Use Standalone Editor

1. Open `stackedit-standalone.html` in your browser
2. Start editing immediately in full-screen mode
3. Use the toolbar to navigate back to docs or open in new tab

### Option C: Use Python Script

1. Make sure you have Python 3.6+ installed
2. Navigate to your repository directory
3. Run the integration script:

```bash
# Open StackEdit
python stackedit_integration.py

# Open a specific file
python stackedit_integration.py --open docs/en/overview.md

# Create a new file
python stackedit_integration.py --create "New Guide" --content "This is a new guide..."

# List all markdown files
python stackedit_integration.py --list

# Sync with GitHub
python stackedit_integration.py --sync "Update documentation"
```

## Python Script Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--open <file>` | Open specific file in StackEdit | `--open docs/en/overview.md` |
| `--create <title>` | Create new markdown file | `--create "User Guide"` |
| `--content <text>` | Set content for new file | `--content "Welcome to the guide"` |
| `--list` | List all markdown files | `--list` |
| `--recent` | Show recently opened files | `--recent` |
| `--favorites` | Show favorite files | `--favorites` |
| `--add-favorite <file>` | Add file to favorites | `--add-favorite overview.md` |
| `--remove-favorite <file>` | Remove file from favorites | `--remove-favorite overview.md` |
| `--sync <message>` | Sync with GitHub | `--sync "Update docs"` |
| `--no-browser` | Don't open browser automatically | `--no-browser` |

## Configuration

The Python script creates a `stackedit_config.json` file that stores:

- Recent files list
- Favorite files
- StackEdit URL
- Browser auto-open preference

You can edit this file manually or use the script commands to manage it.

## Workflow Examples

### Creating New Documentation

1. **Start with Python script:**
   ```bash
   python stackedit_integration.py --create "API Reference" --content "## Overview\n\nThis guide covers..."
   ```

2. **Edit in StackEdit:**
   - Open the created file in StackEdit
   - Add content with real-time preview
   - Save to cloud storage

3. **Sync to repository:**
   ```bash
   python stackedit_integration.py --sync "Add API Reference documentation"
   ```

### Editing Existing Documentation

1. **Open file in StackEdit:**
   ```bash
   python stackedit_integration.py --open docs/en/user-management.md
   ```

2. **Make changes in StackEdit**
3. **Save and sync:**
   ```bash
   python stackedit_integration.py --sync "Update user management guide"
   ```

### Batch Operations

1. **List all files:**
   ```bash
   python stackedit_integration.py --list
   ```

2. **Add frequently used files to favorites:**
   ```bash
   python stackedit_integration.py --add-favorite overview.md
   python stackedit_integration.py --add-favorite user-management.md
   ```

3. **View favorites:**
   ```bash
   python stackedit_integration.py --favorites
   ```

## Features and Benefits

### For Content Creators
- **Real-time preview** eliminates the need to switch between editor and preview
- **Rich Markdown support** including tables, code blocks, and diagrams
- **Cloud storage integration** ensures work is never lost
- **Export options** for sharing and distribution

### For Teams
- **GitHub integration** for seamless repository management
- **Collaborative editing** capabilities
- **Version control** through Git integration
- **Consistent formatting** across team members

### For Documentation Managers
- **Centralized editing** through embedded interface
- **Quality control** with real-time preview
- **Workflow integration** through Python scripting
- **Multi-format export** for different use cases

## Troubleshooting

### Common Issues

1. **Editor not loading:**
   - Check internet connection
   - Try opening in new tab: `https://stackedit.io/app#`
   - Clear browser cache

2. **Python script errors:**
   - Ensure Python 3.6+ is installed
   - Check file permissions
   - Verify you're in the correct directory

3. **Git sync issues:**
   - Ensure Git is installed and configured
   - Check repository permissions
   - Verify remote origin is set

### Getting Help

- **StackEdit documentation**: [https://stackedit.io/](https://stackedit.io/)
- **StackEdit GitHub**: [https://github.com/benweet/stackedit](https://github.com/benweet/stackedit)
- **Markdown guide**: [https://www.markdownguide.org/](https://www.markdownguide.org/)

## Advanced Usage

### Customizing the Integration

You can modify the integration files to:

- Change the StackEdit URL
- Customize the embedded editor size
- Add custom CSS styling
- Integrate with other tools

### Extending Functionality

The Python script can be extended to:

- Add more file format support
- Integrate with other documentation tools
- Add validation and linting
- Implement automated workflows

## Conclusion

The StackEdit integration provides a powerful, professional editing experience for your documentation while maintaining the simplicity and accessibility of your existing MkDocs setup. Whether you prefer the embedded editor, standalone interface, or command-line tools, you have multiple options to enhance your documentation workflow.

Start with the embedded editor for quick access, use the standalone version for focused editing sessions, and leverage the Python script for advanced workflow automation.
