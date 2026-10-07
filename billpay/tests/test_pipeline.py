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


if __name__ == "__main__":
    unittest.main()
