"""Configuration settings for NetWatchdog.

This module defines constants and default settings used across the
NetWatchdog application.
"""

from pathlib import Path

# Default directories for storing data
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = DATA_DIR / "logs"
PCAP_DIR = DATA_DIR / "pcap"

# Network interface to capture packets on
DEFAULT_INTERFACE = "eth0"

# Packet capture filter (BPF syntax)
CAPTURE_FILTER = "ip or arp"

# Log file name
LOG_FILE = LOG_DIR / "netwatchdog.log"

# GeoIP database path (assumes GeoLite2 database)
GEOIP_DB = DATA_DIR / "GeoLite2-City.mmdb"
