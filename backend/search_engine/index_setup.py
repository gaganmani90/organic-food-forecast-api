from search_engine.es_client import get_es_client

def create_index(index_name="organic_stores"):
    es = get_es_client()

    mapping = {
        "mappings": {
            "properties": {
                "store_name": {"type": "text"},
                "certification_id": {"type": "keyword"},
                "state": {"type": "keyword"},
                "location": {"type": "geo_point"},
                "email": {"type": "keyword"},
                "address": {"type": "text"},
                "certification_body": {"type": "keyword"},
                "valid_from": {"type": "date"},
                "valid_to": {"type": "date"},
                "products": {"type": "text"},
                "scraped_at": {"type": "date"}
            }
        }
    }

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)
        print(f"✅ Index `{index_name}` created.")
    else:
        print(f"ℹ️ Index `{index_name}` already exists.")
