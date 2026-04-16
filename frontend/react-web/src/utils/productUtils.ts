export const parseProducts = (productsString: string | null | undefined): string[] => {
  if (!productsString) return [];
  return productsString
    .split(',')
    .map((p) => p.trim())
    .filter((p) => p);
};
