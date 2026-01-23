import { Store, PaginationInfo } from '../types/store';
import { StoreCard } from './StoreCard';
import { Pagination } from './Pagination';

interface StoreListProps {
  stores: Store[];
  pagination: PaginationInfo | null;
  loading: boolean;
  error: Error | null;
  onPageChange: (page: number) => void;
}

export const StoreList = ({ stores, pagination, loading, error, onPageChange }: StoreListProps) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded">
        <p className="font-medium">Error:</p>
        <p>{error.message}</p>
      </div>
    );
  }

  if (stores.length === 0) {
    return (
      <div className="bg-blue-50 border border-blue-200 text-blue-800 px-4 py-3 rounded">
        No results found.
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">
        {pagination ? `Found ${pagination.total} result(s)` : `Found ${stores.length} result(s)`}
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {stores.map((store, index) => (
          <StoreCard key={store.certification_id || index} store={store} />
        ))}
      </div>
      {pagination && (
        <Pagination pagination={pagination} onPageChange={onPageChange} />
      )}
    </div>
  );
};
