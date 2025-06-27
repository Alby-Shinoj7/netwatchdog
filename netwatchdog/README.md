# NetWatchdog

NetWatchdog is a modular real-time packet analysis and network monitoring tool
written in Python. It captures network traffic, parses protocol information,
tracks sessions, maintains statistics, and displays a live dashboard in the
terminal.

**This project is intended for educational and testing purposes.**

## Requirements

- Python 3.10+
- [scapy](https://scapy.net/) for packet capture
- [rich](https://rich.readthedocs.io/) for the CLI dashboard
- Optional: `geoip2` for GeoIP lookups

Install dependencies using pip:

```bash
pip install scapy rich geoip2
```

## Usage

```bash
python -m netwatchdog.main -i eth0 --capture-time 60
```

The tool will capture packets on the specified interface, display live protocol
counts, and save a PCAP file when stopped.
