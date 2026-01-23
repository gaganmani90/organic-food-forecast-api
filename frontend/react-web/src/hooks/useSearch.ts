import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { Store } from '../types/store';

interface UseSearchResult {
  stores: Store[];
  isLoading: boolean;
  error: Error | null;
}

export const useSearch = (query: string): UseSearchResult => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['search', query],
    queryFn: () => api.search(query),
    enabled: query.trim() !== '',
  });

  return {
    stores: data?.results || [],
    isLoading,
    error: error as Error | null,
  };
};
