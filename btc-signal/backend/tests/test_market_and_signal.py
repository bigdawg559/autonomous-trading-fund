from btc_signal.market import Candle, validate_candle
from btc_signal.signals import Signal, decide


def candle(**overrides):
    values = dict(open_time_ms=0, close_time_ms=900000, open=100, high=105, low=95, close=102, volume=10, closed=True)
    values.update(overrides)
    return Candle(**values)


def test_valid_candle():
    assert validate_candle(candle()) == []


def test_invalid_ohlc_is_rejected():
    assert 'invalid_high' in validate_candle(candle(high=101, close=102))


def test_signal_cannot_trade_when_model_is_unhealthy():
    result = decide({'close': 100, 'atr_14': 2, 'trend_score': 3, 'rsi_14': 60}, data_fresh=True, model_healthy=False)
    assert result.signal is Signal.NO_TRADE
    assert 'MODEL_DEGRADED' in result.reason_codes


def test_stale_data_is_no_trade():
    result = decide({'close': 100, 'atr_14': 2, 'trend_score': 3, 'rsi_14': 60}, data_fresh=False, model_healthy=True)
    assert result.signal is Signal.NO_TRADE
    assert 'STALE_DATA' in result.reason_codes
