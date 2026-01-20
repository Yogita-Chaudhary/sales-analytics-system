from collections import defaultdict

# Calculate Total Revenue
def calculate_total_revenue(transactions):
    total_revenue = 0.0
    for tx in transactions:
        total_revenue += (tx['Quantity'] * tx['UnitPrice'])
    return round(total_revenue, 2)


# Region-wise sales analysis
def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """
    # 1. Calculate Total Revenue first for percentage math
    overall_total = calculate_total_revenue(transactions)
    # 2. Use a plain dictionary to store results
    region_stats = {}
    for tx in transactions:
        region = tx['Region']
        revenue = tx['Quantity'] * tx['UnitPrice']
        if region not in region_stats:
            region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}
        region_stats[region]['total_sales'] += revenue
        region_stats[region]['transaction_count'] += 1
    # 3. Calculate percentages
    for region in region_stats:
        sales = region_stats[region]['total_sales']
        percent = (sales / overall_total) * 100
        region_stats[region]['percentage'] = round(percent, 2)
    # 4. Sort by total_sales descending
    sorted_regions = sorted(region_stats.items(),
                            key=lambda item: item[1]['total_sales'],
                            reverse=True)
    return dict(sorted_regions)


# Top selling products
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    """
    # 1. Create a dictionary to store totals for each product
    product_totals = {}
    for tx in transactions:
        name = tx['ProductName']
        qty = tx['Quantity']
        revenue = tx['Quantity'] * tx['UnitPrice']
        if name not in product_totals:
            product_totals[name] = {'total_qty': 0, 'total_revenue': 0.0}
        product_totals[name]['total_qty'] += qty
        product_totals[name]['total_revenue'] += revenue
    # 2. Convert dictionary to a list of tuples for sorting
    product_list = []
    for name, data in product_totals.items():
        product_list.append((name, data['total_qty'], data['total_revenue']))
    # 3. Sort by TotalQuantity (the middle item in the tuple) in descending order
    sorted_products = sorted(product_list, key=lambda x: x[1], reverse=True)
    # 4. Return only the top 'n' items
    return sorted_products[:n]


# Customer purchase Analysis
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    """
    customer_stats = {}
    for tx in transactions:
        c_id = tx['CustomerID']
        spent = tx['Quantity'] * tx['UnitPrice']
        product = tx['ProductName']
        if c_id not in customer_stats:
            customer_stats[c_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': []
            }
        customer_stats[c_id]['total_spent'] += spent
        customer_stats[c_id]['purchase_count'] += 1
        # Only add product if it's not already in their list (Requirement: Unique products)
        if product not in customer_stats[c_id]['products_bought']:
            customer_stats[c_id]['products_bought'].append(product)
    # Calculate Average Order Value and Sort
    for c_id in customer_stats:
        stats = customer_stats[c_id]
        stats['avg_order_value'] = round(
            stats['total_spent'] / stats['purchase_count'], 2)

    # Sort by total_spent descending
    sorted_customers = sorted(customer_stats.items(),
                              key=lambda x: x[1]['total_spent'],
                              reverse=True)
    return dict(sorted_customers)


# Daily Sales Trend
def daily_sales_trend(transactions):
    """
    Groups sales by date to see revenue and customer activity.
    """
    # 1. Create a dictionary to hold daily data
    daily_data = {}
    for tx in transactions:
        date = tx['Date']
        revenue = tx['Quantity'] * tx['UnitPrice']
        customer = tx['CustomerID']
        # 2. STEP: Initialize the date if it's the first time we see it
        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()  # Using a set to automatically keep only unique names
            }
        # 3. STEP: Accumulate the values
        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(customer)
    # 4. STEP: Finalize the data (Convert customer set to a count)
    final_trend = {}
    # Sort by date string (e.g., '2024-12-01' comes before '2024-12-02')
    for date in sorted(daily_data.keys()):
        data = daily_data[date]
        final_trend[date] = {
            'revenue': round(data['revenue'], 2),
            'transaction_count': data['transaction_count'],
            # Count the unique IDs in our set
            'unique_customers': len(data['customers'])
        }
    return final_trend


# Find peak Sales Day
def find_peak_sales_day(transactions):
    """
    Identifies the date with the highest revenue.
    """
    # 1. STEP: Get the daily trends first
    trend = daily_sales_trend(transactions)
    if not trend:
        return None
    peak_date = ""
    max_revenue = -1.0
    tx_count = 0
    # 2. STEP: Loop through each day to find the highest revenue
    for date, metrics in trend.items():
        if metrics['revenue'] > max_revenue:
            max_revenue = metrics['revenue']
            peak_date = date
            tx_count = metrics['transaction_count']
    # 3. STEP: Return as a tuple: (Date, Revenue, Count)
    return (peak_date, max_revenue, tx_count)


# Low Performing Products
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with total quantity sold less than the threshold.
    """
    # 1. STEP: Create a dictionary to count totals for every product
    product_totals = {}
    for tx in transactions:
        name = tx['ProductName']
        quantity = tx['Quantity']
        revenue = tx['Quantity'] * tx['UnitPrice']
        # 2. STEP: Aggregate data (Group by product name)
        if name not in product_totals:
            product_totals[name] = {'total_qty': 0, 'total_rev': 0.0}
        product_totals[name]['total_qty'] += quantity
        product_totals[name]['total_rev'] += revenue
    # 3. STEP: Filter for "Low Sellers"
    low_performers = []
    for name, data in product_totals.items():
        if data['total_qty'] < threshold:
            low_performers.append((name, data['total_qty'], data['total_rev']))
    # 4. STEP: Sort the final list by Quantity (ascending - lowest first)
    # x[1] refers to the TotalQty in our tuple
    low_performers.sort(key=lambda x: x[1])
    return low_performers


ANALYTICS_RESULTS = {}

def run_analytics(transactions, top_n=5, low_threshold=10):
    """
    Run all analytics and store results in the global ANALYTICS_RESULTS.
    Returns the same dict for convenience.
    """
    print("\n[5/10] Performing analytical calculations...")
    ANALYTICS_RESULTS.clear()

    ANALYTICS_RESULTS["total_revenue"] = calculate_total_revenue(transactions)
    ANALYTICS_RESULTS["region_wise_performance"] = region_wise_sales(
        transactions)
    ANALYTICS_RESULTS["top_selling_products"] = top_selling_products(
        transactions, n=top_n)
    ANALYTICS_RESULTS["top_customers"] = customer_analysis(transactions)
    ANALYTICS_RESULTS["daily_sales_trend"] = daily_sales_trend(transactions)
    ANALYTICS_RESULTS["peak_sales_day"] = find_peak_sales_day(transactions)
    ANALYTICS_RESULTS["low_performers"] = low_performing_products(
        transactions, threshold=low_threshold
    )
    print("✓ Analysis complete")
    return ANALYTICS_RESULTS
