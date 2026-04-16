import unittest
from datetime import date, timedelta

from ingestion.scoring.rules import StoreData
from ingestion.scoring.scorer import compute_score, MAX_SCORE, RULES, StoreScorer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def future_date(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()

def past_date(days: int) -> str:
    return (date.today() - timedelta(days=days)).isoformat()


# ---------------------------------------------------------------------------
# HasEmailRule (+5)
# ---------------------------------------------------------------------------

class TestHasEmailRule(unittest.TestCase):

    def test_real_email_scores(self):
        result = compute_score(email="owner@gmail.com")
        self.assertTrue(result["breakdown"]["has_email"])

    def test_none_email_does_not_score(self):
        result = compute_score(email=None)
        self.assertFalse(result["breakdown"]["has_email"])

    def test_empty_email_does_not_score(self):
        result = compute_score(email="   ")
        self.assertFalse(result["breakdown"]["has_email"])

    # --- comma-separated: first valid address is used ---

    def test_comma_separated_first_valid_scores(self):
        # "alka@swanispice.com, ravi@swanispice.com" → first is valid → scores
        self.assertTrue(compute_score(email="alka@swanispice.com, ravi@swanispice.com")["breakdown"]["has_email"])

    def test_comma_first_invalid_second_valid_uses_second(self):
        # first candidate "bad" is invalid; second "good@foo.com" is valid
        self.assertTrue(compute_score(email="bad, good@foo.com")["breakdown"]["has_email"])

    def test_all_invalid_comma_list_does_not_score(self):
        # neither candidate passes → no score
        self.assertFalse(compute_score(email="bad1, bad2")["breakdown"]["has_email"])

    # --- hard malformed: no valid candidate at all ---

    def test_slash_concatenated_emails_do_not_score(self):
        # "mayank@sunatura.in/vikram@sunatura.in" — slash is illegal inside an address
        self.assertFalse(compute_score(email="mayank@sunatura.in/vikram@sunatura.in")["breakdown"]["has_email"])

    def test_space_in_single_email_does_not_score(self):
        self.assertFalse(compute_score(email="a @foo.com")["breakdown"]["has_email"])

    def test_multiple_at_does_not_score(self):
        self.assertFalse(compute_score(email="a@b@foo.com")["breakdown"]["has_email"])

    def test_no_at_does_not_score(self):
        self.assertFalse(compute_score(email="notanemail")["breakdown"]["has_email"])

    def test_missing_domain_tld_does_not_score(self):
        self.assertFalse(compute_score(email="user@localhost")["breakdown"]["has_email"])

    def test_semicolon_separator_does_not_score(self):
        self.assertFalse(compute_score(email="a@foo.com;b@bar.com")["breakdown"]["has_email"])


# ---------------------------------------------------------------------------
# OwnDomainEmailRule (+20)
# ---------------------------------------------------------------------------

class TestOwnDomainEmailRule(unittest.TestCase):

    def test_own_domain_scores(self):
        result = compute_score(email="komal@sowfresh.in")
        self.assertTrue(result["breakdown"]["has_website"])
        self.assertTrue(result["has_website"])

    def test_gmail_does_not_score(self):
        self.assertFalse(compute_score(email="owner@gmail.com")["breakdown"]["has_website"])

    def test_yahoo_does_not_score(self):
        self.assertFalse(compute_score(email="owner@yahoo.com")["breakdown"]["has_website"])

    def test_yahoo_in_does_not_score(self):
        self.assertFalse(compute_score(email="owner@yahoo.in")["breakdown"]["has_website"])

    def test_hotmail_does_not_score(self):
        self.assertFalse(compute_score(email="owner@hotmail.com")["breakdown"]["has_website"])

    def test_rediff_does_not_score(self):
        self.assertFalse(compute_score(email="owner@rediffmail.com")["breakdown"]["has_website"])

    def test_outlook_does_not_score(self):
        self.assertFalse(compute_score(email="owner@outlook.com")["breakdown"]["has_website"])

    def test_no_email_does_not_score(self):
        self.assertFalse(compute_score(email=None)["breakdown"]["has_website"])

    def test_malformed_email_does_not_score(self):
        self.assertFalse(compute_score(email="notanemail")["breakdown"]["has_website"])

    # --- concatenated / garbage emails must NOT score for has_website ---

    def test_slash_concatenated_does_not_score(self):
        # Real bug: "mayank@sunatura.in/vikram@sunatura.in"
        self.assertFalse(compute_score(email="mayank@sunatura.in/vikram@sunatura.in")["breakdown"]["has_website"])

    def test_comma_joined_own_domain_scores(self):
        # First valid address in comma list is "alka@swanispice.com" → own domain → scores
        self.assertTrue(compute_score(email="alka@swanispice.com,alka@swanispice.com")["breakdown"]["has_website"])

    def test_comma_joined_own_domain_second_entry_scores(self):
        # First is invalid, second "info@swanispice.com" is a valid own-domain address
        self.assertTrue(compute_score(email="alka/, info@swanispice.com")["breakdown"]["has_website"])

    def test_space_comma_all_garbage_does_not_score(self):
        # No valid candidate in the list
        self.assertFalse(compute_score(email="alka/, badentry")["breakdown"]["has_website"])

    def test_multiple_at_does_not_score_for_website(self):
        self.assertFalse(compute_score(email="a@b@company.in")["breakdown"]["has_website"])

    def test_domain_without_tld_does_not_score_for_website(self):
        self.assertFalse(compute_score(email="user@localhost")["breakdown"]["has_website"])


# ---------------------------------------------------------------------------
# HasAddressRule (+3)
# ---------------------------------------------------------------------------

class TestHasAddressRule(unittest.TestCase):

    def test_address_present_scores(self):
        result = compute_score(address="Farm no.9, Gurgaon, Haryana")
        self.assertTrue(result["breakdown"]["has_address"])

    def test_none_address_does_not_score(self):
        self.assertFalse(compute_score(address=None)["breakdown"]["has_address"])

    def test_empty_address_does_not_score(self):
        self.assertFalse(compute_score(address="  ")["breakdown"]["has_address"])


# ---------------------------------------------------------------------------
# HasProductsRule (+5)
# ---------------------------------------------------------------------------

class TestHasProductsRule(unittest.TestCase):

    def test_products_present_scores(self):
        result = compute_score(products="Rice, Wheat")
        self.assertTrue(result["breakdown"]["has_products"])

    def test_none_products_does_not_score(self):
        self.assertFalse(compute_score(products=None)["breakdown"]["has_products"])

    def test_empty_products_does_not_score(self):
        self.assertFalse(compute_score(products="")["breakdown"]["has_products"])


# ---------------------------------------------------------------------------
# HasTenPlusProductsRule (+5)
# ---------------------------------------------------------------------------

class TestHasTenPlusProductsRule(unittest.TestCase):

    def test_ten_products_scores(self):
        products = ", ".join([f"Product {i}" for i in range(10)])
        self.assertTrue(compute_score(products=products)["breakdown"]["has_ten_plus_products"])

    def test_eleven_products_scores(self):
        products = ", ".join([f"Product {i}" for i in range(11)])
        self.assertTrue(compute_score(products=products)["breakdown"]["has_ten_plus_products"])

    def test_nine_products_does_not_score(self):
        products = ", ".join([f"Product {i}" for i in range(9)])
        self.assertFalse(compute_score(products=products)["breakdown"]["has_ten_plus_products"])

    def test_no_products_does_not_score(self):
        self.assertFalse(compute_score(products=None)["breakdown"]["has_ten_plus_products"])


# ---------------------------------------------------------------------------
# CertValidOverSixMonthsRule (+10)
# ---------------------------------------------------------------------------

class TestCertValidOverSixMonthsRule(unittest.TestCase):

    def test_valid_over_six_months_scores(self):
        result = compute_score(valid_to=future_date(200))
        self.assertTrue(result["breakdown"]["cert_valid_over_six_months"])

    def test_valid_exactly_six_months_does_not_score(self):
        result = compute_score(valid_to=future_date(180))
        self.assertFalse(result["breakdown"]["cert_valid_over_six_months"])

    def test_valid_under_six_months_does_not_score(self):
        result = compute_score(valid_to=future_date(90))
        self.assertFalse(result["breakdown"]["cert_valid_over_six_months"])

    def test_expired_does_not_score(self):
        result = compute_score(valid_to=past_date(30))
        self.assertFalse(result["breakdown"]["cert_valid_over_six_months"])

    def test_none_valid_to_does_not_score(self):
        self.assertFalse(compute_score(valid_to=None)["breakdown"]["cert_valid_over_six_months"])

    def test_malformed_date_does_not_score(self):
        self.assertFalse(compute_score(valid_to="not-a-date")["breakdown"]["cert_valid_over_six_months"])


# ---------------------------------------------------------------------------
# Aggregate / ScoreResult
# ---------------------------------------------------------------------------

class TestScoreAggregate(unittest.TestCase):

    def test_default_score_is_zero(self):
        result = compute_score()
        self.assertEqual(result["score"], 0)

    def test_perfect_store_scores_max(self):
        result = compute_score(
            email="owner@organicfarm.in",
            products=", ".join([f"Product {i}" for i in range(15)]),
            address="123 Farm Road, Gurgaon",
            valid_to=future_date(365),
        )
        self.assertEqual(result["score"], MAX_SCORE)

    def test_breakdown_contains_all_rule_keys(self):
        result = compute_score()
        expected_keys = {r.key for r in RULES}
        self.assertEqual(set(result["breakdown"].keys()), expected_keys)

    def test_result_contains_required_keys(self):
        result = compute_score()
        self.assertIn("score", result)
        self.assertIn("has_website", result)
        self.assertIn("breakdown", result)

    def test_score_equals_sum_of_passing_rules(self):
        result = compute_score(
            email="owner@organicfarm.in",
            address="123 Farm Road",
        )
        expected = sum(
            r.points for r in RULES
            if result["breakdown"].get(r.key)
        )
        self.assertEqual(result["score"], expected)


if __name__ == "__main__":
    unittest.main()
