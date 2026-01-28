interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info';
  className?: string;
  icon?: string;
}

const variantStyles = {
  default: 'bg-gray-100 text-gray-800 border-gray-200',
  primary: 'bg-blue-100 text-blue-800 border-blue-200',
  success: 'bg-green-100 text-green-800 border-green-200',
  warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  danger: 'bg-red-100 text-red-800 border-red-200',
  info: 'bg-indigo-100 text-indigo-800 border-indigo-200',
};

export const Badge = ({ children, variant = 'default', className = '', icon }: BadgeProps) => {
  return (
    <span
      className={`px-2.5 py-1 rounded-md text-xs font-medium border ${variantStyles[variant]} ${className}`}
    >
      {icon && <span className="mr-1">{icon}</span>}
      {children}
    </span>
  );
};
