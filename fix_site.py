import os
import re

def fix_site():
    html_file = 'index.html'
    
    with open(html_file, 'r') as f:
        content = f.read()

    # Anchor mappings derived from HTML inspection
    anchor_map = {
        "dataItem-ky3ihhu1": "aboutus",
        "dataItem-ky3ikjg8": "services",
        "dataItem-ky3im4t1": "selectedworks",
        "dataItem-ky4qim98": "contact"
    }

    # 1. Replace mapped anchors
    for wix_id, real_id in anchor_map.items():
        # Replace href="#dataItem-..." (from previous run) or original if different
        content = content.replace(f'href="#{wix_id}"', f'href="#{real_id}"')
        content = content.replace(f'href="dandbng/home.html" data-anchor="{wix_id}"', f'href="#{real_id}" data-anchor="{wix_id}"')
        
    # 2. Fix Home Link
    # Replace references to dandbng/home.html with ./
    # This might match the ones we just fixed if we didn't catch them above, so order matters.
    # But since we targeted specific anchors above, this catch-all is fine for the Home button.
    content = content.replace('href="dandbng/home.html"', 'href="./"')

    # 3. Ensure no data-anchor links are left pointing to broken paths
    # (Optional cleanup)
    
    with open(html_file, 'w') as f:
        f.write(content)

    print("HTML updated with correct anchor links and home path.")

if __name__ == "__main__":
    fix_site()
