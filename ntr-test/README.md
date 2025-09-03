# Help Content Management

This directory contains all the help content for the Training Management System. The content is stored as Markdown files and can be edited directly in GitHub.

## File Structure

```
docs/help/
├── help-config.json          # Configuration file defining help sections
├── overview.md               # System overview (Swedish)
├── vouchers.md               # Voucher system (Swedish)
├── user-management.md        # User management (Swedish)
├── training-management.md    # Training management (Swedish)
├── subscriptions.md          # Training subscriptions (Swedish)
├── attendance.md             # Attendance management (Swedish)
├── troubleshooting.md        # Troubleshooting (Swedish)
├── en/                       # English translations
│   ├── overview.md
│   ├── vouchers.md
│   ├── user-management.md
│   ├── training-management.md
│   ├── subscriptions.md
│   ├── attendance.md
│   └── troubleshooting.md
└── README.md                 # This file
```

## How to Edit Help Content

### For Administrators
1. Navigate to the help system in the application
2. Click the "Edit on GitHub" button (only visible to admins)
3. This will take you directly to the GitHub repository where you can edit the Markdown files
4. Make your changes and commit them
5. The changes will be automatically deployed when the application is rebuilt

### For Developers
1. Edit the Markdown files directly in this directory
2. Follow the existing format and structure
3. Update both Swedish and English versions if needed
4. Test your changes by rebuilding the application

## Content Guidelines

### Markdown Format
- Use standard Markdown syntax
- Headers: `#` for main title, `##` for sections
- Lists: Use `-` for bullet points
- **Bold text** for emphasis
- *Italic text* for additional emphasis

### Content Structure
Each help file should follow this structure:
1. **Main title** (H1) - Brief, descriptive title
2. **Sections** (H2) - Logical grouping of information
3. **Subsections** (H3) - Detailed explanations
4. **Lists** - Step-by-step instructions or key points
5. **Best Practices** - Tips and recommendations

### Language Guidelines
- Keep content clear and concise
- Use active voice
- Include step-by-step instructions where appropriate
- Provide examples when helpful
- Maintain consistency in terminology

## Configuration

The `help-config.json` file defines:
- Section IDs and titles
- Keywords for context-sensitive help
- Categories (admin, user, general)
- Language mappings

### Adding New Help Sections

1. Create the Markdown files for both languages
2. Add the section configuration to `help-config.json`
3. Update the help service if needed
4. Test the new section in the application

### Keywords for Context Matching

Keywords are used to automatically select relevant help content based on the user's current context. Choose keywords that:
- Are specific to the section's topic
- Match common user queries
- Include both general and specific terms
- Cover both Swedish and English variations

## Deployment

### Automatic GitHub Pages Deployment

This documentation is automatically deployed to GitHub Pages after every push to the main branch using GitHub Actions.

**Features:**
- ✅ Automatic deployment on every push
- ✅ Built with MkDocs and Material theme
- ✅ Available at: `https://[username].github.io/[repository-name]/`
- ✅ No manual intervention required

**Setup:**
1. The GitHub Actions workflow (`.github/workflows/deploy.yml`) is already configured
2. Enable GitHub Pages in your repository settings
3. Select "GitHub Actions" as the source
4. Push changes to trigger automatic deployment

For detailed setup instructions, see [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md).

### Local Development

For local development and testing:
```bash
cd ntr-test
pip install -r requirements.txt
mkdocs serve
```

The documentation will be available at `http://localhost:8000`

### Manual Deployment

If you need to deploy manually:
```bash
cd ntr-test
mkdocs build
mkdocs gh-deploy
```

No database changes are required since content is loaded from Markdown files.
