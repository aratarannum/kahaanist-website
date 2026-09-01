# Fresh Ideas & Growth Sandbox

This document tracks potential features and marketing optimizations we can inject into the Headless architecture.

## 1. The "Lore" Expansion
Since the brand relies heavily on mythology ("Wearable Lore"), we should add an interactive `/lore` route to the single-page app. Clicking it opens a beautifully designed modal or page detailing the stories of Medusa, Ouroboros, and the Tree of Life, increasing time-on-site and perceived value.

## 2. Dynamic Upsells in the Cart
Instead of just a basic Shopify slide-out cart, we could intercept the "Add to Cart" click and show a custom modal: *"Pairs beautifully with the Medusa Ring."* Since we control the frontend, we can build custom bundling logic before it hits Shopify.

## 3. Localized Welcome Banners
Using the Geo-IP script we are building for the checkout, we can personalize the hero banner:
- US Visitor: "Handcrafted in India. Express Shipping to the United States."
- IN Visitor: "Handcrafted across India. Free Domestic Shipping."

## 4. WebGL/3D Render Previews
You have `.stl` and `.obj` CAD files in your `00-Archive` folder. We could integrate a lightweight Three.js viewer on the product pages, allowing users to spin the CAD models 360 degrees in their browser.
