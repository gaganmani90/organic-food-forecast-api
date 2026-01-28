import { SearchBar } from '../components/SearchBar';
import { api } from '../services/api';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const HomePage = () => {
  const [lastRefresh, setLastRefresh] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLastRefresh = async () => {
      try {
        const response = await api.getLastRefresh();
        if (response.last_refresh) {
          const date = new Date(response.last_refresh);
          setLastRefresh(date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
          }));
        }
      } catch (error) {
        console.error('Failed to fetch last refresh date:', error);
      }
    };
    fetchLastRefresh();
  }, []);

  const handleSearch = (query: string) => {
    navigate(`/search?q=${encodeURIComponent(query)}`);
  };

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="w-full max-w-2xl px-4">
        <SearchBar onSearch={handleSearch} loading={false} centered={true} value="" />
      </div>
    </div>
  );
};