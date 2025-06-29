import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from netwatchdog import storage
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
from scapy.utils import wrpcap


def test_load_pcap(tmp_path):
    path = tmp_path / "test.pcap"
    pkts = [Ether()/IP(src="1.1.1.1", dst="2.2.2.2")/TCP(),
            Ether()/IP(src="3.3.3.3", dst="4.4.4.4")/TCP()]
    wrpcap(str(path), pkts)

    loaded = storage.load_pcap(path)
    assert len(loaded) == 2
    assert loaded[0][IP].src == "1.1.1.1"
    assert loaded[1][IP].dst == "4.4.4.4"
