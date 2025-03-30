import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
STATE_CODES = [
    "AN", "AP", "AR", "AS", "BR", "CH", "CG", "DN", "DD", "GA", "GJ", "HR", "HP",
    "JK", "JH", "KA", "KL", "LD", "MP", "MH", "MN", "ML", "MZ", "NL", "DL", "OD",
    "PY", "PB", "RJ", "SK", "TN", "TS", "TR", "UP", "UK", "WB"
]

class BaseScraper:
    """Base class for web scrapers to allow future extensibility."""
    def __init__(self, source_name):
        self.source_name = source_name

    def fetch_page_data(self, url, params=None):
        response = requests.get(url, params=params, headers=HEADERS)
        return response.text if response.status_code == 200 else None

    def extract_data(self, html_content):
        raise NotImplementedError("Subclasses must implement extract_data")