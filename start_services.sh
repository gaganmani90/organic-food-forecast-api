#!/bin/bash

# Startup script for Organic Food Web Scraper services
# This script starts Elasticsearch, API server, and React frontend automatically

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

# 4. Start React Frontend
echo -e "${YELLOW}🖥️  Step 4: Starting React Frontend...${NC}"

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed or not in PATH${NC}"
    echo -e "${YELLOW}Please install Node.js 18+ and try again.${NC}"
    echo -e "${YELLOW}On macOS: brew install node${NC}"
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed or not in PATH${NC}"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "$PROJECT_ROOT/frontend/react-web" ]; then
    echo -e "${RED}❌ React frontend directory not found at $PROJECT_ROOT/frontend/react-web${NC}"
    exit 1
fi

# Check if node_modules exists, if not install dependencies
if [ ! -d "$PROJECT_ROOT/frontend/react-web/node_modules" ]; then
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    cd "$PROJECT_ROOT/frontend/react-web"
    npm install
    cd "$PROJECT_ROOT"
    echo -e "${GREEN}✅ Dependencies installed!${NC}"
fi

# Check if frontend port is already in use
if lsof -ti:5173 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 5173 is already in use. Killing existing process...${NC}"
    lsof -ti:5173 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Start React dev server in background
cd "$PROJECT_ROOT/frontend/react-web"
nohup npm run dev > "$PROJECT_ROOT/frontend_server.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$PROJECT_ROOT/frontend_server.pid"
cd "$PROJECT_ROOT"

# Wait for frontend to be ready
sleep 5
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ React frontend is running at http://localhost:5173${NC}\n"
else
    echo -e "${YELLOW}⏳ React frontend is starting... (check logs in frontend_server.log)${NC}\n"
fi

# Summary
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✨ All services started successfully!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "📊 Elasticsearch: http://localhost:9200"
echo -e "🌐 API Server:    http://localhost:8000"
echo -e "📖 API Docs:      http://localhost:8000/docs"
echo -e "🖥️  Web UI:        http://localhost:5173"
echo -e ""
echo -e "${YELLOW}📝 Logs:${NC}"
echo -e "   API:      $PROJECT_ROOT/api_server.log"
echo -e "   Frontend: $PROJECT_ROOT/frontend_server.log"
echo -e ""
echo -e "${YELLOW}🛑 To stop all services, run: ./stop_services.sh${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
