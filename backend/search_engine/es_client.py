import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()  # Load from .env file

def get_es_client():
    use_local = os.getenv("USE_LOCAL_ES", "false").lower() == "true"
    
    if use_local:
        # Local Docker Elasticsearch
        es_host = os.getenv("ES_HOST_LOCAL", "http://localhost:9200")
        es = Elasticsearch(
            es_host,
            verify_certs=False  # Local Docker doesn't use SSL
        )
    else:
        # Production Elastic Cloud
        es_host = os.getenv("ES_HOST")
        es_api_key = os.getenv("ES_API_KEY")
        es = Elasticsearch(
            es_host,
            api_key=es_api_key,
            verify_certs=True
        )
    
    if not es.ping():
        raise ConnectionError(f"Elasticsearch is not reachable at {es_host}")

    return es
