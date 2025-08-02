#!/usr/bin/env python3

import os
import re

def fix_image_paths(directory="_posts"):
    """
    Fix common image path issues in markdown files:
    1. Missing closing quotes
    2. Incorrect path formatting
    3. Extra whitespace
    4. Double quotes and extra slashes
    """
    
    # Regular expressions for finding image patterns
    patterns = {
        # Markdown image with or without alt text: ![alt](path) or ![](path)
        'markdown': r'!\[(.*?)\]\((.*?)\)',
        # HTML img tag
        'html': r'<img\s+src=["\']?(.*?)["\']?\s*',
        # Figure tag with img
        'figure': r'<figure>\s*<img\s+src=["\']?(.*?)["\']?\s*'
    }
    
    # Walk through all markdown files in the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                modified = False
                
                # Process each image pattern
                for pattern_type, pattern in patterns.items():
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        # Get the image path from the match
                        if pattern_type == 'markdown':
                            img_path = match.group(2)
                        else:
                            img_path = match.group(1)
                        
                        # Clean up the path
                        cleaned_path = img_path.strip()
                        # Remove any extra quotes and slashes
                        cleaned_path = cleaned_path.strip('"').strip("'").strip('/')
                        # Ensure single leading slash
                        cleaned_path = '/' + cleaned_path
                        
                        # Create properly formatted replacement
                        if pattern_type == 'markdown':
                            old = f'![]({img_path})'
                            new = f'![]({cleaned_path})'
                        else:
                            old = f'src={img_path}'
                            new = f'src="{cleaned_path}"'
                        
                        if old != new:
                            content = content.replace(old, new)
                            modified = True
                            print(f"  Fixed: {old} -> {new}")
                
                # Save changes if any were made
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  Saved changes to {file_path}")

if __name__ == "__main__":
    fix_image_paths()
    print("Done!") 