from search_engine.index_setup import create_index
from search_engine.loader import load_to_elasticsearch
from loaders.file_loader import get_organic_store_data_from_file

if __name__ == "__main__":
    create_index()

    docs = get_organic_store_data_from_file()
    print(f"📦 Loading {len(docs)} documents from file")
    load_to_elasticsearch(docs)
