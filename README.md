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
        "Company Name": "AADHYA ORGANIC HERBS PRIVATE LIMITED Certified",
        "Certification ID": "ORG-2403-000509",
        "Location": "Kurnool",
        "Email": "info@aadhyaorganic.com",
        "Address": "805-2A.Main road, Krishnagiri sub post office, Bapanadoddi village, Kurnool, Andhra Pradesh",
        "Certifying Agency": "NPOP",
        "Valid From": "12/03/2024",
        "Valid To": "11/03/2025",
        "Products": "Ajwain, Alfalfa powder, Amla dried, Amla powder, Amla TBC, ..."
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
