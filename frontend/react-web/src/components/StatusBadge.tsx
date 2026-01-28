import { CertificationStatus } from '../utils/certificationUtils';
import { Badge } from './Badge';

interface StatusBadgeProps {
  status: CertificationStatus;
}

export const StatusBadge = ({ status }: StatusBadgeProps) => {
  const { isExpired, isExpiringSoon, daysUntilExpiry } = status;

  if (isExpired) {
    return (
      <Badge variant="danger">
        Expired
      </Badge>
    );
  }

  if (isExpiringSoon) {
    return (
      <Badge variant="warning" icon="⏰">
        Expires in {daysUntilExpiry} days
      </Badge>
    );
  }

  return (
    <Badge variant="success">
      Active
    </Badge>
  );
};