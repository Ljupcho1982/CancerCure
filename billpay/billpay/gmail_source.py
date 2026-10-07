"""Read-only Gmail source. Scope is gmail.readonly: this code cannot send, delete or modify mail.

Messages are held in memory only and never written to disk.
Needs: pip install -r requirements.txt, plus a Google Cloud OAuth client (credentials.json).
"""
import base64
import html
import re
from email.utils import parseaddr
from typing import List, Optional

from .models import Email

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
DEFAULT_QUERY = "newer_than:30d (сметка OR фактура OR invoice OR bill)"


def authenticate(credentials_path, token_path):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES).run_local_server(port=0)
        token_path.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def _b64(data: str) -> str:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4)).decode("utf-8", errors="replace")


def _strip_html(t: str) -> str:
    t = re.sub(r"(?is)<(script|style).*?</\1>", "", t)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", t)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def _body(payload: dict) -> str:
    """Prefer text/plain; fall back to stripped text/html. Walks nested multipart."""
    plain, rich = [], []

    def walk(part):
        mime, data = part.get("mimeType", ""), part.get("body", {}).get("data")
        if data and mime == "text/plain":
            plain.append(_b64(data))
        elif data and mime == "text/html":
            rich.append(_strip_html(_b64(data)))
        for sub in part.get("parts", []):
            walk(sub)

    walk(payload)
    return "\n".join(plain or rich).strip()


def parse_auth(headers: dict) -> Optional[bool]:
    """From the provider's Authentication-Results: True only if SPF or DKIM passed, False if one failed."""
    ar = headers.get("authentication-results", "").lower()
    if not ar:
        return None
    if re.search(r"\b(spf|dkim)=(fail|softfail|permerror)", ar):
        return False
    return True if re.search(r"\b(spf|dkim)=pass", ar) else None


def to_email(msg: dict) -> Email:
    headers = {h["name"].lower(): h["value"] for h in msg["payload"].get("headers", [])}
    return Email(
        id=msg["id"],
        sender=parseaddr(headers.get("from", ""))[1],
        subject=headers.get("subject", ""),
        body=_body(msg["payload"]),
        authenticated=parse_auth(headers),
    )


def fetch_emails(service, query: str = DEFAULT_QUERY, max_results: int = 50) -> List[Email]:
    out, token = [], None
    while len(out) < max_results:
        resp = service.users().messages().list(
            userId="me", q=query, maxResults=min(50, max_results - len(out)), pageToken=token).execute()
        for ref in resp.get("messages", []):
            msg = service.users().messages().get(userId="me", id=ref["id"], format="full").execute()
            out.append(to_email(msg))
        token = resp.get("nextPageToken")
        if not token:
            break
    return out
