"""Stage 1 (the fast 'Jev'-style filter). Rule-based stand-in: returns is_bill + provider.

Swap `classify` for a small-model call; keep the same signature.
"""
import re
from typing import Optional, Tuple

from .models import Email

KEYWORDS = re.compile(r"сметка|фактура|за плаќање|рок на плаќање|invoice|bill|amount due", re.I)


def classify(email: Email, known_senders: dict) -> Tuple[bool, Optional[str]]:
    domain = email.sender.rsplit("@", 1)[-1].lower()
    provider = known_senders.get(domain)
    is_bill = bool(KEYWORDS.search(email.subject + " " + email.body))
    return (is_bill and provider is not None), provider
