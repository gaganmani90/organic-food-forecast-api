import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { SearchBar } from '../components/SearchBar';
import { StoreList } from '../components/StoreList';
import { useSearch } from '../hooks/useSearch';

export const SearchResultsPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const query = searchParams.get('q') || '';
  const [currentPage, setCurrentPage] = useState<number>(1);
  const pageSize = 20;

  const { stores, pagination, isLoading, error } = useSearch(query, currentPage, pageSize);

  useEffect(() => {
    setCurrentPage(1);
  }, [query]);

  const handleSearch = (newQuery: string) => {
    if (newQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(newQuery)}`);
    } else {
      navigate('/');
    }
    setCurrentPage(1);
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <SearchBar 
        onSearch={handleSearch} 
        loading={isLoading} 
        centered={false}
        value={query}
      />
      
      {isLoading && (
        <div className="mt-4">
          <div className="w-full bg-gray-200 rounded-full h-1.5">
            <div className="bg-green-600 h-1.5 rounded-full animate-pulse" style={{ width: '100%' }}></div>
          </div>
          <p className="text-sm text-gray-500 mt-2 text-center">Searching...</p>
        </div>
      )}
      
      {!isLoading && (
        <StoreList 
          stores={stores} 
          pagination={pagination}
          loading={isLoading} 
          error={error}
          onPageChange={handlePageChange}
        />
      )}
    </div>
  );
};