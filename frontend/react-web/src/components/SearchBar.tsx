import { useEffect, useMemo, useState, FormEvent } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  loading?: boolean;
}

const RECENT_KEY = 'recentSearches';
const MAX_RECENT = 8;

function loadRecent(): string[] {
  try {
    const raw = localStorage.getItem(RECENT_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((x) => typeof x === 'string').map((x) => x.trim()).filter(Boolean);
  } catch {
    return [];
  }
}

function saveRecent(query: string) {
  const q = query.trim();
  if (!q) return;

  const existing = loadRecent();
  const next = [q, ...existing.filter((x) => x.toLowerCase() !== q.toLowerCase())].slice(0, MAX_RECENT);

  try {
    localStorage.setItem(RECENT_KEY, JSON.stringify(next));
  } catch {
    // ignore storage errors
  }
}

export const SearchBar = ({ onSearch, loading = false }: SearchBarProps) => {
  const [query, setQuery] = useState<string>('');
  const [recent, setRecent] = useState<string[]>([]);
  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState<number>(-1);

  useEffect(() => {
    setRecent(loadRecent());
  }, []);

  const filteredRecent = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return recent;
    return recent.filter((x) => x.toLowerCase().includes(q));
  }, [query, recent]);

  const runSearch = (q: string) => {
    const trimmed = q.trim();
    onSearch(trimmed);
    saveRecent(trimmed);
    setRecent(loadRecent());
    setOpen(false);
    setActiveIndex(-1);
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // If user has navigated dropdown, Enter uses that item
    if (open && activeIndex >= 0 && activeIndex < filteredRecent.length) {
      const selected = filteredRecent[activeIndex];
      setQuery(selected);
      runSearch(selected);
      return;
    }

    runSearch(query);
  };

  return (
    <div className="relative mb-8">
      <form onSubmit={handleSubmit} className="flex gap-4">
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setActiveIndex(-1);
            setOpen(true);
          }}
          onFocus={() => {
            setOpen(true);
            setRecent(loadRecent());
          }}
          onBlur={() => {
            // delay close so click on dropdown works
            window.setTimeout(() => setOpen(false), 120);
          }}
          onKeyDown={(e) => {
            if (!open) return;

            if (e.key === 'Escape') {
              setOpen(false);
              setActiveIndex(-1);
              return;
            }

            if (e.key === 'ArrowDown') {
              e.preventDefault();
              if (filteredRecent.length === 0) return;
              setActiveIndex((prev) => Math.min(prev + 1, filteredRecent.length - 1));
              return;
            }

            if (e.key === 'ArrowUp') {
              e.preventDefault();
              if (filteredRecent.length === 0) return;
              setActiveIndex((prev) => Math.max(prev - 1, 0));
              return;
            }

            if (e.key === 'Enter') {
              // form submit will handle selection or query
              return;
            }
          }}
          placeholder="Search stores, products, addresses..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-green-500"
          disabled={loading}
        />

        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {open && filteredRecent.length > 0 && (
        <div className="absolute z-10 mt-2 w-full bg-white border border-gray-200 rounded-md shadow-lg overflow-hidden">
          <div className="px-3 py-2 text-xs text-gray-500">Recent searches</div>
          <ul className="max-h-60 overflow-auto">
            {filteredRecent.map((item, idx) => (
              <li key={`${item}-${idx}`}>
                <button
                  type="button"
                  className={`w-full text-left px-3 py-2 text-sm hover:bg-gray-50 ${
                    idx === activeIndex ? 'bg-gray-100' : ''
                  }`}
                  onMouseDown={(e) => e.preventDefault()} // prevent blur before click
                  onClick={() => {
                    setQuery(item); // fill only, wait for Enter (your requirement)
                    setOpen(false);
                    setActiveIndex(-1);
                  }}
                >
                  {item}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};