"""
Store scoring system.
Each criterion awards points on top of a default score of 0.
Add new criteria here as future requirements come in.
"""

GENERIC_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "yahoo.in", "hotmail.com",
    "rediffmail.com", "outlook.com", "live.com", "icloud.com",
}


def _has_own_domain_email(email: str) -> bool:
    """Returns True if email exists and uses a non-generic domain."""
    if not email or "@" not in email:
        return False
    domain = email.strip().lower().split("@")[-1]
    return domain not in GENERIC_EMAIL_DOMAINS


def compute_score(email: str = None) -> dict:
    """
    Compute a score for a store and return a breakdown.

    Returns:
        {
            "score": int,           # total score
            "has_website": bool,    # inferred from email domain
        }
    """
    score = 0
    has_website = False

    # +20: own-domain email → likely has a website
    if _has_own_domain_email(email):
        score += 20
        has_website = True

    # Future criteria go here:
    # if has_10_plus_products: score += 5
    # if cert_valid_over_6_months: score += 5
    # if has_complete_address: score += 3

    return {
        "score": score,
        "has_website": has_website,
    }
