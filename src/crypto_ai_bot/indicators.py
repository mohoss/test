from __future__ import annotations

from collections.abc import Sequence

Candle = dict[str, float]


def add_indicators(candles: Sequence[Candle], fast_ma: int = 12, slow_ma: int = 26, rsi_period: int = 14) -> list[Candle]:
    """Add common technical-analysis features used by the decision engine."""
    enriched: list[Candle] = []
    closes = [float(candle["close"]) for candle in candles]
    returns = [0.0] + [(closes[i] / closes[i - 1]) - 1 for i in range(1, len(closes))]

    for index, candle in enumerate(candles):
        if index + 1 < max(fast_ma, slow_ma, rsi_period + 1):
            continue
        row = dict(candle)
        row["fast_ma"] = mean(closes[index - fast_ma + 1 : index + 1])
        row["slow_ma"] = mean(closes[index - slow_ma + 1 : index + 1])
        row["return"] = returns[index]
        row["volatility"] = stddev(returns[index - slow_ma + 1 : index + 1])
        row["rsi"] = rsi(closes[index - rsi_period : index + 1])
        enriched.append(row)
    return enriched


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def stddev(values: Sequence[float]) -> float:
    avg = mean(values)
    variance = sum((value - avg) ** 2 for value in values) / len(values)
    return variance**0.5


def rsi(closes: Sequence[float]) -> float:
    gains = 0.0
    losses = 0.0
    for previous, current in zip(closes, closes[1:]):
        change = current - previous
        if change >= 0:
            gains += change
        else:
            losses += abs(change)
    if losses == 0:
        return 100.0
    relative_strength = gains / losses
    return 100 - (100 / (1 + relative_strength))
