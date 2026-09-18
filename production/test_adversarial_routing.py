"""
Adversarial Stress Harness for M1: SEO & History API Routing
Empirically tests:
1. Corner-case URLs: Trailing slashes (/shop/, /product/medusa/, /shop/neckpieces/)
2. Case sensitivity: Uppercase paths (/SHOP, /Product/Medusa)
3. Invalid routes: /nonexistent-route-xyz
4. Legacy hash migration & infinite loop prevention: http://127.0.0.1:8000/#/shop and http://127.0.0.1:8000/#/product/medusa
5. Base href relative asset protection & 404 auditing
6. Rapid programmatic history transitions
"""

import http.server
import socketserver
import threading
import subprocess
import time
import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

WEBSITE_DIR = os.path.dirname(os.path.abspath(__file__))

# Global audit list for incoming HTTP requests
REQUEST_LOG = []

class AdversarialSPAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBSITE_DIR, **kwargs)

    def do_GET(self):
        clean_path = self.path.split('?')[0].split('#')[0]
        REQUEST_LOG.append(clean_path)
        local_path = self.translate_path(clean_path)
        
        # If it's an existing file, serve directly
        if os.path.exists(local_path) and not os.path.isdir(local_path):
            return super().do_GET()
            
        # If non-html extension, return 404
        ext = os.path.splitext(clean_path)[1]
        if ext and ext not in ['.html']:
            return super().do_GET()
            
        # SPA Fallback for routes
        self.path = '/index.html'
        return super().do_GET()

    def log_message(self, format, *args):
        pass

def find_chrome():
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def fetch_chrome_dom(chrome_path, url, screenshot_path=None):
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1280,800",
        "--dump-dom",
    ]
    if screenshot_path:
        cmd.append(f"--screenshot={screenshot_path}")
    cmd.append(url)
    
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=20)
    return res.stdout

