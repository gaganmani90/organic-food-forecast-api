from search_engine.es_client import get_es_client

def search_stores(query: str = "", state: str = "", from_: int = 0, size: int = 10, index_name: str = "organic_stores"):
    es = get_es_client()

    must_clause = [{"match": {"store_name": query}}] if query else [{"match_all": {}}]
    filter_clause = [{"term": {"state": state}}] if state else []

    search_query = {
        "bool": {
            "must": must_clause,
            "filter": filter_clause
        }
    }

    response = es.search(
        index=index_name,
        query=search_query,
        from_=from_,
        size=size
    )

    hits = response["hits"]["hits"]
    return [hit["_source"] for hit in hits]
