import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. New CSS
new_css = """
    /* Product Page CSS */
    .product-page-layout {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 60px;
      margin-top: 40px;
      margin-bottom: 80px;
    }
    .product-page-gallery {
      position: sticky;
      top: 100px;
    }
    .main-image {
      width: 100%;
      height: 600px;
      object-fit: cover;
      background: var(--ink-soft);
      border-radius: 4px;
      margin-bottom: 16px;
    }
    .thumbnails {
      display: flex;
      gap: 12px;
    }
    .thumb {
      width: 80px;
      height: 80px;
      object-fit: cover;
      background: var(--ink-soft);
      cursor: pointer;
      border: 1px solid transparent;
      border-radius: 2px;
      transition: 0.3s;
    }
    .thumb:hover { border-color: var(--brass-light); }
    .product-page-info h1 {
      font-size: 32px;
      margin-bottom: 8px;
    }
    .product-page-price {
      font-size: 24px;
      color: var(--brass-light);
      margin-bottom: 24px;
      font-weight: 500;
    }
    .product-buy-form {
      margin-bottom: 40px;
      padding-bottom: 30px;
      border-bottom: 1px solid var(--ink-soft);
    }
    .product-buy-form .btn {
      width: 100%;
      text-align: center;
      padding: 16px;
      font-size: 16px;
    }
    .product-story {
      margin-bottom: 40px;
      font-size: 17px;
      line-height: 1.6;
      color: var(--parchment);
    }
    .product-specs {
      margin-bottom: 40px;
    }
    .spec-item {
      padding: 16px 0;
      border-bottom: 1px solid var(--ink-soft);
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
    }
    .spec-item h4 {
      margin: 0;
      font-size: 15px;
      font-weight: 600;
      letter-spacing: 0.05em;
    }
    .spec-content {
      display: none;
      padding: 12px 0 16px 0;
      color: var(--parchment-dim);
      font-size: 15px;
      line-height: 1.5;
    }
    .spec-item.active + .spec-content {
      display: block;
    }
    @media (max-width: 900px){
      .product-page-layout { grid-template-columns: 1fr; gap: 40px; }
      .product-page-gallery { position: relative; top: 0; }
      .main-image { height: 400px; }
    }
"""
html = html.replace('</style>', new_css + '\n</style>')

# 2. New HTML
new_html = """
  <!-- ============ PRODUCT PAGE ============ -->
  <main id="page-product" class="page">
    <div class="wrap">
      <a href="#/shop" class="cta" style="display:inline-block; margin-top:20px; font-size:14px;">← Back to Shop</a>
      <div id="product-container"></div>
    </div>
  </main>

<footer>"""
html = html.replace('<footer>', new_html)

