#!/usr/bin/env python3
"""
Broken Image Link Checker for Jekyll Blog

This script scans all posts in _posts/ for image links and checks if they exist.
If images are missing, it looks for them in the _posts_backup/ structure and suggests fixes.
"""

import os
import re
import glob
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from urllib.parse import urlparse
import argparse


class ImageLinkChecker:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.posts_dir = self.root_dir / "_posts"
        self.backup_dir = self.root_dir / "_posts_backup"
        self.assets_dir = self.root_dir / "assets"
    
    def find_posts(self) -> List[Path]:
        """Find all markdown posts in _posts directory"""
        return list(self.posts_dir.glob("*.md"))
    
    def extract_image_links(self, content: str, post_path: Path) -> List[Dict]:
        """Extract all image links from post content"""
        images = []
        
        # Find all markdown images: ![alt](path)
        markdown_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        for match in re.finditer(markdown_pattern, content):
            alt_text = match.group(1)
            image_path = match.group(2).strip()
            # Skip external URLs
            if not image_path.startswith('http'):
                images.append({
                    'alt': alt_text,
                    'path': image_path,
                    'full_match': match.group(0),
                    'type': 'markdown',
                    'line_number': content[:match.start()].count('\n') + 1
                })
        
        # Find all HTML img tags: <img src="path"
        html_pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>'
        for match in re.finditer(html_pattern, content, re.IGNORECASE):
            image_path = match.group(1).strip()
            # Skip external URLs
            if not image_path.startswith('http'):
                images.append({
                    'alt': '',
                    'path': image_path,
                    'full_match': match.group(0),
                    'type': 'html',
                    'line_number': content[:match.start()].count('\n') + 1
                })
        
        return images
    
    def resolve_image_path(self, image_path: str) -> Optional[Path]:
        """Resolve relative image path to absolute filesystem path"""
        # Handle different path formats
        if image_path.startswith('/'):
            # Absolute path from site root
            return self.root_dir / image_path.lstrip('/')
        elif image_path.startswith('http'):
            # External URL - can't check locally
            return None
        else:
            # Relative path
            return self.root_dir / image_path
    
    def check_image_exists(self, image_path: str) -> bool:
        """Check if image file exists on filesystem"""
        resolved_path = self.resolve_image_path(image_path)
        if resolved_path is None:  # External URL
            return True  # Assume external URLs are fine for now
        return resolved_path.exists()
    
    def find_backup_image(self, post_name: str, image_filename: str) -> Optional[Path]:
        """Try to find the image in the backup posts structure"""
        # Extract date and title from post filename
        post_parts = post_name.replace('.md', '').split('-', 3)
        if len(post_parts) >= 4:
            backup_post_dir = self.backup_dir / f"{'-'.join(post_parts)}"
            backup_images_dir = backup_post_dir / "images"
            
            # Look for the image file
            if backup_images_dir.exists():
                for img_file in backup_images_dir.glob("*"):
                    if img_file.name.lower() == image_filename.lower():
                        return img_file
        
        return None
    
    def suggest_fix(self, post_path: Path, broken_image: Dict) -> Dict:
        """Suggest how to fix a broken image link"""
        image_path = broken_image['path']
        image_filename = Path(image_path).name
        post_name = post_path.name
        
        suggestion = {
            'original_path': image_path,
            'suggestions': []
        }
        
        # Look for the image in backup structure
        backup_image = self.find_backup_image(post_name, image_filename)
        if backup_image:
            # Suggest copying to assets directory
            post_assets_dir = self.assets_dir / "images" / post_name.replace('.md', '')
            suggested_path = f"/assets/images/{post_name.replace('.md', '')}/{image_filename}"
            
            suggestion['suggestions'].append({
                'action': 'copy_from_backup',
                'source': str(backup_image),
                'destination': str(self.root_dir / suggested_path.lstrip('/')),
                'new_path': suggested_path,
                'command': f"mkdir -p {post_assets_dir} && cp '{backup_image}' '{post_assets_dir}/{image_filename}'"
            })
        
        # Look for similar images in assets directory
        existing_images = list(self.assets_dir.glob(f"**/{image_filename}"))
        if existing_images:
            for existing_image in existing_images[:3]:  # Limit to first 3 matches
                relative_path = "/" + str(existing_image.relative_to(self.root_dir))
                suggestion['suggestions'].append({
                    'action': 'use_existing',
                    'existing_path': str(existing_image),
                    'new_path': relative_path
                })
        
        return suggestion
    
    def check_post(self, post_path: Path) -> Dict:
        """Check a single post for broken image links"""
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        images = self.extract_image_links(content, post_path)
        broken_images = []
        
        for image in images:
            if not self.check_image_exists(image['path']):
                broken_image = image.copy()
                broken_image['suggestion'] = self.suggest_fix(post_path, image)
                broken_images.append(broken_image)
        
        return {
            'post': str(post_path),
            'total_images': len(images),
            'broken_images': broken_images,
            'broken_count': len(broken_images)
        }
    
    def check_all_posts(self) -> List[Dict]:
        """Check all posts for broken image links"""
        posts = self.find_posts()
        results = []
        
        print(f"Checking {len(posts)} posts for broken image links...")
        
        for post_path in posts:
            result = self.check_post(post_path)
            if result['broken_count'] > 0:
                results.append(result)
                print(f"❌ {post_path.name}: {result['broken_count']} broken images")
            else:
                print(f"✅ {post_path.name}: All images OK")
        
        return results
    
    def generate_report(self, results: List[Dict]) -> str:
        """Generate a detailed report of broken image links"""
        report = []
        report.append("# Broken Image Links Report\n")
        
        total_broken = sum(r['broken_count'] for r in results)
        total_posts_with_issues = len(results)
        
        report.append(f"**Summary:** {total_broken} broken image links found across {total_posts_with_issues} posts\n")
        
        for result in results:
            report.append(f"## {Path(result['post']).name}")
            report.append(f"**Total images:** {result['total_images']} | **Broken:** {result['broken_count']}\n")
            
            for i, broken in enumerate(result['broken_images'], 1):
                report.append(f"### Broken Image #{i}")
                report.append(f"**Path:** `{broken['path']}`")
                report.append(f"**Type:** {broken['type']}")
                if broken['alt']:
                    report.append(f"**Alt text:** {broken['alt']}")
                
                suggestions = broken['suggestion']['suggestions']
                if suggestions:
                    report.append("\n**Suggested fixes:**")
                    for j, suggestion in enumerate(suggestions, 1):
                        if suggestion['action'] == 'copy_from_backup':
                            report.append(f"{j}. **Copy from backup:**")
                            report.append(f"   - Source: `{suggestion['source']}`")
                            report.append(f"   - Command: `{suggestion['command']}`")
                            report.append(f"   - Update link to: `{suggestion['new_path']}`")
                        elif suggestion['action'] == 'use_existing':
                            report.append(f"{j}. **Use existing image:**")
                            report.append(f"   - Found at: `{suggestion['existing_path']}`")
                            report.append(f"   - Update link to: `{suggestion['new_path']}`")
                else:
                    report.append("\n❌ **No automatic fix suggestions found**")
                
                report.append("")
        
        return "\n".join(report)
    
    def generate_fix_script(self, results: List[Dict]) -> str:
        """Generate a shell script to automatically fix issues"""
        script_lines = []
        script_lines.append("#!/bin/bash")
        script_lines.append("# Auto-generated script to fix broken image links")
        script_lines.append("# Review carefully before running!\n")
        
        for result in results:
            script_lines.append(f"# Fixes for {Path(result['post']).name}")
            
            for broken in result['broken_images']:
                suggestions = broken['suggestion']['suggestions']
                copy_suggestions = [s for s in suggestions if s['action'] == 'copy_from_backup']
                
                if copy_suggestions:
                    best_suggestion = copy_suggestions[0]
                    script_lines.append(f"# Fix: {broken['path']}")
                    script_lines.append(best_suggestion['command'])
                    script_lines.append("")
        
        return "\n".join(script_lines)


