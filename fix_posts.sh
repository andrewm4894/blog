#!/bin/bash

# Create necessary directories
mkdir -p _posts_temp
mkdir -p assets/images
mkdir -p _layouts

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
            fi
            
            # Process the markdown file
            awk '
            BEGIN { in_front_matter = 0; has_layout = 0; front_matter_done = 0 }
            /^---$/ {
                if (in_front_matter) {
                    if (!has_layout) {
                        print "layout: post"
                    }
                    in_front_matter = 0
                    front_matter_done = 1
                } else {
                    in_front_matter = 1
                }
                print
                next
            }
            in_front_matter && /^layout:/ {
                has_layout = 1
            }
            in_front_matter && /^coverImage:/ {
                print "coverImage: \"/assets/images/'$dirname'/" substr($2, 2, length($2)-2) "\""
                next
            }
            {
                print
            }' "${dir}index.md" > "_posts_temp/$dirname.md"
        fi
    fi
done

# Handle any direct .md files in _posts
for file in _posts/*.md; do
    if [ -f "$file" ] && [ "$file" != "_posts/*.md" ]; then
        basename=$(basename "$file")
        awk '
        BEGIN { in_front_matter = 0; has_layout = 0; front_matter_done = 0 }
        /^---$/ {
            if (in_front_matter) {
                if (!has_layout) {
                    print "layout: post"
                }
                in_front_matter = 0
                front_matter_done = 1
            } else {
                in_front_matter = 1
            }
            print
            next
        }
        in_front_matter && /^layout:/ {
            has_layout = 1
        }
        {
            print
        }' "$file" > "_posts_temp/$basename"
    fi
done

# Backup original _posts directory if it hasn't been backed up
if [ ! -d "_posts_backup" ]; then
    mv _posts _posts_backup
fi

# Move new posts into place
rm -rf _posts
mv _posts_temp _posts 