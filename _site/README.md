# andrewm4894 Blog

A personal blog focused on Data Science and Machine Learning, built with Jekyll and hosted on GitHub Pages.

## Overview

This blog was migrated from WordPress and is now powered by Jekyll, using the Minimal theme. It's hosted on GitHub Pages at [andrewmaguire.github.io/blog](https://andrewmaguire.github.io/blog).

## Technical Stack

- **Framework**: Jekyll
- **Theme**: Minimal (pages-themes/minimal)
- **Hosting**: GitHub Pages
- **Plugins**:
  - jekyll-feed
  - jekyll-seo-tag
  - jekyll-remote-theme

## Development

### Prerequisites

- Ruby
- Bundler
- Make (for using the Makefile)

### Setup

1. Install dependencies:
   ```bash
   bundle install
   ```

2. Run locally:
   ```bash
   make serve
   ```

### Project Structure

- `_posts/`: Blog posts in Markdown format
- `_layouts/`: Custom layout templates
- `assets/`: Static assets (images, CSS, etc.)
- `_config.yml`: Jekyll configuration
- `fix_images.py` & `fix_posts.sh`: Migration utilities

## License

All content is © andrewm4894. All rights reserved.
