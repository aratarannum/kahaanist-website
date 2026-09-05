const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');
const startMarker = '// ---------- Shopify Integration ----------';
const endMarker = "moneyFormat: 'Rs.%20%7B%7Bamount%7D%7D',";
const start = html.indexOf(startMarker);
const end = html.indexOf(endMarker, start) + endMarker.length;
if (start === -1 || end === -1) { console.log('MARKER NOT FOUND'); process.exit(1); }
const block = html.substring(start, end);
fs.writeFileSync('old_shopify_block.txt', block, 'utf-8');
console.log('Block length:', block.length);
console.log('Saved to old_shopify_block.txt');
