const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf-8');

// 1. Find the direct innerHTML assignment and wrap it in a function
const target1 = "  document.getElementById('home-featured').innerHTML =\r\n    products.slice(0, 6).map(productCardHTML).join('');";
const target1Alt = "document.getElementById('home-featured').innerHTML =\n    products.slice(0, 6).map(productCardHTML).join('');";

const replacement1 = `  function renderHome() {\r\n    const container = document.getElementById('home-featured');\r\n    if (container) container.innerHTML = products.slice(0, 6).map(productCardHTML).join('');\r\n  }\r\n  renderHome();`;

let found = false;
if (html.includes(target1)) {
    html = html.replace(target1, replacement1);
    found = true;
} else {
    // try regex
    const regex = /document\.getElementById\('home-featured'\)\.innerHTML\s*=\s*products\.slice\(0,\s*6\)\.map\(productCardHTML\)\.join\(''\);/g;
    if (regex.test(html)) {
        html = html.replace(regex, replacement1);
        found = true;
    }
}

if (!found) {
    console.log("FAIL: Could not find home-featured assignment");
    process.exit(1);
}

// 2. Add renderHome() to the global visitor rerender block
const target2 = `      // Re-render current page with USD prices\r\n      route();`;
const target2Alt = `      // Re-render current page with USD prices\n      route();`;

let found2 = false;
const replacement2 = `      // Re-render current page with USD prices\r\n      if(typeof renderHome === 'function') renderHome();\r\n      route();`;

if (html.includes(target2)) {
    html = html.replace(target2, replacement2);
    found2 = true;
} else if (html.includes(target2Alt)) {
    html = html.replace(target2Alt, replacement2);
    found2 = true;
} else {
    const regex2 = /\/\/\s*Re-render current page with USD prices\s*route\(\);/g;
    if (regex2.test(html)) {
        html = html.replace(regex2, replacement2);
        found2 = true;
    }
}

if (!found2) {
    console.log("FAIL: Could not find route() in global visitor block");
    process.exit(1);
}

fs.writeFileSync('index.html', html, 'utf-8');
console.log('SUCCESS: Homepage re-render logic fixed!');
