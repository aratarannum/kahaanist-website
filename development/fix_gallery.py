import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

galleries = {
    'medusa-earrings': ['medusa-earrings.mp4', 'medusa-1.jpeg', 'medusacloseup.png', 'medusaearring-video.mp4', 'medusaearring.jpeg', 'medusa_earring_display.png'],
    'ouroboros-pendant': ['ouroboros-pendant.mp4', 'ouroboros-pendant.png', 'snake-infinity-pendant-video.mp4'],
    'mermaids-in-love-pendant': ['queermermaids.png'],
    'mermen-in-love': ['queermermen.jpg'],
    'tree-of-life-pendant': ['tree-of-life.mp4', 'tree.jpg']
}

for slug, gallery in galleries.items():
    pattern = rf"(slug:'{slug}',\s*cat:.*?,)"
    html = re.sub(pattern, rf"\g<1> gallery: {gallery},", html)

old_pattern = re.compile(r"const imageContent = p\.img[\s\S]*?<div class=\"thumbnails\">\s*\$\{p\.img \? `<img src=\"\$\{p\.img\}\" class=\"thumb\">` : `<div class=\"thumb\"></div>`\}\s*<div class=\"thumb\"[^>]*>\+ Video</div>\s*<div class=\"thumb\"[^>]*>\+ Angle</div>\s*</div>\s*</div>")

new_html = """      let galleryHTML = p.img ? `<img src="${p.img}" class="main-image">` : '';
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
          </div>"""

html = old_pattern.sub(new_html, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
