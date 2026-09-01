# Global Headless Architecture Plan

## Current State
- **Frontend:** Single-page application (`index.html`) hosted on Cloudflare Pages.
- **Backend:** Shopify Buy Button SDK connected to a single Indian Shopify store (INR, Razorpay).
- **Design:** Custom gold/parchment theme, interactive video gallery thumbnails.

## Immediate Next Steps (The "Two-Brain" System)
1. **Wait for Merchant:** Await the new Storefront Access Token and the 5 USD Product IDs from the new `kahaanist-global.myshopify.com` Shopify account.
2. **Geo-IP Integration:** Inject a lightweight `fetch('https://ipapi.co/json/')` into `index.html` on load.
3. **Dynamic Routing:**
   - If `country_code === 'IN'`, instantiate `client_in`, render INR prices.
   - If `country_code !== 'IN'`, instantiate `client_us`, render USD prices.
4. **Inventory Sync:** Merchant will install "Syncio" or similar Shopify App to link the IN and US dashboards.

## Future Milestones
- **SEO Optimization:** Implement history API routing (instead of hash routing) if indexability becomes a priority.
- **Analytics:** Inject Meta Pixel and Google Analytics directly into the headless router.
