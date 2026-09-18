/**
 * Rapid Programmatic History Transition Test for M1
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const scriptMatches = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)];
const mainScript = scriptMatches.find(m => m[1].includes('const products ='));

if (!mainScript) {
  console.error('Could not find products script tag.');
  process.exit(1);
}

const classListMap = {};
function getEl(id) {
  if (!classListMap[id]) classListMap[id] = new Set();
  return {
    id,
    classList: {
      add: (c) => classListMap[id].add(c),
      remove: (c) => classListMap[id].delete(c),
      toggle: (c, v) => v ? classListMap[id].add(c) : classListMap[id].delete(c),
      contains: (c) => classListMap[id].has(c)
    },
    innerHTML: '',
    textContent: '',
    setAttribute: () => {},
    dataset: { filter: 'all' }
  };
}

const elements = {
  'page-home': getEl('page-home'),
  'page-shop': getEl('page-shop'),
  'page-product': getEl('page-product'),
  'page-contact': getEl('page-contact'),
  'shop-grid': getEl('shop-grid'),
  'product-container': getEl('product-container'),
  'home-featured': getEl('home-featured'),
  'meta-desc': getEl('meta-desc'),
  'shop-eyebrow': getEl('shop-eyebrow'),
  'shop-title': getEl('shop-title'),
  'shop-desc': getEl('shop-desc')
};

const allElements = Object.values(elements);

const document = {
  createElement: () => ({
    async: false,
    src: '',
    onload: null,
    setAttribute: () => {},
    classList: { add: () => {}, remove: () => {}, toggle: () => {} },
    innerHTML: '',
    textContent: ''
  }),
  head: { appendChild: () => {} },
  getElementsByTagName: () => [{ appendChild: () => {}, addEventListener: () => {} }],
  getElementById: (id) => elements[id] || getEl(id),
  querySelectorAll: (sel) => {
    if (sel === '.page') {
      return [elements['page-home'], elements['page-shop'], elements['page-product'], elements['page-contact']];
    }
    return [];
  },
  querySelector: (sel) => ({ classList: { add: () => {}, remove: () => {} }, addEventListener: () => {}, setAttribute: () => {} }),
  addEventListener: () => {},
  title: ''
};

const location = { hash: '', search: '', pathname: '/' };
const historyStack = ['/'];
const window = {
  addEventListener: () => {},
  scrollTo: () => {},
  location: location,
  history: {
    pushState: (_, __, url) => { location.pathname = url; historyStack.push(url); },
    replaceState: (_, __, url) => { location.pathname = url; historyStack[historyStack.length - 1] = url; }
  }
};
const setTimeout = (fn) => fn();
const IntersectionObserver = class { observe() {} unobserve() {} };

// Run router code in constructed environment
const runner = new Function('document', 'window', 'location', 'setTimeout', 'IntersectionObserver', mainScript[1] + '\n return { navigateTo, route, getNormalizedPath, findProductBySlug };');
const api = runner(document, window, location, setTimeout, IntersectionObserver);

console.log('Testing 500 rapid sequential route navigations and popstate events...');
const testSequence = [
  '/shop',
  '/product/medusa',
  '/shop/neckpieces',
  '/contact',
  '/product/tree-of-life',
  '/refund',
  '/',
  '/shop/earrings'
];

let transitionErrors = 0;
for (let i = 0; i < 500; i++) {
  const target = testSequence[i % testSequence.length];
  api.navigateTo(target);
  
  // Verify that only the target page is active
  const activePages = ['page-home', 'page-shop', 'page-product', 'page-contact']
    .filter(id => classListMap[id] && classListMap[id].has('active'));

  if (activePages.length !== 1) {
    console.error(`Transition error at iteration ${i} (${target}): Active pages = ${activePages.join(', ')}`);
    transitionErrors++;
  }
}

console.log(`Rapid history stress test completed. Transitions: 500. Transition errors: ${transitionErrors}.`);
if (transitionErrors === 0) {
  console.log('✅ Rapid navigation stress test PASSED.');
  process.exit(0);
} else {
  console.error('❌ Rapid navigation stress test FAILED.');
  process.exit(1);
}
