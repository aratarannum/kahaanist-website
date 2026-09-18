import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace("gallery: ['medusa-earrings.mp4', 'medusa-1.jpeg', 'medusacloseup.png', 'medusaearring-video.mp4', 'medusaearring.jpeg', 'medusa_earring_display.png']", "gallery: ['medusa-earrings.mp4']")

html = html.replace("gallery: ['ouroboros-pendant.mp4', 'ouroboros-pendant.png', 'snake-infinity-pendant-video.mp4']", "gallery: ['ouroboros-pendant.mp4']")

html = html.replace("gallery: ['tree-of-life.mp4', 'tree.jpg']", "gallery: ['tree-of-life.mp4']")

html = html.replace(" gallery: ['queermermaids.png'],", "")
html = html.replace(" gallery: ['queermermen.jpg'],", "")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
