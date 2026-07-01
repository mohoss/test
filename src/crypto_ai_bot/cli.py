from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
import json

from .bot import CryptoAIBot
from .config import BotConfig
from .demo import DemoMarketData
from .exchange import CcxtMarketData


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the crypto AI trading bot once.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--demo", action="store_true", help="Run against generated demo candles. No network or API keys required.")
    mode.add_argument("--live-data", action="store_true", help="Fetch live candles using ccxt. Orders remain paper by default.")
    args = parser.parse_args()

    config = BotConfig.from_env()
    if args.live_data:
        data_provider = CcxtMarketData(config.exchange_id)
    else:
        data_provider = DemoMarketData()

    bot = CryptoAIBot(config, data_provider)
    result = bot.run_once()
    print(json.dumps(_json_ready(result), indent=2))


def _json_ready(value: object) -> object:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    return value


if __name__ == "__main__":
    main()
