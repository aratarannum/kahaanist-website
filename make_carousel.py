import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement = """      let mediaArray = [];
      if (p.img) mediaArray.push(p.img);
      if (p.gallery) mediaArray = mediaArray.concat(p.gallery);
      
      let activeMediaHTML = '';
      if (mediaArray.length > 0) {
          let first = mediaArray[0];
          if (first.endsWith('.mp4') || first.endsWith('.webm')) {
              activeMediaHTML = `<video id="main-display-video" src="${first}" autoplay loop muted playsinline class="main-image"></video>
                                 <img id="main-display-img" class="main-image" style="display:none;">`;
          } else {
              activeMediaHTML = `<img id="main-display-img" src="${first}" class="main-image">
                                 <video id="main-display-video" autoplay loop muted playsinline class="main-image" style="display:none;"></video>`;
          }
      }
      
      let thumbnailsHTML = '';
      mediaArray.forEach((asset, idx) => {
          let thumbContent = asset.endsWith('.mp4') 
               ? `<div style="display:flex; align-items:center; justify-content:center; font-size:12px; color:var(--parchment-dim); width:100%; height:100%;">+ Video</div>`
               : `<img src="${asset}" style="width:100%; height:100%; object-fit:cover;">`;
          
          thumbnailsHTML += `<div class="thumb" onclick="window.swapMedia('${asset}')" style="cursor:pointer; overflow:hidden;">${thumbContent}</div>`;
      });
      
      if (!window.swapMedia) {
          window.swapMedia = function(asset) {
              const imgEl = document.getElementById('main-display-img');
              const vidEl = document.getElementById('main-display-video');
              if(asset.endsWith('.mp4') || asset.endsWith('.webm')) {
                  imgEl.style.display = 'none';
                  vidEl.src = asset;
                  vidEl.style.display = 'block';
                  vidEl.play();
              } else {
                  vidEl.style.display = 'none';
                  vidEl.pause();
                  imgEl.src = asset;
                  imgEl.style.display = 'block';
              }
          };
      }
      
      container.innerHTML = `
        <div class="product-page-layout">
          <div class="product-page-gallery" style="display:flex; flex-direction:column; gap:16px;">
            ${activeMediaHTML}
            <div class="thumbnails" style="display:flex; gap:12px;">
                ${thumbnailsHTML}
            </div>
          </div>"""

# Match the old generation logic exactly
pattern = re.compile(r"let galleryHTML = p\.img \? `<img src=\"\$\{p\.img\}\" class=\"main-image\">` : '';[\s\S]*?<div class=\"thumbnails\">\s*\$\{p\.img \? `<img src=\"\$\{p\.img\}\" class=\"thumb\">` : `<div class=\"thumb\"></div>`\}\s*<div class=\"thumb\"[^>]*>\+ Video</div>\s*<div class=\"thumb\"[^>]*>\+ Angle</div>\s*</div>\s*</div>")

html = pattern.sub(replacement, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
