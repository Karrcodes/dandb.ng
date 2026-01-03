#!/usr/bin/env python3
"""
Extract content from old Wix site and populate new site
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

# Paths
OLD_HTML = Path("/Users/abdulalimu-k/Documents/Dandb.ng/index.html")
NEW_HTML = Path("/Users/abdulalimu-k/Documents/Dandb.ng/new-site/index.html")

def extract_text_content(html_content):
    """Extract text content from old site"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all text elements
    texts = {}
    
    # Look for specific IDs and classes
    for elem in soup.find_all(['p', 'h1', 'h2', 'h3', 'span']):
        text = elem.get_text(strip=True)
        if text and len(text) > 10:  # Only meaningful text
            print(f"Found: {text[:100]}")
    
    return texts

def main():
    print("Extracting content from old site...")
    
    with open(OLD_HTML, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    extract_text_content(html_content)

if __name__ == "__main__":
    main()
