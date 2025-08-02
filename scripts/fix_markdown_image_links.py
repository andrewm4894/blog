#!/usr/bin/env python3
"""
Fix Markdown Image Links in Jekyll Posts

This script fixes broken image links in Jekyll posts by updating them to point to the correct paths.
It works in conjunction with check_broken_image_links.py to fix both missing images and incorrect references.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import argparse


def fix_image_links_in_post(post_path: Path, dry_run: bool = True) -> List[Dict]:
    """Fix broken image links in a single post"""
    
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes_made = []
    
    # Extract post name for generating correct asset paths
    post_name = post_path.stem  # filename without .md extension
    
    # Common fixes based on the broken link patterns we found
    fixes = [
        # Fix bare filenames that should be proper asset paths
        {
            'pattern': r'(?<!\()/?"?([^/\s"\'()]+\.(png|jpe?g|gif|webp|svg))"?(?!\))',
            'replacement': lambda m: f'![]({{{{ "/assets/images/{post_name}/{m.group(1)}" | relative_url }}}})',
            'description': 'Convert bare image filenames to proper Jekyll asset paths'
        },
        
        # Fix malformed paths like /"/assets/... 
        {
            'pattern': r'!\[([^\]]*)\]\(/"/assets/images/([^)]+)\)',
            'replacement': r'![\1]({{ "/assets/images/\2" | relative_url }})',
            'description': 'Fix malformed asset paths with extra quotes'
        },
        
        # Update existing asset paths to use Jekyll's relative_url filter
        {
            'pattern': r'!\[([^\]]*)\]\(/assets/images/([^)]+)\)',
            'replacement': r'![\1]({{ "/assets/images/\2" | relative_url }})',
            'description': 'Add Jekyll relative_url filter to existing asset paths'
        }
    ]
    
    for fix in fixes:
        pattern = fix['pattern']
        
        if callable(fix['replacement']):
            # Handle lambda replacements
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            for match in reversed(matches):  # Process in reverse to maintain positions
                replacement = fix['replacement'](match)
                old_text = match.group(0)
                content = content[:match.start()] + replacement + content[match.end():]
                
                if old_text != replacement:
                    fixes_made.append({
                        'old': old_text,
                        'new': replacement,
                        'description': fix['description'],
                        'line_context': get_line_context(original_content, match.start())
                    })
        else:
            # Handle string replacements
            new_content = re.sub(pattern, fix['replacement'], content, flags=re.IGNORECASE)
            
            if new_content != content:
                # Find what changed for reporting
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    old_text = match.group(0)
                    new_text = re.sub(pattern, fix['replacement'], old_text, flags=re.IGNORECASE)
                    
                    fixes_made.append({
                        'old': old_text,
                        'new': new_text,
                        'description': fix['description'],
                        'line_context': get_line_context(content, match.start())
                    })
                
                content = new_content
    
    # Write the fixed content back to the file
    if fixes_made and not dry_run:
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed {len(fixes_made)} image links in {post_path.name}")
    elif fixes_made:
        print(f"🔍 Found {len(fixes_made)} fixable image links in {post_path.name} (dry run)")
    
    return fixes_made


def get_line_context(content: str, position: int) -> str:
    """Get the line number and context for a position in the content"""
    lines = content[:position].split('\n')
    line_number = len(lines)
    current_line = lines[-1] if lines else ""
    
    # Get the full line by finding the complete line around the position
    all_lines = content.split('\n')
    if line_number <= len(all_lines):
        full_line = all_lines[line_number - 1]
        return f"Line {line_number}: {full_line.strip()}"
    
    return f"Line {line_number}: {current_line}"


def main():
    parser = argparse.ArgumentParser(description='Fix broken image links in Jekyll posts')
    parser.add_argument('--apply', action='store_true', 
                       help='Actually apply the fixes (default is dry run)')
    parser.add_argument('--post', type=str,
                       help='Fix links in a specific post (by filename)')
    
    args = parser.parse_args()
    
    posts_dir = Path("_posts")
    if not posts_dir.exists():
        print("❌ _posts directory not found. Run from the blog root directory.")
        return
    
    # Determine which posts to process
    if args.post:
        post_files = [posts_dir / args.post]
        if not post_files[0].exists():
            # Try with .md extension
            post_files = [posts_dir / f"{args.post}.md"]
            if not post_files[0].exists():
                print(f"❌ Post '{args.post}' not found")
                return
    else:
        post_files = list(posts_dir.glob("*.md"))
    
    total_fixes = 0
    posts_with_fixes = 0
    
    mode = "APPLYING FIXES" if args.apply else "DRY RUN"
    print(f"🔧 {mode}: Checking {len(post_files)} posts for fixable image links...\n")
    
    for post_path in post_files:
        fixes = fix_image_links_in_post(post_path, dry_run=not args.apply)
        
        if fixes:
            posts_with_fixes += 1
            total_fixes += len(fixes)
            
            # Show details of fixes for this post
            print(f"\n📝 Fixes for {post_path.name}:")
            for i, fix in enumerate(fixes, 1):
                print(f"  {i}. {fix['description']}")
                print(f"     Old: {fix['old']}")
                print(f"     New: {fix['new']}")
                print(f"     Context: {fix['line_context']}")
                print()
    
    print(f"\n📊 Summary:")
    print(f"   Posts processed: {len(post_files)}")
    print(f"   Posts with fixes: {posts_with_fixes}")
    print(f"   Total fixes: {total_fixes}")
    
    if total_fixes > 0 and not args.apply:
        print(f"\n🚀 Run with --apply to actually make these changes")
    elif total_fixes > 0 and args.apply:
        print(f"\n✅ All fixes have been applied!")
    else:
        print(f"\n🎉 No image link fixes needed!")


if __name__ == "__main__":
    main() 