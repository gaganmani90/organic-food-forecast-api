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

def render_store_result(source: dict):
    st.subheader(source.get("store_name", "Unnamed Store"))

    st.markdown(f"📍 **Address:** {source.get('address', 'N/A')}")
    st.markdown(f"🌍 **State:** {source.get('state', 'N/A')}")
    st.markdown(f"📧 **Email:** [{source.get('email', 'N/A')}](mailto:{source.get('email', '')})")
    st.markdown(f"🏷️ **Certification ID:** {source.get('certification_id', 'N/A')}")
    st.markdown(f"✅ **Certified By:** {source.get('certification_body', 'N/A')}")
    st.markdown(f"📅 **Valid From:** {source.get('valid_from', 'N/A')}")
    st.markdown(f"📅 **Valid To:** {source.get('valid_to', 'N/A')}")
    st.markdown(f"🕒 **Last Scraped:** {source.get('scraped_at', 'N/A')}")

    # Expandable products list
    with st.expander("📦 View Products"):
        products = source.get("products", "")
        product_list = [p.strip() for p in products.split(",") if p.strip()]
        st.markdown(f"🛒 **Total Products:** {len(product_list)}")
        for product in product_list:
            st.markdown(f"- {product}")

    st.markdown("---")


if st.button("Search"):
    try:
        url = f"{api_base_url}/api/search?query={query}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        
        # Handle new clean format
        if "results" in data:
            results = data.get("results", [])
        else:
            # Fallback for old format (backward compatibility)
            results = [hit.get("_source", hit) for hit in data.get("hits", {}).get("hits", [])]
        
        if not results:
            st.write("No results found.")
        else:
            st.write(f"Found {len(results)} result(s)")
            for result in results:
                render_store_result(result)

    except Exception as e:
        st.error(f"API Error: {e}")
