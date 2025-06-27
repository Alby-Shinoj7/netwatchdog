"""Session tracking for TCP/UDP flows."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Dict, Tuple

from .packet_parser import ParsedPacket

logger = logging.getLogger(__name__)


@dataclass
class Session:
    src: str
    dst: str
    sport: int
    dport: int
    start_time: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    packet_count: int = 0
    bytes: int = 0


class SessionTracker:
    """Tracks TCP and UDP sessions."""

    def __init__(self) -> None:
        self.sessions: Dict[Tuple[str, str, int, int], Session] = {}

    def update(self, pkt: ParsedPacket) -> None:
        if pkt.sport is None or pkt.dport is None:
            return
        key = (pkt.src, pkt.dst, pkt.sport, pkt.dport)
        session = self.sessions.get(key)
        length = len(pkt.raw) if pkt.raw else 0
        if session:
            session.last_seen = time.time()
            session.packet_count += 1
            session.bytes += length
        else:
            self.sessions[key] = Session(
                src=pkt.src,
                dst=pkt.dst,
                sport=pkt.sport,
                dport=pkt.dport,
                packet_count=1,
                bytes=length,
            )

    def get_active_sessions(self) -> Dict[Tuple[str, str, int, int], Session]:
        return self.sessions
