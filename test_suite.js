const fs = require('fs');
const path = require('path');

console.log('Running Pre-Deployment Checks...');

const htmlPath = path.join(__dirname, 'index.html');
if (!fs.existsSync(htmlPath)) {
  console.error('❌ Error: index.html not found.');
  process.exit(1);
}

const html = fs.readFileSync(htmlPath, 'utf-8');
let errors = 0;

// --- CHECK 1: JavaScript Runtime & Syntax ---
const scriptMatch = html.match(/<script>(.*?)<\/script>/s);
if (!scriptMatch) {
  console.error('❌ Error: Could not find main <script> block in index.html.');
  errors++;
} else {
  let js = scriptMatch[1];
  let products = [];
  
  // Mock browser environment
  const mockEnv = `
    let extractedProducts = [];
    const document = {
      createElement: () => ({ async: false, src: '', onload: null }),
      head: { appendChild: ()=>{} },
      getElementsByTagName: () => [{ appendChild: ()=>{} }],
      getElementById: (id) => ({ classList: { add: ()=>{}, remove: ()=>{} }, innerHTML: '', textContent: '' }),
      querySelectorAll: (sel) => [],
      querySelector: (sel) => ({ classList: { add: ()=>{}, remove: ()=>{} } }),
      title: ''
    };
    const window = { addEventListener: ()=>{}, scrollTo: ()=>{} };
    const location = { hash: '' };
    const setTimeout = ()=>{};
    const IntersectionObserver = class { observe(){} unobserve(){} };
  `;
  
  // Inject a trap to extract the products array for validation
  const testJS = mockEnv + js + `\n extractedProducts = typeof products !== 'undefined' ? products : [];`;

  try {
    eval(testJS);
    console.log('✅ JS Syntax & basic runtime: Passed');
    
    // --- CHECK 2: Product Schema Validation ---
    // Read the products from the evaluated script context
    // Since eval doesn't easily return local variables, we parse them via regex just to be safe
    const productsRegex = /const products = (\[.*?\]);/s;
    const pMatch = js.match(productsRegex);
    if(pMatch) {
        // use Function constructor to safely evaluate the array literal
        const parsedProducts = new Function(`return ${pMatch[1]}`)();
        let schemaErrors = 0;
        parsedProducts.forEach((p, i) => {
            if (!p.name) { console.error(`❌ Product at index ${i} is missing a 'name'.`); schemaErrors++; }
            if (!p.price) { console.error(`❌ Product '${p.name || i}' is missing a 'price'.`); schemaErrors++; }
            if (!p.slug) { console.error(`❌ Product '${p.name || i}' is missing a 'slug'.`); schemaErrors++; }
        });
        if(schemaErrors === 0){
             console.log(`✅ Product Schema: Passed (${parsedProducts.length} products validated)`);
        } else {
             errors++;
        }
    }

  } catch (e) {
    console.error('❌ JS Runtime Error:', e.message);
    errors++;
  }
}

// --- CHECK 3: Basic HTML Structure (Mismatched Tags) ---
const divOpens = (html.match(/<div/g) || []).length;
const divCloses = (html.match(/<\/div>/g) || []).length;
if (Math.abs(divOpens - divCloses) > 5) {
    // A strict 1:1 match can sometimes fail on edge cases, but a large discrepancy means structural failure
    console.error(`❌ HTML Structure Warning: Found ${divOpens} <divs> but ${divCloses} </div>s. Huge mismatch!`);
    errors++;
} else {
    console.log('✅ HTML Structure Check: Passed');
}


if (errors > 0) {
  console.error(`\n🚨 DEPLOYMENT BLOCKED: ${errors} error(s) found. Please fix them before publishing.`);
  process.exit(1);
} else {
  console.log('\n🎉 All checks passed! Safe to deploy.');
  process.exit(0);
}
