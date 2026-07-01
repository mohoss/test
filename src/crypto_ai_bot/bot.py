from __future__ import annotations

from .config import BotConfig
from .exchange import MarketDataProvider, PaperBroker
from .risk import RiskManager
from .strategy import HybridAIStrategy, Signal


class CryptoAIBot:
    """Coordinates market analysis, risk checks and order planning."""

    def __init__(self, config: BotConfig, data_provider: MarketDataProvider):
        self.config = config
        self.data_provider = data_provider
        self.strategy = HybridAIStrategy(config)
        self.risk = RiskManager(config)
        self.broker = PaperBroker(config.starting_balance)

    def run_once(self) -> dict[str, object]:
        candles = self.data_provider.fetch_ohlcv(self.config.symbol, self.config.timeframe)
        signal = self.strategy.analyze(candles)
        last_price = float(candles[-1]["close"])

        if signal.action == "hold":
            return {"signal": signal, "order": None}

        if self.risk.daily_loss_exceeded(self.config.starting_balance, self.broker.balance):
            return {"signal": Signal("hold", 0.0, "daily loss limit reached"), "order": None}

        plan = self.risk.build_order(signal.action, self.broker.balance, last_price)
        return {"signal": signal, "order": self.broker.submit(plan)}
