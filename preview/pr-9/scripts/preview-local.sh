#!/bin/bash

# Local preview script for testing branch previews
# Usage: ./preview-local.sh [branch-name]
# If no branch name provided, uses current branch

set -e

# Get branch name - use argument if provided, otherwise current branch
if [ -n "$1" ]; then
    BRANCH_NAME="$1"
else
    BRANCH_NAME=$(git branch --show-current)
fi

# Sanitize branch name for URL (same logic as GitHub Actions)
PREVIEW_PATH=$(echo "$BRANCH_NAME" | sed 's/[^a-zA-Z0-9-]/-/g' | tr '[:upper:]' '[:lower:]')

echo "🚀 Building local preview for branch: $BRANCH_NAME"
echo "📁 Preview path: $PREVIEW_PATH"
echo "🌐 Local URL will be: http://localhost:4000/preview/$PREVIEW_PATH/"
echo ""

# Clean any previous builds
echo "🧹 Cleaning previous builds..."
bundle exec jekyll clean

# Build with the preview configuration
echo "🔨 Building site with preview baseurl..."
bundle exec jekyll build -d "_site/preview/$PREVIEW_PATH" --baseurl "/preview/$PREVIEW_PATH"

# Create a simple preview index
echo "📄 Creating preview index..."
mkdir -p _site/preview
cat > _site/preview/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Local Branch Previews</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
        h1 { color: #333; }
        .preview-item { 
            background: #f5f5f5; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 5px; 
            border-left: 4px solid #007cba;
        }
        .preview-item a { 
            text-decoration: none; 
            color: #007cba; 
            font-weight: bold; 
            font-size: 18px;
        }
        .preview-item a:hover { text-decoration: underline; }
        .preview-meta { color: #666; font-size: 14px; margin-top: 5px; }
        .local-note {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>🚀 Local Branch Previews</h1>
    
    <div class="local-note">
        <strong>📍 Local Testing:</strong> This is a local preview. The actual deployed preview will be available at andrewm4894.com/preview/ after pushing to GitHub.
    </div>
    
    <div class="preview-item">
        <a href="/preview/$PREVIEW_PATH/">$PREVIEW_PATH</a>
        <div class="preview-meta">
            Branch: $BRANCH_NAME | Status: Local Preview | Built: $(date)
        </div>
    </div>
</body>
</html>
EOF

# Start the server
echo "🌐 Starting local server..."
echo "Preview will be available at: http://localhost:4000/preview/$PREVIEW_PATH/"
echo "All previews index: http://localhost:4000/preview/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

bundle exec jekyll serve --port 4000 