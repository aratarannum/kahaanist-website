import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Map new IDs
mapping = {
    'mermaids-in-love-earrings': '8742905446583',
    'mermen-in-love': '8742908756151',
    'ouroboros-pendant': '8742904332471',
    'tree-of-life-pendant': '8742902792375',
    'medusa-brass-earrings': '8733191569591'
}

for slug, shopify_id in mapping.items():
    pattern = rf"(slug:'{slug}'.*?shopifyId: ')\d*(')"
    html = re.sub(pattern, rf"\g<1>{shopify_id}\g<2>", html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
