"""GeoIP lookup utilities."""

from __future__ import annotations

import logging
from ipaddress import ip_address
from pathlib import Path
from typing import Optional

try:
    import geoip2.database
except Exception:  # pragma: no cover - optional dependency
    geoip2 = None  # type: ignore

from .. import config

logger = logging.getLogger(__name__)


def lookup(ip: str) -> Optional[str]:
    """Return city and country for an IP if available."""
    if geoip2 is None:
        logger.debug("GeoIP database not available")
        return None
    db_path = Path(config.GEOIP_DB)
    if not db_path.exists():
        logger.debug("GeoIP DB not found: %s", db_path)
        return None
    try:
        with geoip2.database.Reader(str(db_path)) as reader:
            response = reader.city(ip_address(ip).exploded)
            city = response.city.name or ""
            country = response.country.name or ""
            return f"{city}, {country}".strip(", ")
    except Exception as exc:  # pragma: no cover - best effort
        logger.error("GeoIP lookup failed: %s", exc)
        return None
