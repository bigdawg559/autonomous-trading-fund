from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import select

from .database import Candle


def upsert_candle(session, *, symbol: str, timeframe: str, open_time: datetime,
                  close_time: datetime, open: float, high: float, low: float,
                  close: float, volume: float, is_closed: bool = True,
                  source: str = "binance") -> Candle:
    existing = session.scalar(select(Candle).where(
        Candle.symbol == symbol,
        Candle.timeframe == timeframe,
        Candle.open_time == open_time,
    ))
    if existing is None:
        existing = Candle(symbol=symbol, timeframe=timeframe, open_time=open_time,
                          close_time=close_time, open=Decimal(str(open)),
                          high=Decimal(str(high)), low=Decimal(str(low)),
                          close=Decimal(str(close)), volume=Decimal(str(volume)),
                          is_closed=is_closed, source=source)
        session.add(existing)
    else:
        existing.close_time = close_time
        existing.open = Decimal(str(open)); existing.high = Decimal(str(high))
        existing.low = Decimal(str(low)); existing.close = Decimal(str(close))
        existing.volume = Decimal(str(volume)); existing.is_closed = is_closed
    return existing
