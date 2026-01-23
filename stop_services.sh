#!/bin/bash

# Stop script for Organic Food Web Scraper services

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🛑 Stopping all services...${NC}\n"

# Stop API server
if [ -f "$PROJECT_ROOT/api_server.pid" ]; then
    API_PID=$(cat "$PROJECT_ROOT/api_server.pid")
    if kill -0 "$API_PID" 2>/dev/null; then
        echo -e "${YELLOW}🛑 Stopping API server (PID: $API_PID)...${NC}"
        kill "$API_PID" 2>/dev/null || true
        rm "$PROJECT_ROOT/api_server.pid"
        echo -e "${GREEN}✅ API server stopped${NC}"
    fi
fi

# Stop Frontend server
if [ -f "$PROJECT_ROOT/frontend_server.pid" ]; then
    FRONTEND_PID=$(cat "$PROJECT_ROOT/frontend_server.pid")
    if kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo -e "${YELLOW}🛑 Stopping Frontend server (PID: $FRONTEND_PID)...${NC}"
        # Kill the process and its children (npm run dev spawns child processes)
        pkill -P "$FRONTEND_PID" 2>/dev/null || true
        kill "$FRONTEND_PID" 2>/dev/null || true
        rm "$PROJECT_ROOT/frontend_server.pid"
        echo -e "${GREEN}✅ Frontend server stopped${NC}"
    fi
fi

# Kill any processes on ports 8000 and 5173
if lsof -ti:8000 > /dev/null 2>&1; then
    echo -e "${YELLOW}🛑 Killing process on port 8000...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
fi

if lsof -ti:5173 > /dev/null 2>&1; then
    echo -e "${YELLOW}🛑 Killing process on port 5173 (React dev server)...${NC}"
    lsof -ti:5173 | xargs kill -9 2>/dev/null || true
fi

# Stop Elasticsearch (optional - comment out if you want to keep it running)
read -p "Do you want to stop Elasticsearch container? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if docker ps --format '{{.Names}}' | grep -q "^es-mvp$"; then
        echo -e "${YELLOW}🛑 Stopping Elasticsearch container...${NC}"
        docker stop es-mvp
        echo -e "${GREEN}✅ Elasticsearch stopped${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️  Elasticsearch container left running${NC}"
fi

echo -e "\n${GREEN}✅ All services stopped!${NC}"
