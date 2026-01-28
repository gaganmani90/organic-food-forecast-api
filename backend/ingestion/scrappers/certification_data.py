from datetime import datetime
import uuid
import re

def parse_date(raw: str) -> str:
    try:
        # Remove prefix like "validfrom ", strip whitespace
        clean = raw.lower().replace("validfrom", "").strip()
        # Convert from dd/MM/yyyy to yyyy-MM-dd
        parsed = datetime.strptime(clean, "%d/%m/%Y")
        return parsed.date().isoformat()  # Output: '2023-10-13'
    except Exception as e:
        print(f"⚠️ Failed to parse date: {raw} — {e}")
        return None


def clean_store_name(name: str) -> str:
    """Remove 'Certified' suffix from store name if present."""
    if not name:
        return name
    # Remove trailing "Certified" (case-insensitive, with optional whitespace)
    cleaned = re.sub(r'\s+[Cc]ertified\s*$', '', name.strip())
    return cleaned


class CertificationData:
    """Data model for certification records."""
    def __init__(self, name, cert_id, location, email, address, certifying_agency, valid_from, valid_to, products):
        self.name = clean_store_name(name)
        self.cert_id = cert_id
        self.location = location
        self.email = email
        self.address = address
        self.certifying_agency = certifying_agency
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.products = products
        self.scraped_timestamp = datetime.now().isoformat()

    def to_dict(self):
        # Fallback to generated ID if missing
        cert_id = self.cert_id.strip() if self.cert_id else ""
        if not cert_id:
            cert_id = f"auto-{uuid.uuid4()}"
        return {
            "store_name": self.name,
            "certification_id": cert_id,
            "state": self.location,
            "email": self.email,
            "address": self.address,
            "certification_body": self.certifying_agency,
            "valid_from": parse_date(self.valid_from),
            "valid_to": parse_date(self.valid_to),
            "products": ", ".join(self.products),
            "scraped_at": self.scraped_timestamp
        }