.PHONY: install serve build clean preview check-images

# Install dependencies
install:
	brew install rbenv ruby-build || true
	rbenv install 3.1.4 || true
	rbenv global 3.1.4
	rbenv rehash || true
	gem install bundler -v 2.4.22
	bundle init || true
	bundle add jekyll || true
	bundle add github-pages || true
	bundle add webrick || true
	bundle install

# Serve the site locally
serve:
	bundle exec jekyll serve --livereload

# Build the site
build:
	bundle exec jekyll build

# Clean the site
clean:
	bundle exec jekyll clean
	rm -rf .jekyll-cache
	rm -rf _site
	rm -rf vendor

# Preview current branch locally as it would appear in production
preview:
	./scripts/preview-local.sh

# Preview a specific branch locally
preview-branch:
	@read -p "Enter branch name: " branch; ./scripts/preview-local.sh $$branch

# Check for broken image links in posts
check-images:
	python3 scripts/check_broken_image_links.py

# Generate detailed report of broken image links
check-images-report:
	python3 scripts/check_broken_image_links.py --report

# Generate script to fix broken image links
check-images-fix:
	python3 scripts/check_broken_image_links.py --fix-script

# Fix markdown image links in posts (dry run)
fix-image-links:
	python3 scripts/fix_markdown_image_links.py

# Actually apply image link fixes
fix-image-links-apply:
	python3 scripts/fix_markdown_image_links.py --apply

# Default target
all: install serve 