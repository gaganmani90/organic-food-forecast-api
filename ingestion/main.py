from managers.scraper_manager import ScraperManager
from ingestion.scrappers.base_scrapper import STATE_CODES
from ingestion.scrappers.organic_scraper import OrganicFoodScraper

if __name__ == "__main__":
    for state in STATE_CODES:
        scraper = OrganicFoodScraper(state)
        manager = ScraperManager(scraper, f"{state}_organic_food_certifications")
        manager.scrape(max_pages=50, force_scrape=True)
