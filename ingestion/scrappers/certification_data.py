from datetime import datetime

class CertificationData:
    """Data model for certification records."""
    def __init__(self, name, cert_id, location, email, address, certifying_agency, valid_from, valid_to, products):
        self.name = name
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
        return {
            "Company Name": self.name,
            "Certification ID": self.cert_id,
            "Location": self.location,
            "Email": self.email,
            "Address": self.address,
            "Certifying Agency": self.certifying_agency,
            "Valid From": self.valid_from,
            "Valid To": self.valid_to,
            "Products": ", ".join(self.products),
            "Scraped Timestamp": self.scraped_timestamp
        }