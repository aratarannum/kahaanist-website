import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove Tree of Life Drop Earrings
html = re.sub(r'^\s*\{\s*slug:\'tree-of-life-drop-earrings\'.*?\n', '', html, flags=re.MULTILINE)

# Rename Ouroboros Pendant -> Ouroboros Pendant Necklace
html = html.replace("name:'Ouroboros Pendant'", "name:'Ouroboros Pendant Necklace'")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
