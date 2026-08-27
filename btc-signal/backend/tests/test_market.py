from btc_signal.market import Candle


def test_candle_timestamp_is_utc():
    c = Candle(0, 900000, 100, 101, 99, 100.5, 10, True)
    assert c.timestamp.tzinfo is not None
