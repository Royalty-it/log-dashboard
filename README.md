# Log Dashboard – Security Log Analysis

A lightweight web‑based dashboard that parses system logs, detects brute‑force attempts, and visualises events.

## Features
- Multi‑format log support (auth.log, Nginx, Windows Event Log)
- Interactive charts (event distribution, top offending IPs, timeline)
- IP geolocation with country flags
- Real‑time monitoring (auto‑updates)
- Brute‑force detection with Slack/email alerts
- Filtering by IP or event type

## Quick Start
```bash
pip install -r requirements.txt
python generate_logs.py
python app.py
```

## Screenshots
*(Add a screenshot here later)*

## Technologies
- Flask, Pandas, Plotly, Watchdog, Requests
