# Build status

## Implemented

- Binance BTCUSDT 15m REST provider.
- Binance BTCUSDT 15m WebSocket provider with reconnect backoff.
- OHLCV validation and stale-data checks.
- Versioned pandas feature engine.
- FastAPI market, candle, health, signal, and system-status endpoints.
- Persistent worker entry point.
- Next.js dashboard shell.
- Unit-test foundation.
- GitHub Actions validation workflow.
- Railway deployment configuration and instructions.

## Not yet implemented

- PostgreSQL persistence and migrations.
- Multi-timeframe storage/alignment.
- Triple-barrier labels.
- Leakage-safe walk-forward trainer.
- Calibrated ML champion.
- Ensemble and uncertainty model.
- Event-driven backtester with fees/spread/slippage.
- Paper-trading ledger.
- Champion/challenger registry and automated retraining.
- Production Vercel deployment of this branch.
- Railway deployment.

## Verification constraints

The connected execution environment cannot resolve external DNS, so live Binance requests and local package installation could not be executed from this session. GitHub CI is configured to perform dependency installation, compilation, and tests when the branch is reviewed.
