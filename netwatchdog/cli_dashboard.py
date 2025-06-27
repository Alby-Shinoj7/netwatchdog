"""Real-time CLI dashboard using rich."""

from __future__ import annotations

import logging
import time
from threading import Thread

from rich.console import Console
from rich.table import Table

from .stats_engine import StatsEngine

logger = logging.getLogger(__name__)
console = Console()


class CLIDashboard(Thread):
    """Background thread to display stats."""

    def __init__(self, stats: StatsEngine, refresh: float = 1.0) -> None:
        super().__init__(daemon=True)
        self.stats = stats
        self.refresh = refresh
        self.running = False

    def run(self) -> None:
        self.running = True
        while self.running:
            self.render()
            time.sleep(self.refresh)

    def stop(self) -> None:
        self.running = False

    def render(self) -> None:
        console.clear()
        table = Table(title="Protocol Counts")
        table.add_column("Protocol")
        table.add_column("Count")
        for proto, count in self.stats.get_protocol_counts().items():
            table.add_row(proto, str(count))
        console.print(table)
