interface ClearButtonProps {
    onClick: () => void;
    className?: string;
    size?: 'sm' | 'md' | 'lg';
  }
  
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };
  
  export const ClearButton = ({ onClick, className = '', size = 'md' }: ClearButtonProps) => {
    return (
      <button
        type="button"
        onClick={onClick}
        className={`text-gray-400 hover:text-gray-600 focus:outline-none focus:text-gray-600 ${className}`}
        aria-label="Clear"
      >
        <svg
          className={sizeClasses[size]}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    );
  };