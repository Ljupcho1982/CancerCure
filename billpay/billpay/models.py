from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


@dataclass
class Email:
    id: str
    sender: str
    subject: str
    body: str
    authenticated: Optional[bool] = None   # SPF/DKIM verdict from the mail provider; None = unknown


@dataclass
class Bill:
    provider: str
    amount: Decimal
    currency: str
    account: str          # destination account (IBAN / žiro-smetka)
    reference: str        # повикување на број
    email_id: str


@dataclass
class PaymentDraft:
    bill: Bill
    status: str           # READY_FOR_APPROVAL | BLOCKED
    reasons: list = field(default_factory=list)
    dry_run: bool = True
