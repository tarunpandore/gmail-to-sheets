import base64


def _get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def parse_email(message):
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    sender = _get_header(headers, "From")
    subject = _get_header(headers, "Subjects")
    date = _get_header(headers, "Date")

    body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                body_data = part["body"].get("data")
                if body_data:
                    body = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
                    break
    else:
        body_data = payload.get("body", {}).get("data")
        if body_data:
            body = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")

    return {
        "from": sender,
        "subject": subject,
        "date": date,
        "content": body.strip()
    }