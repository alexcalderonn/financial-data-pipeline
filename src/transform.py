import pandas as pd
from pathlib import Path

# Location of our data folders
raw_folder = Path("data/raw")
processed_folder = Path("data/processed")

# Make sure the processed folder exists
processed_folder.mkdir(parents=True, exist_ok=True)

companies = ["NVDA", "DELL", "CVX"]

for ticker in companies:

    print("\n-----------------------------")
    print(f"Transforming {ticker} data")
    print("-----------------------------")

    # Read raw CSV
    file_path = raw_folder / f"{ticker}_stock_data.csv"
    df = pd.read_csv(file_path)

    print(f"Original rows: {len(df)}")

    # Remove duplicate rows
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    print(f"Duplicates removed: {duplicates}")

    # Convert Date into a proper datetime value
    df["Date"] = pd.to_datetime(df["Date"], utc=True)

    # Check important columns for missing values
    important_columns = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    missing_values = df[important_columns].isnull().sum().sum()

    print(f"Missing important values: {missing_values}")

    # Add the company's ticker
    df["Ticker"] = ticker

    # Keep the columns we need
    df = df[
        [
            "Date",
            "Ticker",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]
    ]

    # Standardize column names
    df.columns = [
        "date",
        "ticker",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume"
    ]

    # Save cleaned dataset
    output_path = processed_folder / f"{ticker}_clean.csv"
    df.to_csv(output_path, index=False)

    print(f"Clean rows: {len(df)}")
    print(f"Saved to: {output_path}")

print("\nTransformation complete!")
# ---------------------------------
# Combine all cleaned datasets
# ---------------------------------

print("\nCombining cleaned datasets...")

all_data = []

for ticker in companies:
    file_path = processed_folder / f"{ticker}_clean.csv"

    df = pd.read_csv(file_path)
    all_data.append(df)

# Combine the three DataFrames
master_df = pd.concat(all_data, ignore_index=True)

# Sort by ticker and date
master_df = master_df.sort_values(
    by=["ticker", "date"]
)

# ---------------------------------
# Engineer financial metrics
# ---------------------------------

# Daily dollar price change
master_df["daily_price_change"] = (
    master_df.groupby("ticker")["close_price"].diff()
)

# Daily percentage return
master_df["daily_return_pct"] = (
    master_df.groupby("ticker")["close_price"]
    .pct_change(fill_method=None) * 100
)

# Daily trading range
master_df["daily_range"] = (
    master_df["high_price"] - master_df["low_price"]
)

# 20-day moving average
master_df["moving_avg_20"] = (
    master_df.groupby("ticker")["close_price"]
    .transform(lambda x: x.rolling(20).mean())
)

# 50-day moving average
master_df["moving_avg_50"] = (
    master_df.groupby("ticker")["close_price"]
    .transform(lambda x: x.rolling(50).mean())
)

print("\nFinancial metrics created.")
# Save master dataset
master_path = processed_folder / "master_stock_data.csv"

master_df.to_csv(master_path, index=False)

print(f"Total master rows: {len(master_df)}")
print(f"Companies: {master_df['ticker'].nunique()}")
print(f"Saved to: {master_path}")

print("\nMaster dataset created successfully!")
