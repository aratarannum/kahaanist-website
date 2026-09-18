const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');
const idx = html.indexOf('page-home');
console.log(html.substring(idx, idx + 1000));
