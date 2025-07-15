# Manim Documentation

This directory contains the source code for the Manim documentation website.


## Building the Documentation

To build the documentation locally:

1. Install the documentation requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the HTML documentation:
   ```bash
   make html
   ```

3. Open `_build/html/index.html` in your browser.

## GitHub Pages Deployment

The documentation is automatically built and deployed to GitHub Pages using GitHub Actions. The workflow:

1. Monitors changes to `docs/` and `manimlib/` directories
2. Builds the documentation using Sphinx
3. Deploys to GitHub Pages at `https://[username].github.io/[repo-name]/`

## Documentation Structure

- `conf.py` - Sphinx configuration
- `index.rst` - Main documentation entry point
- `_static/` - Static assets (CSS, JS, images)
- `_templates/` - Custom templates
- `_build/` - Generated HTML files (ignored by git)

## Features

- **Comprehensive API Reference**: Auto-generated from docstrings
- **Search Functionality**: Full-text search across all documentation
- **Cross-references**: Automatic linking between classes and methods
- **Mobile-friendly**: Responsive design that works on all devices
- **Dark/Light Theme**: Professional RTD theme with theme switcher

The documentation includes complete coverage of:
- Scene classes and methods
- Mobject types and operations  
- Animation classes and effects
- Camera and rendering systems
- Utility functions and helpers
- Configuration and constants
