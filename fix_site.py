import os
import re
import urllib.parse

def fix_site():
    base_dir = "media"
    html_file = "index.html"
    
    # Build a map of filename -> local path
    media_map = {}
    
    print("Scanning media directory...")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            key = file
            rel_path = os.path.relpath(os.path.join(root, file), ".")
            rel_path = rel_path.replace("\\", "/") 
            # Pre-calculate encoded path for substitution
            encoded_path = urllib.parse.quote(rel_path, safe='/')
            media_map[key] = encoded_path
            
    print(f"Found {len(media_map)} files in media/.")

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define replacement function for <img> tags
    def replace_img_src(match):
        img_tag = match.group(0)
        
        # 1. Extract current src
        src_match = re.search(r'src="([^"]+)"', img_tag)
        if not src_match:
            return img_tag
        
        current_src = src_match.group(1)
        
        # 2. Extract Alt text for mapping
        alt_match = re.search(r'alt="([^"]+)"', img_tag)
        alt_text = alt_match.group(1) if alt_match else ""
        
        new_src = current_src
        
        # Strategy A: Use Alt text map (Primary for Gallery)
        if alt_text and alt_text in media_map:
            new_src = media_map[alt_text]
            
        # Strategy B: Check if filename is in the Wix URL (Secondary)
        elif "wixstatic.com" in current_src:
            for filename, local_path in media_map.items():
                if filename in current_src or urllib.parse.quote(filename) in current_src:
                    new_src = local_path
                    break
        
        # Strategy C: Local path cleanup (Re-encoding safety)
        # If it's already a local media path, ensure it's encoded correctly BUT NOT DOUBLE ENCODED.
        elif current_src.startswith("media/"):
            # Decode first to ensure we are working with raw characters
            raw_path = urllib.parse.unquote(current_src)
            # Re-encode strictly
            new_src = urllib.parse.quote(raw_path, safe='/')

        # Apply replacement if changed
        if new_src != current_src:
            # Reconstruct the tag with the new src
            # We use replace() on the tag string to be safe vs regex reconstruction
            return img_tag.replace(f'src="{current_src}"', f'src="{new_src}"')
            
        return img_tag

    # Execute Image Replacement
    # We iterate over all <img> tags
    content = re.sub(r'<img\s+[^>]*>', replace_img_src, content)

    # Remove srcset (Wix's responsive images break simple local serving)
    content = re.sub(r'\s+srcset="[^"]*"', '', content)
    
    # Fix Anchor Links
    anchor_map = {
        "dataItem-ky3ihhu1": "aboutus",
        "dataItem-ky3ikjg8": "services",
        "dataItem-ky3im4t1": "selectedworks",
        "dataItem-ky4qim98": "contact"
    }
    for wix_id, real_id in anchor_map.items():
        content = content.replace(f'href="#{wix_id}"', f'href="#{real_id}"')
    
    # Fix Home Link
    content = content.replace('href="dandbng/home.html"', 'href="./"')

    # Extra: Check for any stray "unencoded" spaces in hrefs or srcs just in case
    # (Though the img tag handler covers images)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("HTML fixed. Double-encoding prevention applied.")

if __name__ == "__main__":
    fix_site()
