#!/usr/bin/env python3
"""Run the crypto AI bot directly from a source checkout.

This wrapper is useful on servers (for example Oracle Cloud) where you want to
clone the repository and run the bot without creating a virtual environment or
installing the package first. It adds ``src`` to ``sys.path`` and then delegates
to the normal CLI.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from crypto_ai_bot.cli import main


if __name__ == "__main__":
    main()
