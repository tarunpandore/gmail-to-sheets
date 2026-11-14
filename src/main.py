import sys
import os
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from gmail_service import (
    get_gmail_service,
    fetch_unread_emails,
    get_email,
    mark_as_read
)
from email_parser import parse_email
from sheets_service import get_sheets_service, append_row
from config import SPREADSHEET_ID, SHEET_NAME, LOG_LEVEL
from state_manager import load_processed_ids, save_processed_id

# Configure structured logging for automation & systemd/Docker logs
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("gmail_to_sheets")


def main():
    logger.info("Starting Gmail to Google Sheets synchronization run")
    
    if SPREADSHEET_ID == "your_sheet_id":
        logger.warning("SPREADSHEET_ID is set to placeholder value. Set SPREADSHEET_ID in your environment or config.py.")

    gmail_service, creds = get_gmail_service()
    sheets_service = get_sheets_service(creds)
    processed_ids = load_processed_ids()

    messages = fetch_unread_emails(gmail_service)
    logger.info("Fetched %d unread emails from inbox", len(messages))
    
    MAX_CELL_CHARS = 49000
    processed_count = 0

    for msg in messages:
        msg_id = msg["id"]
        if msg_id in processed_ids:
            logger.debug("Skipping already processed message id: %s", msg_id)
            continue
        
        full_message = get_email(gmail_service, msg_id)
        parsed = parse_email(full_message)
        
        content = parsed["content"]
        if len(content) > MAX_CELL_CHARS:
            content = content[:MAX_CELL_CHARS] + "\n[TRUNCATED]"
        
        row = [
            parsed["from"],
            parsed["subject"],
            parsed["date"],
            content
        ]
        
        append_row(
            sheets_service,
            SPREADSHEET_ID,
            SHEET_NAME,
            row
        )
        
        mark_as_read(gmail_service, msg_id)
        save_processed_id(msg_id)
        processed_count += 1
        logger.info("Logged and marked as read: %s (Subject: '%s')", msg_id, parsed["subject"][:50])
        
    logger.info("Synchronization complete. Successfully processed %d emails.", processed_count)
        
        
if __name__ == "__main__":
    main()
