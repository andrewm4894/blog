#!/bin/bash

# Create a temporary directory for processing
mkdir -p _posts_temp

# Process each directory in _posts
for dir in _posts/*/; do
    if [ -d "$dir" ] && [ "$dir" != "_posts/_drafts/" ]; then
        # Get the directory name (which is the date-title)
        dirname=$(basename "$dir")
        
        # If there's an index.md, copy it to the new location
        if [ -f "${dir}index.md" ]; then
            # Create images directory if it doesn't exist
            if [ -d "${dir}images" ]; then
                mkdir -p "assets/images/$dirname"
                cp -r "${dir}images/"* "assets/images/$dirname/"
                
                # Update image paths in the markdown file
                sed 's|images/|/assets/images/'"$dirname"'/|g' "${dir}index.md" > "_posts_temp/$dirname.md"
            else
                cp "${dir}index.md" "_posts_temp/$dirname.md"
            fi
        fi
    fi
done

# Handle any direct .md files in _posts
for file in _posts/*.md; do
    if [ -f "$file" ]; then
        cp "$file" "_posts_temp/"
    fi
done

# Backup original _posts directory
mv _posts _posts_backup

# Move new posts into place
mv _posts_temp _posts 