import { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { Link } from 'react-router-dom';

export const Header = () => {
  const [lastRefresh, setLastRefresh] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchLastRefresh = async () => {
      try {
        setIsLoading(true);
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
      } finally {
        setIsLoading(false);
      }
    };

    fetchLastRefresh();
  }, []);

  return (
    <header className="bg-green-600 text-white shadow-md">
      <nav className="container mx-auto px-4 py-4">
      <div className="flex flex-col gap-1">
          <div className="flex justify-between items-center">
            <Link to="/" className="text-2xl font-bold hover:underline cursor-pointer">
              Organic Store Search
            </Link>
            {!isLoading && lastRefresh && (
              <div className="text-sm text-green-100">
                Last updated: {lastRefresh}
              </div>
            )}
          </div>
          <p className="text-sm text-green-100">Search certified organic food stores across India</p>
        </div>
      </nav>
    </header>
  );
};
