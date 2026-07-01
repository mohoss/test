from __future__ import annotations

from crypto_ai_bot.bot import CryptoAIBot
from crypto_ai_bot.config import BotConfig
from crypto_ai_bot.risk import RiskManager
from crypto_ai_bot.strategy import HybridAIStrategy


class StaticProvider:
    def __init__(self, closes: list[float]):
        self.closes = closes

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 200) -> list[dict[str, float]]:
        return [
            {
                "timestamp": index,
                "open": price,
                "high": price * 1.01,
                "low": price * 0.99,
                "close": price,
                "volume": 1000,
            }
            for index, price in enumerate(self.closes)
        ]


def test_strategy_generates_buy_signal_for_clear_uptrend() -> None:
    candles = StaticProvider([100 + i for i in range(80)]).fetch_ohlcv("BTC/USDT", "1h")
    signal = HybridAIStrategy(BotConfig()).analyze(candles)

    assert signal.action == "buy"
    assert signal.confidence >= BotConfig().min_confidence


def test_risk_manager_sizes_position_from_configured_risk() -> None:
    plan = RiskManager(BotConfig(risk_per_trade=0.01, stop_loss_pct=0.02)).build_order(
        "buy", balance=10_000, price=50_000
    )

    assert plan.amount == 0.1
    assert plan.stop_loss == 49_000
    assert plan.take_profit == 52_000


def test_bot_places_paper_order_when_signal_is_actionable() -> None:
    bot = CryptoAIBot(BotConfig(), StaticProvider([100 + i for i in range(80)]))
    result = bot.run_once()

    assert result["order"] is not None
    assert len(bot.broker.orders) == 1


def test_demo_provider_allows_local_bot_run() -> None:
    from crypto_ai_bot.demo import DemoMarketData

    bot = CryptoAIBot(BotConfig(), DemoMarketData())
    result = bot.run_once()

    assert result["signal"].action in {"buy", "sell", "hold"}