def main():
    parser = argparse.ArgumentParser(description='Check Jekyll blog posts for broken image links')
    parser.add_argument('--report', '-r', action='store_true', 
                       help='Generate detailed markdown report')
    parser.add_argument('--fix-script', '-f', action='store_true',
                       help='Generate shell script with suggested fixes')
    parser.add_argument('--output', '-o', type=str,
                       help='Output file for report or script')
    
    args = parser.parse_args()
    
    checker = ImageLinkChecker()
    results = checker.check_all_posts()
    
    if not results:
        print("\n🎉 No broken image links found!")
        return
    
    print(f"\n📊 Found issues in {len(results)} posts")
    
    if args.report:
        report = checker.generate_report(results)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to {args.output}")
        else:
            print("\n" + report)
    
    if args.fix_script:
        script = checker.generate_fix_script(results)
        output_file = args.output or 'fix_broken_images.sh'
        with open(output_file, 'w') as f:
            f.write(script)
        os.chmod(output_file, 0o755)  # Make executable
        print(f"🔧 Fix script saved to {output_file}")
    
    if not args.report and not args.fix_script:
        # Default: show summary and basic suggestions
        print("\nRun with --report to see detailed analysis")
        print("Run with --fix-script to generate automated fixes")


if __name__ == "__main__":
    main() 