import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from netwatchdog import exporter
from netwatchdog.packet_parser import ParsedPacket


def test_export_csv_creates_directory(tmp_path):
    path = tmp_path / "exports" / "data.csv"
    packets = [ParsedPacket(protocol="TCP", src="1.1.1.1", dst="2.2.2.2", sport=1234, dport=80)]
    exporter.export_csv(packets, path)
    assert path.exists()


def test_export_json_creates_directory(tmp_path):
    path = tmp_path / "exports" / "data.json"
    packets = [ParsedPacket(protocol="UDP", src="1.1.1.1", dst="2.2.2.2", sport=53, dport=53)]
    exporter.export_json(packets, path)
    assert path.exists()
    data = json.loads(path.read_text())
    assert data[0]["protocol"] == "UDP"
