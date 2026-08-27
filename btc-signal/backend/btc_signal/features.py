from __future__ import annotations

import math
import pandas as pd

FEATURE_VERSION = 'v1.0.0'


def _rsi(close: pd.Series, n: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs = gain / loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))


def _atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    prev = df['close'].shift(1)
    tr = pd.concat([(df['high'] - df['low']), (df['high'] - prev).abs(), (df['low'] - prev).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    required = {'open', 'high', 'low', 'close', 'volume'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'missing columns: {sorted(missing)}')
    x = df.sort_index().copy()
    x['return_1'] = x['close'].pct_change()
    x['log_return_1'] = x['close'].apply(math.log).diff()
    x['body_pct'] = (x['close'] - x['open']) / x['open']
    x['range_pct'] = (x['high'] - x['low']) / x['close']
    for n in (9, 21, 50, 100, 200):
        x[f'ema_{n}'] = x['close'].ewm(span=n, adjust=False).mean()
    x['ema_21_slope'] = x['ema_21'].pct_change(4)
    x['rsi_14'] = _rsi(x['close'])
    fast = x['close'].ewm(span=12, adjust=False).mean()
    slow = x['close'].ewm(span=26, adjust=False).mean()
    x['macd'] = fast - slow
    x['macd_signal'] = x['macd'].ewm(span=9, adjust=False).mean()
    x['atr_14'] = _atr(x)
    x['realized_vol_20'] = x['log_return_1'].rolling(20).std() * (20 ** 0.5)
    x['volume_mean_20'] = x['volume'].rolling(20).mean()
    x['relative_volume'] = x['volume'] / x['volume_mean_20']
    x['obv'] = (x['volume'] * x['return_1'].fillna(0).map(lambda v: 1 if v > 0 else -1 if v < 0 else 0)).cumsum()
    x['trend_score'] = (
        (x['close'] > x['ema_21']).astype(int)
        + (x['ema_21'] > x['ema_50']).astype(int)
        + (x['ema_50'] > x['ema_200']).astype(int)
    )
    return x
