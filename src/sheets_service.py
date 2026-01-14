from googleapiclient.discovery import build


def get_sheets_service(creds):
    service = build("sheets", "v4", credentials=creds)
    return service


def append_row(service, spreadsheet_id, sheet_name, row_values):
    body = {
        "values": [row_values]
    }
    
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A:D",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()