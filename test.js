const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');
const scriptMatch = html.match(/<script>(.*?)<\/script>/s);
if (scriptMatch) {
  let js = scriptMatch[1];
  
  // mock browser APIs
  js = `
    const document = {
      getElementById: (id) => {
        if (!id) return null;
        return {
          classList: { add: ()=>{}, remove: ()=>{} },
          innerHTML: '',
          textContent: ''
        }
      },
      querySelectorAll: (sel) => [],
      querySelector: (sel) => {
        return {
          classList: { add: ()=>{}, remove: ()=>{} }
        }
      },
      title: ''
    };
    const window = {
      addEventListener: ()=>{},
      scrollTo: ()=>{}
    };
    const location = { hash: '' };
    const setTimeout = ()=>{};
    const IntersectionObserver = class {
      observe(){}
      unobserve(){}
    };
  ` + js;
    
  try {
    eval(js);
    console.log('Runtime check passed!');
  } catch (e) {
    console.error('Runtime error:', e);
  }
}
