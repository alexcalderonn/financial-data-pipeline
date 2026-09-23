import pandas as pd
import sqlite3
from pathlib import Path

# ---------------------------------
# File locations
# ---------------------------------

processed_folder = Path("data/processed")
database_folder = Path("database")

# Create database folder if it doesn't exist
database_folder.mkdir(parents=True, exist_ok=True)

stock_file = processed_folder / "master_stock_data.csv"
financial_file = processed_folder / "master_financials.csv"
database_file = database_folder / "financial_data.db"


# ---------------------------------
# Read processed datasets
# ---------------------------------

print("Reading cleaned data...")

stock_df = pd.read_csv(stock_file)
financial_df = pd.read_csv(financial_file)

print(f"Stock rows ready to load: {len(stock_df)}")
print(f"Financial rows ready to load: {len(financial_df)}")


# ---------------------------------
# Connect to SQLite database
# ---------------------------------

connection = sqlite3.connect(database_file)

print("Connected to database.")


# ---------------------------------
# Load stock data
# ---------------------------------

stock_df.to_sql(
    "stock_prices",
    connection,
    if_exists="replace",
    index=False
)

print("Stock data loaded into stock_prices table.")


# ---------------------------------
# Load financial data
# ---------------------------------

financial_df.to_sql(
    "financial_metrics",
    connection,
    if_exists="replace",
    index=False
)

print("Financial data loaded into financial_metrics table.")


# ---------------------------------
# Verify stock data
# ---------------------------------

stock_query = """
SELECT
    ticker,
    COUNT(*) AS total_records,
    MIN(date) AS earliest_date,
    MAX(date) AS latest_date
FROM stock_prices
GROUP BY ticker;
"""

stock_results = pd.read_sql_query(
    stock_query,
    connection
)

print("\nStock database verification:")
print(stock_results)


# ---------------------------------
# Verify financial data
# ---------------------------------

financial_query = """
SELECT
    ticker,
    COUNT(*) AS financial_records,
    MIN(fiscal_date) AS earliest_fiscal_date,
    MAX(fiscal_date) AS latest_fiscal_date
FROM financial_metrics
GROUP BY ticker;
"""

financial_results = pd.read_sql_query(
    financial_query,
    connection
)

print("\nFinancial database verification:")
print(financial_results)


# ---------------------------------
# Close database connection
# ---------------------------------

connection.close()

print("\nDatabase connection closed.")
print("Load complete!")