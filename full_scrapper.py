import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL and Headers
BASE_URL = "https://jaivikbharat.fssai.gov.in/pagination_data.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# Output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure the output directory exists

# List of state codes
STATE_CODES = [
    "AN", "AP", "AR", "AS", "BR", "CH", "CG", "DN", "DD", "GA", "GJ", "HR", "HP",
    "JK", "JH", "KA", "KL", "LD", "MP", "MH", "MN", "ML", "MZ", "NL", "DL", "OD",
    "PY", "PB", "RJ", "SK", "TN", "TS", "TR", "UP", "UK", "WB"
]

def fetch_page_data(page_number, state):
    """Fetch data from the given page number for a specific state."""
    params = {
        "orderby": "asc",
        "page": page_number,
        "stateName": state
    }

    response = requests.get(BASE_URL, params=params, headers=HEADERS)

    if response.status_code == 200:
        return response.text
    else:
        print(f"❌ Failed to fetch page {page_number} for {state}, Status Code: {response.status_code}")
        return None

def extract_certifications(html_content):
    """Extract certification details from the HTML response."""
    soup = BeautifulSoup(html_content, "html.parser")
    certifications = []

    # Find all listing blocks
    listings = soup.find_all("div", class_="right-listing")

    for listing in listings:
        try:
            name = listing.find("h4", class_="list-head").text.strip()
            cert_id = listing.find("h6").find("b").text.strip()
            location = listing.find("span", class_="location-name").text.strip()
            email = listing.find("span", class_="e-address").text.strip() if listing.find("span", class_="e-address") else None
            address = listing.find("h5", class_="address-detail").text.strip() if listing.find("h5", class_="address-detail") else None
            certifying_agency = listing.find("span", class_="certifying").find_next("span", class_="e-address").text.strip()
            valid_from, valid_to = None, None

            # Extract valid from and valid to dates
            valid_dates = listing.find("li", class_="valid-date")
            if valid_dates:
                dates = valid_dates.text.strip().split("to")
                valid_from = dates[0].replace("valid from", "").strip() if len(dates) > 0 else None
                valid_to = dates[1].strip() if len(dates) > 1 else None

            # Extract products
            product_list = []
            product_section = listing.find("div", class_="readmore")
            if product_section:
                product_list = product_section.text.replace("products registered", "").strip().split(",")

            certifications.append({
                "Company Name": name,
                "Certification ID": cert_id,
                "Location": location,
                "Email": email,
                "Address": address,
                "Certifying Agency": certifying_agency,
                "Valid From": valid_from,
                "Valid To": valid_to,
                "Products": ", ".join(product_list)  # Convert list to string
            })
        except Exception as e:
            print(f"⚠️ Error extracting a listing: {e}")

    return certifications

def scrape_all_pages(state, max_pages=50, force_scrape=False):
    """Scrape multiple pages for a given state and store results in a DataFrame."""
    csv_filename = os.path.join(OUTPUT_DIR, f"{state}_organic_food_certifications.csv")
    json_filename = os.path.join(OUTPUT_DIR, f"{state}_organic_food_certifications.json")

    # Check if files already exist
    if not force_scrape and os.path.exists(csv_filename):
        print(f"✅ Data for {state} already exists. Skipping scraping. Use force_scrape=True to refresh.")
        return

    all_certifications = []
    found_empty_page = False

    for page in range(1, max_pages + 1):
        print(f"🔍 Scraping page {page} for state {state}...")
        html_content = fetch_page_data(page, state)

        if html_content:
            certifications = extract_certifications(html_content)
            if not certifications:  # If the page is empty
                print(f"⛔ Found empty page for state {state} on page {page}. Stopping further pagination.")
                found_empty_page = True
                break
            all_certifications.extend(certifications)
        else:
            break  # Stop if a page fails to load

    # Convert to DataFrame
    df = pd.DataFrame(all_certifications)
    print(f"✅ Total records extracted for {state}: {len(df)}")

    # Save files
    df.to_csv(csv_filename, index=False)
    df.to_json(json_filename, orient="records")
    print(f"📂 Data saved: {csv_filename} & {json_filename}")

def scrape_all_states(force_scrape=False):
    """Scrape all states automatically."""
    for state in STATE_CODES:
        scrape_all_pages(state, max_pages=50, force_scrape=force_scrape)

if __name__ == "__main__":
    scrape_all_states(force_scrape=True)  # Set to True if you want to force fresh scraping
