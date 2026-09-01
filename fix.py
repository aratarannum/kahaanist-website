import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r"(slug:'mermaids-in-love-earrings'.*?), shopifyId:", r"\1, img:'Photoroom_20260825_140537.png', shopifyId:", html)
html = re.sub(r"(slug:'ouroboros-pendant'.*?), shopifyId:", r"\1, img:'Photoroom_20260823_140048.jpeg', shopifyId:", html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
