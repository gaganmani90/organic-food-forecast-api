export interface CertificationStatus {
  isExpired: boolean;
  isExpiringSoon: boolean;
  daysUntilExpiry: number;
}

const EXPIRING_SOON_THRESHOLD_DAYS = 90;

export const getCertificationStatus = (validTo: string): CertificationStatus => {
  const expiryDate = new Date(validTo);
  const now = new Date();
  const daysUntilExpiry = Math.ceil((expiryDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
  
  return {
    isExpired: expiryDate < now,
    isExpiringSoon: expiryDate < new Date(now.getTime() + EXPIRING_SOON_THRESHOLD_DAYS * 24 * 60 * 60 * 1000),
    daysUntilExpiry
  };
};
