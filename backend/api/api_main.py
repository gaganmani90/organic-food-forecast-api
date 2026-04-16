import os
import re
import json
import logging
from datetime import datetime
from fastapi import FastAPI, Query, BackgroundTasks, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from search_engine.search import search_stores
from search_engine.es_client import get_es_client
from search_engine.index_setup import create_index
from search_engine.loader import load_to_elasticsearch
from search_engine.loaders.file_loader import get_organic_store_data_from_file
from ingestion.managers.scraper_manager import ScraperManager
from ingestion.scrappers.base_scrapper import STATE_CODES
from ingestion.scrappers.organic_scraper import OrganicFoodScraper

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Security helpers
# ---------------------------------------------------------------------------

# Secret used to protect internal/admin endpoints (scrape-and-load).
# Set INTERNAL_API_SECRET in Vercel environment variables.
# If not set, the check is skipped (dev mode).
_INTERNAL_API_SECRET = os.getenv("INTERNAL_API_SECRET", "")

# Characters that have special meaning in OpenSearch query_string syntax.
_QUERY_ILLEGAL = re.compile(r'[+\-=&|><!(){}\[\]^"~*?:\\\/]')
_QUERY_MAX_LEN  = 100


def verify_internal_secret(authorization: Optional[str] = Header(None)) -> None:
    """Dependency: reject requests that don't carry the internal API secret.

    Passes silently when INTERNAL_API_SECRET is not configured (local dev).
    """
    if not _INTERNAL_API_SECRET:
        return  # dev mode — no secret configured, allow all
    if authorization != f"Bearer {_INTERNAL_API_SECRET}":
        logger.warning("Rejected request with missing/invalid Authorization header")
        raise HTTPException(status_code=401, detail="Unauthorized")


def sanitise_query(raw: Optional[str]) -> str:
    """Strip OpenSearch query operators and cap length.

    Prevents query injection (field targeting, wildcards, boolean bombs).
    """
    if not raw:
        return ""
    cleaned = raw.strip()[:_QUERY_MAX_LEN]
    return _QUERY_ILLEGAL.sub(" ", cleaned).strip()


# ---------------------------------------------------------------------------
# App + middleware
# ---------------------------------------------------------------------------

def get_allowed_origins():
    origins_env = os.getenv("ALLOWED_ORIGINS", "")
    if origins_env:
        return [o.strip() for o in origins_env.split(",") if o.strip()]
    return ["http://localhost:5173", "http://localhost:3000"]


limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Public endpoints
# ---------------------------------------------------------------------------