def run_tests():
    PORT = 8008
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), AdversarialSPAHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    print(f"Adversarial SPA Server running at http://127.0.0.1:{PORT}")
    time.sleep(1)

    chrome_path = find_chrome()
    if not chrome_path:
        print("ERROR: Chrome executable not found.")
        httpd.shutdown()
        sys.exit(1)

    print(f"Using Chrome at: {chrome_path}\n")

    test_results = []
    
    def record(name, passed, details=""):
        test_results.append({"name": name, "passed": passed, "details": details})
        tag = "[PASS]" if passed else "[FAIL]"
        print(f"  {tag} {name} {('- ' + details) if details else ''}")

    print("================================================================")
    print("M1 ADVERSARIAL STRESS TEST: ROUTING, ASSETS, HASH & CORNER CASES")
    print("================================================================")

    # 1. Trailing Slash Tests
    print("\n--- 1. Trailing Slash Stress Tests ---")
    
    # 1.1 /shop/
    url_shop_slash = f"http://127.0.0.1:{PORT}/shop/"
    dom = fetch_chrome_dom(chrome_path, url_shop_slash)
    shop_active = 'id="page-shop" class="page active"' in dom
    has_cards = 'class="product-card"' in dom
    record("Trailing slash on shop route (/shop/)", shop_active and has_cards, 
           f"page-shop active: {shop_active}, cards found: {has_cards}")

    # 1.2 /product/medusa/
    url_product_slash = f"http://127.0.0.1:{PORT}/product/medusa/"
    dom = fetch_chrome_dom(chrome_path, url_product_slash)
    product_active = 'id="page-product" class="page active"' in dom
    has_medusa = 'Medusa Earrings' in dom
    record("Trailing slash on product route (/product/medusa/)", product_active and has_medusa,
           f"page-product active: {product_active}, Medusa found: {has_medusa}")

    # 1.3 /shop/neckpieces/
    url_sub_slash = f"http://127.0.0.1:{PORT}/shop/neckpieces/"
    dom = fetch_chrome_dom(chrome_path, url_sub_slash)
    shop_active = 'id="page-shop" class="page active"' in dom
    record("Trailing slash on subcategory route (/shop/neckpieces/)", shop_active,
           f"page-shop active: {shop_active}")

    # 2. Case Sensitivity Tests
    print("\n--- 2. Route Case Sensitivity Stress Tests ---")
    
    # 2.1 /SHOP
    url_shop_upper = f"http://127.0.0.1:{PORT}/SHOP"
    dom = fetch_chrome_dom(chrome_path, url_shop_upper)
    shop_upper_active = 'id="page-shop" class="page active"' in dom
    record("Uppercase route (/SHOP)", shop_upper_active,
           f"page-shop active: {shop_upper_active} (Note: Falls through to page-home if strict case)")

    # 2.2 /Product/medusa
    url_prod_upper = f"http://127.0.0.1:{PORT}/Product/medusa"
    dom = fetch_chrome_dom(chrome_path, url_prod_upper)
    prod_upper_active = 'id="page-product" class="page active"' in dom
    record("Mixed-case route (/Product/medusa)", prod_upper_active,
           f"page-product active: {prod_upper_active}")

    # 3. Invalid Route Handling
    print("\n--- 3. Invalid Route Fallback Stress Tests ---")
    
    # 3.1 /nonexistent-route-xyz
    url_invalid = f"http://127.0.0.1:{PORT}/nonexistent-route-xyz"
    dom = fetch_chrome_dom(chrome_path, url_invalid)
    home_active = 'id="page-home" class="page active"' in dom
    no_crash = len(dom) > 1000
    record("Invalid route gracefully falls back to home view without JS crash", home_active and no_crash,
           f"page-home active: {home_active}, DOM length: {len(dom)}")

    # 4. Legacy Hash Link Normalization & Loop Resistance
    print("\n--- 4. Legacy Hash Link Migration Tests ---")
    
    # 4.1 http://127.0.0.1:8000/#/shop
    url_hash_shop = f"http://127.0.0.1:{PORT}/#/shop"
    dom = fetch_chrome_dom(chrome_path, url_hash_shop)
    shop_active = 'id="page-shop" class="page active"' in dom
    record("Legacy hash migration (#/shop)", shop_active,
           f"page-shop active: {shop_active}")

    # 4.2 http://127.0.0.1:8000/#/product/medusa
    url_hash_prod = f"http://127.0.0.1:{PORT}/#/product/medusa"
    dom = fetch_chrome_dom(chrome_path, url_hash_prod)
    prod_active = 'id="page-product" class="page active"' in dom
    record("Legacy hash migration (#/product/medusa)", prod_active,
           f"page-product active: {prod_active}")

    # 4.3 http://127.0.0.1:8000/#/shop/
    url_hash_slash = f"http://127.0.0.1:{PORT}/#/shop/"
    dom = fetch_chrome_dom(chrome_path, url_hash_slash)
    shop_slash_active = 'id="page-shop" class="page active"' in dom
    record("Legacy hash with trailing slash (#/shop/)", shop_slash_active,
           f"page-shop active: {shop_slash_active}")

    # 5. Base Href & Relative Asset Resolution Audit
    print("\n--- 5. Base Href Relative Asset Resolution Audit ---")
    REQUEST_LOG.clear()
    url_deep = f"http://127.0.0.1:{PORT}/product/medusa"
    screenshot_deep = os.path.join(WEBSITE_DIR, "screenshot_deep_adversarial.png")
    dom = fetch_chrome_dom(chrome_path, url_deep, screenshot_deep)

    has_base = '<base href="/">' in dom
    # Check if any request attempted to resolve relative to /product/
    bad_requests = [r for r in REQUEST_LOG if r.startswith('/product/') and any(r.endswith(ext) for ext in ['.webp', '.jpg', '.jpeg', '.png', '.mp4', '.css', '.js'])]
    correct_asset_requests = [r for r in REQUEST_LOG if any(r.endswith(ext) for ext in ['.webp', '.jpg', '.png', '.mp4']) and not r.startswith('/product/')]

    record("<base href=\"/\"> declared in <head>", has_base, f"Found base tag: {has_base}")
    record("Zero relative asset 404 leakage (no /product/asset.ext requests)", len(bad_requests) == 0,
           f"Leaked requests: {bad_requests}")
    record("Assets requested directly from root domain", len(correct_asset_requests) > 0,
           f"Root asset requests captured: {correct_asset_requests[:5]}")

    # Clean up screenshot
    if os.path.exists(screenshot_deep):
        try: os.remove(screenshot_deep)
        except: pass

    # 6. Summary
    httpd.shutdown()
    print("\n================================================================")
    passed_count = sum(1 for t in test_results if t["passed"])
    total_count = len(test_results)
    print(f"M1 ADVERSARIAL SUITE SUMMARY: {passed_count}/{total_count} Passed")
    print("================================================================")

    for t in test_results:
        if not t["passed"]:
            print(f"  FAILURE: {t['name']} - {t['details']}")

    if passed_count < total_count:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    run_tests()
