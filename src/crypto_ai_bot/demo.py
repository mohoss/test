from __future__ import annotations

from .indicators import Candle


class DemoMarketData:
    """Deterministic market data provider for local dry-runs and tutorials."""

    def __init__(self, start_price: float = 30_000.0, candles: int = 120):
        self.start_price = start_price
        self.candles = candles

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 200) -> list[Candle]:
        count = min(limit, self.candles)
        rows: list[Candle] = []
        for index in range(count):
            trend = index * 35
            wave = 120 if index % 8 < 4 else -80
            close = self.start_price + trend + wave
            rows.append(
                {
                    "timestamp": float(index),
                    "open": close - 25,
                    "high": close + 90,
                    "low": close - 90,
                    "close": close,
                    "volume": 1_000 + index,
                }
            )
        return rows
