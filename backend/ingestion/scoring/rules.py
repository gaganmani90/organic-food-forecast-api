"""
Scoring rules for organic stores.

Each rule is a self-contained class that:
  - declares how many points it awards (points)
  - declares a unique key used in the score breakdown (key)
  - implements evaluate(store) -> bool

To add a new criterion: create a class, add it to RULES in scorer.py. Done.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


# ---------------------------------------------------------------------------
# Input model
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StoreData:
    """Typed snapshot of a store's fields used for scoring.

    All fields are optional — missing data scores 0, never raises.
    """
    email:    Optional[str] = None
    products: Optional[str] = None   # comma-separated string
    address:  Optional[str] = None
    valid_to: Optional[str] = None   # ISO date string e.g. "2026-06-24"


# ---------------------------------------------------------------------------
# Base rule
# ---------------------------------------------------------------------------

class ScoringRule(ABC):
    """Abstract base for all scoring rules."""

    #: Points awarded when evaluate() returns True.
    points: int

    #: Unique snake_case key included in the score breakdown dict.
    key: str

    @abstractmethod
    def evaluate(self, store: StoreData) -> bool:
        """Return True if this store satisfies the criterion."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(key={self.key!r}, points={self.points})"


# ---------------------------------------------------------------------------
# Concrete rules
# ---------------------------------------------------------------------------

_GENERIC_EMAIL_DOMAINS: frozenset[str] = frozenset({
    "gmail.com", "yahoo.com", "yahoo.in",
    "hotmail.com", "rediffmail.com",
    "outlook.com", "live.com", "icloud.com",
})

# Characters that are illegal *within* a single email address (but comma is
# used as a list separator so we handle it at the extraction layer, not here).
_EMAIL_ILLEGAL_CHARS: frozenset[str] = frozenset({"/", " ", ";", "\t"})


def _validate_single_email(email: str) -> Optional[str]:
    """Validate one email string in isolation.

    Rules (strict but pragmatic):
      - No characters from _EMAIL_ILLEGAL_CHARS.
      - Exactly one '@'.
      - Non-empty local part.
      - Domain part contains at least one '.' with non-empty labels.

    Returns the cleaned email on success, None on failure.
    """
    email = email.strip()
    if not email:
        return None
    if any(c in email for c in _EMAIL_ILLEGAL_CHARS):
        return None
    parts = email.split("@")
    if len(parts) != 2:
        return None
    local, domain = parts
    if not local or not domain:
        return None
    domain_parts = domain.split(".")
    if len(domain_parts) < 2 or not all(domain_parts):
        return None
    return email


def _parse_clean_email(raw: Optional[str]) -> Optional[str]:
    """Extract and validate the first usable email from a raw field value.

    The source data sometimes stores multiple addresses separated by commas
    (e.g. "alka@foo.com, ravi@foo.com") or slashes (garbage concatenation).
    Strategy:
      1. Split on commas to get candidate addresses.
      2. Return the first candidate that passes _validate_single_email.
      3. Return None if no candidate is valid.

    This means we never silently discard a store that has at least one good
    address — we just use the first clean one.
    """
    if not raw:
        return None
    # Split on comma to handle "a@foo.com, b@bar.com" style multi-email fields
    candidates = raw.split(",")
    for candidate in candidates:
        result = _validate_single_email(candidate)
        if result is not None:
            return result
    return None


class HasEmailRule(ScoringRule):
    """Store has a valid, well-formed email address on record."""
    points = 5
    key = "has_email"

    def evaluate(self, store: StoreData) -> bool:
        return _parse_clean_email(store.email) is not None


class OwnDomainEmailRule(ScoringRule):
    """Email uses a company-owned domain (not Gmail/Yahoo/etc.)

    Infers the store likely has a website at that domain.
    Only scores when the email itself is valid (single, well-formed address).
    """
    points = 20
    key = "has_website"

    def evaluate(self, store: StoreData) -> bool:
        email = _parse_clean_email(store.email)
        if not email:
            return False
        domain = email.lower().split("@")[1]
        return domain not in _GENERIC_EMAIL_DOMAINS


class HasAddressRule(ScoringRule):
    """Store has a non-empty address."""
    points = 3
    key = "has_address"

    def evaluate(self, store: StoreData) -> bool:
        return bool(store.address and store.address.strip())


class HasProductsRule(ScoringRule):
    """Store has at least one product listed."""
    points = 5
    key = "has_products"

    def evaluate(self, store: StoreData) -> bool:
        return bool(store.products and store.products.strip())


class HasTenPlusProductsRule(ScoringRule):
    """Store has 10 or more products listed."""
    points = 5
    key = "has_ten_plus_products"

    def evaluate(self, store: StoreData) -> bool:
        if not store.products:
            return False
        items = [p for p in store.products.split(",") if p.strip()]
        return len(items) >= 10


class CertValidOverSixMonthsRule(ScoringRule):
    """Certification is valid for more than 6 months from today."""
    points = 10
    key = "cert_valid_over_six_months"

    _SIX_MONTHS_DAYS = 180

    def evaluate(self, store: StoreData) -> bool:
        if not store.valid_to:
            return False
        try:
            expiry = date.fromisoformat(store.valid_to)
            delta = expiry - date.today()
            return delta.days > self._SIX_MONTHS_DAYS
        except ValueError:
            return False
