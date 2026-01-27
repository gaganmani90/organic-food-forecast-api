# Organic Food Certification Web Scraper

## Overview

This is a complete ETL (Extract, Transform, Load) pipeline for organic food certification data from India's Jaivik Bharat website (FSSAI). The system scrapes certification data, stores it in Elasticsearch, and provides a searchable API and web UI.

## Features

- 🔍 **Web Scraping**: Extracts organic food certification data for all 36 Indian states/UTs
- 💾 **Data Storage**: Saves data in JSON format and indexes in Elasticsearch
- 🔎 **Search Engine**: Full-text search on company names, addresses, products, and more
- 🌐 **REST API**: FastAPI-based API for programmatic access
- 🖥️ **Web UI**: React TypeScript web application for searching and browsing
- ☁️ **Cloud Search**: Uses Bonsai (OpenSearch cloud) for all environments
- ⏰ **Scheduled Scraping**: Automated daily scraping via cron jobs
- 📅 **Last Refresh Display**: UI shows when data was last updated
- ✅ **Testing**: Comprehensive unit and integration tests

---

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Jaivik Bharat Website                     │
│                    (https://jaivikbharat.fssai.gov.in)            │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INGESTION LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Scraper    │→ │   Manager    │→ │  Data Saver  │         │
│  │  (Organic)   │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                  │                  │                │
│         └──────────────────┴──────────────────┘                │
│                            │                                     │
│                            ▼                                     │
│              ┌─────────────────────────┐                        │
│              │  JSON Files (per state)  │                        │
│              │  output/               │                        │
│              └─────────────────────────┘                        │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             │ Load Data
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SEARCH ENGINE LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ File Loader  │→ │   Indexer    │→ │  Bonsai      │         │
│  │              │  │   Setup      │  │  (Cloud)     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         OpenSearch Index: organic_stores               │   │
│  │  - Full-text search on store_name, address, products  │   │
│  │  - Filter by state, certification dates                │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             │ Query
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER                                  │
│  ┌──────────────────────────────────────────────────────┐     │
│  │              FastAPI Server (Port 8000)               │     │
│  │  GET /api/search?query=<search_term>                 │     │
│  │  GET /api/last-refresh                                │     │
│  │  POST /api/scrape-and-load                            │     │
│  │  - CORS enabled                                        │     │
│  │  - Returns up to 10,000 results                       │     │
│  └──────────────────────────────────────────────────────┘     │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       UI LAYER                                  │
│  ┌──────────────────────────────────────────────────────┐     │
│  │         React Web Application (Port 5173)            │     │
│  │  - Modern TypeScript React app                        │     │
│  │  - Search interface with Tailwind CSS                 │     │
│  │  - Display store details, products, certifications  │     │
│  │  - Responsive design                                   │     │
│  └──────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Extract**: Scraper fetches data from Jaivik Bharat website
2. **Transform**: Data is parsed and structured into JSON format
3. **Load**: JSON files are indexed into Bonsai (OpenSearch cloud)
4. **Search**: API queries Bonsai and returns results
5. **Display**: UI renders search results in a user-friendly format

---

## Prerequisites

### Required Software

- **Python 3.8+** (3.13 recommended)
- **Node.js 18+** and **npm** (for React frontend)
- **Git** (for cloning the repository)

### System Requirements

- **RAM**: Minimum 4GB
- **Network**: Internet connection (Bonsai cloud requires internet)

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd organic-food-web-scraper
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file with Bonsai credentials:

```bash
USE_LOCAL_ES=false
ES_HOST=https://forgiving-garcinia-1kxfpcz2.us-east-1.bonsaisearch.net
ES_USERNAME=your-bonsai-username
ES_PASSWORD=your-bonsai-password
DATA_FILE_PATH=/absolute/path/to/organic-food-web-scraper/output/
```

**Note**: All environments use Bonsai (OpenSearch cloud). No Docker needed.

---

## Quick Start (For New Developers)

### Automated Setup (Recommended)

**Start all services:**
```bash
./start_services.sh
```

This single command will:
1. ✅ Check Bonsai connection and load data if needed
2. ✅ Start API server (port 8000)
3. ✅ Start React frontend (port 5173)

**Stop all services:**
```bash
./stop_services.sh
```

### Access the Application

After running `./start_services.sh`, access:

- **🖥️ Web UI**: http://localhost:5173
- **🌐 API Server**: http://localhost:8000
- **📖 API Documentation**: http://localhost:8000/docs
- **☁️ Search Backend**: Bonsai (OpenSearch cloud)

### First Time Setup

If this is your first time running the project:

1. **Scrape data** (if not already done):
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
   python backend/ingestion/main.py
   ```

2. **Load data into Elasticsearch**:
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
   python backend/search_engine/main.py
   ```

3. **Start services**:
   ```bash
   ./start_services.sh
   ```

---

## Testing

### Run All Tests

```bash
# Using the test runner script
python run_tests.py

# Or using unittest directly
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test Coverage

The project includes:

- **Unit Tests**: Mocked tests for OpenSearch client configuration

---

## Dependencies

### Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| **requests** | Latest | HTTP library for web scraping |
| **beautifulsoup4** | Latest | HTML parsing and extraction |
| **pandas** | Latest | Data manipulation and processing |
| **opensearch-py** | Latest | OpenSearch Python client (for Bonsai) |
| **python-dotenv** | Latest | Environment variable management |
| **fastapi** | Latest | Modern web framework for API |
| **uvicorn** | Latest | ASGI server for FastAPI |
| **watchdog** | Latest | File system monitoring |

### External Services

| Service | Purpose | Location |
|---------|---------|----------|
| **Bonsai (OpenSearch)** | Search engine and data storage | Cloud (all environments) |
| **Jaivik Bharat Website** | Data source for scraping | External (FSSAI website) |

### Infrastructure

- **Bonsai**: OpenSearch cloud service (free tier available)
- **Python Virtual Environment**: Dependency isolation
- **Git**: Version control

---

## Project Structure

```
organic-food-web-scraper/
├── backend/                # Backend services
│   ├── api/               # API layer
│   │   └── api_main.py   # FastAPI application
│   ├── ingestion/         # Data scraping layer
│   │   ├── main.py        # Scraper entry point
│   │   ├── managers/      # Scraper management
│   │   ├── scrappers/     # Web scraping logic
│   │   ├── utils/         # Utility functions
│   │   └── output/        # Scraped JSON files
│   └── search_engine/     # Search and indexing layer
│       ├── main.py        # Data loader entry point
│       ├── es_client.py  # OpenSearch client (Bonsai)
│       ├── index_setup.py # Index configuration
│       ├── loader.py      # Data loading logic
│       ├── search.py      # Search functions
│       └── loaders/       # Data loaders
├── frontend/              # Frontend applications
│   └── react-web/        # React TypeScript application
│       ├── src/          # React source code
│       ├── package.json  # Node.js dependencies
│       └── README.md     # Frontend documentation
├── tests/                 # Test suite
│   ├── ingestion/         # Ingestion tests
│   └── search_engine/     # Search engine tests
├── .env                   # Environment configuration
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
├── start_services.sh     # Startup script
├── stop_services.sh      # Shutdown script
└── run_tests.py          # Test runner
```

---

## Configuration

### Infrastructure Setup

**All environments use Bonsai (OpenSearch cloud)** - no local Elasticsearch.

- **Local**: Frontend (localhost:5173) + Backend (localhost:8000) → Bonsai cloud
- **Production**: Vercel (frontend) + Railway (backend) → Bonsai cloud

### Production URLs (Exact Links)

**Frontend (Vercel):**
- Production URL: Check your Vercel dashboard
- Vercel Dashboard: https://vercel.com/dashboard

**Backend (Railway):**
- Production URL: https://organic-food-forecast-api-production.up.railway.app
- API Docs: https://organic-food-forecast-api-production.up.railway.app/docs
- Railway Dashboard: https://railway.app/dashboard

**Search Engine (Bonsai):**
- Cluster URL: https://forgiving-garcinia-1kxfpcz2.us-east-1.bonsaisearch.net
- Bonsai Dashboard: https://app.bonsai.io

**Scheduled Scraping (Cron Job):**
- Service: cron-job.org
- Endpoint: https://organic-food-forecast-api-production.up.railway.app/api/scrape-and-load
- Schedule: Daily at 2 AM UTC (`0 2 * * *`)
- Cron Dashboard: https://cron-job.org

### Environment Variables (.env)

```bash
USE_LOCAL_ES=false
ES_HOST=https://forgiving-garcinia-1kxfpcz2.us-east-1.bonsaisearch.net
ES_USERNAME=your-bonsai-username
ES_PASSWORD=your-bonsai-password
DATA_FILE_PATH=/absolute/path/to/organic-food-web-scraper/output/
```

**Production Deployment:**
- **Frontend (Vercel)**: Set `VITE_API_URL=https://organic-food-forecast-api-production.up.railway.app`
- **Backend (Railway)**: Set `ES_HOST`, `ES_USERNAME`, `ES_PASSWORD`, `DATA_FILE_PATH`


---

## Usage

### Scraping Data

**Option 1: Manual Scraping (Local)**
```bash
export PYTHONPATH="$PWD/backend:$PYTHONPATH"
.venv/bin/python backend/ingestion/main.py
```

**Option 2: API Endpoint (Production)**
```bash
# Trigger scraping via API
curl -X POST https://organic-food-forecast-api-production.up.railway.app/api/scrape-and-load

# Or use GET (also supported)
curl -X GET https://organic-food-forecast-api-production.up.railway.app/api/scrape-and-load
```

**Option 3: Scheduled Scraping (Automated)**
- Configured via cron-job.org
- Runs daily at 2 AM UTC
- Endpoint: `POST https://organic-food-forecast-api-production.up.railway.app/api/scrape-and-load`
- Monitor execution in cron-job.org dashboard

### Loading Data to Bonsai

```bash
export PYTHONPATH="$PWD/backend:$PYTHONPATH"
.venv/bin/python backend/search_engine/main.py
```

### Starting Services Manually

**1. Start API Server:**
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
uvicorn backend.api.api_main:app --reload --port 8000
```

**2. Start React Web UI:**
```bash
cd frontend/react-web
npm install
npm run dev
```
Then access http://localhost:5173 in your browser.

---

## API Documentation

### Base URL
- **Local**: `http://localhost:8000`
- **Production**: `https://organic-food-forecast-api-production.up.railway.app`

### Search Endpoint

**GET** `/api/search`

Query parameters:
- `query` (optional): Search term for full-text search

Example:
```bash
curl "http://localhost:8000/api/search?query=organic"
```

Response:
```json
{
  "results": [
    {
      "store_name": "...",
      "certification_id": "...",
      "state": "...",
      "email": "...",
      "address": "...",
      "products": "...",
      "valid_from": "YYYY-MM-DD",
      "valid_to": "YYYY-MM-DD",
      "scraped_at": "YYYY-MM-DDTHH:MM:SS"
    }
  ],
  "pagination": {
    "total": 123,
    "page": 1,
    "page_size": 20,
    "total_pages": 7
  }
}
```

### Last Refresh Endpoint

**GET** `/api/last-refresh`

Returns the last date when data was refreshed.

**Example Request:**
```bash
curl https://organic-food-forecast-api-production.up.railway.app/api/last-refresh
```

**Example Response:**
```json
{
  "last_refresh": "2025-01-23T14:30:15",
  "last_refresh_formatted": "2025-01-23T14:30:15"
}
```

### Scrape and Load Endpoint

**POST** or **GET** `/api/scrape-and-load`

Triggers scraping for all 36 states and automatically loads data into Bonsai.

**Example Request:**
```bash
curl -X POST https://organic-food-forecast-api-production.up.railway.app/api/scrape-and-load
```

**Example Response:**
```json
{
  "status": "success",
  "message": "Scraping completed successfully. Loaded 5000 records.",
  "total_states": 36,
  "successful_states": 36,
  "failed_states": 0,
  "total_records": 5000,
  "records_loaded": 5000,
  "errors": null
}
```

**Note**: This endpoint may take 20-60+ minutes to complete. The response is returned after scraping finishes.

### Interactive API Docs

Access interactive API documentation (Swagger UI):
- **Local**: http://localhost:8000/docs
- **Production**: https://organic-food-forecast-api-production.up.railway.app/docs

---

## Troubleshooting

### Bonsai Connection Issues

**Problem**: `ConnectionError: Search backend not reachable`
- **Solution**: 
  1. Verify Bonsai cluster is active in dashboard
  2. Check `.env` has correct `ES_HOST`, `ES_USERNAME`, `ES_PASSWORD`
  3. Test connection: `curl -u username:password https://your-cluster.bonsaisearch.net`

### API/UI Not Starting

**Problem**: Port 8000 or 5173 already in use
- **Solution**: 
  ```bash
  # Kill process on port 8000
  lsof -ti:8000 | xargs kill -9
  
  # Kill process on port 5173 (React dev server)
  lsof -ti:5173 | xargs kill -9
  ```

### Data Not Loading

**Problem**: No results in search
- **Solution**: 
  1. Check if data exists: `ls output/*.json`
  2. Load data: `python backend/search_engine/main.py`
  3. Verify Bonsai has data: `curl -u username:password https://your-cluster.bonsaisearch.net/organic_stores/_count`

---

## Development

### Running Tests

```bash
# All tests
python run_tests.py

# Specific test file
python -m unittest tests.search_engine.test_es_client -v
```

### Code Structure

- **Ingestion Layer**: Handles web scraping and data extraction
- **Search Engine Layer**: Manages Bonsai (OpenSearch) indexing and queries
- **API Layer**: Provides REST API endpoints
- **UI Layer**: React TypeScript web application

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and add tests
3. Run tests: `python run_tests.py`
4. Commit and push changes

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

---

## License

MIT License

---

## Contact

For questions or suggestions, reach out to [your email or GitHub handle].

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [OpenSearch Documentation](https://opensearch.org/docs/)
- [Bonsai Documentation](https://docs.bonsai.io/)
