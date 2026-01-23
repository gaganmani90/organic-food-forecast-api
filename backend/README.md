# Backend

This directory contains all backend services for the Organic Food Web Scraper project.

## Structure

```
backend/
├── api/                 # FastAPI REST API
│   └── api_main.py     # Main API application
├── ingestion/           # Web scraping services
│   ├── main.py         # Scraper entry point
│   ├── managers/       # Scraper management
│   ├── scrappers/      # Web scraping logic
│   └── utils/          # Utility functions
└── search_engine/      # Elasticsearch services
    ├── main.py         # Data loader entry point
    ├── es_client.py    # Elasticsearch client
    ├── index_setup.py  # Index configuration
    ├── loader.py       # Data loading
    ├── search.py       # Search functions
    └── loaders/        # Data loaders
```

## API

The FastAPI application provides REST endpoints for searching organic food stores.

**Endpoints:**
- `GET /api/search?query=<search_term>` - Search stores

**To run:**
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
uvicorn backend.api.api_main:app --reload --port 8000
```

**Access:** 
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Development

All backend code uses relative imports within the `backend/` directory. Set `PYTHONPATH` to `backend/` when running scripts.
