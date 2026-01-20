from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter, generate_sales_report
from utils.data_processor import run_analytics
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data

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
        valid_transactions, invalid_count, filter_summary = validate_and_filter(parsed_data)
        # [5/10] ANALYSIS
        run_analytics(valid_transactions)

        # [6-8] API & ENRICHMENT
        api_raw = fetch_all_products()
        product_mapping = create_product_mapping(api_raw)
        enriched_data = enrich_sales_data(valid_transactions, product_mapping)
        save_enriched_data(enriched_data)
        
        # [9/10] Generating report (ALL FIELDS)
        generate_sales_report(
            transactions=valid_transactions,
            enriched_transactions=enriched_data
        )
        
        # 10/10 PROCESS COMPLETED
        print("\n[10/10] Process Complete!")

    except Exception as e:
        print(f"\n✕ Error: {e}")

if __name__ == "__main__":
    main()
