# 📬 Gmail to Google Sheets Automation

[![Python 3.11](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight Linux automation utility that fetches unread emails via the **Gmail API**, parses key headers and body contents, and appends them to a designated **Google Sheet** via the Google Sheets API.

Designed for automated execution via **Linux cron**, **systemd timers**, or as a scheduled **Docker container**.

---

## 🏗️ Architecture & Flow

```
[ Gmail Inbox ]
       │  (Fetch unread messages via OAuth2)
       ▼
[ email_parser ] ──► (Sanitize headers & truncate > 49k char cell limit)
       │
       ▼
[ Google Sheets API ] ──► (Append row: Sender, Subject, Date, Body)
       │
       ▼
[ Mark as Read ] ──► (Prevent duplicate processing & save state)
```

---

## ⚙️ Tech Stack

- **Python 3.11+**
- **Google Client APIs:** `google-api-python-client`, `google-auth-oauthlib`
- **Containerization:** Docker (non-root unprivileged container)
- **Scheduling:** Linux `systemd` timers / `crontab`

---

## 🔐 Credentials & OAuth2 Setup

Google API access requires OAuth 2.0 Client credentials:

1. Enable **Gmail API** and **Google Sheets API** in the [Google Cloud Console](https://console.cloud.google.com/).
2. Create an **OAuth 2.0 Client ID** (Application type: *Desktop App*).
3. Download the JSON credential file, rename it to `credentials.json`, and place it in the project root:
   ```bash
   cp ~/Downloads/client_secret_*.json ./credentials.json
   ```
4. Copy the environment configuration template:
   ```bash
   cp .env.example .env
   # Edit .env and set your SPREADSHEET_ID
   ```

### Token Refresh Lifecycle
On the first run, the script opens a browser prompt to grant read/write scopes. It then generates a local `token.json` file. Subsequent runs use `token.json` and automatically refresh expired access tokens using the embedded refresh token without user intervention.

> ⚠️ **Security Note:** `credentials.json` and `token.json` are strictly excluded from version control via `.gitignore`. Never commit them to Git.

---

## 🚀 Local Installation & Run

```bash
# 1. Clone repository
git clone https://github.com/tarunpandore/gmail-to-sheets.git
cd gmail-to-sheets

# 2. Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Execute script
python src/main.py
```

---

## 🐳 Docker Deployment

The repository includes a non-root, slim Dockerfile:

```bash
# Build Docker image
docker build -t gmail-to-sheets:latest .

# Run container with mounted credentials and environment variables
docker run --rm \
  -e SPREADSHEET_ID="your_google_spreadsheet_id" \
  -v "$(pwd)/credentials.json:/app/credentials.json:ro" \
  -v "$(pwd)/token.json:/app/token.json" \
  gmail-to-sheets:latest
```

---

## ⏰ Linux Automation: Cron & Systemd

### Option A: Standard Crontab (Run every hour)
```bash
crontab -e
# Add the following entry:
0 * * * * cd /opt/gmail-to-sheets && /opt/gmail-to-sheets/.venv/bin/python src/main.py >> /var/log/gmail-to-sheets.log 2>&1
```

### Option B: Systemd Service & Timer (Recommended for Production/Ops)

1. Create service unit `/etc/systemd/system/gmail-sheets.service`:
   ```ini
   [Unit]
   Description=Gmail to Google Sheets Sync Worker
   After=network.target

   [Service]
   Type=oneshot
   User=appuser
   WorkingDirectory=/opt/gmail-to-sheets
   EnvironmentFile=/opt/gmail-to-sheets/.env
   ExecStart=/opt/gmail-to-sheets/.venv/bin/python src/main.py
   StandardOutput=journal
   StandardError=journal
   ```

2. Create timer unit `/etc/systemd/system/gmail-sheets.timer`:
   ```ini
   [Unit]
   Description=Run Gmail to Sheets sync hourly

   [Timer]
   OnCalendar=hourly
   Persistent=true

   [Install]
   WantedBy=timers.target
   ```

3. Enable and start the timer:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now gmail-sheets.timer
   ```

---

## 📝 Logging Output

The script outputs structured logs with timestamps and log levels, making monitoring via `journalctl -u gmail-sheets` or Docker logs straightforward:

```text
2026-11-14 13:54:00,120 [INFO] gmail_to_sheets: Starting Gmail to Google Sheets synchronization run
2026-11-14 13:54:01,345 [INFO] gmail_to_sheets: Fetched 3 unread emails from inbox
2026-11-14 13:54:02,890 [INFO] gmail_to_sheets: Logged and marked as read: 18f1a23b45c6 (Subject: 'Invoice #1024')
2026-11-14 13:54:04,112 [INFO] gmail_to_sheets: Synchronization complete. Successfully processed 3 emails.
```
