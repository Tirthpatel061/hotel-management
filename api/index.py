"""
Vercel serverless entry: expose the Flask app from backend/app.py.
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_backend = str(_ROOT / "backend")
if _backend not in sys.path:
    sys.path.insert(0, _backend)

from app import app  # noqa: E402,F401
