import os
from PIL import Image
import concurrent.futures

def optimize_image(file_path):
    try:
        if not file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            return
        
        with Image.open(file_path) as img:
            # Skip if already optimized (heuristic: check if specific marker exists or size)
            # For now, just optimize everything that matches criteria
            
            # Resize if too big
            max_size = 1920
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
            # Compress
            # If PNG with transparency, keep as PNG but optimize
            # If JPG, save as JPG with quality 80
            # If PNG has no transparency, convert to JPG?
            
            save_kwargs = {"optimize": True}
            
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.jpg', '.jpeg']:
                save_kwargs["quality"] = 80
                img.save(file_path, **save_kwargs)
            elif ext == '.png':
                # Check for transparency
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    # Keep as PNG
                    save_kwargs["compress_level"] = 9
                    img.save(file_path, **save_kwargs)
                else:
                    # Convert to JPG for better compression if user permits? 
                    # User asked for "optimise". Converting format might break paths if I renamed.
                    # So I will keep PNG but just optimize.
                    save_kwargs["compress_level"] = 9
                    img.save(file_path, **save_kwargs)
            
            print(f"Optimized: {file_path}")
            
    except Exception as e:
        print(f"Failed {file_path}: {e}")

def main():
    base_dir = "media"
    images = []
    print("Scanning for images...")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                images.append(os.path.join(root, file))
    
    print(f"Found {len(images)} images. Starting optimization...")
    
    # Use ThreadPool to speed up
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(optimize_image, images)
        
    print("Image optimization complete.")

if __name__ == "__main__":
    main()
