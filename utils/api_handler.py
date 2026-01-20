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

#Function to enrich sales data
def enrich_sales_data(filtered_list, product_mapping):
    """
    Enrich sales transactions with API product metadata.
    """
    enriched_list = []
    print("\n[7/10] Enriching sales data...")
    for tx in filtered_list:
        # 1. Get ProductID using the exact key from Task 1
        pid = tx.get('ProductID')

        try:
            numeric_id = int(str(pid).replace('P', '').replace('p', ''))
        except:
            numeric_id = None

        # 2. Add API Fields
        if numeric_id in product_mapping:
            info = product_mapping[numeric_id]
            tx['API_Category'] = info.get('category', 'N/A')
            tx['API_Brand'] = info.get('brand', 'N/A')
            tx['API_Rating'] = info.get('rating', 0.0)
            tx['API_Match'] = True
        else:
            tx['API_Category'] = "N/A"
            tx['API_Brand'] = "N/A"
            tx['API_Rating'] = 0.0
            tx['API_Match'] = False

        enriched_list.append(tx)
    print(
        f"✓ Enriched {len(enriched_list)}/{len(filtered_list)} transactions.")
    return enriched_list

# ====================================================================================

# Helper function to save enriched data
def save_enriched_data(enriched_list, output_file='data/enriched_sales_data.txt'):
    """
    Save enriched transaction data to a text file.
    """
    print("\n[8/10] Saving enriched data...")
    # 1. Writing to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            headers = ["TransactionID", "Date", "ProductID", "ProductName",
                       "Quantity", "UnitPrice", "CustomerID", "Region",
                       "API_Category", "API_Brand", "API_Rating", "API_Match"]
            f.write("|".join(headers) + "\n")

            for item in enriched_list:
                row = [
                    str(item.get('TransactionID', 'N/A')),
                    str(item.get('Date', 'N/A')),
                    str(item.get('ProductID', 'N/A')),
                    str(item.get('ProductName', 'N/A')),
                    str(item.get('Quantity', 0)),
                    str(item.get('UnitPrice', 0.0)),
                    str(item.get('CustomerID', 'N/A')),
                    str(item.get('Region', 'N/A')),
                    str(item.get('API_Category')),
                    str(item.get('API_Brand')),
                    str(item.get('API_Rating')),
                    str(item.get('API_Match'))
                ]
                f.write("|".join(row) + "\n")

        print(
            f"✓ Success: {output_file} has been created with {len(enriched_list)} rows.")
    except Exception as e:
        print(f"✕ File writing failed: {e}")

    return enriched_list
