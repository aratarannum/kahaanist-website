import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r"(slug:'tree-of-life-pendant'.*?shopifyId: ')8733191569591(')", r"\g<1>8742905446583\g<2>", html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
