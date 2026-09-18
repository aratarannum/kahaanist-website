import os
import shutil
import re

assets_dir = r"C:\Users\arata\OneDrive\Desktop\JewelryDesigns\Assets"
website_dir = r"C:\Users\arata\OneDrive\Desktop\JewelryDesigns\Website"

# 1. Copy images and videos to Website folder, renaming the .tmp.mp4 files
folders = [
    ("01-Tree-of-life-pendant-necklace", "tree-of-life-2.png", "tree-of-life.mp4"),
    ("02-Medusa-earrings", "medusa-earrings.jpg", "medusa-earrings.mp4"),
    ("03-Ouroboros-pendant", "Photoroom_20260823_140048.jpeg", "ouroboros-pendant.mp4"),
    ("04-Mermen-in-love", "mermen-in-love.png", None),
    ("05-Mermaids-in-love", "Photoroom_20260825_140537.png", None)
]

images = {}
videos = {}

for folder, img_name, vid_name in folders:
    folder_path = os.path.join(assets_dir, folder)
    img_path = os.path.join(folder_path, img_name)
    if os.path.exists(img_path):
        shutil.copy(img_path, os.path.join(website_dir, img_name))
        images[folder] = img_name
        print(f"Copied {img_name}")
    
    # Check for .tmp.mp4
    if vid_name:
        for file in os.listdir(folder_path):
            if file.endswith('.tmp.mp4'):
                src_vid = os.path.join(folder_path, file)
                dest_vid = os.path.join(website_dir, vid_name)
                shutil.copy(src_vid, dest_vid)
                videos[folder] = vid_name
                print(f"Copied {file} as {vid_name}")

# 2. Update index.html products array with new images and fix slug/name for Ouroboros
index_path = os.path.join(website_dir, "index.html")
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Update Tree of life image
html = re.sub(r"img:'tree-of-life-main\.jpg'", f"img:'tree-of-life-2.png'", html)
# Update Mermaids in love
html = re.sub(r"(slug:'mermaids-in-love-earrings'.*?), checkout:", f"\\1, img:'Photoroom_20260825_140537.png', checkout:", html)
# Update Ouroboros ring to pendant
html = re.sub(r"slug:'ouroboros-band-ring', cat:'rings', name:'Ouroboros Band Ring'", "slug:'ouroboros-pendant', cat:'neckpieces', name:'Ouroboros Pendant'", html)
html = re.sub(r"(slug:'ouroboros-pendant'.*?), checkout:", f"\\1, img:'Photoroom_20260823_140048.jpeg', checkout:", html)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
