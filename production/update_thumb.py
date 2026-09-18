import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_logic = """          let thumbContent = asset.endsWith('.mp4') 
               ? `<div style="display:flex; align-items:center; justify-content:center; font-size:12px; color:var(--parchment-dim); width:100%; height:100%;">+ Video</div>`
               : `<img src="${asset}" style="width:100%; height:100%; object-fit:cover;">`;"""

new_logic = """          let thumbContent = (asset.endsWith('.mp4') || asset.endsWith('.webm'))
               ? `<div style="position:relative; width:100%; height:100%;">
                    <video src="${asset}#t=0.1" muted playsinline style="width:100%; height:100%; object-fit:cover; pointer-events:none;"></video>
                    <div style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:rgba(0,0,0,0.25);">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="#efe6d3"><path d="M8 5v14l11-7z"/></svg>
                    </div>
                  </div>`
               : `<img src="${asset}" style="width:100%; height:100%; object-fit:cover;">`;"""

if old_logic in html:
    html = html.replace(old_logic, new_logic)
    print("Successfully replaced.")
else:
    print("Old logic not found!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
