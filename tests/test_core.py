import unittest
from reviewreply.core import classify, draft_reply

class T(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(classify(5, "Great and friendly, recommend")["sentiment"], "positive")
    def test_negative(self):
        self.assertEqual(classify(1, "rude and late")["sentiment"], "negative")
    def test_legal_escalates(self):
        d = draft_reply({"name": "A B", "rating": 1, "text": "I will sue"}, "Acme")
        self.assertEqual(d["priority"], "ESCALATE"); self.assertTrue(d["needs_human_review"])
        self.assertIn("HOLD", d["draft_reply"])
    def test_safe_positive_reply(self):
        d = draft_reply({"name": "Sam", "rating": 5, "text": "Great, fast"}, "Acme")
        self.assertIn("Thank you", d["draft_reply"]); self.assertEqual(d["priority"], "LOW")
    def test_no_promises(self):
        d = draft_reply({"name": "X", "rating": 1, "text": "terrible"}, "Acme")
        self.assertNotIn("refund", d["draft_reply"].lower())
if __name__ == "__main__":
    unittest.main()
