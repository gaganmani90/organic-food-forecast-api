import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from opensearchpy import OpenSearch

load_dotenv()  # Load from .env file


def get_es_client():
    use_local = os.getenv("USE_LOCAL_ES", "false").lower() == "true"

    if use_local:
        # Local Docker Elasticsearch
        es_host = os.getenv("ES_HOST_LOCAL", "http://localhost:9200")
        parsed = urlparse(es_host)
        client = OpenSearch(
            hosts=[{"host": parsed.hostname, "port": parsed.port or 9200}],
            use_ssl=parsed.scheme == "https",
            verify_certs=False,
        )
    else:
        # Production (Bonsai/OpenSearch or Elastic Cloud)
        es_host = os.getenv("ES_HOST")
        es_api_key = os.getenv("ES_API_KEY")
        es_username = os.getenv("ES_USERNAME")
        es_password = os.getenv("ES_PASSWORD")

        parsed = urlparse(es_host)
        host = parsed.hostname
        port = parsed.port or 443
        use_ssl = parsed.scheme == "https"

        if es_username and es_password:
            # Bonsai / OpenSearch (basic auth)
            client = OpenSearch(
                hosts=[{"host": host, "port": port}],
                http_auth=(es_username, es_password),
                use_ssl=use_ssl,
                verify_certs=True,
            )
        elif es_api_key:
            # Elastic Cloud (API key) – opensearch-py uses same auth
            client = OpenSearch(
                hosts=[{"host": host, "port": port}],
                http_auth=("", es_api_key),  # API key as password
                use_ssl=use_ssl,
                verify_certs=True,
            )
        else:
            raise ValueError("Set ES_USERNAME/ES_PASSWORD (Bonsai) or ES_API_KEY (Elastic Cloud)")

    try:
        client.info()
    except Exception as e:
        raise ConnectionError(f"Search backend not reachable at {es_host}: {e}") from e

    return client
