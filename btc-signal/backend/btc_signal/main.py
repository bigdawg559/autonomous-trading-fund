from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
import pandas as pd

from .features import FEATURE_VERSION, compute_features
from .market import BinanceSpotProvider, is_stale
from .signals import decide

app = FastAPI(title='BTCUSDT Adaptive ML Signal Engine', version='0.1.0')
provider = BinanceSpotProvider()


@app.get('/health')
async def health():
    try:
        candles = await provider.fetch_klines(limit=2)
        fresh = bool(candles) and not is_stale(candles[-1])
        return {'status': 'HEALTHY' if fresh else 'DEGRADED', 'market_data': 'HEALTHY' if fresh else 'STALE', 'model': 'DEGRADED', 'feature_version': FEATURE_VERSION}
    except Exception as exc:
        return {'status': 'SYSTEM_HALTED', 'market_data': 'UNAVAILABLE', 'model': 'DEGRADED', 'error_type': type(exc).__name__}


@app.get('/api/market/btcusdt')
async def market():
    try:
        candles = await provider.fetch_klines(limit=1)
        if not candles:
            raise HTTPException(503, 'DATA_UNAVAILABLE')
        c = candles[-1]
        return {'symbol': 'BTCUSDT', 'timeframe': '15m', 'price': c.close, 'timestamp': c.close_time_ms, 'stale': is_stale(c)}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(503, detail={'status': 'DATA_UNAVAILABLE', 'error_type': type(exc).__name__})


@app.get('/api/candles/btcusdt/15m')
async def candles(limit: int = Query(200, ge=10, le=1000)):
    try:
        rows = await provider.fetch_klines(limit=limit)
        return [c.__dict__ for c in rows]
    except Exception as exc:
        raise HTTPException(503, detail={'status': 'DATA_UNAVAILABLE', 'error_type': type(exc).__name__})


@app.get('/api/signal/current')
async def current_signal():
    try:
        rows = await provider.fetch_klines(limit=250)
        df = pd.DataFrame([c.__dict__ for c in rows])
        df = df.set_index(pd.to_datetime(df['open_time_ms'], unit='ms', utc=True))
        features = compute_features(df).dropna()
        if features.empty:
            return {'signal': 'NO_TRADE', 'reason_codes': ['INSUFFICIENT_DATA'], 'model_status': 'DEGRADED'}
        last = features.iloc[-1].to_dict()
        decision = decide(last, data_fresh=not is_stale(rows[-1]), model_healthy=False)
        return {'signal': decision.signal, 'reason_codes': list(decision.reason_codes), 'entry': decision.entry, 'stop_loss': decision.stop_loss, 'tp1': decision.tp1, 'tp2': decision.tp2, 'risk_reward': decision.risk_reward, 'model_status': 'DEGRADED'}
    except Exception as exc:
        raise HTTPException(503, detail={'status': 'SYSTEM_HALTED', 'error_type': type(exc).__name__})


@app.get('/api/system/status')
async def system_status():
    return await health()
