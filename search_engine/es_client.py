import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()  # Load from .env file

def get_es_client():
    es_host = os.getenv("ES_HOST", "http://localhost:9200")
    es = Elasticsearch(es_host)

    if not es.ping():
        raise ConnectionError(f"Elasticsearch is not reachable at {es_host}")

    return es
