import os
import re
import urllib.parse
import shutil

def fix_site():
    base_dir = "media"
    html_file = "index.html"
    backup_file = "index.html.bak"

    # --- 0. RESTORE FROM BACKUP (Clean Slate) ---
    if os.path.exists(backup_file):
        print(f"Restoring {html_file} from {backup_file} to ensure clean build...")
        shutil.copy(backup_file, html_file)
    else:
        print(f"Creating initial backup: {backup_file}")
        shutil.copy(html_file, backup_file)
    
    # Build a map of filename -> local path
    media_map = {}
    
    print("Scanning media directory...")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            key = file
            rel_path = os.path.relpath(os.path.join(root, file), ".")
            rel_path = rel_path.replace("\\", "/") 
            encoded_path = urllib.parse.quote(rel_path, safe='/')
            media_map[key] = encoded_path
            
    print(f"Found {len(media_map)} files in media/.")

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. Disable Wix Scripts ---
    print("Disabling Wix Hydration Scripts...")
    script_patterns = [
        r'<script[^>]*wix-thunderbolt[^>]*>.*?</script>',
        r'<script[^>]*viewer-model[^>]*>.*?</script>', 
        r'<script[^>]*wix-style-react[^>]*>.*?</script>',
        r'<script id="wix-warmup-data"[^>]*>.*?</script>',
        r'<script[^>]*src="[^"]*wix-thunderbolt[^"]*"[^>]*>.*?</script>'
    ]
    for pattern in script_patterns:
        content = re.sub(pattern, "<!-- DISABLED WIX SCRIPT -->", content, flags=re.DOTALL)

    # --- 2. Force Visibility ---
    print("Revealing hidden gallery items...")
    content = content.replace('opacity:0', 'opacity:1')
    content = content.replace('display:none', 'display:block')
    content = content.replace('visibility:hidden', 'visibility:visible')

    # --- 3. FIX: Replace Hero Video ---
    print("Fixing Hero Video...")
    video_replacement = """
    <div style="width:100%; height:100%; position:relative; overflow:hidden;">
        <video autoplay muted loop playsinline style="width:100%; height:100%; object-fit:cover; position:absolute; top:0; left:0;">
            <source src="media/video/hero_video.mp4" type="video/mp4">
        </video>
    </div>
    """
    content = re.sub(
        r'<wix-video id="videoContainer_comp-l5kwdtq5"[^>]*>.*?</wix-video>', 
        video_replacement, 
        content, 
        flags=re.DOTALL
    )

    # --- 4. FIX: Layout, Smooth Scroll, Header Gradient, Indicators ---
    print("Fixing Layout, Smooth Scroll, and Header Gradient...")
    
    # --- 5. Trusted By - Manual Injection (CSS Marquee) ---
    print("Injecting Manual Trusted By Marquee...")
    
    # Selected logos from media/Logos/
    # Using URL encodings where appropriate
    marquee_logos = [
        "central-bank-of-nigeria-cbn-logo-42FD3093EE-seeklogo.com.png",
        "NNPC.png",
        "Kaduna-State-Logo.jpg",
        "fha-logo.png", 
        "Afreximbank_Logo_RGB.jpg",
        "NSITF-logo.png",
        "Yobe_State_Logo.png",
        "Taraba-Logo3.png",
        "fct-logo_0.png",
        "AMAC.jpg"
    ]
    
    marquee_items_html = ""
    for logo in marquee_logos:
        # Check standard paths
        src = ""
        if logo in media_map:
            src = media_map[logo]
        else:
             # Try manual match for some tricky ones
            encoded_logo = urllib.parse.quote(logo)
            if encoded_logo in media_map:
                 src = media_map[encoded_logo]
            else:
                 # Fallback to direct path if we found it in 'media/Logos'
                 src = f"media/Logos/{logo}"
        
        marquee_items_html += f'<img src="{src}" alt="Partner Logo" class="trusted-logo">'

    # Duplicate logos for seamless infinite scroll
    marquee_inner_html = f"""
    <div class="trusted-marquee-container">
        <div class="trusted-marquee-track">
            {marquee_items_html}
            {marquee_items_html}
        </div>
    </div>
    """

    # Inject CSS for Marquee
    marquee_css = """
    <style>
        .trusted-marquee-container {
            width: 100%;
            height: 180px;
            overflow-x: auto;
            overflow-y: hidden;
            display: flex;
            align-items: center;
        }
        .trusted-marquee-track {
            display: flex;
            gap: 100px;
            width: max-content;
        }
        .trusted-logo {
            height: 120px;
            width: auto;
            max-width: 250px;
            object-fit: contain;
        }
        
        /* Mobile adjustment */
        @media (max-width: 600px) {
            .trusted-marquee-container { height: 120px; }
            .trusted-logo { height: 70px; }
            .trusted-marquee-track { gap: 50px; }
        }
    </style>
    """
    
    if '</head>' in content:
        content = content.replace('</head>', marquee_css + '\n</head>')

    # Regex to replace content of comp-l5kwdtqw
    # Matches <div id="comp-l5kwdtqw"...> ... </div>
    # We'll use a safer approach: find the specific start tag and replace innerHTML manually roughly
    
    # Find the container
    # <div id="comp-l5kwdtqw" class="  "><div class="comp-l5kwdtqw">
    # It might be safer to replace the whole inner div structure
    
    # We know the ID is comp-l5kwdtqw.
    # Let's try to inject it right after the opening tag if we can match it securely.
    # Or finding the style block inside it and replacing the whole block.
    
    # Matches: <div id="comp-l5kwdtqw" class="  "><div class="comp-l5kwdtqw"><style>... .comp-l5kwdtqw { ... } ... </style> ... </div></div>
    
    # Simplified regex to targeting the ID and replacing EVERYTHING inside up to the next matching closing div chain might be risky.
    # Instead, we will replace the whole known inner block if we can find a unique signature.
    # The signature is `<div id="comp-l5kwdtqw" class="  ">`
    
    print("Injecting Marquee HTML...")
    # Replacing the entire inner content of the trusted by container
    # We will look for the unique start tag and simply append our marquee logic, ignoring the old empty stuff or hiding it.
    
    # A safer way: Add our marquee JS/HTML via a script that runs on load, OR simple string replace if we are confident.
    # Let's rely on the string replacement of the STYLE block we saw earlier?
    # No, that style block definition `.comp-l5kwdtqw` is unique.
    
    pattern_trusted = r'(<div id="comp-l5kwdtqw"[^>]*>)(.*?)(</div></div>)' # this is risky with greedy .*
    # Better: Replace the specific known substring of CSS variables? No.
    
    # Robust approach: 
    # Find `<div id="comp-l5kwdtqw"`
    # Replace it with `<div id="comp-l5kwdtqw" ... > [MARQUEE] <div style="display:none">` 
    # preventing old content from showing.
    
    content = re.sub(
        r'(<div id="comp-l5kwdtqw"[^>]*>)', 
        f'\\1 {marquee_inner_html} <div style="display:none">', 
        content, 
        count=1
    )
    # And we hope the closing </div> closes our new div or the old hidden ones. 
    # Actually, we injected a `div` (marquee) which is closed. 
    # Then we opened a `<div style="display:none">` to hide the OLD content (original children).
    # We need to ensure we don't break the DOM tree.
    # If we just open a div and never close it, it breaks.
    # The old content ends with `</div></div>` (closing inner and outer).
    # So we should probably just `display:none` the original inner child via CSS and append ours.
    
    # Easier plan:
    # 1. Hide original content via CSS: `.comp-l5kwdtqw > div { display: none !important; }` (target inner wrapper)
    # 2. Inject new content right after the opening tag `id="comp-l5kwdtqw" ... >`
    
    layout_css_addition = """
    #comp-l5kwdtqw > .comp-l5kwdtqw { display: none !important; }
    """
    content = content.replace('</style>', layout_css_addition + '\n</style>', 1) # Add to first style block found (unsafe)
    
    # Better: add to our marquee CSS block
    marquee_css = marquee_css.replace('</style>', '#comp-l5kwdtqw > .comp-l5kwdtqw { display: none !important; }\n</style>')
    
    content = re.sub(
        r'(<div id="comp-l5kwdtqw"[^>]*>)', 
        f'\\1 {marquee_inner_html}', 
        content, 
        count=1
    )


    layout_css = """
    <style>
        html { scroll-behavior: smooth; }
        body, html { margin: 0 !important; padding: 0 !important; }
        #site-root { top: 0 !important; margin-top: 0 !important; }
        #masterPage { margin-top: 0 !important; }
        #SITE_HEADER { 
            top: 0 !important; 
            margin-top: 0 !important; 
            position: fixed !important; 
            transition: background 0.3s ease;
        }
        #SITE_HEADER.scrolled-header {
             background: linear-gradient(to bottom, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0) 100%) !important;
             backdrop-filter: blur(2px);
             -webkit-backdrop-filter: blur(2px);
             box-shadow: none !important;
        }
        .Vd6aQZ .mHZSwn { display: none !important; }
        
        /* Trusted By Manual Fix */
        #comp-l5kwdtqw {
            overflow-x: auto; /* Make it scrollable */
            overflow-y: hidden;
        }
        /* Mobile adjustment */
        @media (max-width: 600px) {
            .trusted-logo { height: 50px; }
            .trusted-marquee-track { gap: 30px; }
        }

        /* Scroll Indicator Overlay */
        .pro-gallery-indicator-wrapper {
            position: relative;
        }
    </style>
    """
    if '</head>' in content:
        content = content.replace('</head>', layout_css + '\n</head>')

    scroll_js = """
    <script>
        document.addEventListener('scroll', function() {
            const header = document.getElementById('SITE_HEADER');
            // Throttled header check could also help, but it's global scroll
            if (window.scrollY > 50) {
                if (!header.classList.contains('scrolled-header')) header.classList.add('scrolled-header');
            } else {
                if (header.classList.contains('scrolled-header')) header.classList.remove('scrolled-header');
            }
        }, { passive: true });

        window.addEventListener('load', function() {
            // Helper to get ALL descendants
            function getDescendants(node) {
                let nodes = [];
                for(let child of node.children) {
                    nodes.push(child);
                    nodes = nodes.concat(getDescendants(child));
                }
                return nodes;
            }

            // Reset Trusted By scroll position to start
            const trustedByContainer = document.querySelector('.trusted-marquee-container');
            if (trustedByContainer) {
                trustedByContainer.scrollLeft = 0;
            }

            // PROJECT GALLERIES + TRUSTED BY - Indicators
            const allGalleries = Array.from(document.querySelectorAll('.pro-gallery'));
            
            // Also add Trusted By container to the list
            if (trustedByContainer && !allGalleries.includes(trustedByContainer)) {
                allGalleries.push(trustedByContainer);
            }
            
             allGalleries.forEach(gallery => {
                // DEDUPLICATION:
                // Only act if we aren't inside another wrapper
                if (gallery.closest('.pro-gallery-indicator-wrapper')) return;

                // CHECK if this gallery actually has scrollable content?
                let descendants = getDescendants(gallery);
                let hasScrollable = descendants.some(d => d.scrollWidth > d.clientWidth + 5);
                
                if (hasScrollable) {
                    gallery.classList.add('pro-gallery-indicator-wrapper');
                }
            });

            // AUTO-SCROLL for Trusted By (JavaScript-based, performant)
            if (trustedByContainer) {
                let scrollSpeed = 0.5; // pixels per frame
                let isUserScrolling = false;
                let userScrollTimeout;
                let lastScrollLeft = 0;
                
                // Detect actual user scrolling (not auto-scroll)
                trustedByContainer.addEventListener('scroll', () => {
                    const currentScroll = trustedByContainer.scrollLeft;
                    // If scroll changed by more than our auto-scroll speed, user is scrolling
                    if (Math.abs(currentScroll - lastScrollLeft) > scrollSpeed * 2) {
                        isUserScrolling = true;
                        clearTimeout(userScrollTimeout);
                        userScrollTimeout = setTimeout(() => {
                            isUserScrolling = false;
                        }, 3000); // Resume after 3 seconds of no user interaction
                    }
                    lastScrollLeft = currentScroll;
                }, { passive: true });
                
                // Auto-scroll animation
                function autoScroll() {
                    if (!isUserScrolling && trustedByContainer) {
                        trustedByContainer.scrollLeft += scrollSpeed;
                        lastScrollLeft = trustedByContainer.scrollLeft;
                        
                        // Reset to beginning when reaching halfway (seamless loop)
                        const maxScroll = trustedByContainer.scrollWidth / 2;
                        if (trustedByContainer.scrollLeft >= maxScroll) {
                            trustedByContainer.scrollLeft = 0;
                            lastScrollLeft = 0;
                        }
                    }
                    requestAnimationFrame(autoScroll);
                }
                
                // Start auto-scroll
                requestAnimationFrame(autoScroll);
            }
        });
    </script>
    """
    if '</body>' in content:
        content = content.replace('</body>', scroll_js + '\n</body>')

    # Remove Text/More
    print("Removing accessibility text and 'More' menu item...")
    content = content.replace('Use tab to navigate through the menu items.', '')
    content = re.sub(r'<li id="comp-kxm44xig__more__".*?</li>', '', content, flags=re.DOTALL)

    # Images
    def replace_img_src(match):
        img_tag = match.group(0)
        src_match = re.search(r'src="([^"]+)"', img_tag)
        if not src_match: return img_tag
        current_src = src_match.group(1)
        
        alt_match = re.search(r'alt="([^"]+)"', img_tag)
        alt_text = alt_match.group(1) if alt_match else ""
        
        new_src = current_src
        if alt_text and alt_text in media_map:
            new_src = media_map[alt_text]
        elif "wixstatic.com" in current_src:
            for filename, local_path in media_map.items():
                if filename in current_src or urllib.parse.quote(filename) in current_src:
                    new_src = local_path
                    break
        elif current_src.startswith("media/"):
            raw_path = urllib.parse.unquote(current_src)
            new_src = urllib.parse.quote(raw_path, safe='/')

        new_tag = img_tag
        if new_src != current_src:
            new_tag = new_tag.replace(f'src="{current_src}"', f'src="{new_src}"')
        
        if 'loading=' not in new_tag:
             new_tag = new_tag.replace('<img ', '<img loading="lazy" ')
        return new_tag

    content = re.sub(r'<img\s+[^>]*>', replace_img_src, content)
    content = re.sub(r'\s+srcset="[^"]*"', '', content)
    
    # Anchors
    print("Fixing Anchor Links...")
    anchor_map = {
        "dataItem-ky3ihhu1": "aboutus",
        "dataItem-ky3ikjg8": "services",
        "dataItem-ky3im4t1": "selectedworks",
        "dataItem-ky4qim98": "contact"
    }
    def replace_anchor(match):
        a_tag = match.group(0)
        da_match = re.search(r'data-anchor="([^"]+)"', a_tag)
        if da_match:
            anchor_id = da_match.group(1)
            if anchor_id in anchor_map:
                real_id = anchor_map[anchor_id]
                a_tag = re.sub(r'href="[^"]+"', f'href="#{real_id}"', a_tag)
        return a_tag

    content = re.sub(r'<a\s+[^>]*>', replace_anchor, content)
    content = content.replace('href="dandbng/home.html"', 'href="./"')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("HTML fixed. Full UI Polish applied.")

if __name__ == "__main__":
    fix_site()