# 3. New JS Array & productCardHTML
new_js_products = """const products = [
    { slug:'tree-of-life-pendant', cat:'neckpieces', name:'Tree of Life Pendant Necklace', price:'₹2,899', quote:'Roots below, branches above — grounded and growing at once.', img:'tree-of-life-main.jpg', checkout:'https://your-shopify-store.myshopify.com/cart/12345', story: 'The Tree of Life is an ancient symbol found in mythologies from the Norse Yggdrasil to the Celtic Crann Bethadh. It represents the interconnectedness of everything in the universe. We cast this piece in solid brass to give you a wearable reminder to stay grounded in your roots while reaching for what is next.', materials: 'Solid Recycled Brass, 18K Gold Plated finish.', size: 'Pendant diameter: 25mm. Chain length: 18 inches with a 2-inch extender.', shipping: 'Free shipping across India. 7-day hassle-free replacement for any defects.' },
    { slug:'mermen-in-love', cat:'neckpieces', name:'Mermen in Love Pendant', price:'₹2,899', quote:'Eternal devotion beneath the waves.', img:'mermen-in-love.png', checkout:'https://your-shopify-store.myshopify.com/cart/12345', story: 'A celebration of love in all its forms. Inspired by ancient maritime legends of sirens and mermen, this piece represents a bond that survives the deepest waters and the strongest tides. Wear it as a token of unyielding devotion.', materials: 'Solid Recycled Brass, Hand-painted enamel details.', size: 'Pendant diameter: 30mm. Chain length: 20 inches.', shipping: 'Free shipping across India. 7-day hassle-free replacement.' },
    { slug:'medusa-brass-earrings', cat:'earrings', name:'Medusa Brass Earrings', price:'₹4,499', quote:'A gaze that stops time.', img:'medusa-earrings.jpg', checkout:'https://your-shopify-store.myshopify.com/cart/12345', story: 'Long misunderstood as a monster, Medusa was originally a protector and a symbol of female rage and power. Her visage was placed on shields and temples to ward off evil. We designed these earrings for the days you need to channel her fierce, unapologetic energy.', materials: 'Solid Recycled Brass. Hypoallergenic posts.', size: 'Drop length: 45mm. Width: 30mm.', shipping: 'Free shipping across India. 7-day hassle-free replacement.' },
    { slug:'mermaids-in-love-earrings', cat:'earrings', name:'Mermaids in Love Earrings', price:'₹2,899', quote:'A subtle nod to infinite romance.', checkout:'https://your-shopify-store.myshopify.com/cart/12345', story: 'Reflecting the gentle and protective nature of the ocean\\'s guardians, these earrings symbolize a quiet but infinite romance. Designed for those who carry the sea in their hearts.', materials: 'Solid Recycled Brass.', size: 'Drop length: 30mm.', shipping: 'Free shipping across India. 7-day hassle-free replacement.' },
    { slug:'tree-of-life-drop-earrings', cat:'earrings', name:'Tree of Life Drop Earrings', price:'₹2,899', quote:'Carry the whole tree with you.', checkout:'https://your-shopify-store.myshopify.com/cart/12345', story: 'Matching our signature pendant, these drop earrings frame the face with the grounding energy of the Tree of Life. They sway gently, reminding you of the balance between the earth and sky.', materials: 'Solid Recycled Brass. Hypoallergenic posts.', size: 'Drop length: 35mm.', shipping: 'Free shipping across India. 7-day hassle-free replacement.' },
    { slug:'ouroboros-band-ring', cat:'rings', name:'Ouroboros Band Ring', price:'₹2,899', quote:'A cycle you wear, not just believe in.', checkout:'https://your-shopify-store.myshopify.com/cart/12345', story: 'The Ouroboros—a serpent eating its own tail—is one of the oldest mystical symbols in the world. It represents eternity, the cycle of life and death, and constant recreation. This ring is cast to wrap continuously around your finger as a daily talisman of renewal.', materials: 'Solid Recycled Brass.', size: 'Available in US sizes 5 through 9.', shipping: 'Free shipping across India. 7-day hassle-free replacement.' },
    { slug:'medusa-signet-ring', cat:'rings', name:'Medusa Signet Ring', price:'₹2,899', quote:'Small enough for daily wear, sharp enough to notice.', checkout:'https://your-shopify-store.myshopify.com/cart/12345', story: 'A miniature shield for your hand. This signet carries the protective gaze of Medusa in a compact, everyday design. Perfect for stacking or wearing alone as a bold statement.', materials: 'Solid Recycled Brass.', size: 'Available in US sizes 5 through 9.', shipping: 'Free shipping across India. 7-day hassle-free replacement.' }
  ];

  const catLabel = { neckpieces:'Neckpiece', earrings:'Earring', rings:'Finger Ring' };

  function productCardHTML(p){
    const imageContent = p.img
      ? `<img src="${p.img}" alt="${p.name} — brass ${catLabel[p.cat].toLowerCase()} inspired by mythology" loading="lazy">`
      : `<svg viewBox="0 0 100 100" fill="none"><circle cx="50" cy="50" r="34" stroke="#d9ab5f" stroke-width="1.2"/><circle cx="50" cy="50" r="20" stroke="#efe6d3" stroke-opacity="0.5" stroke-width="1"/><path d="M50 16 L50 84 M16 50 L84 50" stroke="#2f4a3e" stroke-width="1"/></svg>`;
    
    return `
      <div class="product-card">
        <div class="product-flip">
          <div class="product-face product-front">
            <a href="#/product/${p.slug}" class="product-image" style="display:block; text-decoration:none;">
              ${imageContent}
            </a>
            <div class="product-info">
              <div class="cat">${catLabel[p.cat]}</div>
              <a href="#/product/${p.slug}" style="text-decoration:none; color:inherit;"><h4>${p.name}</h4></a>
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
  }"""
html = re.sub(r'const products = \[.*?function productCardHTML\(p\)\{.*?  \}', new_js_products, html, flags=re.DOTALL)

