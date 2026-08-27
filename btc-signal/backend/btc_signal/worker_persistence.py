from __future__ import annotations

import asyncio

from .config import settings
from .database import create_schema, make_engine, make_session_factory
from .market import BinanceSpotProvider
from .persistence import upsert_candle


async def run_worker() -> None:
    provider = BinanceSpotProvider()
    engine = make_engine(settings.database_url)
    create_schema(engine)
    Session = make_session_factory(engine)

    # REST bootstrap establishes a contiguous recent history before streaming.
    candles = await provider.fetch_klines(limit=500)
    with Session() as session:
        for candle in candles:
            upsert_candle(session, symbol=settings.symbol, timeframe=settings.timeframe,
                          open_time=candle.timestamp,
                          close_time=candle.timestamp + (candle.close_time_ms - candle.open_time_ms) / 1000,
                          open=candle.open, high=candle.high, low=candle.low,
                          close=candle.close, volume=candle.volume, is_closed=candle.closed)
        session.commit()

    async for candle in provider.stream():
        with Session() as session:
            upsert_candle(session, symbol=settings.symbol, timeframe=settings.timeframe,
                          open_time=candle.timestamp,
                          close_time=candle.timestamp + (candle.close_time_ms - candle.open_time_ms) / 1000,
                          open=candle.open, high=candle.high, low=candle.low,
                          close=candle.close, volume=candle.volume, is_closed=candle.closed)
            session.commit()


if __name__ == '__main__':
    asyncio.run(run_worker())
