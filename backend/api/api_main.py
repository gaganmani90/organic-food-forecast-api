from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from search_engine.search import search_stores

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/search")
async def search(query: Optional[str] = Query("")):
    try:
        results = search_stores(query=query, from_=0, size=10000)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}
