interface ProductListProps {
  products: string[];
}

export const ProductList = ({ products }: ProductListProps) => {
  if (products.length === 0) {
    return null;
  }

  return (
    <details className="mt-4">
      <summary className="cursor-pointer font-medium text-gray-700 hover:text-gray-900">
        📦 View Products ({products.length})
      </summary>
      <ul className="mt-2 space-y-1 pl-4">
        {products.map((product, index) => (
          <li key={index} className="text-sm text-gray-600">
            • {product}
          </li>
        ))}
      </ul>
    </details>
  );
};
