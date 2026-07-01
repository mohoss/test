from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .indicators import Candle
from .risk import OrderPlan


class MarketDataProvider(Protocol):
    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 200) -> list[Candle]:
        ...


@dataclass
class PaperBroker:
    """Simple paper broker that records planned orders without real execution."""

    balance: float
    orders: list[OrderPlan] = field(default_factory=list)

    def submit(self, plan: OrderPlan) -> OrderPlan:
        self.orders.append(plan)
        return plan


class CcxtMarketData:
    """Fetch OHLCV candles through ccxt when the optional live dependency exists."""

    def __init__(self, exchange_id: str):
        import ccxt

        exchange_cls = getattr(ccxt, exchange_id)
        self.exchange = exchange_cls({"enableRateLimit": True})

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 200) -> list[Candle]:
        rows = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        keys = ["timestamp", "open", "high", "low", "close", "volume"]
        return [dict(zip(keys, row, strict=True)) for row in rows]
