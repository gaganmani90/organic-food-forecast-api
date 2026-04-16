export interface Store {
  store_name: string;
  certification_id: string;
  state: string;
  address: string;
  email: string;
  certification_body: string;
  valid_from: string;
  valid_to: string;
  products: string;
  scraped_at: string;
  score?: number;
  has_website?: boolean;
  location?: {
    lat: number;
    lon: number;
  };
}

export interface PaginationInfo {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface SearchResponse {
  results: Store[];
  pagination?: PaginationInfo;
  error?: string;
}
