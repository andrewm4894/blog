# andrewm4894 Blog

A personal blog focused on Data Science and Machine Learning, built with Jekyll and hosted on GitHub Pages.

## Overview

This blog was migrated from WordPress and is now powered by Jekyll, using the Minimal theme. It's hosted on GitHub Pages at [andrewm4894.com](https://andrewm4894.com).

## Technical Stack

- **Framework**: Jekyll
- **Theme**: Minimal (pages-themes/minimal)
- **Hosting**: GitHub Pages
- **Plugins**:
  - jekyll-feed
  - jekyll-seo-tag
  - jekyll-remote-theme

## Branch Preview System 🚀

This blog includes an automated branch preview system that creates deployments for every branch and pull request.

### How It Works

1. **Branch Previews**: When you push to any branch (except `main`), a preview is automatically built and deployed to `https://andrewm4894.com/preview/{branch-name}/`

2. **Pull Request Previews**: When you create a PR, a preview is deployed to `https://andrewm4894.com/preview/pr-{number}/` and a comment is added to the PR with the preview link

3. **Preview Index**: All active previews are listed at `https://andrewm4894.com/preview/`

4. **Automatic Cleanup**: Old previews are cleaned up weekly, removing previews for deleted branches and closed PRs

### Workflows

- **Branch Preview Deploy** (`.github/workflows/branch-preview.yml`): Builds previews for branches and PRs
- **Deploy Main Site** (`.github/workflows/pages-preview.yml`): Deploys the main site while preserving previews
- **Cleanup Old Previews** (`.github/workflows/cleanup-previews.yml`): Weekly cleanup of stale previews

### Using Previews

1. Create a new branch: `git checkout -b feature/my-new-post`
2. Make your changes and push: `git push origin feature/my-new-post`
3. Visit the Actions tab to see the deployment progress
4. Once complete, visit `https://andrewm4894.com/preview/feature-my-new-post/`
5. Create a PR to get an additional PR-specific preview

### Local Preview Testing

Use the included script to test your changes locally before pushing:

```bash
# Test how your branch will look as a preview
./preview-local.sh feature-my-new-post

# Or test the current branch
./preview-local.sh
```

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
