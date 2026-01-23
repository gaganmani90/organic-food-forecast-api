import { useState } from 'react';
import { Header } from './components/Layout/Header';
import { Footer } from './components/Layout/Footer';
import { SearchBar } from './components/SearchBar';
import { StoreList } from './components/StoreList';
import { useSearch } from './hooks/useSearch';

function App() {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [currentPage, setCurrentPage] = useState<number>(1);
  const pageSize = 20;

  const { stores, pagination, isLoading, error } = useSearch(searchQuery, currentPage, pageSize);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setCurrentPage(1); // Reset to page 1 on new search
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    // Scroll to top when page changes
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />
      <main className="container mx-auto px-4 py-8 flex-1">
        <SearchBar onSearch={handleSearch} loading={isLoading} />
        <StoreList 
          stores={stores} 
          pagination={pagination}
          loading={isLoading} 
          error={error}
          onPageChange={handlePageChange}
        />
      </main>
      <Footer />
    </div>
  );
}

export default App;
