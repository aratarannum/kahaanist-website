import re

html = open('index.html', 'r', encoding='utf-8').read()

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

old_str = """      const imageContent = p.img
        ? `<img src="${p.img}" alt="${p.name}" class="main-image">`
        : `<div class="main-image" style="display:flex; align-items:center; justify-content:center; border:1px solid var(--ink-soft);"><svg viewBox="0 0 100 100" fill="none" width="100" height="100"><circle cx="50" cy="50" r="34" stroke="#d9ab5f" stroke-width="1.2"/></svg></div>`;
      
      container.innerHTML = `
        <div class="product-page-layout">
          <div class="product-page-gallery">
            ${imageContent}
            <div class="thumbnails">
              ${p.img ? `<img src="${p.img}" class="thumb">` : `<div class="thumb"></div>`}
              <div class="thumb" style="display:flex; align-items:center; justify-content:center; font-size:12px; color:var(--parchment-dim);">+ Video</div>
              <div class="thumb" style="display:flex; align-items:center; justify-content:center; font-size:12px; color:var(--parchment-dim);">+ Angle</div>
            </div>
          </div>"""

new_str = """      let galleryHTML = p.img ? `<img src="${p.img}" class="main-image">` : '';
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

html = html.replace(old_str, new_str)
open('index.html', 'w', encoding='utf-8').write(html)
