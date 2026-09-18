import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

errors = 0

# 1. Update Medusa Earrings global price to $99
old_medusa = "shopifyId: '8733191569591', shopifyIdGlobal: '9412325867753', priceGlobal: '$65'"
new_medusa = "shopifyId: '8733191569591', shopifyIdGlobal: '9412325867753', priceGlobal: '$99'"

if old_medusa in html:
    html = html.replace(old_medusa, new_medusa)
    print("OK: Updated Medusa global price to $99")
else:
    print("FAIL: Could not find Medusa global price string")
    errors += 1

# 2. Update Social Links
old_social = """      <div class="fcol">
        <h5>Follow</h5>
        <a href="#">Instagram</a>
        <a href="#">Pinterest</a>
        <a href="#">WhatsApp</a>
      </div>"""

new_social = """      <div class="fcol">
        <h5>Follow</h5>
        <a href="https://www.instagram.com/thekahaanist?igsi=MWd1dmFwbnA2dTZpbA==" target="_blank" rel="noopener noreferrer">Instagram</a>
        <a href="https://www.facebook.com/share/19GVioFotP/?mibextid=wwXIfr" target="_blank" rel="noopener noreferrer">Facebook</a>
      </div>"""

if old_social in html:
    html = html.replace(old_social, new_social)
    print("OK: Updated social links")
else:
    # Try an alternative matching using regex in case of slight whitespace differences
    import re
    social_regex = re.compile(r'<div class="fcol">\s*<h5>Follow</h5>\s*<a href="#">Instagram</a>\s*<a href="#">Pinterest</a>\s*<a href="#">WhatsApp</a>\s*</div>', re.MULTILINE)
    if social_regex.search(html):
        html = social_regex.sub(new_social, html)
        print("OK: Updated social links (via regex)")
    else:
        print("FAIL: Could not find social links block")
        errors += 1


if errors > 0:
    print(f"\nFATAL: {errors} error(s). File NOT saved.")
    sys.exit(1)
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("\nSUCCESS: Saved changes to index.html!")
