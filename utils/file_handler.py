from .data_processor import ANALYTICS_RESULTS
from datetime import datetime
import os

def read_sales_data(filename):
    """
    Read raw sales transactions from a text file using common encodings.
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    print("\n[1/10] Reading sales data...")
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                lines = f.readlines()
                cleaned_lines = [
                    line.strip() for line in lines[1:] if line.strip()
                ]
                print(
                    f"✓ Successfully read {len(cleaned_lines)} transactions")
                return cleaned_lines
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings (utf-8, latin-1, cp1252).")
    return []

# ========================================================================

#  Function that parse the raw data and handle data quality issues.
def parse_transactions(raw_lines):
    """
    Parse raw transaction lines into structured dictionaries.
    """
    parsed_data = []
    print("\n[2/10] Parsing data...")
    for line in raw_lines:
        # 1. Split by pipe delimiter '|'
        parts = line.split('|')
        # 2. Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue
        try:
            # 3. Handle commas within ProductName
            product_name = parts[3].replace(',', ' ')
            # 4. Remove commas from numeric fields and convert to proper types
            qty_raw = parts[4].replace(',', '')
            price_raw = parts[5].replace(',', '')
            # 5. Convert types
            quantity = int(qty_raw)
            unit_price = float(price_raw)
            # Create the dictionary for this transaction
            transaction = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': product_name.strip(),
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }

            parsed_data.append(transaction)

        except (ValueError, TypeError):
            continue
    print(f"✓ Parsed {len(parsed_data)} records")
    return parsed_data

# ========================================================================

#Function to validate data
def validate_data(transactions):
    """
    Validate parsed transactions and remove invalid records.
    """
    valid_transactions = []
    invalid_count = 0
    total_input = len(transactions)
    for tx in transactions:
        missing_data = (tx['CustomerID'] == '' or tx['Region'] == '')
        incorrect_number = tx['Quantity'] <= 0 or tx['UnitPrice'] <= 0
        incorrect_ID = not (tx['TransactionID'].startswith('T') and
                            tx['ProductID'].startswith('P') and
                            tx['CustomerID'].startswith('C'))
        if missing_data or incorrect_number or incorrect_ID:
            invalid_count += 1
        else:
            valid_transactions.append(tx)
    return valid_transactions, total_input, invalid_count

#Function to display filter
def display_filter_options(transactions):
    """
    Display available filter options and collect filter inputs from the user.
    """
    available_regions = sorted(
        list(set(t['Region'] for t in transactions)))
    amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
    print("\n[3/10] Filter Options Available:")
    print(f"Available Regions: {', '.join(available_regions)}")
    if amounts:
        print(
            f"Transaction Amount Range: Min: {min(amounts):.2f}, Max: {max(amounts):.2f}")
    is_filter_valid = False
    yes_values = ['y', 'yes']
    no_values = ['n', 'no']
    while not is_filter_valid:
        want_filter = input(
            "Do you want to filter data? (y/n): ").lower().strip()
        if want_filter in yes_values + no_values:
            is_filter_valid = True
        else:
            print('Give a valid input')

    region = None
    min_amount = None
    max_amount = None

    if want_filter in yes_values:
        is_valid = False

        while not is_valid:
            user_region = input("Enter Region (or leave blank): ").strip()
            if user_region == "":
                is_valid = True
            elif user_region != "" and user_region.isalpha() and user_region.title() in available_regions:
                is_valid = True
                region = user_region.title()
            else:
                print("Region should be from the list of available regions.")

        is_valid = False
        while not is_valid:
            user_min = input("Enter Minimum Amount (or leave blank): ").strip()
            if user_min == "":
                is_valid = True
            elif user_min != "" and user_min.isnumeric() and float(user_min) >= 0:
                is_valid = True
                min_amount = float(user_min)
            else:
                print("Minimum amount should be numeric and greater than 0.")
        is_valid = False
        while not is_valid:
            user_max = input("Enter Maximum Amount (or leave blank): ").strip()
            if user_max == "":
                is_valid = True
            elif user_max != "" and user_max.isnumeric() and float(user_max) > float(user_min if user_min else 0):
                is_valid = True
                max_amount = float(user_max)
            else:
                print(
                    "Maximum amount should be numeric and greater than minimum amount.")
    return region, min_amount, max_amount

# Function to apply region filter
def apply_region_filter(valid_transactions, region):
    """
    Filter transactions by region.
    """
    region_filtered_count = 0
    if region:
        pre_count = len(valid_transactions)
        valid_transactions[:] = [
            t for t in valid_transactions if t["Region"] == region]
        region_filtered_count = pre_count - len(valid_transactions)
        print(f"Records after region filter: {len(valid_transactions)}")
    return region_filtered_count

# Function to apply amount filter
def apply_amount_filter(valid_transactions, min_amount, max_amount):
    """
    Filter transactions by total transaction amount.
    """
    # Amount Filter (Quantity * UnitPrice)
    if min_amount is None and max_amount is None:
        print(f"Records after amount filter: {len(valid_transactions)}")
        return 0
    pre_count = len(valid_transactions)
    valid_transactions[:] = [
        t for t in valid_transactions
        if (min_amount is None or (t["Quantity"] * t["UnitPrice"]) > min_amount)
        and (max_amount is None or (t["Quantity"] * t["UnitPrice"]) <= max_amount)
    ]
    amt_filtered_count = pre_count - len(valid_transactions)
    print(f"Records after amount filter: {len(valid_transactions)}")
    return amt_filtered_count

#Function to validate, filter and make summary of the data
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validate parsed transactions and apply optional region/amount filters.
    """
    valid_transactions, invalid_count, total_input = validate_data(transactions)
    print("-" * 30)
    print('Summary of valid records after cleaning the data:')
    # --- REQUIRED OUTPUT FORMAT ---
    print(f"Total records parsed: {total_input}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_transactions)}")
    print("-" * 30)

    region, min_amount, max_amount = display_filter_options(valid_transactions)

    # [4/10] Validating and Applying Filters
    print("\n[4/10] Validating transactions...")
    region_filtered_count = apply_region_filter(valid_transactions, region)
    amt_filtered_count = apply_amount_filter(
        valid_transactions, min_amount, max_amount)

    # Summary Report
    filter_summary = {
        'Total_Input': total_input,
        'Invalid_Count': invalid_count,
        'Filtered_by_Region': region_filtered_count,
        'Filtered_by_Amount': amt_filtered_count,
        'Final_Count': len(valid_transactions)
    }
    print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
    print("\n--- DATA VALIDATION SUMMARY ---")
    for key, value in filter_summary.items():
        display_name = key.replace('_', ' ').title()
        print(f"{display_name:<20}: {value}")
    print("-" * 30)
    return valid_transactions, invalid_count, filter_summary

