import os
import json
import logging
from datetime import datetime
from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from search_engine.search import search_stores
from search_engine.es_client import get_es_client
from search_engine.index_setup import create_index
from search_engine.loader import load_to_elasticsearch
from search_engine.loaders.file_loader import get_organic_store_data_from_file
from ingestion.managers.scraper_manager import ScraperManager
from ingestion.scrappers.base_scrapper import STATE_CODES
from ingestion.scrappers.organic_scraper import OrganicFoodScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

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
async def search(
    query: Optional[str] = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    try:
        # Calculate offset from page number
        from_ = (page - 1) * page_size
        
        # Get results and total count
        results, total = search_stores(query=query, from_=from_, size=page_size)
        
        # Calculate total pages
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        return {
            "results": results,
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/scraping-status")
async def get_scraping_status():
    """
    Get the current status of the scraping job.
    """
    try:
        es = get_es_client()
        try:
            response = es.get(index="organic_stores", id="_scraping_job_status")
            status = response["_source"]
            return {
                "status": status.get("status"),
                "message": status.get("message"),
                "timestamp": status.get("timestamp"),
                "details": {k: v for k, v in status.items() if k not in ["status", "message", "timestamp"]}
            }
        except Exception:
            # No job status found
            return {
                "status": "unknown",
                "message": "No scraping job has been run yet",
                "timestamp": None
            }
    except Exception as e:
        logger.error(f"Error getting scraping status: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


@app.get("/api/last-refresh")
async def get_last_refresh():
    """
    Get the last date when data was refreshed from metadata document.
    """
    try:
        es = get_es_client()
        
        # Get the metadata document with fixed ID
        try:
            response = es.get(index="organic_stores", id="_metadata")
            last_refresh = response["_source"].get("last_refresh")
            return {
                "last_refresh": last_refresh,
                "last_refresh_formatted": last_refresh
            }
        except Exception:
            # Metadata document doesn't exist yet
            return {
                "last_refresh": None,
                "last_refresh_formatted": None
            }
    except Exception as e:
        logger.error(f"Error getting last refresh date: {e}", exc_info=True)
        return {"error": str(e), "last_refresh": None}


def update_job_status(status: str, message: str, details: dict = None):
    """Update job status in Elasticsearch for monitoring."""
    try:
        es = get_es_client()
        job_status = {
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            **(details or {})
        }
        es.index(index="organic_stores", id="_scraping_job_status", body=job_status)
        logger.info(f"Job status updated: {status} - {message}")
    except Exception as e:
        logger.error(f"Failed to update job status: {e}", exc_info=True)


def run_scraping_task():
    """
    Background task that performs the actual scraping and loading.
    This runs asynchronously so the API can return immediately.
    """
    try:
        update_job_status("running", "Scraping task started")
        total_states = len(STATE_CODES)
        successful_states = 0
        failed_states = 0
        errors = []
        total_records_scraped = 0
        
        # Step 1: Ensure output directory exists
        output_dir = os.getenv("DATA_FILE_PATH", "output")
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Output directory set to: {output_dir}")
        
        # Step 2: Scrape data for all states
        logger.info(f"Starting scraping for {total_states} states...")
        
        for state in STATE_CODES:
            try:
                logger.info(f"Scraping state: {state}")
                scraper = OrganicFoodScraper(state)
                manager = ScraperManager(scraper, f"{state}_organic_food_certifications")
                manager.scrape(max_pages=50, force_scrape=True)
                
                # Count records for this state
                output_file = os.path.join("output", f"{state}_organic_food_certifications.json")
                if os.path.exists(output_file):
                    with open(output_file, "r", encoding="utf-8") as f:
                        state_data = json.load(f)
                        record_count = len(state_data) if isinstance(state_data, list) else 0
                        total_records_scraped += record_count
                        logger.info(f"State {state}: Scraped {record_count} records")
                
                successful_states += 1
                logger.info(f"Successfully completed scraping for state: {state}")
            except Exception as e:
                failed_states += 1
                error_msg = f"State {state}: {str(e)}"
                errors.append(error_msg)
                logger.error(f"Error scraping state {state}: {e}", exc_info=True)
        
        # Step 3: Create/ensure index exists
        try:
            logger.info("Creating/verifying Bonsai index...")
            create_index()
            logger.info("Index created/verified successfully")
        except Exception as e:
            error_msg = f"Index creation: {str(e)}"
            errors.append(error_msg)
        logger.error(f"Failed to create/verify index: {e}", exc_info=True)
        update_job_status("failed", "Failed to create/verify index", {"error": str(e)})
        return
        
        # Step 4: Load all scraped data into Bonsai
        records_loaded = 0
        try:
            logger.info("Loading scraped data from files...")
            docs = get_organic_store_data_from_file()
            logger.info(f"Found {len(docs)} documents to load into Bonsai")
            load_to_elasticsearch(docs)
            records_loaded = len(docs)
            logger.info(f"Successfully loaded {records_loaded} records into Bonsai")
            
            # Store metadata with last refresh timestamp
            if records_loaded > 0:
                es = get_es_client()
                metadata = {
                    "last_refresh": datetime.now().isoformat(),
                    "records_count": records_loaded,
                    "successful_states": successful_states,
                    "total_states": total_states
                }
                es.index(index="organic_stores", id="_metadata", body=metadata)
                logger.info("Metadata updated with last refresh timestamp")
        except Exception as e:
            error_msg = f"Data loading: {str(e)}"
            errors.append(error_msg)
            logger.error(f"Error loading data into Bonsai: {e}", exc_info=True)
        
        # Determine overall status
        if failed_states == 0 and records_loaded > 0:
            overall_status = "success"
            message = f"Scraping completed successfully. Loaded {records_loaded} records."
            logger.info(f"Scraping job completed successfully: {successful_states}/{total_states} states, {records_loaded} records loaded")
            update_job_status("success", message, {
                "total_states": total_states,
                "successful_states": successful_states,
                "failed_states": failed_states,
                "total_records": total_records_scraped,
                "records_loaded": records_loaded
            })
        elif successful_states > 0:
            overall_status = "partial"
            message = f"Scraping completed with {failed_states} state(s) failed. Loaded {records_loaded} records."
            logger.warning(f"Scraping job completed with partial success: {successful_states}/{total_states} states succeeded, {failed_states} failed, {records_loaded} records loaded")
            update_job_status("partial", message, {
                "total_states": total_states,
                "successful_states": successful_states,
                "failed_states": failed_states,
                "total_records": total_records_scraped,
                "records_loaded": records_loaded,
                "errors": errors[:10]  # Store first 10 errors
            })
        else:
            overall_status = "error"
            message = "Scraping failed for all states."
            logger.error(f"Scraping job failed completely: {failed_states}/{total_states} states failed")
            update_job_status("failed", message, {
                "total_states": total_states,
                "successful_states": successful_states,
                "failed_states": failed_states,
                "errors": errors[:10]
            })
        
        logger.info(f"Scraping task completed: {overall_status} - {message}")
    except Exception as e:
        error_msg = f"Fatal error in scraping task: {e}"
        logger.error(error_msg, exc_info=True)
        update_job_status("failed", error_msg, {"fatal_error": str(e)})


@app.post("/api/scrape-and-load")
@app.get("/api/scrape-and-load")  # Also support GET for cron services
async def scrape_and_load(background_tasks: BackgroundTasks):
    """
    Trigger scraping for all states and load into Bonsai.
    Returns immediately and runs scraping in the background.
    Supports both GET and POST methods for compatibility with different cron services.
    """
    # Add the scraping task to background tasks
    background_tasks.add_task(run_scraping_task)
    
    logger.info("Scraping task queued to run in background")
    
    return {
        "status": "accepted",
        "message": "Scraping task has been queued and will run in the background. This may take 20-60+ minutes to complete.",
        "note": "Check Railway logs to monitor progress"
    }
