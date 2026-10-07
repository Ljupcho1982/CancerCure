import json
import os
import sys
from pathlib import Path

from . import extractor
from .ollama_extractor import make_extractor
from .pipeline import load_inbox, run

root = Path(__file__).resolve().parent.parent
inbox = sys.argv[1] if len(sys.argv) > 1 else root / "fixtures/inbox.json"
config = json.loads((root / "fixtures/config.json").read_text(encoding="utf-8"))
backend = os.environ.get("BILLPAY_BACKEND", "regex")  # regex | ollama
extract_fn = make_extractor() if backend == "ollama" else extractor.extract
print(f"Extractor: {backend}")
drafts, skipped = run(load_inbox(inbox), config, extract_fn)
print(f"Skipped (not bills): {skipped}\n")
for d in drafts:
    b = d.bill
    head = f"{b.provider}: {b.amount} {b.currency} -> {b.account} ref {b.reference}" if b else "(unparsed)"
    print(f"[{d.status}] {head}")
    for r in d.reasons:
        print(f"    ! {r}")
print("\nDRY RUN: nothing was paid. Approve manually in your bank.")
