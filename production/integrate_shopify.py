import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the products array to use shopifyId instead of checkout URL
html = re.sub(
    r"checkout:'https://your-shopify-store\.myshopify\.com/cart/12345'",
    r"shopifyId: ''",
    html
)
# Inject the specific ID for Tree of Life
html = html.replace(
    r"slug:'tree-of-life-pendant', cat:'neckpieces', name:'Tree of Life Pendant Necklace', price:'₹2,899', quote:'Roots below, branches above — grounded and growing at once.', img:'tree-of-life-main.jpg', shopifyId: ''",
    r"slug:'tree-of-life-pendant', cat:'neckpieces', name:'Tree of Life Pendant Necklace', price:'₹2,899', quote:'Roots below, branches above — grounded and growing at once.', img:'tree-of-life-main.jpg', shopifyId: '8733191569591'"
)


# 2. Add Shopify UI Initialization to the top of the script
shopify_init_code = """
  // ---------- Shopify Integration ----------
  let shopifyUI;
  const scriptURL = 'https://sdks.shopifycdn.com/buy-button/latest/buy-button-storefront.min.js';
  const script = document.createElement('script');
  script.async = true;
  script.src = scriptURL;
  document.head.appendChild(script);
  script.onload = () => {
    const client = ShopifyBuy.buildClient({
      domain: '13e62n-fw.myshopify.com',
      storefrontAccessToken: 'a644d9e6d80b87611a5f4c9cf0199a5d',
    });
    ShopifyBuy.UI.onReady(client).then((ui) => {
      shopifyUI = ui;
      renderShopifyButtons();
    });
  };

  const shopifyOptions = {
    moneyFormat: 'Rs.%20%7B%7Bamount%7D%7D',
    options: {
      product: {
        contents: { img: false, title: false, price: false },
        text: { button: 'Add to Cart' },
        styles: {
          product: { '@media (min-width: 601px)': { 'max-width': '100%', 'margin': '0' } },
          button: {
            'background-color': '#b8863b',
            'color': '#fff',
            'font-family': 'sans-serif',
            'border-radius': '2px',
            'width': '100%'
          }
        }
      },
      cart: { text: { total: 'Subtotal', button: 'Checkout' } }
    }
  };

  function renderShopifyButtons() {
    if (!shopifyUI) return;
    document.querySelectorAll('.shopify-buy-container:not(.rendered)').forEach(node => {
      const id = node.dataset.shopifyId;
      if (id) {
        node.classList.add('rendered');
        shopifyUI.createComponent('product', {
          id: id,
          node: node,
          moneyFormat: shopifyOptions.moneyFormat,
          options: shopifyOptions.options
        });
      }
    });
  }
"""
html = html.replace('// ---------- Product data ----------', shopify_init_code + '\n  // ---------- Product data ----------')


# 3. Update productCardHTML (Grid View)
old_card_cta = """              ${p.checkout 
                ? `<a href="${p.checkout}" target="_blank" class="cta" style="display:inline-block; border:1px solid var(--brass-light); padding:8px 16px; margin-top:12px; border-radius:2px;">Buy Now →</a>` 
                : ``
              }"""
new_card_cta = """              ${p.shopifyId 
                ? `<div class="shopify-buy-container" data-shopify-id="${p.shopifyId}" style="margin-top:12px;"></div>` 
                : `<div class="cta" style="margin-top:12px; color:var(--parchment-dim);">Coming Soon</div>`
              }"""
html = html.replace(old_card_cta, new_card_cta)


# 4. Update renderProductPage (Product View)
old_page_cta = """          <div class="product-buy-form">
            <a href="${p.checkout || '#'}" target="_blank" class="btn btn-primary">Buy Now — Checkout via Shopify</a>
            <div style="font-size:13px; color:var(--parchment-dim); text-align:center; margin-top:12px;">Secure checkout. Free shipping across India.</div>
          </div>"""
new_page_cta = """          <div class="product-buy-form">
            ${p.shopifyId 
                ? `<div class="shopify-buy-container" data-shopify-id="${p.shopifyId}"></div>` 
                : `<div class="btn btn-primary" style="opacity:0.5; cursor:not-allowed;">Product currently unavailable</div>`
            }
            <div style="font-size:13px; color:var(--parchment-dim); text-align:center; margin-top:12px;">Secure checkout. Free shipping across India.</div>
          </div>"""
html = html.replace(old_page_cta, new_page_cta)


# 5. Make sure renderShopifyButtons is called on route change
html = html.replace('renderShop(filter);', 'renderShop(filter);\n      setTimeout(renderShopifyButtons, 100);')
html = html.replace('renderProductPage(slug);', 'renderProductPage(slug);\n      setTimeout(renderShopifyButtons, 100);')


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
