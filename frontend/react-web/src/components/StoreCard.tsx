import { useState } from 'react';
import { Store } from '../types/store';
import { StatusBadge } from './StatusBadge';
import { ProductList } from './ProductList';
import { getCertificationStatus } from '../utils/certificationUtils';
import { formatDate } from '../utils/dateUtils';
import { parseProducts } from '../utils/productUtils';

const toTitleCase = (str: string): string => {
  if (!str) return str;
  const letters = (str.match(/[a-zA-Z]/g) || []).length;
  const uppers = (str.match(/[A-Z]/g) || []).length;
  if (letters === 0 || uppers / letters < 0.7) return str;
  return str.toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
};

/**
 * Returns the bare domain (e.g. "sowfresh.in") only when the email is a
 * single, well-formed address.  Returns null for anything ambiguous so we
 * never construct a broken URL.
 *
 * Rejects: multiple '@', slashes, commas, spaces, and any domain that
 * doesn't look like  something.tld.
 */
const extractDomain = (email: string | undefined): string | null => {
  if (!email) return null;
  const trimmed = email.trim();
  // Reject illegal characters that indicate concatenated / malformed emails
  if (/[/,; \t]/.test(trimmed)) return null;
  const parts = trimmed.split('@');
  if (parts.length !== 2) return null;
  const [local, domain] = parts;
  if (!local || !domain) return null;
  // Domain must have at least one dot with non-empty labels on each side
  const domainParts = domain.split('.');
  if (domainParts.length < 2 || domainParts.some(p => p === '')) return null;
  return domain.toLowerCase();
};

interface StoreCardProps {
  store: Store;
}

export const StoreCard = ({ store }: StoreCardProps) => {
  const [showDetails, setShowDetails] = useState(false);
  const productList = parseProducts(store.products);
  const status = getCertificationStatus(store.valid_to);
  const websiteDomain = store.has_website ? extractDomain(store.email) : null;

  return (
    <div className="bg-white rounded-lg shadow-md p-5 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-base font-semibold text-gray-900 mr-2 leading-snug">
          {toTitleCase(store.store_name)}
        </h3>
        <div className="shrink-0">
          <StatusBadge status={status} />
        </div>
      </div>

      <div className="space-y-1 text-sm text-gray-600">
        <p><span className="font-medium">📍</span> {store.state}</p>
        <p>
          <span className="font-medium">📅 Valid:</span>{' '}
          {formatDate(store.valid_from)} → {formatDate(store.valid_to)}
        </p>
        {websiteDomain && (
          <p>
            <a
              href={`https://${websiteDomain}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-xs font-medium text-blue-600 hover:text-blue-800"
            >
              🌐 Visit Website
            </a>
          </p>
        )}
      </div>

      {showDetails && (
        <div className="space-y-1.5 text-sm text-gray-600 mt-3 pt-3 border-t border-gray-100">
          {store.address && (
            <p><span className="font-medium">🏠 Address:</span> {store.address}</p>
          )}
          {store.email && (
            <p>
              <span className="font-medium">📧 Email:</span>{' '}
              <a href={`mailto:${store.email}`} className="text-blue-600 hover:underline">
                {store.email}
              </a>
            </p>
          )}
          <p><span className="font-medium">🏷️ Cert ID:</span> {store.certification_id}</p>
          <p><span className="font-medium">✅ Certified By:</span> {store.certification_body}</p>
        </div>
      )}

      <div className="mt-3 flex items-center gap-4">
        <button
          onClick={() => setShowDetails(v => !v)}
          className="text-xs text-green-600 hover:text-green-800 font-medium"
        >
          {showDetails ? '▲ Less' : '▼ Details'}
        </button>
      </div>

      <ProductList products={productList} />
    </div>
  );
};
