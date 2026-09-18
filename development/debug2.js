const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');
const idx = html.indexOf("hashchange");
if (idx === -1) { console.log('NOT FOUND'); process.exit(1); }
const chunk = html.substring(idx - 50, idx + 80);
console.log(JSON.stringify(chunk));
