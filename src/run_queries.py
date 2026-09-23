import sqlite3
import pandas as pd

# Connect to the database
connection = sqlite3.connect(
    "database/financial_data.db"
)

print("Connected to database.")


# ---------------------------------
# Query 1: Stock price analysis
# ---------------------------------

stock_query = """
SELECT
    ticker,
    COUNT(*) AS trading_days,
    ROUND(AVG(close_price), 2) AS average_closing_price,
    ROUND(MIN(close_price), 2) AS lowest_closing_price,
    ROUND(MAX(close_price), 2) AS highest_closing_price
FROM stock_prices
GROUP BY ticker
ORDER BY ticker;
"""

stock_results = pd.read_sql_query(
    stock_query,
    connection
)

print("\n" + "=" * 60)
print("STOCK PRICE ANALYSIS")
print("=" * 60)

print(stock_results)


# ---------------------------------
# Query 2: Financial performance
# ---------------------------------

financial_query = """
SELECT
    ticker,
    fiscal_date,
    ROUND(revenue / 1000000000.0, 2) AS revenue_billions,
    ROUND(net_income / 1000000000.0, 2) AS net_income_billions,
    ROUND(net_profit_margin, 2) AS net_profit_margin_pct,
    ROUND(current_ratio, 2) AS current_ratio,
    ROUND(debt_to_assets, 2) AS debt_to_assets
FROM financial_metrics
WHERE revenue IS NOT NULL
ORDER BY ticker, fiscal_date;
"""

financial_results = pd.read_sql_query(
    financial_query,
    connection
)

print("\n" + "=" * 60)
print("FINANCIAL PERFORMANCE ANALYSIS")
print("=" * 60)

print(financial_results)


# Close database connection
connection.close()

print("\nDatabase connection closed.")
