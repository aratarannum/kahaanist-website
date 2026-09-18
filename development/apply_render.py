import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

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

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Replacement successful")
else:
    print("Old string not found!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
