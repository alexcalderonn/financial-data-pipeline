import pandas as pd
from pathlib import Path
import sys

processed_folder = Path("data/processed")

stock_file = processed_folder / "master_stock_data.csv"
financial_file = processed_folder / "master_financials.csv"

print("=" * 50)
print("DATA QUALITY VALIDATION")
print("=" * 50)

errors = []

# ---------------------------------
# Validate stock data
# ---------------------------------

print("\nChecking stock data...")

stock_df = pd.read_csv(stock_file)

# Check that dataset is not empty
if stock_df.empty:
    errors.append("Stock dataset is empty.")

# Check for duplicate ticker/date combinations
duplicates = stock_df.duplicated(
    subset=["ticker", "date"]
).sum()

if duplicates > 0:
    errors.append(
        f"Stock data contains {duplicates} duplicate records."
    )

# Check for missing important values
required_stock_columns = [
    "date",
    "ticker",
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "volume"
]

missing_stock = (
    stock_df[required_stock_columns]
    .isnull()
    .sum()
    .sum()
)

if missing_stock > 0:
    errors.append(
        f"Stock data contains {missing_stock} missing important values."
    )

# Check for negative trading volume
negative_volume = (
    stock_df["volume"] < 0
).sum()

if negative_volume > 0:
    errors.append(
        f"Stock data contains {negative_volume} negative volume values."
    )

print(f"Stock records checked: {len(stock_df)}")


# ---------------------------------
# Validate financial data
# ---------------------------------

print("\nChecking financial data...")

financial_df = pd.read_csv(financial_file)

if financial_df.empty:
    errors.append("Financial dataset is empty.")

financial_duplicates = financial_df.duplicated(
    subset=["ticker", "fiscal_date"]
).sum()

if financial_duplicates > 0:
    errors.append(
        f"Financial data contains {financial_duplicates} duplicate records."
    )

print(
    f"Financial records checked: {len(financial_df)}"
)


# ---------------------------------
# Final validation result
# ---------------------------------

if errors:

    print("\nVALIDATION FAILED")

    for error in errors:
        print(f"- {error}")

    sys.exit(1)

else:

    print("\nAll validation checks passed!")
    print("Data is ready to load into SQL.")