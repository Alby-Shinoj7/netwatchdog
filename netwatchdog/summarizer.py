"""Generate human readable summaries of capture statistics."""
from __future__ import annotations

import os
import logging

from .stats_engine import StatsEngine
from .session_tracker import SessionTracker, Session
from .utils import geoip

try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - optional
    openai = None  # type: ignore

logger = logging.getLogger(__name__)


def _build_text_summary(stats: StatsEngine, sessions: SessionTracker) -> str:
    """Return a plain text summary of stats and sessions."""
    lines: list[str] = []
    lines.append("Protocol counts:")
    for proto, count in stats.get_protocol_counts().items():
        lines.append(f"  {proto}: {count}")
    active = sessions.get_active_sessions()
    if not active:
        lines.append("No active sessions.")
    else:
        lines.append("Active sessions:")
        for s in active.values():
            src_geo = geoip.lookup(s.src)
            dst_geo = geoip.lookup(s.dst)
            geo_part = ""
            if src_geo or dst_geo:
                geo_part = f" ({src_geo or '?'} -> {dst_geo or '?'})"
            lines.append(
                f"  {s.src}:{s.sport} -> {s.dst}:{s.dport}{geo_part} "
                f"packets={s.packet_count} bytes={s.bytes}"
            )
    return "\n".join(lines)


def summarize(stats: StatsEngine, sessions: SessionTracker) -> str:
    """Generate a summary of the capture.

    If the ``NETWATCHDOG_USE_AI`` environment variable is set and the ``openai``
    package is available, an AI-generated summary will be returned. The API key
    is read from ``OPENAI_API_KEY``. Otherwise a simple text summary is used.
    """

    summary = _build_text_summary(stats, sessions)
    if os.getenv("NETWATCHDOG_USE_AI") and openai is not None:
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Summarize:\n{summary}"}],
                max_tokens=150,
            )
            return response.choices[0].message["content"].strip()
        except Exception as exc:  # pragma: no cover - best effort
            logger.error("AI summary failed: %s", exc)
    return summary
