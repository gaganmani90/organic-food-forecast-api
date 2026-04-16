import unittest
from ingestion.scoring.scorer import compute_score


class TestComputeScore(unittest.TestCase):

    # --- has_website / own-domain email (+20) ---

    def test_own_domain_email_scores_20(self):
        result = compute_score(email="komal.jain@sowfresh.in")
        self.assertEqual(result["score"], 20)
        self.assertTrue(result["has_website"])

    def test_gmail_scores_0(self):
        result = compute_score(email="owner@gmail.com")
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["has_website"])

    def test_yahoo_scores_0(self):
        result = compute_score(email="store@yahoo.com")
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["has_website"])

    def test_yahoo_in_scores_0(self):
        result = compute_score(email="store@yahoo.in")
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["has_website"])

    def test_rediff_scores_0(self):
        result = compute_score(email="owner@rediffmail.com")
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["has_website"])

    def test_hotmail_scores_0(self):
        result = compute_score(email="store@hotmail.com")
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["has_website"])

    def test_outlook_scores_0(self):
        result = compute_score(email="store@outlook.com")
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["has_website"])

    # --- edge cases ---

    def test_no_email_scores_0(self):
        result = compute_score(email=None)
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["has_website"])

    def test_empty_email_scores_0(self):
        result = compute_score(email="")
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["has_website"])

    def test_malformed_email_scores_0(self):
        result = compute_score(email="notanemail")
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["has_website"])

    def test_default_score_is_zero(self):
        """Every store starts at 0 before any criteria are met."""
        result = compute_score(email=None)
        self.assertEqual(result["score"], 0)

    def test_returns_score_and_has_website_keys(self):
        result = compute_score(email="test@example.com")
        self.assertIn("score", result)
        self.assertIn("has_website", result)


if __name__ == "__main__":
    unittest.main()
