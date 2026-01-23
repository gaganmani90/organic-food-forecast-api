#!/bin/bash

# Startup script for Organic Food Web Scraper services
# This script starts Elasticsearch, API server, and UI automatically

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Organic Food Web Scraper Services...${NC}\n"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed or not in PATH${NC}"
    exit 1
fi

# Check if Docker daemon is running
if ! docker ps &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running${NC}"
    echo -e "${YELLOW}Please start Docker Desktop and wait for it to be ready, then run this script again.${NC}"
    echo -e "${YELLOW}You can start Docker Desktop from Applications or by running: open -a Docker${NC}"
    exit 1
fi

# 1. Start Elasticsearch Docker container
echo -e "${YELLOW}📦 Step 1: Starting Elasticsearch...${NC}"
if docker ps -a --format '{{.Names}}' | grep -q "^es-mvp$"; then
    if docker ps --format '{{.Names}}' | grep -q "^es-mvp$"; then
        echo -e "${GREEN}✅ Elasticsearch container already running${NC}"
    else
        echo -e "${YELLOW}🔄 Starting existing Elasticsearch container...${NC}"
        docker start es-mvp
    fi
else
    echo -e "${YELLOW}🆕 Creating new Elasticsearch container...${NC}"
    docker run -d \
        --name es-mvp \
        -p 9200:9200 \
        -e "discovery.type=single-node" \
        -e "xpack.security.enabled=false" \
        docker.elastic.co/elasticsearch/elasticsearch:7.17.13
fi

# Wait for Elasticsearch to be ready
echo -e "${YELLOW}⏳ Waiting for Elasticsearch to be ready...${NC}"
for i in {1..60}; do
    if curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Elasticsearch is ready!${NC}\n"
        break
    fi
    if [ $i -eq 60 ]; then
        echo -e "${RED}❌ Elasticsearch did not become ready in time${NC}"
        exit 1
    fi
    sleep 1
done

# 2. Check if data needs to be loaded
echo -e "${YELLOW}📊 Step 2: Checking Elasticsearch data...${NC}"
ES_COUNT=$(curl -s http://localhost:9200/organic_stores/_count 2>/dev/null | grep -o '"count":[0-9]*' | cut -d':' -f2 || echo "0")

if [ "$ES_COUNT" = "0" ] || [ -z "$ES_COUNT" ]; then
    echo -e "${YELLOW}📥 No data found. Loading data into Elasticsearch...${NC}"
    export PYTHONPATH="$PROJECT_ROOT/backend:$PYTHONPATH"
    "$PROJECT_ROOT/.venv/bin/python" "$PROJECT_ROOT/backend/search_engine/main.py"
    echo -e "${GREEN}✅ Data loaded!${NC}\n"
else
    echo -e "${GREEN}✅ Elasticsearch already has $ES_COUNT documents${NC}\n"
fi

# 3. Start API server
echo -e "${YELLOW}🌐 Step 3: Starting API server...${NC}"
export PYTHONPATH="$PROJECT_ROOT/backend:$PYTHONPATH"

# Check if API is already running
if lsof -ti:8000 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use. Killing existing process...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Start API server in background
nohup "$PROJECT_ROOT/.venv/bin/uvicorn" backend.api.api_main:app --reload --port 8000 > "$PROJECT_ROOT/api_server.log" 2>&1 &
API_PID=$!
echo $API_PID > "$PROJECT_ROOT/api_server.pid"

# Wait for API to be ready
sleep 3
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API server is running at http://localhost:8000${NC}\n"
else
    echo -e "${YELLOW}⏳ API server is starting... (check logs in api_server.log)${NC}\n"
fi

# 4. Start UI
echo -e "${YELLOW}🖥️  Step 4: Starting Streamlit UI...${NC}"

# Check if UI is already running
if lsof -ti:8501 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 8501 is already in use. Killing existing process...${NC}"
    lsof -ti:8501 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Start UI in background
cd "$PROJECT_ROOT/frontend/streamlit-ui"
nohup "$PROJECT_ROOT/.venv/bin/streamlit" run search_ui.py > "$PROJECT_ROOT/ui_server.log" 2>&1 &
UI_PID=$!
echo $UI_PID > "$PROJECT_ROOT/ui_server.pid"
cd "$PROJECT_ROOT"

sleep 3
echo -e "${GREEN}✅ Streamlit UI is starting...${NC}\n"

# Summary
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✨ All services started successfully!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "📊 Elasticsearch: http://localhost:9200"
echo -e "🌐 API Server:    http://localhost:8000"
echo -e "📖 API Docs:      http://localhost:8000/docs"
echo -e "🖥️  UI:            http://localhost:8501"
echo -e ""
echo -e "${YELLOW}📝 Logs:${NC}"
echo -e "   API: $PROJECT_ROOT/api_server.log"
echo -e "   UI:  $PROJECT_ROOT/ui_server.log"
echo -e ""
echo -e "${YELLOW}🛑 To stop all services, run: ./stop_services.sh${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
