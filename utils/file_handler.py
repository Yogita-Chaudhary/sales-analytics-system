

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

