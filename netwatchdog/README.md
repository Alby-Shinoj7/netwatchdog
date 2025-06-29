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
- Optional: `openai` for AI-generated summaries

Install dependencies using pip:

```bash
pip install scapy rich geoip2 openai  # optional
```

## Usage

```bash
python -m netwatchdog.main -i eth0 --capture-time 60
```

The tool will capture packets on the specified interface, display live protocol
counts, and save a PCAP file when stopped.

To analyze an existing PCAP instead of capturing live traffic:

```bash
python -m netwatchdog.main --pcap-file /path/to/file.pcap
```

## Running from source

The `python -m netwatchdog.main` command must either be executed from this
project's root directory or run with `PYTHONPATH` set to include it so that the
`netwatchdog` package can be located.

```bash
# from the project root
python -m netwatchdog.main

# from any other directory
PYTHONPATH=/path/to/netwatchdog python -m netwatchdog.main
```

## Summaries

After processing traffic or analyzing a PCAP, NetWatchdog prints a concise
summary of observed protocols and active sessions. To generate an AI-powered
summary instead, install the optional `openai` package and set the environment
variable `NETWATCHDOG_USE_AI=1`. The OpenAI API key is read from
`OPENAI_API_KEY`.
