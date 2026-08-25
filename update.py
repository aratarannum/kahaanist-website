import re
with open('Website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_products = '''const products = [
    { cat:'neckpieces', name:'Tree of Life Pendant Necklace', price:'₹2,899', quote:'Roots below, branches above — grounded and growing at once.', img:'tree-of-life-main.jpg', checkout:'https://your-shopify-store.myshopify.com/cart/12345' },
    { cat:'neckpieces', name:'Mermen in Love Pendant', price:'₹2,899', quote:'Eternal devotion beneath the waves.', img:'mermen-in-love.png', checkout:'https://your-shopify-store.myshopify.com/cart/12345' },
    { cat:'earrings', name:'Medusa Brass Earrings', price:'₹4,499', quote:'A gaze that stops time.', img:'medusa-earrings.jpg', checkout:'https://your-shopify-store.myshopify.com/cart/12345' },
    { cat:'earrings', name:'Mermaids in Love Earrings', price:'₹2,899', quote:'A subtle nod to infinite romance.', checkout:'https://your-shopify-store.myshopify.com/cart/12345' },
    { cat:'earrings', name:'Tree of Life Drop Earrings', price:'₹2,899', quote:'Carry the whole tree with you.', checkout:'https://your-shopify-store.myshopify.com/cart/12345' },
    { cat:'rings', name:'Ouroboros Band Ring', price:'₹2,899', quote:'A cycle you wear, not just believe in.', checkout:'https://your-shopify-store.myshopify.com/cart/12345' },
    { cat:'rings', name:'Medusa Signet Ring', price:'₹2,899', quote:'Small enough for daily wear, sharp enough to notice.', checkout:'https://your-shopify-store.myshopify.com/cart/12345' }
  ];'''

html = re.sub(r'const products = \[.*?\];', new_products, html, flags=re.DOTALL)

new_card_html = '''  function productCardHTML(p){
    const imageContent = p.img
      ? `<img src="${p.img}" alt="${p.name} — brass ${catLabel[p.cat].toLowerCase()} inspired by mythology" loading="lazy">`
      : `<svg viewBox="0 0 100 100" fill="none">
                <circle cx="50" cy="50" r="34" stroke="#d9ab5f" stroke-width="1.2"/>
                <circle cx="50" cy="50" r="20" stroke="#efe6d3" stroke-opacity="0.5" stroke-width="1"/>
                <path d="M50 16 L50 84 M16 50 L84 50" stroke="#2f4a3e" stroke-width="1"/>
              </svg>`;
    return `
      <div class="product-card">
        <div class="product-flip">
          <div class="product-face product-front">
            <div class="product-image">
              ${imageContent}
            </div>
            <div class="product-info">
              <div class="cat">${catLabel[p.cat]}</div>
              <h4>${p.name}</h4>
              <div class="price">${p.price}</div>
              ${p.checkout 
                ? `<a href="${p.checkout}" target="_blank" class="cta" style="display:inline-block; border:1px solid var(--brass-light); padding:8px 16px; margin-top:12px; border-radius:2px;">Buy Now →</a>` 
                : ``
              }
            </div>
          </div>
          <div class="product-face product-back">
            <div class="quote">"${p.quote}"</div>
          </div>
        </div>
      </div>`;
  }'''

html = re.sub(r'  function productCardHTML\(p\)\{.*?  \}', new_card_html, html, flags=re.DOTALL)

with open('Website/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
