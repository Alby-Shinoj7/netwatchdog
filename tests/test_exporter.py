import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from netwatchdog import exporter
from netwatchdog.packet_parser import ParsedPacket


def test_export_csv_creates_directory(tmp_path, monkeypatch):
    path = tmp_path / "exports" / "data.csv"
    packets = [ParsedPacket(protocol="TCP", src="1.1.1.1", dst="2.2.2.2", sport=1234, dport=80)]

    monkeypatch.setattr(
        "netwatchdog.utils.geoip.lookup",
        lambda ip: {"1.1.1.1": "A", "2.2.2.2": "B"}.get(ip),
    )

    exporter.export_csv(packets, path)
    assert path.exists()
    rows = path.read_text().splitlines()
    header = rows[0].split(",")
    assert "src_geo" in header and "dst_geo" in header
    data = rows[1].split(",")
    idx_src = header.index("src_geo")
    idx_dst = header.index("dst_geo")
    assert data[idx_src] == "A"
    assert data[idx_dst] == "B"


def test_export_json_creates_directory(tmp_path, monkeypatch):
    path = tmp_path / "exports" / "data.json"
    packets = [ParsedPacket(protocol="UDP", src="1.1.1.1", dst="2.2.2.2", sport=53, dport=53)]

    monkeypatch.setattr(
        "netwatchdog.utils.geoip.lookup",
        lambda ip: {"1.1.1.1": "A", "2.2.2.2": "B"}.get(ip),
    )

    exporter.export_json(packets, path)
    assert path.exists()
    data = json.loads(path.read_text())
    assert data[0]["protocol"] == "UDP"
    assert data[0]["src_geo"] == "A"
    assert data[0]["dst_geo"] == "B"
