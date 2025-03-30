import os

from ingestion.scrappers.metadata_logger import MetadataLogger
from ingestion.utils.data_saver import DataSaver


class ScraperManager:
    def __init__(self, scraper, output_filename):
        self.scraper = scraper
        self.output_csv = os.path.join("output", f"{output_filename}.csv")
        self.output_json = os.path.join("output", f"{output_filename}.json")

    def scrape(self, max_pages=50, force_scrape=False):
        if not force_scrape and os.path.exists(self.output_csv):
            print(f"✅ Data already exists. Skipping scraping.")
            return

        print(f"🔍 Starting scraping for {self.scraper.state} up to {max_pages} pages...")
        all_data = self.scraper.extract_data(force_scrape, max_pages)

        print(f"✅ Total records extracted: {len(all_data)}")
        DataSaver.save_to_csv(all_data, self.output_csv)
        DataSaver.save_to_json(all_data, self.output_json)

        # ✅ Call MetadataLogger after scraping
        # MetadataLogger.save_metadata()
