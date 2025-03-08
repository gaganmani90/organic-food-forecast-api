import os
import requests
from bs4 import BeautifulSoup
from src.scrappers.base_scrapper import BaseScraper
from src.scrappers.certification_data import CertificationData
from src.utils.data_saver import DataSaver

# Constants
BASE_URL = "https://jaivikbharat.fssai.gov.in/pagination_data.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
OUTPUT_DIR = os.path.abspath(os.path.join(os.getcwd(), 'output'))

class OrganicFoodScraper(BaseScraper):
    def __init__(self, state):
        super().__init__("Jaivik Bharat")
        self.state = state

    def extract_data(self, force_scrape=False, max_pages=50):
        """
        Main entry point for extracting data.
        - Proceeds with scraping pages.
        """
        csv_file = os.path.join(OUTPUT_DIR, f"{self.state}_organic_food_certifications.csv")
        json_file = os.path.join(OUTPUT_DIR, f"{self.state}_organic_food_certifications.json")

        return self._scrape_pages(max_pages)

    def fetch_page_data(self, page_number):
        """
        Fetches HTML content for a given page number.
        """
        params = {"orderby": "asc", "page": page_number, "stateName": self.state}
        response = requests.get(BASE_URL, params=params, headers=HEADERS)
        return response.text if response.status_code == 200 else None

    def _scrape_pages(self, max_pages):
        """
        Handles pagination and calls _extract_listings() for each page.
        - Stops when an empty page is encountered.
        - Collects extracted listings and passes them to _save_data().
        """
        certifications = []
        page_number = 1

        while page_number <= max_pages and (page_number == 1 or certifications):
            print(f"🔍 Scraping page {page_number} for {self.state}...")
            html_content = self.fetch_page_data(page_number)
            if not html_content:
                print(f"⛔ No data received for page {page_number}. Stopping.")
                break

            soup = BeautifulSoup(html_content, "html.parser")
            listings = soup.find_all("div", class_="right-listing")

            if not listings:
                print(f"⛔ No more data on page {page_number}. Stopping.")
                break

            certifications.extend(self._extract_listings(listings))
            page_number += 1

        if certifications:
            self._save_data(certifications)
        return certifications

    def _extract_listings(self, listings):
        """
        Extracts details from a list of HTML elements.
        - Parses business information such as name, ID, location, email, and products.
        - Returns a list of dictionaries containing extracted data.
        """
        certifications = []
        for listing in listings:
            try:
                name = listing.find("h4", class_="list-head").text.strip()
                cert_id = listing.find("h6").find("b").text.strip()
                location = listing.find("span", class_="location-name").text.strip()
                email = listing.find("span", class_="e-address").text.strip() if listing.find("span", class_="e-address") else None
                address = listing.find("h5", class_="address-detail").text.strip() if listing.find("h5", class_="address-detail") else None
                certifying_agency = listing.find("span", class_="certifying").find_next("span", class_="e-address").text.strip()

                valid_from, valid_to = None, None
                valid_dates = listing.find("li", class_="valid-date")
                if valid_dates:
                    dates = valid_dates.text.strip().split("to")
                    valid_from = dates[0].replace("valid from", "").strip() if len(dates) > 0 else None
                    valid_to = dates[1].strip() if len(dates) > 1 else None

                product_list = []
                product_section = listing.find("div", class_="readmore")
                if product_section:
                    product_list = [p.strip() for p in product_section.text.replace("products registered:", "").strip().split(",") if p.strip()]

                certification = CertificationData(
                    name, cert_id, location, email, address, certifying_agency, valid_from, valid_to, product_list
                )
                certifications.append(certification.to_dict())
            except Exception as e:
                print(f"⚠️ Error extracting a listing: {e}")
        return certifications

    def _save_data(self, certifications):
        """
        Saves extracted data to CSV and JSON files.
        """
        if certifications:
            csv_file = os.path.join(OUTPUT_DIR, f"{self.state}_organic_food_certifications.csv")
            json_file = os.path.join(OUTPUT_DIR, f"{self.state}_organic_food_certifications.json")

            DataSaver.save_to_csv(certifications, csv_file)
            DataSaver.save_to_json(certifications, json_file)
            print(f"✅ Scraped {len(certifications)} businesses for {self.state}.")
