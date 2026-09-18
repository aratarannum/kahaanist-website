import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

errors = 0

# ============================================================
# STEP 1: Add shopifyIdGlobal and priceGlobal to each product
# ============================================================

global_mapping = {
    "shopifyId: '8742902792375'": "shopifyId: '8742902792375', shopifyIdGlobal: '9412329701609', priceGlobal: '$65'",
    "shopifyId: '8742908756151'": "shopifyId: '8742908756151', shopifyIdGlobal: '9412331176169', priceGlobal: '$65'",
    "shopifyId: '8733191569591'": "shopifyId: '8733191569591', shopifyIdGlobal: '9412325867753', priceGlobal: '$65'",
    "shopifyId: '8742905446583'": "shopifyId: '8742905446583', shopifyIdGlobal: '9412330586345', priceGlobal: '$65'",
    "shopifyId: '8742904332471'": "shopifyId: '8742904332471', shopifyIdGlobal: '9412331962601', priceGlobal: '$65'",
}

for old, new in global_mapping.items():
    if old in html:
        html = html.replace(old, new)
        print(f"  OK: Added global ID for {old}")
    else:
        # Already replaced from previous partial run
        if new in html:
            print(f"  SKIP: Already present for {old}")
        else:
            print(f"  FAIL: Could not find {old}")
            errors += 1

# ============================================================
# STEP 2: Replace Shopify SDK init with Two-Brain system
# ============================================================

# Use the EXACT whitespace from the file (2-space indent, \r\n line endings)
old_block = "// ---------- Shopify Integration ----------\r\n  let shopifyUI;\r\n  const scriptURL = 'https://sdks.shopifycdn.com/buy-button/latest/buy-button-storefront.min.js';\r\n  const script = document.createElement('script');\r\n  script.async = true;\r\n  script.src = scriptURL;\r\n  document.head.appendChild(script);\r\n  script.onload = () => {\r\n    const client = ShopifyBuy.buildClient({\r\n      domain: 'kahaanist.myshopify.com',\r\n      storefrontAccessToken: 'a644d9e6d80b87611a5f4c9cf0199a5d',\r\n    });\r\n    ShopifyBuy.UI.onReady(client).then((ui) => {\r\n      shopifyUI = ui;\r\n      renderShopifyButtons();\r\n    });\r\n  };\r\n\r\n  const shopifyOptions = {\r\n    moneyFormat: 'Rs.%20%7B%7Bamount%7D%7D',"

new_block = "// ---------- Shopify Integration (Two-Brain: IN + Global) ----------\r\n  let shopifyUI;\r\n  let isGlobalVisitor = false;\r\n\r\n  // Geo-IP detection\r\n  async function detectCountry() {\r\n    try {\r\n      const resp = await fetch('https://ipapi.co/json/', { signal: AbortSignal.timeout(3000) });\r\n      const data = await resp.json();\r\n      return data.country_code;\r\n    } catch(e) {\r\n      return 'IN';\r\n    }\r\n  }\r\n\r\n  async function initShopify() {\r\n    const country = await detectCountry();\r\n    isGlobalVisitor = (country !== 'IN');\r\n\r\n    const domain = isGlobalVisitor ? 'sjm0m7-iv.myshopify.com' : 'kahaanist.myshopify.com';\r\n    const token  = isGlobalVisitor ? '2b53a4ed899e25df22ee289a3df89bf0' : 'a644d9e6d80b87611a5f4c9cf0199a5d';\r\n\r\n    // Swap prices and Shopify IDs for global visitors\r\n    if (isGlobalVisitor) {\r\n      products.forEach(p => {\r\n        if (p.priceGlobal) p.price = p.priceGlobal;\r\n        if (p.shopifyIdGlobal) p.shopifyId = p.shopifyIdGlobal;\r\n      });\r\n      // Re-render current page with USD prices\r\n      route();\r\n    }\r\n\r\n    const scriptURL = 'https://sdks.shopifycdn.com/buy-button/latest/buy-button-storefront.min.js';\r\n    const script = document.createElement('script');\r\n    script.async = true;\r\n    script.src = scriptURL;\r\n    document.head.appendChild(script);\r\n    script.onload = () => {\r\n      const client = ShopifyBuy.buildClient({\r\n        domain: domain,\r\n        storefrontAccessToken: token,\r\n      });\r\n      ShopifyBuy.UI.onReady(client).then((ui) => {\r\n        shopifyUI = ui;\r\n        renderShopifyButtons();\r\n      });\r\n    };\r\n  }\r\n\r\n  initShopify();\r\n\r\n  const shopifyOptions = {\r\n    moneyFormat: 'Rs.%20%7B%7Bamount%7D%7D',"

if old_block in html:
    html = html.replace(old_block, new_block)
    print("  OK: Replaced Shopify init with Two-Brain system")
else:
    print("  FAIL: Could not find old Shopify init block!")
    errors += 1

# ============================================================
# STEP 3: Update shipping text for global visitors
# ============================================================

old_shipping = "Secure checkout. Free shipping across India."
new_shipping = "${isGlobalVisitor ? 'Secure checkout. International shipping included.' : 'Secure checkout. Free shipping across India.'}"

if old_shipping in html:
    html = html.replace(old_shipping, new_shipping)
    print("  OK: Updated shipping text")
else:
    if new_shipping in html:
        print("  SKIP: Shipping text already updated")
    else:
        print("  WARN: Could not find shipping text (non-critical)")

# ============================================================
# SAVE
# ============================================================

if errors > 0:
    print(f"\nFATAL: {errors} error(s). File NOT saved.")
    sys.exit(1)
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("\nSUCCESS: index.html updated with Two-Brain global routing!")
