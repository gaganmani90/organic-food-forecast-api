import axios, { AxiosInstance } from 'axios';
import { SearchResponse } from '../types/store';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface LastRefreshResponse {
  last_refresh: string | null;
  last_refresh_formatted: string | null;
  error?: string;
}

export const api = {
  search: async (query: string, page: number = 1, pageSize: number = 20): Promise<SearchResponse> => {
    const response = await apiClient.get<SearchResponse>('/api/search', {
      params: { query, page, page_size: pageSize },
    });
    return response.data;
  },
  getLastRefresh: async (): Promise<LastRefreshResponse> => {
    const response = await apiClient.get<LastRefreshResponse>('/api/last-refresh');
    return response.data;
  },
};
