"""Entry point for NetWatchdog."""

from __future__ import annotations

import logging
import signal
from argparse import ArgumentParser
from pathlib import Path

from . import config
from .alerts import AlertEngine
from .capture_engine import CaptureEngine
from .cli_dashboard import CLIDashboard
from .packet_parser import parse_packet
from .session_tracker import SessionTracker
from .stats_engine import StatsEngine
from .storage import save_pcap

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("netwatchdog")


def main() -> None:
    parser = ArgumentParser(description="NetWatchdog - network monitoring tool")
    parser.add_argument("-i", "--interface", help="Network interface", default=config.DEFAULT_INTERFACE)
    parser.add_argument("--capture-time", type=int, default=30, help="Seconds to capture")
    args = parser.parse_args()

    stats = StatsEngine()
    sessions = SessionTracker()
    alerts = AlertEngine(stats)

    captured: list = []

    def handle_packet(packet: object) -> None:
        parsed = parse_packet(packet)
        if not parsed:
            return
        captured.append(parsed)
        stats.update(parsed)
        sessions.update(parsed)
        alerts.process(parsed)

    capturer = CaptureEngine(interface=args.interface)
    capturer.register_callback(handle_packet)

    dashboard = CLIDashboard(stats)
    dashboard.start()

    def shutdown(*_args):
        logger.info("Stopping NetWatchdog")
        capturer.stop()
        dashboard.stop()
        save_pcap(captured, "capture.pcap")
        exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    capturer.start()

    logger.info("Capturing for %d seconds...", args.capture_time)
    try:
        signal.signal(signal.SIGALRM, shutdown)
        signal.alarm(args.capture_time)
        signal.pause()
    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":  # pragma: no cover
    main()
