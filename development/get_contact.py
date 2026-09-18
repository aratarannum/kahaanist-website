import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<main id="page-contact".*?</main>', html, re.DOTALL)
if m:
    print(m.group(0))
