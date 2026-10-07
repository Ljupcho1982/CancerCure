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


if __name__ == "__main__":
    unittest.main()
