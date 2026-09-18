const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf-8');

const oldDomain = 'sjm0m7-iv.myshopify.com';
const newDomain = 'kahaanist-global.myshopify.com';

const count = (html.match(new RegExp(oldDomain, 'g')) || []).length;

if (count > 0) {
    html = html.split(oldDomain).join(newDomain);
    fs.writeFileSync('index.html', html, 'utf-8');
    console.log('SUCCESS: Replaced ' + count + ' occurrence(s) of ' + oldDomain + ' with ' + newDomain);
} else {
    console.log('FAIL: Could not find ' + oldDomain + ' in index.html');
    process.exit(1);
}
