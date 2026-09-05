const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf-8');

// 1. Update the display text to US$ instead of $
html = html.replace(/priceGlobal:\s*'\$99'/g, "priceGlobal: 'US$99'");
html = html.replace(/priceGlobal:\s*'\$65'/g, "priceGlobal: 'US$65'");
console.log('OK: Replaced $ with US$ in products array');

// 2. Inject moneyFormat override into initShopify
const target = `    // Swap prices and Shopify IDs for global visitors\r\n    if (isGlobalVisitor) {`;
const fallbackTarget = `    // Swap prices and Shopify IDs for global visitors\n    if (isGlobalVisitor) {`;
const replacement = `    // Swap prices and Shopify IDs for global visitors\r\n    if (isGlobalVisitor) {\r\n      shopifyOptions.moneyFormat = 'US$%20%7B%7Bamount%7D%7D';`;

if (html.includes(target)) {
    html = html.replace(target, replacement);
    console.log('OK: Injected moneyFormat override for global visitor');
} else if (html.includes(fallbackTarget)) {
    html = html.replace(fallbackTarget, `    // Swap prices and Shopify IDs for global visitors\n    if (isGlobalVisitor) {\n      shopifyOptions.moneyFormat = 'US$%20%7B%7Bamount%7D%7D';`);
    console.log('OK: Injected moneyFormat override for global visitor (LF)');
} else {
    // regex
    const regex = /\/\/\s*Swap prices and Shopify IDs for global visitors\s*if\s*\(isGlobalVisitor\)\s*\{/;
    if (regex.test(html)) {
        html = html.replace(regex, `// Swap prices and Shopify IDs for global visitors\n    if (isGlobalVisitor) {\n      shopifyOptions.moneyFormat = 'US$%20%7B%7Bamount%7D%7D';`);
        console.log('OK: Injected moneyFormat override (regex)');
    } else {
        console.log('FAIL: Could not find global visitor block');
        process.exit(1);
    }
}

fs.writeFileSync('index.html', html, 'utf-8');
console.log('SUCCESS: Fixed money format and cart display!');
