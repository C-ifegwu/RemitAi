import React from 'react';
import { motion } from 'framer-motion';
import { LockClosedIcon, BanknotesIcon, ArrowTrendingUpIcon } from '@heroicons/react/24/outline';
import { useVault } from '../../contexts/VaultContext';
import { formatCurrency } from '../../utils/formatters';

interface VaultSummaryCardProps {
  onClick?: () => void;
}

const VaultSummaryCard: React.FC<VaultSummaryCardProps> = ({ onClick }) => {
  const { vaults, isLoading } = useVault();
  
  // Calculate total values
  const calculateTotals = () => {
    if (!vaults.length) return { totalLocked: 0, totalYield: 0, activeVaults: 0 };
    
    const activeVaults = vaults.filter(v => v.status !== 'WITHDRAWN');
    const totalLocked = activeVaults.reduce((sum, vault) => sum + vault.usdcAmount, 0);
    const totalYield = activeVaults.reduce((sum, vault) => sum + vault.mockYieldEarned, 0);
    
    return {
      totalLocked,
      totalYield,
      activeVaults: activeVaults.length
    };
  };
  
  const { totalLocked, totalYield, activeVaults } = calculateTotals();
  
  if (isLoading) {
    return (
      <div className="card bg-white p-5 animate-pulse">
        <div className="h-6 bg-neutral-200 rounded w-1/3 mb-4"></div>
        <div className="h-8 bg-neutral-200 rounded w-1/2 mb-2"></div>
        <div className="h-4 bg-neutral-200 rounded w-1/4 mb-4"></div>
        <div className="h-4 bg-neutral-200 rounded w-3/4"></div>
      </div>
    );
  }
  
  return (
    <motion.div
      className="card bg-gradient-to-br from-blue-50 to-indigo-50 hover:shadow-md transition-shadow cursor-pointer"
      whileHover={{ y: -5 }}
      onClick={onClick}
    >
      <div className="p-5">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-lg font-semibold text-neutral-900">Savings Vault</h3>
          <div className="p-2 rounded-full bg-blue-100">
            <LockClosedIcon className="h-5 w-5 text-blue-600" />
          </div>
        </div>
        
        {activeVaults > 0 ? (
          <>
            <div className="mb-4">
              <p className="text-sm text-neutral-600 mb-1">Total Locked Value</p>
              <p className="text-xl font-bold text-neutral-900">
                {formatCurrency(totalLocked, 'USDC')}
              </p>
              <p className="text-xs text-neutral-500">
                Across {activeVaults} active vault{activeVaults !== 1 ? 's' : ''}
              </p>
            </div>
            
            <div className="flex items-center space-x-1 text-green-600 text-sm">
              <ArrowTrendingUpIcon className="h-4 w-4" />
              <span>+{formatCurrency(totalYield, 'USDC')} yield earned</span>
            </div>
          </>
        ) : (
          <div className="py-2">
            <p className="text-neutral-600 mb-2">Protect your money from inflation</p>
            <p className="text-sm text-neutral-500">
              Create a vault to convert local currency to USDC and earn yield while it's locked
            </p>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default VaultSummaryCard;
