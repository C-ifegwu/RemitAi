import React from 'react';
import { motion } from 'framer-motion';
import { CurrencyDollarIcon, ArrowPathIcon } from '@heroicons/react/24/outline';

interface BalanceCardProps {
  balance: string;
  currency: string;
  lastUpdated?: string;
}

const BalanceCard: React.FC<BalanceCardProps> = ({ 
  balance, 
  currency,
  lastUpdated 
}) => {
  return (
    <motion.div 
      className="card bg-gradient-to-br from-primary-500 to-primary-400 text-neutral-900 overflow-hidden relative"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="absolute top-0 right-0 w-32 h-32 bg-primary-300 rounded-full opacity-20 -mr-10 -mt-10" />
      <div className="absolute bottom-0 left-0 w-24 h-24 bg-primary-300 rounded-full opacity-20 -ml-10 -mb-10" />
      
      <div className="flex justify-between items-start mb-2">
        <span className="text-sm font-medium opacity-80">Available Balance</span>
        <button 
          className="p-1 rounded-full hover:bg-primary-400 transition-colors"
          aria-label="Refresh balance"
        >
          <ArrowPathIcon className="h-4 w-4" />
        </button>
      </div>
      
      <div className="flex items-center mb-4">
        <CurrencyDollarIcon className="h-8 w-8 mr-2" />
        <span className="text-3xl font-bold">{balance}</span>
        <span className="ml-2 text-lg font-medium">{currency}</span>
      </div>
      
      {lastUpdated && (
        <div className="text-xs opacity-70">
          Last updated: {lastUpdated}
        </div>
      )}
    </motion.div>
  );
};

export default BalanceCard;
