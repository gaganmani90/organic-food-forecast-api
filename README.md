# Organic Food Certification Web Scraper

## Overview

This Python scraper extracts organic food certification data from the Jaivik Bharat website. It retrieves information about certified companies, including certification details, locations, and registered products. The scraper is designed to work for all Indian states.

## Features
- Scrapes certification data for organic food companies.
- Supports multiple states using state codes.
- Extracts company name, certification ID, location, email, address, certifying agency, validity dates, and products.
- Saves data in CSV and JSON formats for easy processing.
- Automatically updates a metadata file summarizing the number of businesses per state and the last scraped timestamp.

## Prerequisites
Make sure you have Python installed (version 3.8+ recommended) and the required dependencies.

## Installation
Clone the repository and install the dependencies:
```sh
pip install -r requirements.txt
```

## Usage
Run the scraper to fetch data for all states:
```sh
python main.py
```
Or specify a particular state (e.g., Rajasthan - RJ):
```sh
python main.py --state RJ
```

## Output
- Extracted data is saved in `output/<state>_organic_food_certifications.csv` and `output/<state>_organic_food_certifications.json`.
- A metadata file (`scraping_metadata.csv`) is created in the output directory, summarizing the scraped data.
- **Sample Metadata Format:**
```csv
State,Business Count,Last Scraped
RJ,118,2025-03-08T10:30:45.249586
MH,95,2025-03-08T10:35:20.123456
```
- **Sample Data Format:**
```json
[
  {
    "store_name": "AADHYA ORGANIC HERBS PRIVATE LIMITED Certified",
    "certification_id": "ORG-2403-000509",
    "state": "Kurnool",
    "email": "info@aadhyaorganic.com",
    "address": "805-2A. Main Road, Krishnagiri Sub Post Office, Bapanadoddi Village, Kurnool, Andhra Pradesh",
    "certification_body": "NPOP",
    "valid_from": "2024-03-12",
    "valid_to": "2025-03-11",
    "products": "Ajwain, Alfalfa powder, Amla dried, Amla powder, Amla TBC",
    "scraped_at": "2025-03-30T18:21:34.785247"
  }
]

```

## Configuration
- Modify `max_pages` in `main.py` to change the number of pages scraped per state.
- Update the `STATE_CODES` list in `main.py` to include additional states if needed.

## Contributing
Feel free to fork the project and submit pull requests for improvements.

## License
MIT License

## Contact
For questions or suggestions, reach out to [your email or GitHub handle].

# Search Engine 

```shell
# start server locally 
docker run -d --name es-mvp -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.17.13

```
Configuration .env file
```shell
ES_HOST=http://localhost:9200
DATA_FILE_PATH=ingestion/output/

```

Load data via
```shell
python search_engine/main.py

```