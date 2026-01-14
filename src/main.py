import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gmail_service import (
    get_gmail_service,
    fetch_unread_emails,
    get_email,
    mark_as_read
)
from email_parser import parse_email
from sheets_service import get_sheets_service, append_row
from config import SPREADSHEET_ID, SHEET_NAME
from state_manager import load_processed_ids, save_processed_id


def main():
    gmail_service, creds = get_gmail_service()
    sheets_service = get_sheets_service(creds)
    processed_ids = load_processed_ids()

    messages = fetch_unread_emails(gmail_service)
    print(f"Fetched {len(messages)} unread emails")
    
    MAX_CELL_CHARS = 49000

    for msg in messages:
        if msg["id"] in processed_ids:
            continue
        
        full_message = get_email(gmail_service, msg["id"])
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
        
        mark_as_read(gmail_service, msg["id"])
        
    print("Emails successfully logged to Google Sheets.")
        
        
if __name__ == "__main__":
    main()