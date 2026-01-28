interface ToggleProps {
    checked: boolean;
    onChange: (checked: boolean) => void;
    label: string;
    description?: string;
  }
  
  export const Toggle = ({ checked, onChange, label, description }: ToggleProps) => {
    return (
      <div className="flex items-center gap-3">
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={checked}
            onChange={(e) => onChange(e.target.checked)}
            className="sr-only peer"
          />
          <div className="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
        </label>
        <div className="flex flex-col">
          <span className="text-sm font-semibold text-gray-700">{label}</span>
          {description && (
            <span className="text-xs text-gray-500">{description}</span>
          )}
        </div>
      </div>
    );
  };