"""Real-time statistics engine."""

from __future__ import annotations

import logging
import time
from collections import Counter, defaultdict
from typing import Dict

from .packet_parser import ParsedPacket

logger = logging.getLogger(__name__)


class StatsEngine:
    """Maintains live protocol statistics and bandwidth usage."""

    def __init__(self) -> None:
        self.protocol_counts: Counter[str] = Counter()
        self.bandwidth: Dict[int, int] = defaultdict(int)  # second -> bytes
        self.malformed: int = 0

    def update(self, pkt: ParsedPacket) -> None:
        now = int(time.time())
        length = len(pkt.raw) if pkt.raw else 0
        self.protocol_counts[pkt.protocol] += 1
        self.bandwidth[now] += length

    def get_protocol_counts(self) -> Dict[str, int]:
        return dict(self.protocol_counts)

    def get_bandwidth_last_n(self, seconds: int = 60) -> Dict[int, int]:
        now = int(time.time())
        return {ts: self.bandwidth.get(ts, 0) for ts in range(now - seconds, now + 1)}
