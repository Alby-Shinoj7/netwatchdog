"""Packet capture engine using scapy.

This module captures live packets from a network interface and forwards
raw packets to registered handlers for further processing.
"""

from __future__ import annotations

import logging
from typing import Callable, Iterable

from scapy.all import AsyncSniffer

from . import config

logger = logging.getLogger(__name__)


class CaptureEngine:
    """Capture packets using scapy's AsyncSniffer."""

    def __init__(self, interface: str | None = None, bpf_filter: str | None = None):
        self.interface = interface or config.DEFAULT_INTERFACE
        self.bpf_filter = bpf_filter or config.CAPTURE_FILTER
        self._callbacks: list[Callable[[object], None]] = []
        self.sniffer: AsyncSniffer | None = None

    def register_callback(self, callback: Callable[[object], None]) -> None:
        """Register a callback to be invoked for each captured packet."""
        self._callbacks.append(callback)

    def start(self) -> None:
        """Start asynchronous packet capture."""
        logger.info("Starting packet capture on %s", self.interface)
        self.sniffer = AsyncSniffer(
            iface=self.interface,
            filter=self.bpf_filter,
            prn=self._handle_packet,
            store=False,
        )
        self.sniffer.start()

    def stop(self) -> None:
        """Stop packet capture."""
        if self.sniffer:
            logger.info("Stopping packet capture")
            self.sniffer.stop()
            self.sniffer = None

    def _handle_packet(self, packet: object) -> None:
        for cb in self._callbacks:
            try:
                cb(packet)
            except Exception as exc:  # pragma: no cover - best effort
                logger.error("Error in callback: %s", exc)
