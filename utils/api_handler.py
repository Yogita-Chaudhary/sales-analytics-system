import requests

#Function to fetch all products from DummyJSON with limit 100
def fetch_all_products():
    """
    Fetches all products from DummyJSON API and returns only required fields.
    """
    url = "https://dummyjson.com/products?limit=100"
    print("\n[6/10] Fetching product data from API...")
    try:
        # 1. STEP: Make the GET request
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            raw_products = data.get('products', [])
            # 2. STEP: Clean the API data to match the "Expected Output Format"
            cleaned_products = []
            for p in raw_products:
                formatted_product = {
                    'id': p.get('id'),
                    'title': p.get('title'),
                    'category': p.get('category'),
                    'brand': p.get('brand'),
                    'price': p.get('price'),
                    'rating': p.get('rating')
                }
                cleaned_products.append(formatted_product)
            print(
                f"✓ Success: Fetched and formatted {len(cleaned_products)} products.")
            return cleaned_products
        else:
            print(f"✕ API Error: Status {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"✕ Connection Error: {e}")
        return []

# ====================================================================================

#Function for product mapping
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.
    """
    # 1. STEP: Initialize an empty dictionary
    mapping = {}
    for item in api_products:
        # 2. STEP: Get the ID and ensure it is an integer
        product_id = item['id']
        # 3. STEP: Create the 'Value' dictionary with only the required fields
        product_info = {
            'title': item.get('title'),
            'category': item.get('category'),
            'brand': item.get('brand'),
            'rating': item.get('rating')
        }
        # 4. STEP: Assign the info to that specific ID key
        mapping[product_id] = product_info
    return mapping

# ====================================================================================

