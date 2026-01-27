import os
import json
from glob import glob
from dotenv import load_dotenv

load_dotenv()

def get_organic_store_data_from_file():
    # Default to "output" directory where scraper saves files
    # DATA_FILE_PATH can be set to override this default
    folder_path = os.getenv("DATA_FILE_PATH", "output")

    # Resolve absolute path
    abs_folder_path = os.path.abspath(folder_path)

    # Find all .json files in the folder
    json_files = glob(os.path.join(abs_folder_path, "*.json"))

    if not json_files:
        raise FileNotFoundError(f"No JSON files found in folder: {abs_folder_path}")

    print(f"📂 Found {len(json_files)} JSON files in: {abs_folder_path}")

    all_docs = []

    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    all_docs.extend(data)
                else:
                    print(f"⚠️ Skipped non-list JSON file: {file_path}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error in {file_path}: {e}")

    print(f"📦 Total documents loaded: {len(all_docs)}")
    return all_docs
