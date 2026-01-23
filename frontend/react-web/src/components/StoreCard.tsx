import { Store } from '../types/store';

interface StoreCardProps {
  store: Store;
}

export const StoreCard = ({ store }: StoreCardProps) => {
  const productList = store.products
    .split(',')
    .map((p) => p.trim())
    .filter((p) => p);

  const validTo = new Date(store.valid_to);
  const isExpired = validTo < new Date();
  const isExpiringSoon = validTo < new Date(Date.now() + 90 * 24 * 60 * 60 * 1000);

  const getStatusColor = () => {
    if (isExpired) return 'bg-red-100 text-red-800';
    if (isExpiringSoon) return 'bg-yellow-100 text-yellow-800';
    return 'bg-green-100 text-green-800';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-semibold text-gray-900">
          {store.store_name}
        </h3>
        <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor()}`}>
          {isExpired ? 'Expired' : isExpiringSoon ? 'Expiring Soon' : 'Active'}
        </span>
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
          <span className="font-medium">📅 Valid From:</span> {store.valid_from}
        </p>
        <p>
          <span className="font-medium">📅 Valid To:</span> {store.valid_to}
        </p>
      </div>

      <details className="mt-4">
        <summary className="cursor-pointer font-medium text-gray-700 hover:text-gray-900">
          📦 View Products ({productList.length})
        </summary>
        <ul className="mt-2 space-y-1 pl-4">
          {productList.map((product, index) => (
            <li key={index} className="text-sm text-gray-600">
              • {product}
            </li>
          ))}
        </ul>
      </details>
    </div>
  );
};
