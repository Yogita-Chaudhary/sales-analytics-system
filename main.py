from utils.file_handler import read_sales_data, parse_transactions

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
    except Exception as e:
        print(f"\n✕ Error: {e}")


if __name__ == "__main__":
    main()
