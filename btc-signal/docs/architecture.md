# BTCUSDT Adaptive Signal Architecture

## Components

1. Binance Spot public market data: BTCUSDT 15m REST backfill and WebSocket stream.
2. Railway persistent worker: ingestion, reconciliation, feature calculation, inference, monitoring, and later retraining.
3. PostgreSQL: durable candles, features, signals, predictions, model registry, and paper-trade records.
4. FastAPI: request/response API boundary.
5. Vercel/Next.js: dashboard and lightweight API-facing web application.
6. GitHub Actions: deterministic validation and tests.

## Worker boundary

The worker must not depend on a Vercel invocation remaining alive. It owns the long-lived exchange connection and scheduled ML work.

## ML promotion boundary

No model becomes a production champion merely because it has a good in-sample score. Promotion requires leakage tests, chronological walk-forward evaluation, calibration checks, regime evaluation, minimum sample size, and drawdown constraints.

## Current limitation

The first vertical slice intentionally has no trained production ML model. Until enough real historical observations have been accumulated and evaluated, the public signal endpoint reports `MODEL_DEGRADED` and `NO_TRADE` rather than inventing probabilities.
