"""Application configuration (loads from environment)."""
import os
from pathlib import Path
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent


def _build_sqlalchemy_uri() -> str:
    """Support DATABASE_URL or DB_HOST/DB_USER/DB_PASSWORD/DB_NAME/DB_PORT."""
    explicit = os.environ.get("DATABASE_URL")
    if explicit:
        return explicit
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "3306")
    user = os.environ.get("DB_USER", "root")
    password = os.environ.get("DB_PASSWORD", "")
    name = os.environ.get("DB_NAME", "hotel_management")
    pwd = quote_plus(password) if password else ""
    auth = f"{user}:{pwd}" if pwd else user
    return f"mysql+pymysql://{auth}@{host}:{port}/{name}?charset=utf8mb4"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-change-me-in-production")
    SQLALCHEMY_DATABASE_URI = _build_sqlalchemy_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # GST percentage applied on subtotal for bills (optional)
    GST_PERCENT = float(os.environ.get("GST_PERCENT", "5"))
    # Real-time: SSE poll interval hint (seconds) for clients
    LIVE_REFRESH_SECONDS = int(os.environ.get("LIVE_REFRESH_SECONDS", "3"))
    # Branding (Swagat Corner). Override via env or place PNG at frontend/static/images/swagat-corner-menu.png
    BRAND_NAME = os.environ.get("BRAND_NAME", "Swagat Corner")
    # Default matches https://swagatcorner.com/ hero line
    BRAND_TAGLINE = os.environ.get(
        "BRAND_TAGLINE",
        "Where Every Bite Tells a Delicious Story!",
    )
    # Path under frontend/static/ (official logo downloaded from the website)
    BRAND_LOGO = os.environ.get("BRAND_LOGO", "images/swagat-logo.png")
