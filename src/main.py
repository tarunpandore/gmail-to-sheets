from gmail_service import get_gmail_service, fetch_unread_emails

def main():
    service = get_gmail_service()
    messages = fetch_unread_emails(service)

    print(f"Fetched {len(messages)} unread emails")

    for msg in messages:
        print(f"Email ID: {msg['id']}")
        
        
if __name__ == "__main__":
    main()