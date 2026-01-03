#!/usr/bin/env python3
"""
Build script to populate the new site with content from the old Wix export
"""

import os
import shutil
from pathlib import Path

# Paths
OLD_SITE = Path(__file__).parent.parent
NEW_SITE = Path(__file__).parent
MEDIA_DIR = OLD_SITE / "media"

def create_media_symlink():
    """Create symlink to media directory"""
    new_media = NEW_SITE / "media"
    
    # Remove existing symlink/directory
    if new_media.exists() or new_media.is_symlink():
        if new_media.is_symlink():
            new_media.unlink()
        else:
            shutil.rmtree(new_media)
    
    # Create symlink
    new_media.symlink_to(MEDIA_DIR, target_is_directory=True)
    print(f"✓ Created media symlink: {new_media} -> {MEDIA_DIR}")

def create_js_directory():
    """Ensure js directory exists"""
    js_dir = NEW_SITE / "js"
    js_dir.mkdir(exist_ok=True)
    print(f"✓ Created js directory: {js_dir}")

def create_css_directory():
    """Ensure css directory exists"""
    css_dir = NEW_SITE / "css"
    css_dir.mkdir(exist_ok=True)
    print(f"✓ Created css directory: {css_dir}")

def main():
    print("Building new site...")
    print("-" * 50)
    
    create_css_directory()
    create_js_directory()
    create_media_symlink()
    
    print("-" * 50)
    print("✓ Build complete!")
    print(f"\nTo view the site:")
    print(f"  cd {NEW_SITE}")
    print(f"  python3 -m http.server 8000")
    print(f"  Open http://localhost:8000")

if __name__ == "__main__":
    main()
