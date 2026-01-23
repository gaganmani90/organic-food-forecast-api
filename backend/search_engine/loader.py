from elasticsearch.helpers import bulk, BulkIndexError
from search_engine.es_client import get_es_client

def load_to_elasticsearch(docs, index_name="organic_stores"):
    es = get_es_client()

    actions = []
    for doc in docs:
        # Skip docs missing a unique ID
        if not doc.get("certification_id"):
            print("⚠️ Skipping doc with missing certification_id:", doc.get("store_name", "Unknown Store"))
            continue

        actions.append({
            "_index": index_name,
            "_id": doc["certification_id"],
            "_source": doc
        })

    try:
        success, _ = bulk(es, actions)
        print(f"✅ Loaded {success} documents to index `{index_name}`.")
    except BulkIndexError as e:
        print(f"❌ {len(e.errors)} documents failed to index.")
        for err in e.errors[:5]:
            print("⚠️ Error detail:", err)
