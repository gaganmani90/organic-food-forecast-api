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
  location?: {
    lat: number;
    lon: number;
  };
}

export interface SearchResponse {
  results: Store[];
  error?: string;
}
