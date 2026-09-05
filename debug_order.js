const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');
const lines = html.split('\n');

const markers = ['initShopify()', 'const products =', 'function route()', 'function renderShopifyButtons'];
for (const m of markers) {
    const idx = lines.findIndex(l => l.includes(m));
    console.log('Line ' + (idx+1) + ': ' + m);
}
