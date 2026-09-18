import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Medusa Brass Earrings -> Medusa Earrings
html = html.replace("slug:'medusa-brass-earrings'", "slug:'medusa-earrings'")
html = html.replace("name:'Medusa Brass Earrings'", "name:'Medusa Earrings'")

# Mermaids in Love Earrings -> Pendant Necklace
html = html.replace("slug:'mermaids-in-love-earrings'", "slug:'mermaids-in-love-pendant'")
html = html.replace("cat:'earrings', name:'Mermaids in Love Earrings'", "cat:'neckpieces', name:'Mermaids in Love Pendant Necklace'")
html = html.replace("these earrings symbolize", "this pendant symbolizes")
html = html.replace("size: 'Drop length: 30mm.'", "size: 'Pendant diameter: 30mm. Chain length: 20 inches.'")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
