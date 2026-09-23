import pandas as pd
import yfinance as yf

# Companies included in our financial data pipeline
companies = {
    "NVDA": "NVIDIA",
    "DELL": "Dell Technologies",
    "CVX": "Chevron"
}

# Loop through each company
for ticker_symbol, company_name in companies.items():

    print("\n-----------------------------")
    print(f"Collecting data for {company_name}")
    print("-----------------------------")

    ticker = yf.Ticker(ticker_symbol)

    # Get historical stock prices
    stock_data = ticker.history(period="5y")

    print(f"Ticker: {ticker_symbol}")
    print(f"Rows collected: {len(stock_data)}")

    # Save the raw data
    file_path = f"data/raw/{ticker_symbol}_stock_data.csv"

    stock_data.to_csv(file_path)

    print(f"Saved to: {file_path}")

print("\nData extraction complete!")
# ---------------------------------
# Extract company financial statements
# ---------------------------------

print("\nExtracting financial statements...")

for ticker_symbol, company_name in companies.items():

    print("\n-----------------------------")
    print(f"Financial statements: {company_name}")
    print("-----------------------------")

    ticker = yf.Ticker(ticker_symbol)

    # Income statement
    income_statement = ticker.financials.T
    income_statement["ticker"] = ticker_symbol

    income_path = f"data/raw/{ticker_symbol}_income_statement.csv"
    income_statement.to_csv(income_path)

    print(f"Income statement saved: {income_path}")

    # Balance sheet
    balance_sheet = ticker.balance_sheet.T
    balance_sheet["ticker"] = ticker_symbol

    balance_path = f"data/raw/{ticker_symbol}_balance_sheet.csv"
    balance_sheet.to_csv(balance_path)

    print(f"Balance sheet saved: {balance_path}")

    # Cash flow statement
    cash_flow = ticker.cashflow.T
    cash_flow["ticker"] = ticker_symbol

    cashflow_path = f"data/raw/{ticker_symbol}_cash_flow.csv"
    cash_flow.to_csv(cashflow_path)

    print(f"Cash flow statement saved: {cashflow_path}")

print("\nFinancial statement extraction complete!")