@app.get("/api/search")
@limiter.limit("60/minute")
async def search(
    request: Request,
    query: Optional[str] = Query(""),
    state: Optional[str] = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    try:
        clean_query = sanitise_query(query)
        clean_state = sanitise_query(state)

        # Cap deep pagination — large offsets are expensive on OpenSearch
        from_ = min((page - 1) * page_size, 10_000)

        results, total = search_stores(
            query=clean_query,
            state=clean_state,
            from_=from_,
            size=page_size,
        )
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "results": results,
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
            },
        }
    except Exception:
        logger.error("Search failed", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Search unavailable. Please try again."})


@app.get("/api/last-refresh")
@limiter.limit("30/minute")
async def get_last_refresh(request: Request):
    try:
        es = get_es_client()
        try:
            response = es.get(index="organic_stores", id="_metadata")
            last_refresh = response["_source"].get("last_refresh")
            return {"last_refresh": last_refresh, "last_refresh_formatted": last_refresh}
        except Exception:
            return {"last_refresh": None, "last_refresh_formatted": None}
    except Exception:
        logger.error("Failed to fetch last-refresh metadata", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Unable to fetch refresh info."})


@app.get("/api/scraping-status")
@limiter.limit("30/minute")
async def get_scraping_status(request: Request):
    try:
        es = get_es_client()
        try:
            response = es.get(index="organic_stores", id="_scraping_job_status")
            status = response["_source"]
            return {
                "status": status.get("status"),
                "message": status.get("message"),
                "timestamp": status.get("timestamp"),
            }
        except Exception:
            return {"status": "unknown", "message": "No scraping job has been run yet", "timestamp": None}
    except Exception:
        logger.error("Failed to fetch scraping status", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Unable to fetch scraping status."})


# ---------------------------------------------------------------------------
# Internal endpoints — require INTERNAL_API_SECRET
# ---------------------------------------------------------------------------

def update_job_status(status: str, message: str, details: dict = None):
    """Persist job progress to Elasticsearch for monitoring."""
    try:
        es = get_es_client()
        es.index(
            index="organic_stores",
            id="_scraping_job_status",
            body={
                "status": status,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                **(details or {}),
            },
        )
        logger.info(f"Job status: {status} — {message}")
    except Exception:
        logger.error("Failed to update job status", exc_info=True)


def run_scraping_task():
    """Background task: scrape all states then load into Bonsai."""
    try:
        update_job_status("running", "Scraping task started")
        total_states = len(STATE_CODES)
        successful_states = 0
        failed_states = 0
        errors = []
        total_records_scraped = 0

        output_dir = os.getenv("DATA_FILE_PATH", "output")
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Output directory: {output_dir}")

        # Step 1 — Scrape
        for state in STATE_CODES:
            try:
                logger.info(f"Scraping state: {state}")
                scraper = OrganicFoodScraper(state)
                manager = ScraperManager(scraper, f"{state}_organic_food_certifications")
                manager.scrape(max_pages=50, force_scrape=True)

                output_file = os.path.join("output", f"{state}_organic_food_certifications.json")
                if os.path.exists(output_file):
                    with open(output_file, "r", encoding="utf-8") as f:
                        state_data = json.load(f)
                        count = len(state_data) if isinstance(state_data, list) else 0
                        total_records_scraped += count
                        logger.info(f"State {state}: {count} records")

                successful_states += 1
            except Exception as e:
                failed_states += 1
                errors.append(f"State {state}: {e}")
                logger.error(f"Error scraping {state}", exc_info=True)

        # Step 2 — Ensure index
        try:
            create_index()
        except Exception as e:
            errors.append(f"Index creation: {e}")
            logger.error("Failed to create/verify index", exc_info=True)
            update_job_status("failed", "Failed to create/verify index")
            return

        # Step 3 — Load
        records_loaded = 0
        try:
            docs = get_organic_store_data_from_file()
            logger.info(f"Loading {len(docs)} documents into Bonsai")
            load_to_elasticsearch(docs)
            records_loaded = len(docs)

            if records_loaded > 0:
                es = get_es_client()
                es.index(
                    index="organic_stores",
                    id="_metadata",
                    body={
                        "last_refresh": datetime.now().isoformat(),
                        "records_count": records_loaded,
                        "successful_states": successful_states,
                        "total_states": total_states,
                    },
                )
        except Exception as e:
            errors.append(f"Data loading: {e}")
            logger.error("Error loading data into Bonsai", exc_info=True)

        # Step 4 — Final status
        if failed_states == 0 and records_loaded > 0:
            update_job_status("success", f"Loaded {records_loaded} records.", {
                "total_states": total_states,
                "successful_states": successful_states,
                "failed_states": failed_states,
                "total_records": total_records_scraped,
                "records_loaded": records_loaded,
            })
        elif successful_states > 0:
            update_job_status("partial", f"{failed_states} state(s) failed. Loaded {records_loaded} records.", {
                "total_states": total_states,
                "successful_states": successful_states,
                "failed_states": failed_states,
                "errors": errors[:10],
            })
        else:
            update_job_status("failed", "Scraping failed for all states.", {
                "total_states": total_states,
                "failed_states": failed_states,
                "errors": errors[:10],
            })

    except Exception:
        logger.error("Fatal error in scraping task", exc_info=True)
        update_job_status("failed", "Fatal error in scraping task")


@app.post("/api/scrape-and-load")
@app.get("/api/scrape-and-load")
async def scrape_and_load(
    request: Request,
    background_tasks: BackgroundTasks,
    _: None = None,  # placeholder; dependency injected below via Depends
    authorization: Optional[str] = Header(None),
):
    verify_internal_secret(authorization)
    background_tasks.add_task(run_scraping_task)
    logger.info("Scraping task queued")
    return {
        "status": "accepted",
        "message": "Scraping task queued. Takes 20-60+ minutes.",
    }
