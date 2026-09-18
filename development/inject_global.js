const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf-8');

// Read the exact old block from the extracted file
const oldBlock = fs.readFileSync('old_shopify_block.txt', 'utf-8');

const newBlock = `// ---------- Shopify Integration (Two-Brain: IN + Global) ----------\r
  let shopifyUI;\r
  let isGlobalVisitor = false;\r
\r
  // Geo-IP detection\r
  async function detectCountry() {\r
    try {\r
      const resp = await fetch('https://ipapi.co/json/', { signal: AbortSignal.timeout(3000) });\r
      const data = await resp.json();\r
      return data.country_code;\r
    } catch(e) {\r
      return 'IN';\r
    }\r
  }\r
\r
  async function initShopify() {\r
    const country = await detectCountry();\r
    isGlobalVisitor = (country !== 'IN');\r
\r
    const domain = isGlobalVisitor ? 'sjm0m7-iv.myshopify.com' : 'kahaanist.myshopify.com';\r
    const token  = isGlobalVisitor ? '2b53a4ed899e25df22ee289a3df89bf0' : 'a644d9e6d80b87611a5f4c9cf0199a5d';\r
\r
    // Swap prices and Shopify IDs for global visitors\r
    if (isGlobalVisitor) {\r
      products.forEach(p => {\r
        if (p.priceGlobal) p.price = p.priceGlobal;\r
        if (p.shopifyIdGlobal) p.shopifyId = p.shopifyIdGlobal;\r
      });\r
      // Re-render current page with USD prices\r
      route();\r
    }\r
\r
    const scriptURL = 'https://sdks.shopifycdn.com/buy-button/latest/buy-button-storefront.min.js';\r
    const script = document.createElement('script');\r
    script.async = true;\r
    script.src = scriptURL;\r
    document.head.appendChild(script);\r
    script.onload = () => {\r
      const client = ShopifyBuy.buildClient({\r
        domain: domain,\r
        storefrontAccessToken: token,\r
      });\r
      ShopifyBuy.UI.onReady(client).then((ui) => {\r
        shopifyUI = ui;\r
        renderShopifyButtons();\r
      });\r
    };\r
  }\r
\r
  initShopify();\r
\r
  const shopifyOptions = {\r
    moneyFormat: 'Rs.%20%7B%7Bamount%7D%7D',`;

if (html.includes(oldBlock)) {
    html = html.replace(oldBlock, newBlock);
    console.log('OK: Replaced Shopify init with Two-Brain system');
} else {
    console.log('FAIL: Could not find old Shopify init block!');
    process.exit(1);
}

// Add global IDs to products (if not already present)
const mapping = [
    ["shopifyId: '8742902792375'", "shopifyId: '8742902792375', shopifyIdGlobal: '9412329701609', priceGlobal: '$65'"],
    ["shopifyId: '8742908756151'", "shopifyId: '8742908756151', shopifyIdGlobal: '9412331176169', priceGlobal: '$65'"],
    ["shopifyId: '8733191569591'", "shopifyId: '8733191569591', shopifyIdGlobal: '9412325867753', priceGlobal: '$65'"],
    ["shopifyId: '8742905446583'", "shopifyId: '8742905446583', shopifyIdGlobal: '9412330586345', priceGlobal: '$65'"],
    ["shopifyId: '8742904332471'", "shopifyId: '8742904332471', shopifyIdGlobal: '9412331962601', priceGlobal: '$65'"],
];

for (const [oldStr, newStr] of mapping) {
    if (html.includes(oldStr) && !html.includes(newStr)) {
        html = html.replace(oldStr, newStr);
        console.log(`OK: Added global ID for ${oldStr}`);
    } else if (html.includes(newStr)) {
        console.log(`SKIP: Already present for ${oldStr}`);
    } else {
        console.log(`FAIL: Could not find ${oldStr}`);
        process.exit(1);
    }
}

// Update shipping text
const oldShip = 'Secure checkout. Free shipping across India.';
const newShip = "${isGlobalVisitor ? 'Secure checkout. International shipping included.' : 'Secure checkout. Free shipping across India.'}";
if (html.includes(oldShip)) {
    html = html.replace(oldShip, newShip);
    console.log('OK: Updated shipping text');
}

fs.writeFileSync('index.html', html, 'utf-8');
console.log('\nSUCCESS: index.html updated with Two-Brain global routing!');
