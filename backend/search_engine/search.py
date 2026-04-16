import time

from search_engine.es_client import get_es_client


# ---------------------------------------------------------------------------
# Field weights for relevance ranking.
# Format: "field^boost" — higher boost = more influence on _score.
# ---------------------------------------------------------------------------
_SEARCH_FIELDS = [
    "store_name^4",    # exact store name match is most valuable
    "products^2",      # product match (e.g. "rice", "honey") is next
    "state",           # state match — normal weight
    "address",         # address match — normal weight
]


def _active_first_sort(now_ms: int) -> dict:
    """Painless script sort: active stores (0) before expired (1) before unknown (2)."""
    return {
        "_script": {
            "type": "number",
            "order": "asc",
            "script": {
                "lang": "painless",
                "source": """
                    if (doc['valid_to'].size() == 0) return 2;
                    long vt = doc['valid_to'].value.toInstant().toEpochMilli();
                    return vt >= params.now ? 0 : 1;
                """,
                "params": {"now": now_ms},
            },
        }
    }


def search_stores(
    query: str = "",
    state: str = "",
    from_: int = 0,
    size: int = 10,
    index_name: str = "organic_stores",
):
    es = get_es_client()
    now_ms = int(time.time() * 1000)

    if query:
        # Text query: field-boosted search with fuzzy matching + AND operator.
        #
        # fuzziness=AUTO  → tolerates 1 typo for words ≥5 chars, 0 for short words
        # default_operator=AND → all words must appear (better precision than OR)
        # fields with ^N  → boosts relevance score for matches in those fields
        #
        # Sort: relevance (_score) first so the most relevant result leads,
        # then our quality score, then active-before-expired, then valid_to.
        must_clause = [
            {
                "query_string": {
                    "query": query,
                    "fields": _SEARCH_FIELDS,
                    "fuzziness": "AUTO",
                    "default_operator": "AND",
                }
            }
        ]
        sort = [
            {"_score": {"order": "desc"}},
            {"score": {"order": "desc", "unmapped_type": "integer"}},
            _active_first_sort(now_ms),
            {"valid_to": {"order": "desc", "unmapped_type": "date"}},
        ]
    else:
        # Browse mode (no query): sort purely by our quality score so the
        # best-verified stores always surface first.
        must_clause = [{"match_all": {}}]
        sort = [
            {"score": {"order": "desc", "unmapped_type": "integer"}},
            _active_first_sort(now_ms),
            {"valid_to": {"order": "desc", "unmapped_type": "date"}},
        ]

    filter_clause = [{"term": {"state": state}}] if state else []

    body = {
        "query": {
            "bool": {
                "must": must_clause,
                "filter": filter_clause,
            }
        },
        "sort": sort,
        "from": from_,
        "size": size,
    }

    response = es.search(index=index_name, body=body)
    hits = response["hits"]["hits"]
    total = (
        response["hits"]["total"]["value"]
        if isinstance(response["hits"]["total"], dict)
        else response["hits"]["total"]
    )
    return [hit["_source"] for hit in hits], total
