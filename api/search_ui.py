import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load from .env
load_dotenv()
DEFAULT_API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Sidebar: Config
st.sidebar.header("API Configuration")
api_base_url = st.sidebar.text_input(
    "API Base URL",
    DEFAULT_API_BASE_URL,
    help="Set your FastAPI server base URL here"
)

# Main UI
st.title("Organic Store Search")

query = st.text_input("Search query", "snow")

if st.button("Search"):
    try:
        url = f"{api_base_url}/api/search?query={query}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            st.write("No results found.")
        for hit in hits:
            source = hit["_source"]
            st.subheader(source.get("store_name", "Unnamed Store"))
            st.text(source.get("address", ""))
            st.text(f"{source.get('city', '')}, {source.get('state', '')} {source.get('zip_code', '')}")
            st.markdown("---")
    except Exception as e:
        st.error(f"API Error: {e}")
