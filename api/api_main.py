from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from search_engine.es_client import get_es_client

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

es = get_es_client()

@app.get("/api/search")
async def search(query: Optional[str] = Query("")):
    try:
        result = es.search(
            index="organic_stores",
            body={
                "query": {
                    "query_string": {
                        "query": query
                    }
                },
                "size": 10000  # max allowed value
            }
        )
        return result
    except Exception as e:
        return {"error": str(e)}
