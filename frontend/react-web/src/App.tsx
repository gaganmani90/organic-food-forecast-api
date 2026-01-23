import { useState } from 'react';
import { Header } from './components/Layout/Header';
import { Footer } from './components/Layout/Footer';
import { SearchBar } from './components/SearchBar';
import { StoreList } from './components/StoreList';
import { useSearch } from './hooks/useSearch';

function App() {
  const [searchQuery, setSearchQuery] = useState<string>('');

  const { stores, isLoading, error } = useSearch(searchQuery);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />
      <main className="container mx-auto px-4 py-8 flex-1">
        <SearchBar onSearch={handleSearch} loading={isLoading} />
        <StoreList stores={stores} loading={isLoading} error={error} />
      </main>
      <Footer />
    </div>
  );
}

export default App;
