# Organic Food Certification Web Scraper

## Overview

This is a complete ETL (Extract, Transform, Load) pipeline for organic food certification data from India's Jaivik Bharat website (FSSAI). The system scrapes certification data, stores it in Elasticsearch, and provides a searchable API and web UI.

## Features

- 🔍 **Web Scraping**: Extracts organic food certification data for all 36 Indian states/UTs
- 💾 **Data Storage**: Saves data in JSON format and indexes in Elasticsearch
- 🔎 **Search Engine**: Full-text search on company names, addresses, products, and more
- 🌐 **REST API**: FastAPI-based API for programmatic access
- 🖥️ **Web UI**: React TypeScript web application for searching and browsing
- 🐳 **Docker Support**: Easy local development with Docker Elasticsearch
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
│  │ File Loader  │→ │   Indexer    │→ │ Elasticsearch│         │
│  │              │  │   Setup      │  │  (Docker)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Elasticsearch Index: organic_stores            │   │
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
3. **Load**: JSON files are indexed into Elasticsearch
4. **Search**: API queries Elasticsearch and returns results
5. **Display**: UI renders search results in a user-friendly format

---

## Prerequisites

### Required Software

- **Python 3.8+** (3.13 recommended)
- **Node.js 18+** and **npm** (for React frontend)
- **Docker Desktop** (for local Elasticsearch)
- **Git** (for cloning the repository)

### System Requirements

- **RAM**: Minimum 4GB (8GB+ recommended for Elasticsearch)
- **Disk Space**: ~2GB for Docker images and data
- **Network**: Internet connection for scraping and package installation

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

Create/update `.env` file:

```bash
# Local Development (Docker)
ES_HOST_LOCAL=http://localhost:9200

# Production (Elastic Cloud) - Optional
ES_HOST=https://your-elastic-cloud-url:443
ES_API_KEY=your-api-key

# Use local Elasticsearch if set to true, otherwise use production
USE_LOCAL_ES=true

# Data file path
DATA_FILE_PATH=/path/to/your/project/output/

# API base URL
API_BASE_URL=http://localhost:8000
```

### 5. Install Docker Desktop

- **macOS**: `brew install --cask docker` or download from [docker.com](https://www.docker.com/products/docker-desktop/)
- **Linux**: Follow [Docker installation guide](https://docs.docker.com/engine/install/)
- **Windows**: Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)

**Important**: Start Docker Desktop before running the services.

---

## Quick Start (For New Developers)

### Automated Setup (Recommended)

**Start all services:**
```bash
./start_services.sh
```

This single command will:
1. ✅ Check Docker is running
2. ✅ Start Elasticsearch container
3. ✅ Wait for Elasticsearch to be ready
4. ✅ Check and load data if needed
5. ✅ Start API server (port 8000)
6. ✅ Start React frontend (port 5173)

**Stop all services:**
```bash
./stop_services.sh
```

### Access the Application

After running `./start_services.sh`, access:

- **🖥️ Web UI**: http://localhost:5173
- **🌐 API Server**: http://localhost:8000
- **📖 API Documentation**: http://localhost:8000/docs
- **📊 Elasticsearch**: http://localhost:9200

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

- **Unit Tests**: Mocked tests for Elasticsearch client configuration
- **Integration Tests**: Real Docker-based tests that:
  - Start Elasticsearch container
  - Test connections and operations
  - Clean up after completion

### Running Integration Tests

Integration tests require Docker to be running:

```bash
# Make sure Docker Desktop is running
docker ps

# Run tests
python -m unittest tests.search_engine.test_es_client -v
```

The integration tests will:
- Automatically start an Elasticsearch test container
- Run all test cases
- Clean up test data
- Stop and remove the container

---

## Dependencies

### Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| **requests** | Latest | HTTP library for web scraping |
| **beautifulsoup4** | Latest | HTML parsing and extraction |
| **pandas** | Latest | Data manipulation and processing |
| **elasticsearch** | Latest | Elasticsearch Python client |
| **python-dotenv** | Latest | Environment variable management |
| **fastapi** | Latest | Modern web framework for API |
| **uvicorn** | Latest | ASGI server for FastAPI |
| **watchdog** | Latest | File system monitoring |

### External Services

| Service | Purpose | Local/Cloud |
|---------|---------|-------------|
| **Elasticsearch** | Search engine and data storage | Docker (local) or Elastic Cloud (production) |
| **Jaivik Bharat Website** | Data source for scraping | External (FSSAI website) |

### Infrastructure

- **Docker**: Container runtime for Elasticsearch
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
│       ├── es_client.py  # Elasticsearch client
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

- **Local development**: Frontend (localhost:5173) + Backend (localhost:8000) → Bonsai cloud
- **Production**: Same setup, different URLs

### Environment Variables (.env)

USE_LOCAL_ES=false
ES_HOST=https://forgiving-garcinia-1kxfpcz2.us-east-1.bonsaisearch.net
ES_USERNAME=******
ES_PASSWORD=***
DATA_FILE_PATH=/Users/gaganmani/IdeaProjects/organic-food-web-scraper/output/


---

## Usage

### Scraping Data

Scrape data for all states:
```bash
export PYTHONPATH="$PWD/backend:$PYTHONPATH"
.venv/bin/python backend/ingestion/main.py
```

### Loading Data to Elasticsearch

```bash
export PYTHONPATH="$PWD/backend:$PYTHONPATH"
.venv/bin/python backend/search_engine/main.py
```

### Starting Services Manually

**1. Start Elasticsearch:**
```bash
docker run -d --name es-mvp -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:7.17.13
```

**2. Start API Server:**
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
uvicorn backend.api.api_main:app --reload --port 8000
```

**3. Start React Web UI:**
```bash
cd frontend/react-web
npm install
npm run dev
```
Then access http://localhost:5173 in your browser.

---

## API Documentation

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

### Interactive API Docs

Visit http://localhost:8000/docs for interactive Swagger documentation.

---

## Troubleshooting

### Docker Issues

**Problem**: `Cannot connect to Docker daemon`
- **Solution**: Start Docker Desktop application

**Problem**: Port 9200 already in use
- **Solution**: Stop existing Elasticsearch container: `docker stop es-mvp`

### Elasticsearch Connection Issues

**Problem**: `ConnectionError: Elasticsearch is not reachable`
- **Solution**: 
  1. Check Docker is running: `docker ps`
  2. Check Elasticsearch is ready: `curl http://localhost:9200`
  3. Verify `.env` has correct `ES_HOST_LOCAL` setting

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
  3. Verify Elasticsearch has data: `curl http://localhost:9200/organic_stores/_count`

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
- **Search Engine Layer**: Manages Elasticsearch indexing and queries
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
- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Docker Documentation](https://docs.docker.com/)
