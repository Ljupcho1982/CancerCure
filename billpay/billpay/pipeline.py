import json
from decimal import Decimal
from pathlib import Path

from . import classifier, extractor, guard
from .models import Email, PaymentDraft


def load_inbox(path):
    return [Email(**e) for e in json.loads(Path(path).read_text(encoding="utf-8"))]


def run(emails, config, extract_fn=extractor.extract):
    providers = config["providers"]
    known = {p["domain"]: name for name, p in providers.items()}
    max_amount = Decimal(str(config["max_amount"]))
    drafts, skipped = [], []
    for em in emails:
        is_bill, provider = classifier.classify(em, known)
        if not is_bill:
            skipped.append(em.id)
            continue
        if em.authenticated is False:
            drafts.append(PaymentDraft(None, "BLOCKED", ["sender failed SPF/DKIM (possible spoofing)"]))
            continue
        bill = extract_fn(em, provider)
        if bill is None:
            drafts.append(PaymentDraft(None, "BLOCKED", ["could not extract fields"]))
            continue
        reasons = guard.check(bill, providers, config.get("history", {}), max_amount)
        drafts.append(PaymentDraft(bill, "BLOCKED" if reasons else "READY_FOR_APPROVAL", reasons))
    return drafts, skipped
