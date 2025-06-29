"""Export captured data to CSV or JSON."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Sequence

from .packet_parser import ParsedPacket
from .utils import geoip


def export_csv(packets: Iterable[ParsedPacket], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "protocol",
            "src",
            "dst",
            "sport",
            "dport",
            "src_geo",
            "dst_geo",
        ])
        for pkt in packets:
            writer.writerow([
                int(pkt.raw.time) if pkt.raw else 0,
                pkt.protocol,
                pkt.src,
                pkt.dst,
                pkt.sport or "",
                pkt.dport or "",
                geoip.lookup(pkt.src) or "",
                geoip.lookup(pkt.dst) or "",
            ])


def export_json(packets: Sequence[ParsedPacket], path: Path) -> None:
    data = [
        {
            "timestamp": int(pkt.raw.time) if pkt.raw else 0,
            "protocol": pkt.protocol,
            "src": pkt.src,
            "dst": pkt.dst,
            "sport": pkt.sport,
            "dport": pkt.dport,
            "src_geo": geoip.lookup(pkt.src),
            "dst_geo": geoip.lookup(pkt.dst),
        }
        for pkt in packets
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
