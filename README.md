# Gmail to Google Sheets Automation

**Author:** Tarun

---

## Overview
This project reads unrerad emails from a Gmail inbox using the Gmail API and logs them into a Google Sheet using the Google Sheets API.

---

## Tech Stack
- Python 3
- Gmail API
- Google Sheets API
- OAuth 2.0

## Project Structure
    gmail-to-sheets/
    ├──src/
    |   ├──gmail_service.py # Gmail API auth & email fetching
    |   ├──sheets_service.py # Google Sheets API operations
    |   ├──email_parser.py # Extracts headers & body
    |   ├──state_manager.py # Prevents duplicate processing
    |   ├──main.py # Application entry point
    ├──credentials/
    |   ├──credentials.json # OAuth credentials (NOT commited)
    ├──config.py # Spreadsheet configuration
    ├──requirements.txt
    ├──README.md
    ├──.gitignore

## Setup Instruction

### 1. Clone Repository
```bash
git clone https://github.com/tarunpandore/gmail-to-sheets.git
cd gmail-to-sheets
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\Activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Google Cloud Setup
- Create a Google Cloud project
- Enable:
  - Gmail API
  - Google Sheets API
- Configure OAuth consent screen (**External**)
- Add your Gmail as a **Test User**
- Create OAuth Client ID (**Desktop App**)
- Download the `.json` file as `credentials.json` → place it inside `/credentials`

---

## OAuth Flow Explanation
- Uses OAuth 2.0 Installed App Flow
- User manually grants Gmail & Sheets access
- Access token stored locally in `token.json`
- Token automatically refreshed when expired
- No service accounts used (as required)

### Scopes Used
- `gmail.modify` → read & mark emails as read
- `spreadsheets` → append rows to Sheets

---

## Email Processing Logic
- Reads unread emails only from Inbox
- Extracts:
  - Sender
  - Subject
  - Date
  - Plain-text content
- HTML emails are safely converted to text
- Long email bodies are truncated to respect Google Sheets  
  *(There is a limit of 50,000 characters per cell)*

---

## Duplicate Prevention & State Persistence

**Problem:**  
Script should not reprocess emails on rerun.

**Solution:**
- Each Gmail has a unique message ID
- Processed IDs are stored locally in `processed_ids.txt`
- On every run:
  - IDs already processed are skipped
  - Only new emails are appended

**Why this approach:**
- No reliance on timestamps
- Gmail guarantees ID uniqueness
- Simple, reliable, and restart-safe

---

## Google Sheets Output
Each processed email is appended as a new row:

| From | Subject | Date | Content |
|------|---------|------|---------|

Rows are append-only, never overwritten.

---

## Proof of Execution
Screenshots included in `/proof` folder:
- Gmail inbox showing unread emails
- Google Sheet populated with at least 5 rows
- OAuth consent screen (email blurred if needed)

A short screen-recorded video demonstrates:
- End-to-end flow
- Gmail → Sheets data movement
- Duplicate prevention
- Re-running the script safely

---

## Limitations
- Attachments are not processed
- Email body is truncated if too long
- State stored locally (not distributed)

---

## Bonus Features Implemented
- HTML → plain text conversion
- Defensive handling of long emails
- Clean modular architecture
- Logging-friendly structure
- Retry-safe idempotent design