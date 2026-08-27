from btc_signal.signals import Signal, decide


def test_filter_not_satisfied_is_no_trade():
    result = decide({'close': 100, 'atr_14': 2, 'trend_score': 1, 'rsi_14': 50}, True, True)
    assert result.signal is Signal.NO_TRADE
