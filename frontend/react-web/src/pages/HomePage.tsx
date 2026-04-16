import { useQuery } from '@tanstack/react-query';
import { SearchBar } from '../components/SearchBar';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';

export const HomePage = () => {
  const navigate = useNavigate();

  const handleSearch = (query: string) => {
    navigate(`/search?q=${encodeURIComponent(query)}`);
  };

  const { data: totalData } = useQuery({
    queryKey: ['totalCount'],
    queryFn: () => api.search('', 1, 1),
    staleTime: 10 * 60 * 1000,
  });

  const { data: refreshData } = useQuery({
    queryKey: ['lastRefresh'],
    queryFn: () => api.getLastRefresh(),
    staleTime: 10 * 60 * 1000,
  });

  const totalStores = totalData?.pagination?.total;
  const lastRefresh = refreshData?.last_refresh
    ? new Date(refreshData.last_refresh).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    : null;

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
      <div className="w-full max-w-2xl">
        <SearchBar onSearch={handleSearch} loading={false} centered={true} value="" />

        <div className="mt-10 grid grid-cols-3 gap-4 text-center">
          <div className="bg-green-50 rounded-lg p-4">
            <p className="text-2xl font-bold text-green-700">
              {totalStores ? totalStores.toLocaleString('en-IN') : '—'}
            </p>
            <p className="text-sm text-gray-500 mt-1">Certified Stores</p>
          </div>
          <div className="bg-green-50 rounded-lg p-4">
            <p className="text-2xl font-bold text-green-700">36</p>
            <p className="text-sm text-gray-500 mt-1">States &amp; UTs</p>
          </div>
          <div className="bg-green-50 rounded-lg p-4">
            <p className="text-2xl font-bold text-green-700">
              {lastRefresh ?? '—'}
            </p>
            <p className="text-sm text-gray-500 mt-1">Last Updated</p>
          </div>
        </div>
      </div>
    </div>
  );
};
