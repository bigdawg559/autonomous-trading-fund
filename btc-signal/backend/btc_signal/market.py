from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import AsyncIterator

import httpx
import websockets

from .config import settings


@dataclass(frozen=True)
class Candle:
    open_time_ms: int
    close_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    closed: bool

    @property
    def timestamp(self) -> datetime:
        return datetime.fromtimestamp(self.open_time_ms / 1000, tz=timezone.utc)


def validate_candle(c: Candle) -> list[str]:
    errors: list[str] = []
    if min(c.open, c.high, c.low, c.close, c.volume) < 0:
        errors.append('negative_market_value')
    if c.high < max(c.open, c.close, c.low):
        errors.append('invalid_high')
    if c.low > min(c.open, c.close, c.high):
        errors.append('invalid_low')
    if c.close_time_ms <= c.open_time_ms:
        errors.append('invalid_time_range')
    if c.volume == 0:
        errors.append('zero_volume')
    return errors


class BinanceSpotProvider:
    def __init__(self, symbol: str | None = None, interval: str | None = None):
        self.symbol = (symbol or settings.symbol).lower()
        self.interval = interval or settings.timeframe
        self.rest_url = settings.binance_rest_url.rstrip('/')
        self.ws_url = settings.binance_ws_url.rstrip('/')

    async def fetch_klines(self, limit: int = 500) -> list[Candle]:
        params = {'symbol': self.symbol.upper(), 'interval': self.interval, 'limit': limit}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f'{self.rest_url}/api/v3/klines', params=params)
            response.raise_for_status()
            rows = response.json()
        candles = [
            Candle(int(r[0]), int(r[6]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5]), True)
            for r in rows
        ]
        if any(validate_candle(c) for c in candles):
            raise ValueError('Binance returned invalid OHLCV data')
        return candles

    async def stream(self) -> AsyncIterator[Candle]:
        url = f'{self.ws_url}/{self.symbol}@kline_{self.interval}'
        backoff = 1
        while True:
            try:
                async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                    backoff = 1
                    async for message in ws:
                        payload = __import__('json').loads(message)
                        k = payload.get('k', {})
                        candle = Candle(
                            int(k['t']), int(k['T']), float(k['o']), float(k['h']), float(k['l']),
                            float(k['c']), float(k['v']), bool(k['x'])
                        )
                        if not validate_candle(candle):
                            yield candle
            except Exception:
                await asyncio.sleep(min(backoff, 60))
                backoff *= 2


def is_stale(candle: Candle, now_ms: int | None = None) -> bool:
    now = now_ms if now_ms is not None else int(time.time() * 1000)
    return now - candle.close_time_ms > settings.stale_after_seconds * 1000
