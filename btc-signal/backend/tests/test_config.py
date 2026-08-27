from btc_signal.config import Settings


def test_defaults_target_btcusdt_15m():
    s = Settings()
    assert s.symbol == 'BTCUSDT'
    assert s.timeframe == '15m'
