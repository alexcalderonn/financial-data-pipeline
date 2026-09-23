import pandas as pd

companies = ["NVDA", "DELL", "CVX"]

for ticker in companies:

    print("\n" + "=" * 60)
    print(f"{ticker} FINANCIAL STATEMENT FIELDS")
    print("=" * 60)

    # Income Statement
    income = pd.read_csv(
        f"data/raw/{ticker}_income_statement.csv"
    )

    print("\nINCOME STATEMENT:")
    print(income.columns.tolist())

    # Balance Sheet
    balance = pd.read_csv(
        f"data/raw/{ticker}_balance_sheet.csv"
    )

    print("\nBALANCE SHEET:")
    print(balance.columns.tolist())

    # Cash Flow
    cashflow = pd.read_csv(
        f"data/raw/{ticker}_cash_flow.csv"
    )

    print("\nCASH FLOW:")
    print(cashflow.columns.tolist())
    