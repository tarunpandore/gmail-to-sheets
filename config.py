import os

# Google Sheets Configuration (Environment variable support with fallback)
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "your_sheet_id")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
