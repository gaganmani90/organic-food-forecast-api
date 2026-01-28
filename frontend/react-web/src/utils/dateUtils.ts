export const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

export const calculateDaysBetween = (date1: Date, date2: Date): number => {
  return Math.ceil((date2.getTime() - date1.getTime()) / (1000 * 60 * 60 * 24));
};

export const calculateDaysUntilExpiry = (validTo: string): number => {
  const expiryDate = new Date(validTo);
  const now = new Date();
  return calculateDaysBetween(now, expiryDate);
};

export const calculateDaysSinceStart = (validFrom: string): number => {
  const startDate = new Date(validFrom);
  const now = new Date();
  return calculateDaysBetween(startDate, now);
};
