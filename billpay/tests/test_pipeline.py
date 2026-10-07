import json, unittest
from decimal import Decimal
from pathlib import Path
from billpay.extractor import parse_amount
from billpay.pipeline import load_inbox, run

R = Path(__file__).resolve().parent.parent


class T(unittest.TestCase):
    def test_amounts(self):
        self.assertEqual(parse_amount("1.450"), Decimal("1450"))
        self.assertEqual(parse_amount("1.450,50"), Decimal("1450.50"))
        self.assertEqual(parse_amount("620"), Decimal("620"))

    def test_flow(self):
        cfg = json.loads((R / "fixtures/config.json").read_text(encoding="utf-8"))
        drafts, skipped = run(load_inbox(R / "fixtures/inbox.json"), cfg)
        self.assertEqual(skipped, ["2"])
        self.assertEqual([d.status for d in drafts], ["READY_FOR_APPROVAL", "BLOCKED", "BLOCKED"])
        self.assertTrue(any("account mismatch" in r for r in drafts[1].reasons))
        self.assertTrue(any("previous" in r for r in drafts[2].reasons))
        self.assertTrue(all(d.dry_run for d in drafts))

    def test_ollama_extractor_with_fake_model(self):
        from billpay.ollama_extractor import make_extractor
        cfg = json.loads((R / "fixtures/config.json").read_text(encoding="utf-8"))
        good = '{"amount":"1.450","currency":"MKD","account":"MK07300000000012345","reference":"X1"}'
        outs = iter([good, "not json", '{"amount":"1.450"}', good])
        ex = make_extractor(chat_fn=lambda *a: next(outs))
        drafts, _ = run(load_inbox(R / "fixtures/inbox.json"), cfg, ex)
        self.assertEqual(drafts[0].status, "READY_FOR_APPROVAL")
        self.assertEqual(drafts[0].bill.amount, Decimal("1450"))
        self.assertEqual(drafts[1].reasons, ["could not extract fields"])
        self.assertEqual(drafts[2].reasons, ["could not extract fields"])


class FakeGmail:
    """Mimics service.users().messages().list/get(...).execute()."""
    def __init__(self, msgs): self.m = {x["id"]: x for x in msgs}
    def users(self): return self
    def messages(self): return self
    def list(self, **kw): self._r = {"messages": [{"id": i} for i in self.m]}; return self
    def get(self, id, **kw): self._r = self.m[id]; return self
    def execute(self): return self._r


class GmailTests(unittest.TestCase):
    def _msg(self, id, frm, mime, text, auth=None):
        import base64
        hdr = [{"name": "From", "value": frm}, {"name": "Subject", "value": "Сметка"}]
        if auth: hdr.append({"name": "Authentication-Results", "value": auth})
        data = base64.urlsafe_b64encode(text.encode()).decode().rstrip("=")
        return {"id": id, "payload": {"headers": hdr, "mimeType": "multipart/alternative",
                "parts": [{"mimeType": mime, "body": {"data": data}}]}}

    def test_fetch_and_flow(self):
        from billpay.gmail_source import fetch_emails
        cfg = json.loads((R / "fixtures/config.json").read_text(encoding="utf-8"))
        body = "Износ: 1.450 ден. Жиро-сметка: MK07300000000012345. Повикување на број: A1"
        svc = FakeGmail([
            self._msg("a", "EVN <billing@evn.mk>", "text/plain", body, "mx; dkim=pass"),
            self._msg("b", "billing@evn.mk", "text/html", "<p>" + body.replace(". ", ".<br>") + "</p>", "mx; spf=fail"),
        ])
        emails = fetch_emails(svc)
        self.assertEqual(emails[0].sender, "billing@evn.mk")
        self.assertTrue(emails[0].authenticated)
        self.assertFalse(emails[1].authenticated)
        drafts, _ = run(emails, cfg)
        self.assertEqual(drafts[0].status, "READY_FOR_APPROVAL")
        self.assertEqual(drafts[1].reasons, ["sender failed SPF/DKIM (possible spoofing)"])


if __name__ == "__main__":
    unittest.main()
