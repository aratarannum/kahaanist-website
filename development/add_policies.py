import re
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Contact Page
old_contact_match = re.search(r'<main id="page-contact".*?</main>', html, re.DOTALL)
if not old_contact_match:
    print("Could not find contact page")
    sys.exit(1)

new_contact = """<main id="page-contact" class="page">
  <div class="wrap contact-wrap" style="display:flex; justify-content:center; padding:80px 20px;">
    <div class="contact-info reveal" style="text-align:center;">
      <div class="eyebrow">GET IN TOUCH</div>
      <h1 style="margin-top:16px; font-size:clamp(30px,3.6vw,42px);">Tell us your story.</h1>
      
      <div class="info-block" style="margin-top:40px;">
        <div class="label" style="font-size:14px; letter-spacing:0.1em; color:var(--brass-light); text-transform:uppercase;">Email</div>
        <div class="val" style="font-size:20px; font-weight:400; color:var(--parchment); margin-top:8px;">connect@kahaanist.com</div>
      </div>
      
      <!-- TODO: Open a WhatsApp Business account and a dedicated phone number. Once active, update this section with those details. -->
    </div>
  </div>
</main>"""

html = html.replace(old_contact_match.group(0), new_contact)
print("Updated Contact Page")

# 2. Add Policy Pages right before <footer>
new_pages = """
<main id="page-privacy" class="page">
  <div class="wrap" style="max-width:800px; padding:80px 20px;">
    <h1 style="margin-bottom:30px;">Privacy Policy</h1>
    <div style="line-height:1.7; color:var(--parchment-dim);">
      <p>We respect your privacy. Kahaanist collects only the information necessary to process your order, communicate with you, and improve your shopping experience.</p>
      <p>Your payment information is securely processed by our payment gateways (Razorpay / PayPal / Shopify Payments). We do not store your credit card details.</p>
      <p>If you have any questions about how your data is handled, please reach out to us at connect@kahaanist.com.</p>
    </div>
  </div>
</main>

<main id="page-terms" class="page">
  <div class="wrap" style="max-width:800px; padding:80px 20px;">
    <h1 style="margin-bottom:30px;">Terms of Service</h1>
    <div style="line-height:1.7; color:var(--parchment-dim);">
      <p>By visiting our site and/or purchasing something from us, you engage in our "Service" and agree to be bound by the following terms and conditions.</p>
      <p>All our jewelry is handcrafted. Due to the artisanal nature of our products, slight variations in texture, color, and finish may occur. These are not defects but a hallmark of genuine hand-cast brass.</p>
      <p>Prices for our products are subject to change without notice.</p>
    </div>
  </div>
</main>

<main id="page-refund" class="page">
  <div class="wrap" style="max-width:800px; padding:80px 20px;">
    <h1 style="margin-bottom:30px;">Refund & Replacement Policy</h1>
    <div style="line-height:1.7; color:var(--parchment-dim);">
      <p>At Kahaanist, every piece is carefully handcrafted. Due to the personal nature of our jewelry and our commitment to hygiene and quality, <strong>all sales are final and products are non-returnable.</strong></p>
      <p><strong>Manufacturing Defects:</strong></p>
      <p>We take pride in our craftsmanship. However, if you receive a piece with a genuine manufacturing defect, we will gladly offer a replacement.</p>
      <ul style="margin-top:10px; margin-bottom:20px; padding-left:20px;">
        <li style="margin-bottom:8px;">You must contact customer care at connect@kahaanist.com within <strong>48 hours</strong> of receiving the package.</li>
        <li style="margin-bottom:8px;">Please include your order number, a brief description of the issue, and clear, unedited photographs showing the defect.</li>
        <li style="margin-bottom:8px;">Once our quality check team verifies the defect, we will initiate a free replacement for the exact same item.</li>
      </ul>
      <p><em>Please note that natural tarnishing of brass over time or minor textural variations inherent to the hand-casting process are not considered defects.</em></p>
    </div>
  </div>
</main>

<main id="page-shipping" class="page">
  <div class="wrap" style="max-width:800px; padding:80px 20px;">
    <h1 style="margin-bottom:30px;">Shipping Policy</h1>
    <div style="line-height:1.7; color:var(--parchment-dim);">
      <p><strong>Domestic (India):</strong><br>We offer <strong>Free Shipping</strong> across India on all orders above ₹2,899. For orders below this threshold, a standard shipping fee applies at checkout.</p>
      <p style="margin-top:20px;"><strong>International (Rest of the World):</strong><br>We offer <strong>Free International Shipping</strong> on all orders above US$65. For orders below this amount, international shipping rates will be calculated at checkout based on your location.</p>
      <p style="margin-top:20px;"><strong>Processing Time:</strong><br>All orders are processed and dispatched within 3-5 business days. Once shipped, you will receive a tracking link via email.</p>
    </div>
  </div>
</main>
"""

# Insert right before <footer>
html = html.replace('<footer>', new_pages + '\n<footer>')
print("Injected Policy Pages")

# 3. Update router function to handle the new pages
old_route = """    if(hash.startsWith('/product/')){
      document.getElementById('page-product').classList.add('active');"""

new_route = """    if(hash === '/privacy'){
      document.getElementById('page-privacy').classList.add('active');
    } else if(hash === '/terms'){
      document.getElementById('page-terms').classList.add('active');
    } else if(hash === '/refund'){
      document.getElementById('page-refund').classList.add('active');
    } else if(hash === '/shipping'){
      document.getElementById('page-shipping').classList.add('active');
    } else if(hash.startsWith('/product/')){
      document.getElementById('page-product').classList.add('active');"""

if old_route in html:
    html = html.replace(old_route, new_route)
    print("Updated router")
else:
    print("FAIL: Could not update router")
    sys.exit(1)

# 4. Update Footer Links
# Find Brand & Legal column
footer_legal_regex = re.compile(r'<div class="fcol">\s*<h5>Brand & Legal</h5>.*?</div>', re.DOTALL)
if not footer_legal_regex.search(html):
    print("FAIL: Could not find footer legal section")
    sys.exit(1)

new_footer_legal = """<div class="fcol">
        <h5>Brand & Legal</h5>
        <a href="#/">Home</a>
        <a href="#/contact">Contact / Story</a>
        <a href="#/privacy">Privacy Policy</a>
        <a href="#/terms">Terms of Service</a>
        <a href="#/refund">Refund Policy</a>
        <a href="#/shipping">Shipping Policy</a>
      </div>"""

html = footer_legal_regex.sub(new_footer_legal, html)
print("Updated Footer Links")

# Save
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("SUCCESS: index.html updated")
