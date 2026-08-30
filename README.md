# Log Dashboard - Security Log Analysis

A lightweight web-based dashboard for parsing system logs (SSH, Nginx, Windows Event Log), detecting bruteforce attacks, visualizing event data and sending real-time alerts.

Features

-   Multiformat log support - auth.log, Nginx access log, Windows Event Log
-   Interactive charts - event distribution, top offending IPs, timeline
-   IP geolocation - country flags to every source IP address
-   Realtime monitoring - auto-updating when the log file is modified
-   Brute-force detection - Slack or email alerts
-   Filtering - filter events based on IP or log event type

Quick Start

1.  Clone the repo:

``bash

git clone https://github.com/Royalty-it/log-dashboard.git

cd log-dashboard

`

2.  Create a virtual environment and install dependencies:

`bash

python -m venv venv

source venv/bin/activate # Windows: venv\Scripts\activate

pip install -r requirements.txt

`

3.  Generate a sample log file (or use your own):

`bash

python generate_logs.py

`

4.  Run the application:

`bash

python app.py

``

Open http://127.0.0.1:5000 in your browser.

## Technologies
- Flask, Pandas, Plotly, Watchdog, Requests
