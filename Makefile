.PHONY: install serve build clean

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

# Default target
all: install serve 