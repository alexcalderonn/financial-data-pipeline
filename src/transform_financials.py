import pandas as pd
from pathlib import Path

raw_folder = Path("data/raw")
processed_folder = Path("data/processed")

companies = ["NVDA", "DELL", "CVX"]

all_financials = []

for ticker in companies:

    print("\n" + "=" * 50)
    print(f"Transforming financial data for {ticker}")
    print("=" * 50)

    # -----------------------------
    # Read financial statements
    # -----------------------------

    income = pd.read_csv(
        raw_folder / f"{ticker}_income_statement.csv"
    )

    balance = pd.read_csv(
        raw_folder / f"{ticker}_balance_sheet.csv"
    )

    cashflow = pd.read_csv(
        raw_folder / f"{ticker}_cash_flow.csv"
    )

    # Rename the first column to fiscal_date
    income = income.rename(
        columns={"Unnamed: 0": "fiscal_date"}
    )

    balance = balance.rename(
        columns={"Unnamed: 0": "fiscal_date"}
    )

    cashflow = cashflow.rename(
        columns={"Unnamed: 0": "fiscal_date"}
    )

    # -----------------------------
    # Select important fields
    # -----------------------------

    income = income[
        [
            "fiscal_date",
            "ticker",
            "Total Revenue",
            "Operating Income",
            "Net Income"
        ]
    ]

    balance = balance[
        [
            "fiscal_date",
            "ticker",
            "Total Assets",
            "Current Assets",
            "Current Liabilities",
            "Stockholders Equity",
            "Total Debt"
        ]
    ]

    cashflow = cashflow[
        [
            "fiscal_date",
            "ticker",
            "Operating Cash Flow",
            "Capital Expenditure",
            "Free Cash Flow"
        ]
    ]

    # -----------------------------
    # Merge statements
    # -----------------------------

    financials = income.merge(
        balance,
        on=["fiscal_date", "ticker"],
        how="outer"
    )

    financials = financials.merge(
        cashflow,
        on=["fiscal_date", "ticker"],
        how="outer"
    )

    # Convert fiscal date
    financials["fiscal_date"] = pd.to_datetime(
        financials["fiscal_date"]
    )

    # -----------------------------
    # Standardize column names
    # -----------------------------

    financials = financials.rename(
        columns={
            "Total Revenue": "revenue",
            "Operating Income": "operating_income",
            "Net Income": "net_income",
            "Total Assets": "total_assets",
            "Current Assets": "current_assets",
            "Current Liabilities": "current_liabilities",
            "Stockholders Equity": "stockholders_equity",
            "Total Debt": "total_debt",
            "Operating Cash Flow": "operating_cash_flow",
            "Capital Expenditure": "capital_expenditure",
            "Free Cash Flow": "free_cash_flow"
        }
    )

    # -----------------------------
    # Calculate financial KPIs
    # -----------------------------

    financials["net_profit_margin"] = (
        financials["net_income"]
        / financials["revenue"]
    ) * 100

    financials["operating_margin"] = (
        financials["operating_income"]
        / financials["revenue"]
    ) * 100

    financials["current_ratio"] = (
        financials["current_assets"]
        / financials["current_liabilities"]
    )

    financials["debt_to_assets"] = (
        financials["total_debt"]
        / financials["total_assets"]
    )

    financials["return_on_assets"] = (
        financials["net_income"]
        / financials["total_assets"]
    ) * 100

    # Sort by fiscal date
    financials = financials.sort_values(
        "fiscal_date"
    )

    # Revenue growth
    financials["revenue_growth_pct"] = (
        financials["revenue"]
        .pct_change(fill_method=None)
        * 100
    )

    all_financials.append(financials)

    print(f"Financial records processed: {len(financials)}")


# ---------------------------------
# Combine all companies
# ---------------------------------

master_financials = pd.concat(
    all_financials,
    ignore_index=True
)

master_financials = master_financials.sort_values(
    ["ticker", "fiscal_date"]
)

output_path = (
    processed_folder /
    "master_financials.csv"
)

master_financials.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 50)
print("FINANCIAL TRANSFORMATION COMPLETE")
print("=" * 50)

print(
    f"Total financial records: "
    f"{len(master_financials)}"
)

print(
    f"Companies: "
    f"{master_financials['ticker'].nunique()}"
)

print(
    f"Saved to: {output_path}"
)
