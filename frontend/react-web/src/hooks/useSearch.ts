import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { Store, PaginationInfo } from '../types/store';

interface UseSearchResult {
  stores: Store[];
  pagination: PaginationInfo | null;
  isLoading: boolean;
  error: Error | null;
}

export const useSearch = (query: string, page: number = 1, pageSize: number = 20): UseSearchResult => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['search', query, page, pageSize],
    queryFn: () => api.search(query, page, pageSize),
    enabled: query.trim() !== '',
  });

  return {
    stores: data?.results || [],
    pagination: data?.pagination || null,
    isLoading,
    error: error as Error | null,
  };
};
