from btc_signal.market import BinanceSpotProvider


def test_provider_defaults():
    p = BinanceSpotProvider()
    assert p.symbol == 'btcusdt'
    assert p.interval == '15m'
