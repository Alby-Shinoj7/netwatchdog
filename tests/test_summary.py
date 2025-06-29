import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from netwatchdog.stats_engine import StatsEngine
from netwatchdog.session_tracker import SessionTracker, Session
from netwatchdog.summarizer import summarize


def test_plain_summary(monkeypatch):
    monkeypatch.delenv("NETWATCHDOG_USE_AI", raising=False)
    stats = StatsEngine()
    stats.protocol_counts["TCP"] = 2
    sessions = SessionTracker()
    sessions.sessions[("1.1.1.1", "2.2.2.2", 1234, 80)] = Session(
        src="1.1.1.1",
        dst="2.2.2.2",
        sport=1234,
        dport=80,
        packet_count=1,
        bytes=100,
    )
    summary = summarize(stats, sessions)
    assert "TCP: 2" in summary
    assert "1.1.1.1:1234 -> 2.2.2.2:80" in summary
