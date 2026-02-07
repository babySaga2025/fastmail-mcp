"""Utility helpers for environment handling and logging setup."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict
from zoneinfo import ZoneInfo

# Automatically handles CST (UTC-6) and CDT (UTC-5) transitions
DISPLAY_TZ = ZoneInfo("America/Chicago")


def to_local(dt: datetime) -> datetime:
    """Convert a datetime to the display timezone."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(DISPLAY_TZ)


def format_local(dt: datetime) -> str:
    """Format a datetime as a human-readable string in the display timezone."""
    local = to_local(dt)
    # %Z gives "CST" or "CDT" automatically
    return local.strftime("%Y-%m-%d %I:%M %p %Z")

_ENV_COMMENT_PREFIXES = ("#", "//")


def load_env(path: Path | None = None) -> Dict[str, str]:
    """Load key/value pairs from a .env file without overriding existing vars."""

    env_path = path or Path(".env")
    if env_path.exists():
        for raw_line in env_path.read_text().splitlines():
            line = raw_line.strip()
            if not line or line.startswith(_ENV_COMMENT_PREFIXES):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())
    return {key: os.environ[key] for key in os.environ.keys()}


def get_required_env(key: str) -> str:
    """Return a required environment variable or raise a helpful error."""

    try:
        value = os.environ[key]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise RuntimeError(f"Missing required environment variable: {key}") from exc
    if not value:
        raise RuntimeError(f"Environment variable {key} is empty")
    return value
