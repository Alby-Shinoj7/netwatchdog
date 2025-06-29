"""File storage utilities."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

from scapy.utils import wrpcap, rdpcap
from scapy.packet import Packet

from . import config
from .packet_parser import ParsedPacket

logger = logging.getLogger(__name__)


def save_pcap(packets: Iterable[ParsedPacket], filename: str) -> Path:
    path = config.PCAP_DIR / filename
    raw_packets = [pkt.raw for pkt in packets if pkt.raw]
    path.parent.mkdir(parents=True, exist_ok=True)
    wrpcap(str(path), raw_packets)
    logger.info("Saved PCAP to %s", path)
    return path


def load_pcap(path: Path) -> list[Packet]:
    """Load packets from a PCAP file."""
    logger.info("Loading PCAP from %s", path)
    packets = rdpcap(str(path))
    return list(packets)
