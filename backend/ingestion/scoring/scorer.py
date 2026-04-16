"""
StoreScorer: orchestrates all scoring rules and returns a ScoreResult.

Usage
-----
    from ingestion.scoring.scorer import compute_score

    result = compute_score(
        email="owner@sowfresh.in",
        products="Rice, Wheat, Dal",
        address="Farm no.9, Gurgaon",
        valid_to="2026-12-31",
    )
    result.score        # 43
    result.has_website  # True
    result.breakdown    # {"has_website": True, "has_email": True, ...}

Adding a new rule
-----------------
1. Create a class in rules.py that extends ScoringRule.
2. Add an instance to the RULES list below.
That's it — nothing else needs to change.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ingestion.scoring.rules import (
    ScoringRule,
    StoreData,
    HasEmailRule,
    OwnDomainEmailRule,
    HasAddressRule,
    HasProductsRule,
    HasTenPlusProductsRule,
    CertValidOverSixMonthsRule,
)

# ---------------------------------------------------------------------------
# Registered rules — order doesn't matter, all are evaluated independently.
# ---------------------------------------------------------------------------

RULES: list[ScoringRule] = [
    HasEmailRule(),
    OwnDomainEmailRule(),
    HasAddressRule(),
    HasProductsRule(),
    HasTenPlusProductsRule(),
    CertValidOverSixMonthsRule(),
]

# Max possible score — useful for normalisation or UI display.
MAX_SCORE: int = sum(r.points for r in RULES)


# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ScoreResult:
    score: int
    breakdown: dict[str, bool]

    @property
    def has_website(self) -> bool:
        """Convenience accessor kept for backward compatibility."""
        return self.breakdown.get("has_website", False)


# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------

class StoreScorer:
    """Runs all registered rules against a StoreData and returns a ScoreResult."""

    def __init__(self, rules: list[ScoringRule]) -> None:
        self._rules = rules

    def compute(self, store: StoreData) -> ScoreResult:
        score = 0
        breakdown: dict[str, bool] = {}

        for rule in self._rules:
            passed = rule.evaluate(store)
            breakdown[rule.key] = passed
            if passed:
                score += rule.points

        return ScoreResult(score=score, breakdown=breakdown)


# ---------------------------------------------------------------------------
# Module-level default instance
# ---------------------------------------------------------------------------

_DEFAULT_SCORER = StoreScorer(RULES)


def compute_score(
    email: Optional[str] = None,
    products: Optional[str] = None,
    address: Optional[str] = None,
    valid_to: Optional[str] = None,
) -> dict:
    """Convenience wrapper used by CertificationData.to_dict().

    Returns a plain dict so callers don't need to import ScoreResult:
        {
            "score":       int,
            "has_website": bool,
            "breakdown":   dict[str, bool],
        }
    """
    store = StoreData(
        email=email,
        products=products,
        address=address,
        valid_to=valid_to,
    )
    result = _DEFAULT_SCORER.compute(store)
    return {
        "score":     result.score,
        "has_website": result.has_website,
        "breakdown": result.breakdown,
    }
