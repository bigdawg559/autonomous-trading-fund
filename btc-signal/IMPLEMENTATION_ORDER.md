# Implementation gates

1. Market-data ingestion and validation — current.
2. PostgreSQL candle/feature persistence.
3. Historical reconciliation and multi-timeframe alignment.
4. Feature/label dataset builder.
5. Baseline classifiers and leakage-safe training.
6. Event-driven backtester.
7. Probability calibration and uncertainty.
8. Regime engine.
9. Signal/risk engine with model health gates.
10. Paper-trading ledger.
11. Champion/challenger registry.
12. Drift monitoring and controlled retraining.
13. Production Vercel preview and deployment.
14. Railway worker deployment.
15. End-to-end production verification.

A later gate must not be represented as complete merely because its source files exist. Each gate requires executable tests and measured evidence.
