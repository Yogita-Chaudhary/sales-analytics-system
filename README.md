**Sales Analytics & Data Enrichment System**
A robust Python-based ETL (Extract, Transform, Load) pipeline that processes raw sales data, performs multi-dimensional business analytics, and enriches local records with real-time metadata from the DummyJSON API.

**🚀 Key Features**
1. ***Data Cleaning***: Automatically handles encoding issues and filters invalid records (negative values, missing IDs).
2. ***Dynamic Filtering***: Interactive CLI allows users to filter data by Region or Transaction Amount.
3. ***API Enrichment***: Integrates with a REST API to map local Product IDs to Categories, Brands, and Ratings.
4. ***Business Intelligence***: Generates metrics for Top Products, Top Customers, Regional Performance, and Daily Trends.
5. ***Comprehensive Reporting***: Produces both a raw enriched dataset and a formatted summary report.

**📂 Project Structure**
- ***main.py***: The application entry point (orchestrates the 10-step pipeline).
- ***utils/file_handler.py***: Manages file I/O, parsing, and user-driven filtering.
- ***utils/data_processor.py***: Contains the core logic for revenue and trend calculations.
- ***utils/api_handler.py***: Manages API requests, product mapping, and data enrichment.
- ***data/***: Input (sales_data.txt) and output (enriched_sales_data.txt) storage.
- ***output/***: Destination for the final sales_report.txt.

**🛠️ Setup & Usage**
1. ***Prerequisites***
    Ensure you have Python 3.8+ installed. This project requires the requests library.
2. ***Installation***
    Clone the project and install dependencies:Bashpip install requests
3. ***Running the System***
    a. Place your raw data in data/sales_data.txt.
    b. Execute the main script:
        Bash
        python main.py
    c. Follow the CLI prompts to apply optional filters for specific regions or price ranges.
    
**📊 Output Files**
File                                                                Description
data/enriched_sales_data.txt     Pipe-delimited file containing original data merged with API categories and brands.
output/sales_report.txt             A formatted business report including Top 5 rankings and revenue summaries.
