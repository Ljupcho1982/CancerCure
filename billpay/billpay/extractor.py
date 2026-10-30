"""Stage 2 (the LLM-agent stand-in). Regex extraction; replace with an LLM call
that returns the same fields as JSON, then validate with the same checks."""
import re
from decimal import Decimal, InvalidOperation
from typing import Optional

from .models import Bill, Email

AMOUNT = re.compile(r"(?:износ|amount due|вкупно)\D{0,15}([\d.,]+)\s*(ден|МКД|MKD|EUR|€)?", re.I)
ACCOUNT = re.compile(r"(?:жиро[- ]?сметка|сметка|IBAN)\s*[:№]?\s*([A-Z]{2}\d{2}[A-Z0-9 ]{10,30}|\d{15})", re.I)
REFERENCE = re.compile(r"(?:повикување на број|reference)\s*[:№]?\s*([\w\-/]+)", re.I)


def parse_amount(raw: str) -> Decimal:
    raw = raw.strip(".,")
    if "," in raw and "." in raw:            # 1.450,00 (MK) or 1,450.00
        dec = "," if raw.rfind(",") > raw.rfind(".") else "."
        thousands = "." if dec == "," else ","
        raw = raw.replace(thousands, "").replace(dec, ".")
    elif "," in raw:
        raw = raw.replace(",", ".") if len(raw.split(",")[-1]) != 3 else raw.replace(",", "")
    elif raw.count(".") == 1 and len(raw.split(".")[-1]) == 3:
        raw = raw.replace(".", "")           # 1.450 -> 1450
    return Decimal(raw)


def extract(email: Email, provider: str) -> Optional[Bill]:
    text = email.body
    a, acc, ref = AMOUNT.search(text), ACCOUNT.search(text), REFERENCE.search(text)
    if not (a and acc and ref):
        return None
    try:
        amount = parse_amount(a.group(1))
    except InvalidOperation:
        return None
    cur = (a.group(2) or "MKD").upper().replace("ДЕН", "MKD").replace("€", "EUR")
    return Bill(provider, amount, cur, acc.group(1).replace(" ", ""), ref.group(1), email.id)
