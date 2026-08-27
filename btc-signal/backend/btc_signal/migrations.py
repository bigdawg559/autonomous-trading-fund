from __future__ import annotations

from sqlalchemy import text

from .database import Base, make_engine


def migrate(database_url: str) -> None:
    engine = make_engine(database_url)
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_candles_symbol_timeframe_open_time ON candles(symbol, timeframe, open_time)"))


if __name__ == "__main__":
    import os
    migrate(os.environ["DATABASE_URL"])
