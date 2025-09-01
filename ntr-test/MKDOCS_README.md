# MkDocs Setup for Training Management System Help

This directory contains the MkDocs configuration and documentation for the Training Management System help content.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Serve the documentation locally:**
   ```bash
   mkdocs serve
   ```

3. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:8000
   ```

## Project Structure

```
ntr-test/
├── mkdocs.yml                 # MkDocs configuration
├── requirements.txt           # Python dependencies
├── index.md                  # Homepage
├── stylesheets/
│   └── extra.css             # Custom CSS styles
├── javascripts/
│   └── mathjax.js            # MathJax configuration
├── en/                       # English documentation
│   ├── overview.md
│   ├── vouchers.md
│   ├── user-management.md
│   ├── training-management.md
│   ├── subscriptions.md
│   ├── attendance.md
│   └── troubleshooting.md
├── sv/                       # Swedish documentation
│   ├── overview.md
│   ├── vouchers.md
│   ├── user-management.md
│   ├── training-management.md
│   ├── subscriptions.md
│   ├── attendance.md
│   └── troubleshooting.md
├── CONTENT_GUIDELINES.md     # Content writing standards
├── TONE_AND_VOICE_GUIDELINES.md
├── WRITING_CHECKLIST.md
└── help-config.json          # Original help configuration
```

## Features

### 🎨 Material Theme
- Modern, responsive design
- Dark/light mode toggle
- Mobile-friendly navigation
- Search functionality

### 🌐 Multilingual Support
- Swedish and English documentation
- Organized navigation by language
- Consistent structure across languages

### 📱 Responsive Design
- Works on desktop, tablet, and mobile
- Optimized for different screen sizes
- Touch-friendly navigation

### 🔍 Advanced Features
- Full-text search
- Table of contents
- Code syntax highlighting
- Mathematical notation support
- Git revision dates

## Commands

### Development
```bash
# Start local development server
mkdocs serve

# Start with auto-reload on file changes
mkdocs serve --livereload

# Build static site
mkdocs build

# Clean build directory
mkdocs build --clean
```

### Deployment
```bash
# Build for production
mkdocs build

# Deploy to GitHub Pages (if configured)
mkdocs gh-deploy
```

## Configuration

### mkdocs.yml
The main configuration file includes:

- **Site metadata** (name, description, author)
- **Theme settings** (Material theme with custom palette)
- **Navigation structure** (organized by content type and language)
- **Plugins** (search, git revision dates, minification)
- **Markdown extensions** (admonitions, code highlighting, etc.)

### Custom Styling
- `stylesheets/extra.css` - Custom CSS for enhanced appearance
- Responsive design improvements
- Role-based section styling
- Print-friendly styles

## Content Management

### Adding New Content

1. **Create the content file:**
   - Place in appropriate language directory (`en/` or `sv/`)
   - Follow existing naming conventions
   - Use `.md` extension

2. **Update navigation:**
   - Edit `mkdocs.yml` to add new page to navigation
   - Maintain consistent structure across languages

3. **Follow content guidelines:**
   - Refer to `CONTENT_GUIDELINES.md`
   - Use established tone and voice
   - Include both Swedish and English versions

### Content Guidelines

- **Swedish is the master language** - Write Swedish content first
- **Translate to English** - Maintain same structure and meaning
- **Use established formatting** - Follow existing patterns
- **Test instructions** - Verify all steps work correctly
- **Update both languages** - Keep versions synchronized

## Deployment

### Local Development
```bash
mkdocs serve
```

### Production Build
```bash
mkdocs build
```

### GitHub Pages Deployment
```bash
mkdocs gh-deploy
```

## Customization

### Theme Customization
Edit `mkdocs.yml` to modify:
- Color scheme
- Navigation features
- Theme options

### Styling
Modify `stylesheets/extra.css` to:
- Change appearance
- Add custom components
- Improve responsive design

### Plugins
Add or configure plugins in `mkdocs.yml`:
- Additional search features
- Content processing
- Export options

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   mkdocs serve -a 127.0.0.1:8001
   ```

2. **Missing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Build errors:**
   - Check markdown syntax
   - Verify file paths in navigation
   - Ensure all referenced files exist

### Getting Help

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Issues](https://github.com/mkdocs/mkdocs/issues)

## Contributing

1. **Follow content guidelines** in `CONTENT_GUIDELINES.md`
2. **Test changes locally** before committing
3. **Update both languages** when making changes
4. **Use descriptive commit messages**
5. **Review and test** all instructions

## License

This documentation is part of the Training Management System project.
