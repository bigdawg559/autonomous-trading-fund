from datetime import datetime, timezone
from decimal import Decimal

from btc_signal.database import Candle, Base, make_engine, make_session_factory, create_schema


def test_candle_round_trip_and_unique_key():
    engine = make_engine("sqlite:///:memory:")
    create_schema(engine)
    Session = make_session_factory(engine)
    when = datetime(2026, 1, 1, tzinfo=timezone.utc)
    with Session() as session:
        session.add(Candle(symbol="BTCUSDT", timeframe="15m", open_time=when, close_time=when,
                           open=Decimal("100"), high=Decimal("110"), low=Decimal("90"),
                           close=Decimal("105"), volume=Decimal("12")))
        session.commit()
        row = session.query(Candle).one()
        assert row.symbol == "BTCUSDT"
        assert row.close == Decimal("105.000000000000")
