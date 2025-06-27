"""Packet parsing utilities."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import ARP, Ether
from scapy.packet import Packet

logger = logging.getLogger(__name__)


@dataclass
class ParsedPacket:
    """Structured representation of a parsed packet."""

    protocol: str
    src: str
    dst: str
    sport: Optional[int] = None
    dport: Optional[int] = None
    raw: Packet | None = None


def parse_packet(packet: Packet) -> ParsedPacket | None:
    """Parse scapy packet into :class:`ParsedPacket`."""
    try:
        if Ether in packet:
            eth = packet[Ether]
            if ARP in packet:
                arp = packet[ARP]
                return ParsedPacket(
                    protocol="ARP",
                    src=arp.psrc,
                    dst=arp.pdst,
                    raw=packet,
                )
            if IP in packet:
                ip = packet[IP]
                if TCP in packet:
                    tcp = packet[TCP]
                    return ParsedPacket(
                        protocol="TCP",
                        src=ip.src,
                        dst=ip.dst,
                        sport=tcp.sport,
                        dport=tcp.dport,
                        raw=packet,
                    )
                if UDP in packet:
                    udp = packet[UDP]
                    return ParsedPacket(
                        protocol="UDP",
                        src=ip.src,
                        dst=ip.dst,
                        sport=udp.sport,
                        dport=udp.dport,
                        raw=packet,
                    )
                if ICMP in packet:
                    return ParsedPacket(
                        protocol="ICMP",
                        src=ip.src,
                        dst=ip.dst,
                        raw=packet,
                    )
                return ParsedPacket(
                    protocol="IP",
                    src=ip.src,
                    dst=ip.dst,
                    raw=packet,
                )
        return None
    except Exception as exc:  # pragma: no cover - best effort
        logger.error("Failed to parse packet: %s", exc)
        return None
