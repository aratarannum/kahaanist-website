const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf-8');
let errors = 0;

// STEP 1: Remove the premature initShopify() call
const oldCall = '  // initShopify() is called after products & route() are defined (see below)';
// Check if already fixed from partial run
if (html.includes(oldCall)) {
    console.log('SKIP: premature call already removed');
} else {
    const origCall = '  initShopify();\r\n\r\n  const shopifyOptions = {';
    if (html.includes(origCall)) {
        html = html.replace(origCall, '  // initShopify() deferred\r\n\r\n  const shopifyOptions = {');
        console.log('OK: Removed premature initShopify() call');
    } else {
        console.log('FAIL: Could not find initShopify() call');
        errors++;
    }
}

// STEP 2: Insert initShopify() after route(); call
// The exact text from the file (note the mixed indentation)
const target = "  window.addEventListener('hashchange', route);\r\n    route();";
const replacement = "  window.addEventListener('hashchange', route);\r\n    route();\r\n\r\n    // Now that products[] and route() exist, init Two-Brain\r\n    initShopify();";

if (html.includes(target)) {
    html = html.replace(target, replacement);
    console.log('OK: Moved initShopify() after route() definition');
} else {
    console.log('FAIL: Could not find route init block');
    // Try alternate whitespace
    const alt = "window.addEventListener('hashchange', route);\r\n    route();";
    const idx = html.indexOf(alt);
    if (idx !== -1) {
        html = html.replace(alt, alt + "\r\n\r\n    // Now that products[] and route() exist, init Two-Brain\r\n    initShopify();");
        console.log('OK: (alt match) Moved initShopify() after route()');
    } else {
        console.log('FAIL: Could not find alternate either');
        errors++;
    }
}

// STEP 3: Fix moneyFormat to be dynamic
const oldMoney = "          moneyFormat: shopifyOptions.moneyFormat,";
const newMoney = "          moneyFormat: isGlobalVisitor ? '%24%7B%7Bamount%7D%7D' : shopifyOptions.moneyFormat,";

if (html.includes(newMoney)) {
    console.log('SKIP: moneyFormat already dynamic');
} else if (html.includes(oldMoney)) {
    html = html.replace(oldMoney, newMoney);
    console.log('OK: Made moneyFormat dynamic');
} else {
    console.log('WARN: Could not find moneyFormat line');
}

if (errors > 0) {
    console.log('\nFATAL: ' + errors + ' error(s). File NOT saved.');
    process.exit(1);
} else {
    fs.writeFileSync('index.html', html, 'utf-8');
    console.log('\nSUCCESS: Execution order fixed!');
}
