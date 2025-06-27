"""Protocol analysis utilities."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from scapy.layers.dns import DNS, DNSQR
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import TCP
from scapy.packet import Packet

from .packet_parser import ParsedPacket

logger = logging.getLogger(__name__)


@dataclass
class HTTPInfo:
    method: str
    host: str
    path: str


@dataclass
class DNSQuery:
    qname: str


def extract_http(packet: Packet) -> Optional[HTTPInfo]:
    """Extract HTTP request information if present."""
    if packet.haslayer(HTTPRequest):
        req = packet[HTTPRequest]
        return HTTPInfo(method=req.Method.decode(), host=req.Host.decode(), path=req.Path.decode())
    return None


def extract_dns(packet: Packet) -> Optional[DNSQuery]:
    """Extract DNS query if present."""
    if packet.haslayer(DNS) and packet[DNS].qdcount > 0:
        qname = packet[DNSQR].qname.decode()
        return DNSQuery(qname=qname)
    return None
