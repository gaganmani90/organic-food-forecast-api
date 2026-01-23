# React TypeScript Web Frontend Setup

## Prerequisites

Make sure you have Node.js 18+ and npm installed. Check with:
```bash
node --version  # Should be 18+
npm --version
```

If not installed:
- **macOS**: `brew install node`
- **Linux**: Use your package manager or [nvm](https://github.com/nvm-sh/nvm)
- **Windows**: Download from [nodejs.org](https://nodejs.org/)

## Setup Commands

Run these commands in order:

### 1. Install Dependencies
```bash
cd frontend/react-web
npm install
```

### 2. Install Additional Dependencies (if not already in package.json)
```bash
npm install @tanstack/react-query axios
npm install -D tailwindcss postcss autoprefixer
```

### 3. Initialize Tailwind CSS (if not already done)
```bash
npx tailwindcss init -p
```

### 4. Verify Setup
```bash
npm run type-check  # Check TypeScript
npm run dev         # Start dev server (should work after source files are created)
```

## Development

```bash
npm run dev      # Start dev server on http://localhost:5173
npm run build    # Build for production
npm run type-check  # Type check without building
```

## Environment Variables

Create `.env` file in `frontend/react-web/`:
```
VITE_API_URL=http://localhost:8000
```
