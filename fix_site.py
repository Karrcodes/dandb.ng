import os
import re
import urllib.parse

def fix_site():
    base_dir = "media"
    html_file = "index.html"
    
    # Build a map of filename -> local path
    # Key: simple filename (e.g., "Image.jpg")
    # Value: local relative path (encoded) (e.g., "media/Folder/Image.jpg")
    media_map = {}
    
    print("Scanning media directory...")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            # We use the raw filename as key because 'alt' usually matches the filename
            key = file
            rel_path = os.path.relpath(os.path.join(root, file), ".")
            rel_path = rel_path.replace("\\", "/") 
            # Encode path for URL safety
            encoded_path = urllib.parse.quote(rel_path, safe='/')
            
            # Store in map. If duplicate, we might overwrite, but that's acceptable for now.
            media_map[key] = encoded_path
            
    print(f"Found {len(media_map)} files in media/.")

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strategy 1 (Existing): Replace by checking if filename is in URL
    # (Kept for trusted-by images where URL contains filename)
    def replace_media_url_by_match(match):
        url = match.group(0)
        # Check against our map keys (filenames)
        for filename, local_path in media_map.items():
            # Check if filename is in URL (ignoring encoding differences slightly?)
            # Usually Wix URLs have the filename at the end.
            if filename in url:
                return local_path
            # Check encoded version too
            if urllib.parse.quote(filename) in url:
                return local_path
        return url

    content = re.sub(r'https?://static\.wixstatic\.com/media/[^"\'\s)]+', replace_media_url_by_match, content)

    # Strategy 2 (New): Replace remaining Wix URLs by matching ALT text to filename
    # We iterate over all <img> tags manually because nested regex is hard.
    
    def replace_img_src_by_alt(match):
        img_tag = match.group(0)
        
        # Check if src is still a remote Wix URL
        src_match = re.search(r'src="(https?://static\.wixstatic\.com/media/[^"]+)"', img_tag)
        if not src_match:
            return img_tag # Already local or not Wix
            
        src_url = src_match.group(1)
        
        # Extract Alt
        alt_match = re.search(r'alt="([^"]+)"', img_tag)
        if not alt_match:
            return img_tag # No alt, can't map
            
        alt_text = alt_match.group(1)
        
        # Look up alt_text in media_map
        if alt_text in media_map:
            local_path = media_map[alt_text]
            # Replace src URL with local path in the tag string
            new_tag = img_tag.replace(src_url, local_path)
            return new_tag
            
        return img_tag

    # Match <img> tags. Beware of > inside attributes, but for standard HTML it's okay.
    # We use a non-greedy match for content inside tag.
    content = re.sub(r'<img\s+[^>]*>', replace_img_src_by_alt, content)

    # Strategy 3: Local path encoding fix (already implemented)
    def fix_local_path(match):
        path = match.group(1)
        return 'src="media/' + urllib.parse.quote(path, safe='/') + '"'
    content = re.sub(r'src="media/([^"]+)"', fix_local_path, content)

    # Cleanup
    content = re.sub(r'\s+srcset="[^"]*"', '', content)
    
    # Anchors
    anchor_map = {
        "dataItem-ky3ihhu1": "aboutus",
        "dataItem-ky3ikjg8": "services",
        "dataItem-ky3im4t1": "selectedworks",
        "dataItem-ky4qim98": "contact"
    }
    for wix_id, real_id in anchor_map.items():
        content = content.replace(f'href="#{wix_id}"', f'href="#{real_id}"')
    content = content.replace('href="dandbng/home.html"', 'href="./"')

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("HTML updated with Alt-Text Text matching strategy.")

if __name__ == "__main__":
    fix_site()