# 4. New JS Logic (renderProduct + router update)
new_js_logic = """
  function toggleSpec(el){
    el.classList.toggle('active');
  }

  function renderProductPage(slug){
    const p = products.find(x => x.slug === slug);
    if(!p) {
        location.hash = '/shop';
        return;
    }
    const container = document.getElementById('product-container');
    const imageContent = p.img
      ? `<img src="${p.img}" alt="${p.name}" class="main-image">`
      : `<div class="main-image" style="display:flex; align-items:center; justify-content:center; border:1px solid var(--ink-soft);"><svg viewBox="0 0 100 100" fill="none" width="100" height="100"><circle cx="50" cy="50" r="34" stroke="#d9ab5f" stroke-width="1.2"/></svg></div>`;
    
    container.innerHTML = `
      <div class="product-page-layout">
        <div class="product-page-gallery">
          ${imageContent}
          <div class="thumbnails">
            ${p.img ? `<img src="${p.img}" class="thumb">` : `<div class="thumb"></div>`}
            <div class="thumb" style="display:flex; align-items:center; justify-content:center; font-size:12px; color:var(--parchment-dim);">+ Video</div>
            <div class="thumb" style="display:flex; align-items:center; justify-content:center; font-size:12px; color:var(--parchment-dim);">+ Angle</div>
          </div>
        </div>
        <div class="product-page-info">
          <div class="cat" style="margin-bottom:8px;">${catLabel[p.cat]}</div>
          <h1>${p.name}</h1>
          <div class="product-page-price">${p.price}</div>
          
          <div class="product-buy-form">
            <a href="${p.checkout || '#'}" target="_blank" class="btn btn-primary">Buy Now — Checkout via Shopify</a>
            <div style="font-size:13px; color:var(--parchment-dim); text-align:center; margin-top:12px;">Secure checkout. Free shipping across India.</div>
          </div>

          <div class="product-story">
            <strong style="color:var(--brass-light); display:block; margin-bottom:12px;">The Myth</strong>
            ${p.story || p.quote}
          </div>

          <div class="product-specs">
            <div class="spec-item" onclick="toggleSpec(this)">
              <h4>Material & Craftsmanship</h4>
              <span style="font-size:20px; color:var(--brass-light);">+</span>
            </div>
            <div class="spec-content">${p.materials || 'Solid brass. Handcrafted in India.'}</div>
            
            <div class="spec-item" onclick="toggleSpec(this)">
              <h4>Size & Fit</h4>
              <span style="font-size:20px; color:var(--brass-light);">+</span>
            </div>
            <div class="spec-content">${p.size || 'One size fits most.'}</div>
            
            <div class="spec-item" onclick="toggleSpec(this)">
              <h4>Shipping & Returns</h4>
              <span style="font-size:20px; color:var(--brass-light);">+</span>
            </div>
            <div class="spec-content">${p.shipping || 'Free shipping across India. 7-day hassle-free replacement policy.'}</div>
          </div>

          <div style="margin-top:60px; padding-top:40px; border-top:1px solid var(--ink-soft);">
            <h4 style="margin-bottom:20px; color:var(--brass-light);">Seen On</h4>
            <div style="display:flex; gap:12px; overflow-x:auto; padding-bottom:12px;">
                <div style="width:120px; height:150px; background:var(--ink-soft); flex-shrink:0; border-radius:4px; display:flex; align-items:center; justify-content:center; color:var(--parchment-dim); font-size:12px; text-align:center;">Community<br>Photo 1</div>
                <div style="width:120px; height:150px; background:var(--ink-soft); flex-shrink:0; border-radius:4px; display:flex; align-items:center; justify-content:center; color:var(--parchment-dim); font-size:12px; text-align:center;">Community<br>Photo 2</div>
                <div style="width:120px; height:150px; background:var(--ink-soft); flex-shrink:0; border-radius:4px; display:flex; align-items:center; justify-content:center; color:var(--parchment-dim); font-size:12px; text-align:center;">Community<br>Photo 3</div>
            </div>
          </div>

        </div>
      </div>
    `;
    document.title = p.name + " | Kahaanist";
    window.scrollTo(0,0);
  }

  function route(){
    let hash = location.hash.replace('#','') || '/';
    document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
    document.querySelectorAll('.navlinks a').forEach(a=>a.classList.remove('active'));

    if(hash.startsWith('/product/')){
      document.getElementById('page-product').classList.add('active');
      const slug = hash.replace('/product/', '');
      renderProductPage(slug);
    } else if(hash.startsWith('/shop')){
"""
html = html.replace('function route(){', new_js_logic)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
