import os
import shutil
import re

archive_dir = r"C:\Users\arata\OneDrive\Desktop\JewelryDesigns\Assets\00-Archive"
website_dir = r"C:\Users\arata\OneDrive\Desktop\JewelryDesigns\Website"

# Mapping of product slug to list of extra files in 00-Archive (and existing copied files)
product_assets = {
    'medusa-earrings': {
        'archive_files': ['medusa 1.jpeg', 'MedusaCloseUp.png', 'medusaearring video.mp4', 'MedusaEarring.jpeg', 'medusa_earring_display.png'],
        'existing': ['medusa-earrings.mp4']
    },
    'ouroboros-pendant': {
        'archive_files': ['Ouroboros pendant.png', 'Snake infinity Pendant video.mp4'],
        'existing': ['ouroboros-pendant.mp4']
    },
    'mermaids-in-love-pendant': {
        'archive_files': ['queermermaids.png'],
        'existing': []
    },
    'mermen-in-love': {
        'archive_files': ['QueerMermen.jpg'],
        'existing': []
    },
    'tree-of-life-pendant': {
        'archive_files': ['Tree.jpg'],
        'existing': ['tree-of-life.mp4']
    }
}

galleries = {}

for slug, data in product_assets.items():
    gallery = []
    
    # Add existing copied files
    for ext in data['existing']:
        gallery.append(ext)
        
    # Copy and add archive files
    for f in data['archive_files']:
        src = os.path.join(archive_dir, f)
        if os.path.exists(src):
            clean_name = f.replace(" ", "-").lower()
            dest = os.path.join(website_dir, clean_name)
            shutil.copy(src, dest)
            gallery.append(clean_name)
    
    galleries[slug] = gallery

# Now update index.html
with open(os.path.join(website_dir, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# Add gallery array to each product in products
for slug, gallery in galleries.items():
    gallery_str = str(gallery)
    # find the object for this slug and add gallery: ['...']
    pattern = rf"(slug:'{slug}',\s*cat:.*?,)"
    replacement = rf"\1 gallery: {gallery_str},"
    html = re.sub(pattern, replacement, html)

# Replace the HTML renderer for product-page-gallery
new_renderer = """
      let galleryHTML = p.img ? `<img src="${p.img}" class="main-image">` : '';
      if(p.gallery && p.gallery.length > 0){
          p.gallery.forEach(asset => {
              if(asset.endsWith('.mp4') || asset.endsWith('.webm')){
                  galleryHTML += `<video src="${asset}" autoplay loop muted playsinline class="main-image" style="margin-top:20px;"></video>`;
              } else {
                  galleryHTML += `<img src="${asset}" class="main-image" style="margin-top:20px;" loading="lazy">`;
              }
          });
      }
      
      container.innerHTML = `
        <div class="product-page-layout">
          <div class="product-page-gallery" style="display:flex; flex-direction:column;">
            ${galleryHTML}
          </div>
"""

# Replace the old container.innerHTML part
old_pattern = r"const imageContent = p\.img[\s\S]*?<div class=\"product-page-layout\">\s*<div class=\"product-page-gallery\">\s*\$\{imageContent\}\s*<div class=\"thumbnails\">\s*\$\{p\.img \? `<img src=\"\$\{p\.img\}\" class=\"thumb\">` : `<div class=\"thumb\"></div>`\}\s*<div class=\"thumb\"[^>]*>\+ Video</div>\s*<div class=\"thumb\"[^>]*>\+ Angle</div>\s*</div>\s*</div>"
html = re.sub(old_pattern, new_renderer, html)

with open(os.path.join(website_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)
