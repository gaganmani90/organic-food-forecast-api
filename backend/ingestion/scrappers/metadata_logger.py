import os
import pandas as pd
from datetime import datetime
from ingestion.utils.data_saver import OUTPUT_DIR

class MetadataLogger:
    """Handles logging metadata for scraping runs."""

    @staticmethod
    def save_metadata():
        """
        Reads from the output folder, aggregates metadata for all state files, and saves it.
        """
        metadata_file = os.path.join(OUTPUT_DIR, "scraping_metadata.csv")
        metadata_entries = []

        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith("_organic_food_certifications.csv"):
                state = filename.split("_")[0]  # Extract state name from filename
                file_path = os.path.join(OUTPUT_DIR, filename)
                existing_data = pd.read_csv(file_path)
                count = len(existing_data)
                latest_timestamp = existing_data["Scraped Timestamp"].max() if "Scraped Timestamp" in existing_data else datetime.now().isoformat()

                metadata_entries.append({
                    "State": state,
                    "Business Count": count,
                    "Last Scraped": latest_timestamp
                })

        metadata_df = pd.DataFrame(metadata_entries)
        metadata_df.to_csv(metadata_file, index=False)
        print(f"📄 Metadata file updated with data from {len(metadata_entries)} states.")
