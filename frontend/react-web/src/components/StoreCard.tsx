import { Store } from '../types/store';
import { StatusBadge } from './StatusBadge';
import { ProductList } from './ProductList';
import { getCertificationStatus } from '../utils/certificationUtils';
import { formatDate } from '../utils/dateUtils';
import { parseProducts } from '../utils/productUtils';

interface StoreCardProps {
  store: Store;
}

export const StoreCard = ({ store }: StoreCardProps) => {
  const productList = parseProducts(store.products);
  const status = getCertificationStatus(store.valid_to);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-semibold text-gray-900">
          {store.store_name}
        </h3>
        <StatusBadge status={status} />
      </div>

      <div className="space-y-2 text-sm text-gray-600">
        <p>
          <span className="font-medium">📍 Address:</span> {store.address}
        </p>
        <p>
          <span className="font-medium">🌍 State:</span> {store.state}
        </p>
        <p>
          <span className="font-medium">📧 Email:</span>{' '}
          <a
            href={`mailto:${store.email}`}
            className="text-blue-600 hover:underline"
          >
            {store.email}
          </a>
        </p>
        <p>
          <span className="font-medium">🏷️ Certification ID:</span>{' '}
          {store.certification_id}
        </p>
        <p>
          <span className="font-medium">✅ Certified By:</span>{' '}
          {store.certification_body}
        </p>
        <p>
          <span className="font-medium">📅 Valid From:</span> {formatDate(store.valid_from)}
        </p>
        <p>
          <span className="font-medium">📅 Valid To:</span> {formatDate(store.valid_to)}
        </p>
      </div>

      <ProductList products={productList} />
    </div>
  );
};