# ========================================================================

#Function to generate sales report
def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generate and save a formatted sales analytics report to a text file.
    """
    print("\n[9/10] Generating report...")
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        total_records = len(transactions)
        # API Stats
        matched = [et for et in enriched_transactions if et.get('API_Match')]
        unmatched = list(
            set(et['ProductName'] for et in enriched_transactions if not et.get('API_Match')))
        success_rate = (len(matched) / total_records *
                        100) if total_records > 0 else 0

        report = []
        # 1. HEADER
        report.append("============================================")
        report.append(f"{'SALES ANALYTICS REPORT':^44}")
        report.append(
            f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"   Total Records Processed: {total_records}")
        report.append("============================================\n")

        # 2. OVERALL SUMMARY
        report.append("OVERALL SUMMARY")
        report.append("--------------------------------------------")
        report.append(
            f"Total Revenue:         ₹{ANALYTICS_RESULTS['total_revenue']:,.2f}")
        report.append(f"Total Transactions:    {total_records}")
        report.append(
            f"Average Order Value:   ₹{(ANALYTICS_RESULTS['total_revenue']/total_records if total_records > 0 else 0):,.2f}")
        d_keys = sorted(ANALYTICS_RESULTS['daily_sales_trend'].keys())
        report.append(
            f"Date Range:            {d_keys[0]} to {d_keys[-1] if d_keys else 'N/A'}\n")

        # 3. REGION-WISE PERFORMANCE
        report.append("REGION-WISE PERFORMANCE")
        report.append("--------------------------------------------")
        report.append(
            f"{'Region':<12} {'Sales':<15} {'% Total':<10} {'Transactions'}")
        for region, data in ANALYTICS_RESULTS['region_wise_performance'].items():
            report.append(
                f"{region:<12} ₹{data['total_sales']:<14,.2f} {data['percentage']:>6.2f}% {data['transaction_count']:>10}")
        report.append("\n")

        # 4. TOP 5 PRODUCTS
        report.append("TOP 5 PRODUCTS")
        report.append("--------------------------------------------")
        report.append(
            f"{'Rank':<5} {'Product Name':<20} {'Quantity Sold':<10} {'Revenue'}")
        for i, (name, quantity, revenue) in enumerate(ANALYTICS_RESULTS['top_selling_products'][:5], 1):
            report.append(
                f"{i:<5} {name[:19]:<20} {quantity:<10} ₹{revenue:,.2f}")
        report.append("\n")

        # 5. TOP 5 CUSTOMERS
        report.append("TOP 5 CUSTOMERS")
        report.append("--------------------------------------------")
        report.append(
            f"{'Rank':<5} {'Customer ID':<15} {'Total Spent':<15} {'Order Count'}")
        for i, (c_id, data) in enumerate(list(ANALYTICS_RESULTS['top_customers'].items())[:5], 1):
            report.append(
                f"{i:<5} {c_id:<15} ₹{data['total_spent']:<14,.2f} {data['purchase_count']}")
        report.append("\n")

        # 6. DAILY SALES TREND
        report.append("DAILY SALES TREND")
        report.append("--------------------------------------------")
        report.append(
            f"{'Date':<15} {'Revenue':<15} {'Transactions':<8} {'Unique Customers'}")
        for date, data in list(ANALYTICS_RESULTS['daily_sales_trend'].items())[:5]:
            report.append(
                f"{date:<15} ₹{data['revenue']:<14,.2f} {data['transaction_count']:<8} {data['unique_customers']}")
        report.append("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS
        report.append("PRODUCT PERFORMANCE ANALYSIS")
        report.append("--------------------------------------------")
        report.append(
            f"Best selling day:      {ANALYTICS_RESULTS['peak_sales_day'][0]} (₹{ANALYTICS_RESULTS['peak_sales_day'][1]:,.2f})")
        low_names = [p[0] for p in ANALYTICS_RESULTS['low_performers'][:3]]
        report.append(
            f"Low performing products:        {', '.join(low_names) if low_names else 'None'}")
        avg_reg_val = ANALYTICS_RESULTS['total_revenue'] / \
            len(ANALYTICS_RESULTS['region_wise_performance']
                ) if ANALYTICS_RESULTS['region_wise_performance'] else 0
        report.append(f"Average Revenue per Region:    ₹{avg_reg_val:,.2f}\n")

        # 8. API ENRICHMENT SUMMARY
        report.append("API ENRICHMENT SUMMARY")
        report.append("--------------------------------------------")
        report.append(f"Total products enriched: {len(matched)}")
        report.append(f"Success rate percentage: {success_rate:.2f}%")
        report.append(
            f"Unenriched Products:     {', '.join(unmatched[:3])}...")
        report.append("============================================")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(report))
        print(f"✓ Report saved to: {output_file}")
    except Exception as e:
        print(f"✕ Report Error: {e}")

# ========================================================================
