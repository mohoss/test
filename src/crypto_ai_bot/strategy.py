from __future__ import annotations

from dataclasses import dataclass
import math
from collections.abc import Sequence

from .config import BotConfig
from .indicators import Candle, add_indicators


@dataclass(frozen=True)
class Signal:
    action: str
    confidence: float
    reason: str


class HybridAIStrategy:
    """Rule-based AI-style strategy with optional ML-friendly features.

    This is intentionally explainable: it combines trend, momentum and risk
    filters into a confidence score instead of promising impossible guaranteed
    profits. You can later replace ``score_market`` with a trained model.
    """

    def __init__(self, config: BotConfig):
        self.config = config

    def analyze(self, candles: Sequence[Candle]) -> Signal:
        data = add_indicators(
            candles,
            fast_ma=self.config.fast_ma,
            slow_ma=self.config.slow_ma,
            rsi_period=self.config.rsi_period,
        )
        if not data:
            return Signal("hold", 0.0, "not enough candle data")

        latest = data[-1]
        score = self.score_market(latest)
        confidence = min(abs(score), 1.0)

        if score > self.config.min_confidence:
            return Signal("buy", confidence, "uptrend confirmed by MA, RSI and volatility filters")
        if score < -self.config.min_confidence:
            return Signal("sell", confidence, "downtrend confirmed by MA, RSI and volatility filters")
        return Signal("hold", confidence, "signal confidence below threshold")

    @staticmethod
    def score_market(row: Candle) -> float:
        trend = 1 if row["fast_ma"] > row["slow_ma"] else -1
        momentum = (float(row["rsi"]) - 50) / 50
        volatility_penalty = min(max(float(row["volatility"]) * 10, 0), 0.35)
        raw_score = (0.65 * trend) + (0.35 * momentum)
        return math.copysign(max(abs(raw_score) - volatility_penalty, 0), raw_score)
