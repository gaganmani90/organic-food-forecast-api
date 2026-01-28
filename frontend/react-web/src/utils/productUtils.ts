export const parseProducts = (productsString: string): string[] => {
  return productsString
    .split(',')
    .map((p) => p.trim())
    .filter((p) => p);
};
