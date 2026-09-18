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

class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBSITE_DIR, **kwargs)

    def do_GET(self):
        # Clean path from query params or hashes
        clean_path = self.path.split('?')[0].split('#')[0]
        local_path = self.translate_path(clean_path)
        
        # If it's an existing file, serve it directly (CSS, JS, images, videos)
        if os.path.exists(local_path) and not os.path.isdir(local_path):
            return super().do_GET()
            
        # If path has a non-html file extension, let standard handler 404
        ext = os.path.splitext(clean_path)[1]
        if ext and ext not in ['.html']:
            return super().do_GET()
            
        # SPA Fallback: serve index.html for route paths like /shop, /product/medusa
        self.path = '/index.html'
        return super().do_GET()

    def log_message(self, format, *args):
        # Suppress noisy server log output during test run
        pass

def run_test():
    PORT = 8000
    
    # Allow socket reuse in case previous run left TIME_WAIT
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), SPAHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    print(f"Local SPA Server running at http://127.0.0.1:{PORT}")
    time.sleep(1)

    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    chrome_path = None
    for c in chrome_candidates:
        if os.path.exists(c):
            chrome_path = c
            break
            
    if not chrome_path:
        print("Error: Chrome executable not found on host machine.")
        httpd.shutdown()
        sys.exit(1)

    print(f"Using Chrome at: {chrome_path}")

    # Test 1: Direct navigation to /shop
    screenshot_shop = os.path.join(WEBSITE_DIR, "screenshot_shop.png")
    if os.path.exists(screenshot_shop):
        try: os.remove(screenshot_shop)
        except: pass

    cmd_shop = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1280,800",
        f"--screenshot={screenshot_shop}",
        "--dump-dom",
        f"http://127.0.0.1:{PORT}/shop"
    ]
    print("Navigating to http://127.0.0.1:8000/shop ...")
    res_shop = subprocess.run(cmd_shop, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    dom_shop = res_shop.stdout

    # Assertions for /shop
    assert 'id="page-shop" class="page active"' in dom_shop, "Assertion Failed: #page-shop is not active on /shop"
    assert 'class="product-card"' in dom_shop, "Assertion Failed: .product-card elements not found in /shop DOM"
    assert os.path.exists(screenshot_shop) and os.path.getsize(screenshot_shop) > 0, "Assertion Failed: screenshot_shop.png not generated"
    print("✅ TEST 1 PASSED: Navigated to http://localhost:8000/shop without hash, verified #page-shop.active, product cards rendered, and saved screenshot_shop.png.")

    # Test 2: Direct navigation to /product/medusa
    screenshot_medusa = os.path.join(WEBSITE_DIR, "screenshot_product_medusa.png")
    if os.path.exists(screenshot_medusa):
        try: os.remove(screenshot_medusa)
        except: pass

    cmd_medusa = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1280,800",
        f"--screenshot={screenshot_medusa}",
        "--dump-dom",
        f"http://127.0.0.1:{PORT}/product/medusa"
    ]
    print("Navigating to http://127.0.0.1:8000/product/medusa ...")
    res_medusa = subprocess.run(cmd_medusa, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    dom_medusa = res_medusa.stdout

    # Assertions for /product/medusa
    assert 'id="page-product" class="page active"' in dom_medusa, "Assertion Failed: #page-product is not active on /product/medusa"
    assert 'Medusa Earrings' in dom_medusa, "Assertion Failed: Medusa Earrings product details not found in DOM"
    assert os.path.exists(screenshot_medusa) and os.path.getsize(screenshot_medusa) > 0, "Assertion Failed: screenshot_product_medusa.png not generated"
    print("✅ TEST 2 PASSED: Navigated to http://localhost:8000/product/medusa, verified #page-product.active, Medusa Earrings details rendered, and saved screenshot_product_medusa.png.")

    httpd.shutdown()
    print("\n🎉 All headless routing and visual verification tests passed successfully!")

if __name__ == '__main__':
    run_test()
