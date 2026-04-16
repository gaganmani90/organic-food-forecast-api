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
  const [activeOnly, setActiveOnly] = useState<boolean>(true);
  const [selectedState, setSelectedState] = useState<string>('');
  const pageSize = 20;

  const { stores, pagination, isLoading, error } = useSearch(query, currentPage, pageSize);

  // Collect unique state values for dropdown
  const stateOptions = useMemo(() => {
    const unique = Array.from(new Set(stores.map(s => s.state).filter(Boolean))).sort();
    return unique;
  }, [stores]);

  // Filter stores based on activeOnly toggle and state selection
  const filteredStores = useMemo(() => {
    return stores.filter(store => {
      if (activeOnly) {
        const status = getCertificationStatus(store.valid_to);
        if (status.isExpired) return false;
      }
      if (selectedState && store.state !== selectedState) return false;
      return true;
    });
  }, [stores, activeOnly, selectedState]);

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
        <div className="mt-6 mb-4 flex flex-wrap items-center gap-4 bg-white rounded-lg border border-gray-200 shadow-sm p-4">
          <Toggle
            checked={activeOnly}
            onChange={(val) => { setActiveOnly(val); }}
            label="Active Only"
            description={activeOnly ? `Hiding ${expiredCount} expired certification${expiredCount !== 1 ? 's' : ''}` : 'Show only active certifications'}
          />
          {stateOptions.length > 1 && (
            <select
              value={selectedState}
              onChange={e => setSelectedState(e.target.value)}
              className="ml-auto text-sm border border-gray-300 rounded-md px-3 py-1.5 text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="">All Locations</option>
              {stateOptions.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
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