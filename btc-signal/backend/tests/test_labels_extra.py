from btc_signal.labels import label_event


def test_invalid_label_event_returns_neutral():
    assert label_event([100], [0], 0) == 0
