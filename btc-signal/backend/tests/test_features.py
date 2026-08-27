import pandas as pd

from btc_signal.features import FEATURE_VERSION, compute_features


def test_feature_version_and_columns():
    idx = pd.date_range('2026-01-01', periods=220, freq='15min', tz='UTC')
    df = pd.DataFrame({
        'open': 100 + pd.Series(range(220), index=idx) * 0.01,
        'high': 101 + pd.Series(range(220), index=idx) * 0.01,
        'low': 99 + pd.Series(range(220), index=idx) * 0.01,
        'close': 100 + pd.Series(range(220), index=idx) * 0.012,
        'volume': 1000.0,
    }, index=idx)
    out = compute_features(df)
    assert FEATURE_VERSION == 'v1.0.0'
    assert {'ema_21', 'rsi_14', 'atr_14', 'relative_volume', 'trend_score'} <= set(out.columns)
