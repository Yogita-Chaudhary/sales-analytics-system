

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
    # Filter Display: Help the user see what they can filter by
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
    print("-" * 30)

    region, min_amount, max_amount = display_filter_options(valid_transactions)
    
    return valid_transactions, invalid_count