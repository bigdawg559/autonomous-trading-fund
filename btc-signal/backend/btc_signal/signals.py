from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Signal(str, Enum):
    LONG = 'LONG'
    SHORT = 'SHORT'
    NO_TRADE = 'NO_TRADE'


@dataclass(frozen=True)
class SignalDecision:
    signal: Signal
    reason_codes: tuple[str, ...]
    entry: float | None = None
    stop_loss: float | None = None
    tp1: float | None = None
    tp2: float | None = None
    risk_reward: float | None = None


def decide(last: dict, data_fresh: bool, model_healthy: bool = False) -> SignalDecision:
    if not data_fresh:
        return SignalDecision(Signal.NO_TRADE, ('STALE_DATA',))
    if not model_healthy:
        return SignalDecision(Signal.NO_TRADE, ('MODEL_DEGRADED',))

    close = float(last['close'])
    atr = float(last.get('atr_14') or 0)
    trend = int(last.get('trend_score') or 0)
    rsi = float(last.get('rsi_14') or 50)
    if atr <= 0:
        return SignalDecision(Signal.NO_TRADE, ('INSUFFICIENT_VOLATILITY_DATA',))

    # This is deliberately a gate, not a claim of predictive accuracy.
    if trend >= 3 and 50 < rsi < 72:
        stop = close - 1.5 * atr
        tp1 = close + 1.5 * atr
        tp2 = close + 3.0 * atr
        return SignalDecision(Signal.LONG, ('TREND_UP', 'MOMENTUM_SUPPORT'), close, stop, tp1, tp2, 2.0)
    if trend <= 0 and 28 < rsi < 50:
        stop = close + 1.5 * atr
        tp1 = close - 1.5 * atr
        tp2 = close - 3.0 * atr
        return SignalDecision(Signal.SHORT, ('TREND_DOWN', 'MOMENTUM_SUPPORT'), close, stop, tp1, tp2, 2.0)
    return SignalDecision(Signal.NO_TRADE, ('NO_STATISTICAL_MODEL_READY', 'FILTER_NOT_SATISFIED'))
