import os
import unittest
import pandas as pd
from src.scrappers.organic_scraper import OrganicFoodScraper
from src.scrappers.metadata_logger import MetadataLogger

class TestOrganicFoodScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup temporary files and test state before running tests."""
        cls.test_state = "TEST_STATE"
        cls.test_output_dir = os.path.abspath(os.path.join(os.getcwd(), 'output'))
        cls.test_csv = os.path.join(cls.test_output_dir, f"{cls.test_state}_organic_food_certifications.csv")
        cls.test_metadata = os.path.join(cls.test_output_dir, "scraping_metadata.csv")

        # Ensure output directory exists
        os.makedirs(cls.test_output_dir, exist_ok=True)

    def test_scraper_fetch_and_extract(self):
        """Test if scraper fetches and extracts data correctly."""
        scraper = OrganicFoodScraper(self.test_state)

        # **Updated Sample HTML** with all required fields
        sample_html = """
        <div class='right-listing'>
            <h4 class='list-head'>Test Company</h4>
            <h6><b>12345</b></h6>
            <span class='location-name'>Test Location</span>
            <span class='e-address'>test@example.com</span>
            <h5 class='address-detail'>123 Test Street</h5>
            <span class='certifying'><span class='e-address'>Test Certifying Agency</span></span>
            <li class='valid-date'>valid from 2025-01-01 to 2026-01-01</li>
            <div class='readmore'>products registered: Product1, Product2</div>
        </div>
        """
        extracted_data = scraper.extract_data(sample_html, force_scrape=True)

        self.assertGreater(len(extracted_data), 0, "Failed to extract data")
        self.assertEqual(extracted_data[0]['Company Name'], "Test Company", "Company Name mismatch")

    def test_metadata_update(self):
        """Test if metadata is updated correctly."""
        # Create a mock CSV file
        test_data = pd.DataFrame([
            {"Company Name": "Test Company", "Scraped Timestamp": "2025-03-08T12:00:00Z"}
        ])
        test_data.to_csv(self.test_csv, index=False)

        # Update metadata
        MetadataLogger.save_metadata(self.test_state, self.test_csv)

        # Check if metadata was updated
        self.assertTrue(os.path.exists(self.test_metadata), "Metadata file was not created")

        metadata_df = pd.read_csv(self.test_metadata)

        # ✅ Verify that metadata contains correct state
        self.assertIn(self.test_state, metadata_df["State"].values, "Metadata entry missing for test state")

        # ✅ Verify Business Count matches the CSV file
        business_count = metadata_df.loc[metadata_df["State"] == self.test_state, "Business Count"].values[0]
        self.assertEqual(business_count, 1, "Incorrect business count in metadata")

        # ✅ Verify the latest timestamp is correctly updated
        last_scraped_timestamp = metadata_df.loc[metadata_df["State"] == self.test_state, "Last Scraped"].values[0]
        self.assertEqual(last_scraped_timestamp, "2025-03-08T12:00:00Z", "Metadata timestamp is incorrect")

    def test_metadata_single_entry_per_state(self):
        """Test that metadata file does not contain multiple entries for the same state."""
        # Ensure metadata file exists with initial entry
        test_data = pd.DataFrame([
            {"Company Name": "Test Company", "Scraped Timestamp": "2025-03-08T12:00:00Z"}
        ])
        test_data.to_csv(self.test_csv, index=False)

        # Update metadata twice
        MetadataLogger.save_metadata(self.test_state, self.test_csv)
        MetadataLogger.save_metadata(self.test_state, self.test_csv)

        # Read metadata file
        metadata_df = pd.read_csv(self.test_metadata)

        # ✅ Check that only one entry exists per state
        state_count = metadata_df[metadata_df["State"] == self.test_state].shape[0]
        self.assertEqual(state_count, 1, "Metadata contains multiple entries for the same state!")

    @classmethod
    def tearDownClass(cls):
        """Cleanup generated files after tests."""
        if os.path.exists(cls.test_csv):
            os.remove(cls.test_csv)
        if os.path.exists(cls.test_metadata):
            os.remove(cls.test_metadata)

if __name__ == "__main__":
    unittest.main()
