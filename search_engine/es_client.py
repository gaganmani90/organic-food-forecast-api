import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()  # Load from .env file

def get_es_client():
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
