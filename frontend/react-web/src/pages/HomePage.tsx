import { SearchBar } from '../components/SearchBar';
import { useNavigate } from 'react-router-dom';

export const HomePage = () => {
  const navigate = useNavigate();

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