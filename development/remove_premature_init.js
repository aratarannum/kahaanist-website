const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf-8');

// The block containing the premature initShopify() call looks like:
/*
  }

  initShopify();

  const shopifyOptions = {
*/

const target = '  }\r\n\r\n  initShopify();\r\n\r\n  const shopifyOptions = {';
const fallbackTarget = '  }\n\n  initShopify();\n\n  const shopifyOptions = {';

let found = false;

if (html.includes(target)) {
    html = html.replace(target, '  }\r\n\r\n  // initShopify() deferred\r\n\r\n  const shopifyOptions = {');
    found = true;
} else if (html.includes(fallbackTarget)) {
    html = html.replace(fallbackTarget, '  }\n\n  // initShopify() deferred\n\n  const shopifyOptions = {');
    found = true;
} else {
    // If exact match fails, use regex
    const regex = /\}\s*initShopify\(\);\s*const shopifyOptions = \{/m;
    if (regex.test(html)) {
        html = html.replace(regex, '}\n\n  // initShopify() deferred\n\n  const shopifyOptions = {');
        found = true;
    }
}

if (found) {
    fs.writeFileSync('index.html', html, 'utf-8');
    console.log('SUCCESS: Removed premature initShopify() call');
} else {
    console.log('FAIL: Could not find premature initShopify() call');
    process.exit(1);
}
