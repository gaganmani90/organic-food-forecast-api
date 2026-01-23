import time

from search_engine.es_client import get_es_client

def search_stores(query: str = "", state: str = "", from_: int = 0, size: int = 10, index_name: str = "organic_stores"):
    es = get_es_client()
    now_ms = int(time.time() * 1000)

    # Use query_string to search across all fields (like original API)
    if query:
        must_clause = [{"query_string": {"query": query}}]
    else:
        must_clause = [{"match_all": {}}]
    
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
        sort=[
            {
                "_script": {
                    "type": "number",
                    "order": "asc",
                    "script": {
                        "lang": "painless",
                        # 0 = active (valid_to >= now), 1 = expired (valid_to < now), 2 = missing valid_to (last)
                        "source": """
                            if (doc['valid_to'].size() == 0) return 2;
                            long vt = doc['valid_to'].value.toInstant().toEpochMilli();
                            return vt >= params.now ? 0 : 1;
                        """,
                        "params": {"now": now_ms},
                    },
                }
            },
            {
                "valid_to": {
                    "order": "desc",
                    "unmapped_type": "date"
                }
            },
        ],
        from_=from_,
        size=size
    )

    hits = response["hits"]["hits"]
    total = response["hits"]["total"]["value"] if isinstance(response["hits"]["total"], dict) else response["hits"]["total"]
    
    results = [hit["_source"] for hit in hits]
    return results, total
