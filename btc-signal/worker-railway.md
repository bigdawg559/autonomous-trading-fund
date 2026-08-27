# Railway worker

Use a persistent Railway service for the worker process.

Start command:

```text
python -m btc_signal.worker
```

Required variables:

```text
DATABASE_URL
BINANCE_REST_URL=https://api.binance.com
BINANCE_WS_URL=wss://stream.binance.com:9443/ws
SYMBOL=BTCUSDT
TIMEFRAME=15m
```

The current Railway account connected to this build has an expired trial and cannot create/deploy a service. Do not interpret this repository configuration as a completed Railway deployment.
