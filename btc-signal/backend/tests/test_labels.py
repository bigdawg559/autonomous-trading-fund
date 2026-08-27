from btc_signal.labels import TripleBarrierConfig, label_event


def test_label_only_uses_future_bars():
    close = [100, 100, 102, 100]
    atr = [1, 1, 1, 1]
    assert label_event(close, atr, 0, TripleBarrierConfig(profit_atr=1.5, loss_atr=1.5, max_bars=3)) == 1


def test_unresolved_event_is_neutral():
    close = [100, 100.2, 99.9, 100.1]
    atr = [1, 1, 1, 1]
    assert label_event(close, atr, 0, TripleBarrierConfig(profit_atr=2, loss_atr=2, max_bars=3)) == 0
