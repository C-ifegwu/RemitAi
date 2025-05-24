import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRightIcon } from '@heroicons/react/24/outline';

interface ActionButtonProps {
  icon: React.ReactNode;
  label: string;
  onClick: () => void;
  color?: 'primary' | 'secondary' | 'neutral';
}

const ActionButton: React.FC<ActionButtonProps> = ({ 
  icon, 
  label, 
  onClick,
  color = 'primary'
}) => {
  const colorClasses = {
    primary: 'bg-primary-500 text-neutral-900',
    secondary: 'bg-secondary-500 text-white',
    neutral: 'bg-white text-neutral-800 border border-neutral-200'
  };

  return (
    <motion.button
      className={`flex items-center justify-between w-full p-4 rounded-2xl shadow-sm ${colorClasses[color]}`}
      onClick={onClick}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-center">
        <div className="mr-3">
          {icon}
        </div>
        <span className="font-medium">{label}</span>
      </div>
      <ArrowRightIcon className="h-5 w-5" />
    </motion.button>
  );
};

export default ActionButton;
