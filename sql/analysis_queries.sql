SELECT
    ticker,
    COUNT(*) AS trading_days,
    ROUND(AVG(close_price), 2) AS average_closing_price,
    ROUND(MIN(close_price), 2) AS lowest_closing_price,
    ROUND(MAX(close_price), 2) AS highest_closing_price
FROM stock_prices
GROUP BY ticker
ORDER BY ticker;


-- Financial performance analysis

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