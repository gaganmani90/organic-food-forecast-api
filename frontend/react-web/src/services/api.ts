import axios, { AxiosInstance } from 'axios';
import { SearchResponse } from '../types/store';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  search: async (query: string): Promise<SearchResponse> => {
    const response = await apiClient.get<SearchResponse>('/api/search', {
      params: { query },
    });
    return response.data;
  },
};
