from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class BotConfig:
    """Runtime settings for the trading bot.

    The defaults are deliberately conservative and paper-trading first. Live
    trading must be enabled explicitly by setting ``TRADING_MODE=live``.
    """

    symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    exchange_id: str = "binance"
    trading_mode: str = "paper"
    starting_balance: float = 10_000.0
    risk_per_trade: float = 0.01
    max_daily_loss: float = 0.03
    stop_loss_pct: float = 0.02
    take_profit_pct: float = 0.04
    min_confidence: float = 0.58
    fast_ma: int = 12
    slow_ma: int = 26
    rsi_period: int = 14

    @classmethod
    def from_env(cls) -> "BotConfig":
        return cls(
            symbol=os.getenv("SYMBOL", cls.symbol),
            timeframe=os.getenv("TIMEFRAME", cls.timeframe),
            exchange_id=os.getenv("EXCHANGE_ID", cls.exchange_id),
            trading_mode=os.getenv("TRADING_MODE", cls.trading_mode),
            starting_balance=float(os.getenv("STARTING_BALANCE", cls.starting_balance)),
            risk_per_trade=float(os.getenv("RISK_PER_TRADE", cls.risk_per_trade)),
            max_daily_loss=float(os.getenv("MAX_DAILY_LOSS", cls.max_daily_loss)),
            stop_loss_pct=float(os.getenv("STOP_LOSS_PCT", cls.stop_loss_pct)),
            take_profit_pct=float(os.getenv("TAKE_PROFIT_PCT", cls.take_profit_pct)),
            min_confidence=float(os.getenv("MIN_CONFIDENCE", cls.min_confidence)),
        )
