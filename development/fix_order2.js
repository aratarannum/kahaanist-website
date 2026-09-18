const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf-8');

// The exact text from the file
const target = "window.addEventListener('hashchange', route);\r\n  route();\r\n\r\n  // ---------- Reveal on scroll";
const replacement = "window.addEventListener('hashchange', route);\r\n  route();\r\n\r\n  // Now that products[] and route() exist, init Two-Brain\r\n  initShopify();\r\n\r\n  // ---------- Reveal on scroll";

if (html.includes(target)) {
    html = html.replace(target, replacement);
    fs.writeFileSync('index.html', html, 'utf-8');
    console.log('SUCCESS: Inserted initShopify() after route()');
} else {
    console.log('FAIL: Could not find target');
    process.exit(1);
}
