import { useState, useEffect, useMemo } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { SearchBar } from '../components/SearchBar';
import { StoreList } from '../components/StoreList';
import { Toggle } from '../components/Toggle';
import { useSearch } from '../hooks/useSearch';
import { getCertificationStatus } from '../utils/certificationUtils';

export const SearchResultsPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const query = searchParams.get('q') || '';
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [activeOnly, setActiveOnly] = useState<boolean>(false);
  const pageSize = 20;

  const { stores, pagination, isLoading, error } = useSearch(query, currentPage, pageSize);

  // Filter stores based on activeOnly toggle
  const filteredStores = useMemo(() => {
    if (!activeOnly) return stores;
    return stores.filter(store => {
      const status = getCertificationStatus(store.valid_to);
      return !status.isExpired;
    });
  }, [stores, activeOnly]);

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

  const expiredCount = stores.length - filteredStores.length;

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
      
      {!isLoading && stores.length > 0 && (
        <div className="mt-6 mb-4 flex items-center justify-between bg-white rounded-lg border border-gray-200 shadow-sm p-4">
          <Toggle
            checked={activeOnly}
            onChange={setActiveOnly}
            label="Active Only"
            description={activeOnly ? `Hiding ${expiredCount} expired certification${expiredCount !== 1 ? 's' : ''}` : 'Show only active certifications'}
          />
          {activeOnly && (
            <div className="text-sm text-gray-600">
              <span className="font-semibold text-green-600">{filteredStores.length}</span>
              <span className="text-gray-500"> of {stores.length} results</span>
            </div>
          )}
        </div>
      )}
      
      {!isLoading && (
        <StoreList 
          stores={filteredStores} 
          pagination={pagination}
          loading={isLoading} 
          error={error}
          onPageChange={handlePageChange}
        />
      )}
    </div>
  );
};