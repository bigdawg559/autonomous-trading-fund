from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TripleBarrierConfig:
    profit_atr: float = 1.5
    loss_atr: float = 1.0
    max_bars: int = 16


def label_event(close: list[float], atr: list[float], start: int, cfg: TripleBarrierConfig = TripleBarrierConfig()) -> int:
    """Return +1 long, -1 short, 0 unresolved/neutral.

    The event starts at `start` and only inspects bars strictly after start,
    preventing the current bar from being used as a future outcome.
    """
    if start < 0 or start >= len(close) or start >= len(atr) or atr[start] <= 0:
        return 0
    entry = close[start]
    upper = entry + cfg.profit_atr * atr[start]
    lower = entry - cfg.loss_atr * atr[start]
    end = min(len(close), start + 1 + cfg.max_bars)
    for i in range(start + 1, end):
        if close[i] >= upper:
            return 1
        if close[i] <= lower:
            return -1
    return 0
