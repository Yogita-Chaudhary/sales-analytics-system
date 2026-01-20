from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter

def main():
    try:
        print("=" * 55)
        print("               SALES ANALYTICS SYSTEM         ")
        print("=" * 55)
        # [1/10] LOAD
        raw_lines = read_sales_data('data/sales_data.txt')
        if not raw_lines:
            print("Stopping process: No data available.")
            return
        # [2/10] PARSE THE DATA
        parsed_data = parse_transactions(raw_lines)
        valid_transactions, invalid_count = validate_and_filter(parsed_data)
    except Exception as e:
        print(f"\n✕ Error: {e}")


if __name__ == "__main__":
    main()
