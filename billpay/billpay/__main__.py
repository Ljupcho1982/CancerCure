import json
import os
import sys
from pathlib import Path

from . import extractor
from .ollama_extractor import make_extractor
from .pipeline import load_inbox, run

root = Path(__file__).resolve().parent.parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
use_gmail = "--gmail" in sys.argv
config = json.loads((root / "fixtures/config.json").read_text(encoding="utf-8"))
backend = os.environ.get("BILLPAY_BACKEND", "regex")  # regex | ollama
extract_fn = make_extractor() if backend == "ollama" else extractor.extract
print(f"Extractor: {backend}")
if use_gmail:
    from .gmail_source import authenticate, fetch_emails
    emails = fetch_emails(authenticate(root / "credentials.json", root / "token.json"))
    print(f"Gmail: read {len(emails)} messages (read-only)")
else:
    emails = load_inbox(args[0] if args else root / "fixtures/inbox.json")
drafts, skipped = run(emails, config, extract_fn)
print(f"Skipped (not bills): {skipped}\n")
for d in drafts:
    b = d.bill
    head = f"{b.provider}: {b.amount} {b.currency} -> {b.account} ref {b.reference}" if b else "(unparsed)"
    print(f"[{d.status}] {head}")
    for r in d.reasons:
        print(f"    ! {r}")
print("\nDRY RUN: nothing was paid. Approve manually in your bank.")
