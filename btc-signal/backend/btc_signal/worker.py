from __future__ import annotations

import asyncio
import logging

from .market import BinanceSpotProvider

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('btc-signal-worker')


async def run() -> None:
    provider = BinanceSpotProvider()
    log.info('starting BTCUSDT %s worker', provider.interval)
    # Initial reconciliation/backfill. Persistence is added in the database stage.
    candles = await provider.fetch_klines(limit=1000)
    log.info('validated %d historical candles', len(candles))
    async for candle in provider.stream():
        if candle.closed:
            log.info('closed candle %s close=%s volume=%s', candle.timestamp.isoformat(), candle.close, candle.volume)


if __name__ == '__main__':
    asyncio.run(run())
