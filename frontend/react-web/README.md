# React TypeScript Web Frontend

Modern React web application using TypeScript, plain React components (standard HTML elements), and Tailwind CSS. Follows React 19+ patterns from [react.dev](https://react.dev).

## Technology Stack

- **React 19+** - Latest React library
- **TypeScript 5+** - Type-safe JavaScript
- **Vite 5+** - Fast build tool
- **Tailwind CSS 3+** - Utility-first CSS
- **TanStack Query v5+** - Server state management
- **Axios** - HTTP client

## Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

## Installation

### 1. Install Dependencies

```bash
cd frontend/react-web
npm install
```

### 2. Install Additional Dependencies (if needed)

```bash
npm install @tanstack/react-query axios
npm install -D tailwindcss postcss autoprefixer
```

### 3. Initialize Tailwind CSS (if not already done)

```bash
npx tailwindcss init -p
```

## Environment Setup

The `.env` file is already configured with:
```
VITE_API_URL=http://localhost:8000
```

Update this if your API runs on a different port.

## Development

### Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Type Checking

```bash
npm run type-check
```

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
react-web/
├── src/
│   ├── components/
│   │   ├── SearchBar.tsx
│   │   ├── StoreCard.tsx
│   │   ├── StoreList.tsx
│   │   └── Layout/
│   │       ├── Header.tsx
│   │       └── Footer.tsx
│   ├── services/
│   │   └── api.ts
│   ├── hooks/
│   │   └── useSearch.ts
│   ├── types/
│   │   └── store.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── public/
├── .env
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Features

- ✅ TypeScript for type safety
- ✅ React Query for efficient data fetching
- ✅ Tailwind CSS for styling
- ✅ Plain React components (standard HTML elements)
- ✅ Responsive design (mobile-first)
- ✅ Loading and error states
- ✅ Search functionality
- ✅ Store cards with certification status
- ✅ Expandable product lists

## React Patterns Used

Following [react.dev](https://react.dev) best practices:

1. **Component Composition** - Build UI from reusable components
2. **State Management** - `useState` for local state, React Query for server state
3. **Event Handling** - Standard React event handlers (`onSubmit`, `onChange`)
4. **Conditional Rendering** - `if` statements, ternary operators
5. **Lists and Keys** - `map()` with proper keys
6. **Standard HTML Elements** - `<div>`, `<form>`, `<input>`, `<button>`, `<details>`, etc.

## API Integration

The frontend connects to the FastAPI backend at `/api/search` endpoint:

```typescript
GET /api/search?query=<search_term>
```

Response format:
```json
{
  "results": [
    {
      "store_name": "...",
      "certification_id": "...",
      "state": "...",
      "address": "...",
      "email": "...",
      "certification_body": "...",
      "valid_from": "...",
      "valid_to": "...",
      "products": "...",
      "scraped_at": "..."
    }
  ]
}
```

## Development Notes

- All components use TypeScript with strict type checking
- No component libraries - uses standard HTML elements
- Tailwind CSS for all styling
- React Query handles caching and refetching automatically
- Components follow React 19+ patterns from react.dev
