# BTCUSDT Adaptive ML Signal Engine

A research-first BTCUSDT 15-minute quantitative decision-support service.

## Current stage

This branch is the first executable vertical slice. It implements:

- real Binance Spot BTCUSDT 15m market-data ingestion;
- REST recovery/backfill plus WebSocket candle streaming;
- OHLCV validation, duplicate detection, gap/staleness checks;
- versioned feature calculation;
- a transparent rule-based baseline signal engine that returns LONG/SHORT/NO_TRADE only from measured inputs;
- FastAPI health/market/candle/signal endpoints;
- a worker entry point suitable for Railway;
- a Next.js dashboard shell;
- tests for data validation and signal gating.

ML training, calibrated probabilities, walk-forward backtesting, champion/challenger promotion, and adaptive retraining are deliberately gated behind sufficient real historical data. The system must not invent those results.

## Market data source

Primary source: Binance Spot public market data for `BTCUSDT`, with 15-minute klines. No trading credentials are required for public market-data ingestion. REST is used for recovery and initial backfill; WebSocket is used for continuous updates.

## Architecture

```text
Binance REST/WebSocket
        |
        v
Railway persistent worker
  validation -> storage -> features -> signal engine
        |
        v
PostgreSQL
        |
        v
FastAPI service / Vercel-compatible API boundary
        |
        v
Next.js dashboard
```

The worker is intentionally separate from Vercel. Vercel is not treated as an always-running process host.

## Safety states

- `DATA_UNAVAILABLE`: no sufficiently fresh validated market data.
- `MODEL_DEGRADED`: model artifact is unavailable or fails health gates.
- `SYSTEM_HALTED`: critical infrastructure failure.
- `NO_TRADE`: valid system state but no statistically/risk-qualified trade setup.

This foundation does not claim profitability or accuracy.

## Environment

See `.env.example`.

Important variables:

- `DATABASE_URL`
- `BINANCE_REST_URL`
- `BINANCE_WS_URL`
- `SYMBOL=BTCUSDT`
- `TIMEFRAME=15m`
- `STALE_AFTER_SECONDS=120`
- `ENVIRONMENT=local`

## Worker

```bash
python -m btc_signal.worker
```

The worker is designed for a Railway service with a persistent start command. Railway deployment is intentionally not enabled until a Railway plan with sufficient runtime credit is available.

## API

- `GET /health`
- `GET /api/market/btcusdt`
- `GET /api/candles/btcusdt/15m`
- `GET /api/signal/current`
- `GET /api/system/status`

## Development status

This is an incremental build. Do not treat the current branch as the finished production trading system. The next gates are historical-data accumulation, leakage-safe labels, chronological walk-forward evaluation, probability calibration, realistic backtesting, and only then adaptive model promotion.
