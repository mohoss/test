from __future__ import annotations

from dataclasses import dataclass

from .config import BotConfig


@dataclass(frozen=True)
class OrderPlan:
    side: str
    amount: float
    entry_price: float
    stop_loss: float
    take_profit: float


class RiskManager:
    """Position sizing and loss limits for safer automated trading."""

    def __init__(self, config: BotConfig):
        self.config = config

    def build_order(self, side: str, balance: float, price: float) -> OrderPlan:
        risk_cash = balance * self.config.risk_per_trade
        stop_distance = price * self.config.stop_loss_pct
        amount = risk_cash / stop_distance
        if side == "buy":
            stop_loss = price * (1 - self.config.stop_loss_pct)
            take_profit = price * (1 + self.config.take_profit_pct)
        else:
            stop_loss = price * (1 + self.config.stop_loss_pct)
            take_profit = price * (1 - self.config.take_profit_pct)
        return OrderPlan(side, amount, price, stop_loss, take_profit)

    def daily_loss_exceeded(self, starting_equity: float, current_equity: float) -> bool:
        return (starting_equity - current_equity) / starting_equity >= self.config.max_daily_loss
