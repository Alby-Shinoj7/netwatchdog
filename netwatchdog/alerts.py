"""Simple alert detection."""

from __future__ import annotations

import logging
import time
from typing import Dict, Set

from .packet_parser import ParsedPacket
from .stats_engine import StatsEngine

logger = logging.getLogger(__name__)


class AlertEngine:
    """Detects basic anomalies on the network."""

    def __init__(self, stats: StatsEngine) -> None:
        self.stats = stats
        self.known_macs: Set[str] = set()
        self.bandwidth_threshold = 10_000_000  # bytes per second

    def process(self, pkt: ParsedPacket) -> None:
        if pkt.protocol == "ARP" and pkt.src not in self.known_macs:
            logger.warning("New device detected: %s", pkt.src)
            self.known_macs.add(pkt.src)
        # bandwidth check
        bw = sum(self.stats.bandwidth.get(ts, 0) for ts in self.stats.bandwidth)
        if bw > self.bandwidth_threshold:
            logger.warning("High bandwidth usage detected: %d bytes", bw)
