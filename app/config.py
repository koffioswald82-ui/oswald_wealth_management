import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH  = BASE_DIR / "database" / "oswald_wealth.db"

APP_NAME    = "Oswald Wealth Management"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Your AI Private Banker — Institutional Wealth Intelligence"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

DEFAULT_CURRENCY = "EUR"
DEFAULT_COUNTRY  = "France"
