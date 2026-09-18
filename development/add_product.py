import os
import webbrowser

INDEX_FILE = os.path.join(os.path.dirname(__file__), 'index.html')

def main():
    print("=== Add New Kahaanist Jewelry Design ===")
    cat = input("Category (neckpieces, earrings, rings): ").strip()
    name = input("Product Name: ").strip()
    price = input("Price (e.g. ₹1,500): ").strip()
    quote = input("Quote / Description: ").strip()
    img = input("Image filename (e.g. new-ring.jpg): ").strip()
    checkout = input("Shopify Checkout Link (URL): ").strip()

    new_product = f"""
    {{ 
      cat: '{cat}', 
      name: '{name}', 
      price: '{price}', 
      quote: '{quote}', 
      img: '{img}',
      checkout: '{checkout}'
    }},"""

    # Read from index.html
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    target = "const products = ["
    if target in html:
        parts = html.split(target, 1)
        # Insert the new product right after the array opening
        new_html = parts[0] + target + new_product + parts[1]
        
        # Save to index.html
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"\nSuccess! The new design was added.")
        print(f"Saved to: {INDEX_FILE}")
        print("Opening in your web browser...")
        
        # Open in default browser
        webbrowser.open('file://' + INDEX_FILE.replace('\\', '/'))
    else:
        print("Error: Could not find 'const products = [' in the HTML file.")

    input("\nPress Enter to close this window...")

if __name__ == "__main__":
    main()
