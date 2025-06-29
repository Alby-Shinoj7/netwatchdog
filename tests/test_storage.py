import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from netwatchdog import storage, config

class DummyPacket:
    def __init__(self, raw):
        self.raw = raw


def test_save_pcap_creates_directory(tmp_path, monkeypatch):
    pcap_dir = tmp_path / "pcap"
    monkeypatch.setattr(config, "PCAP_DIR", pcap_dir)
    assert not pcap_dir.exists()

    packets = [DummyPacket(b"foo"), DummyPacket(b"bar")]
    filename = "test.pcap"
    path = storage.save_pcap(packets, filename)

    assert path == pcap_dir / filename
    assert path.exists()
