"""Safety checks. Anything failing here is BLOCKED and needs a human."""
from decimal import Decimal
from .models import Bill


def check(bill: Bill, providers: dict, history: dict, max_amount: Decimal, spike: Decimal = Decimal("2")):
    reasons = []
    cfg = providers.get(bill.provider)
    if cfg is None:
        return ["provider not whitelisted"]
    if bill.account != cfg["account"].replace(" ", ""):
        reasons.append(f"account mismatch: email says {bill.account}, whitelist says {cfg['account']}")
    if bill.amount <= 0:
        reasons.append("non-positive amount")
    if bill.amount > max_amount:
        reasons.append(f"amount {bill.amount} exceeds limit {max_amount}")
    past = history.get(bill.provider)
    if past and bill.amount > Decimal(str(past)) * spike:
        reasons.append(f"amount > {spike}x previous ({past})")
    return reasons
