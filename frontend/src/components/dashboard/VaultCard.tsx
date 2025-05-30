import React from 'react';
import { motion } from 'framer-motion';
import { LockClosedIcon, LockOpenIcon, ArrowPathIcon } from '@heroicons/react/24/outline';
import { formatCurrency, formatDate } from '../../utils/formatters';

interface VaultCardProps {
  localCurrency: string;
  originalAmount: number;
  usdcAmount: number;
  currentValue: number | null;
  yieldEarned: number;
  startDate: string;
  endDate: string;
  status: string;
  isWithdrawable: boolean;
  onClick?: () => void;
}

const VaultCard: React.FC<VaultCardProps> = ({
  localCurrency,
  originalAmount,
  usdcAmount,
  currentValue,
  yieldEarned,
  startDate,
  endDate,
  status,
  isWithdrawable,
  onClick
}) => {
  const getStatusColor = () => {
    switch (status) {
      case 'LOCKED':
        return 'bg-amber-100 text-amber-800';
      case 'UNLOCKED':
        return 'bg-green-100 text-green-800';
      case 'WITHDRAWN':
        return 'bg-neutral-100 text-neutral-800';
      default:
        return 'bg-neutral-100 text-neutral-800';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'LOCKED':
        return <LockClosedIcon className="h-4 w-4 mr-1" />;
      case 'UNLOCKED':
        return <LockOpenIcon className="h-4 w-4 mr-1" />;
      case 'WITHDRAWN':
        return <ArrowPathIcon className="h-4 w-4 mr-1" />;
      default:
        return null;
    }
  };

  const calculateGrowth = () => {
    if (!currentValue || status === 'WITHDRAWN') return null;
    const growth = ((currentValue - originalAmount) / originalAmount) * 100;
    return growth.toFixed(2);
  };

  const growth = calculateGrowth();

  return (
    <motion.div
      className="card bg-white shadow-md hover:shadow-lg transition-shadow cursor-pointer"
      whileHover={{ y: -5 }}
      onClick={onClick}
    >
      <div className="p-5">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-lg font-semibold text-neutral-900">Vault Savings</h3>
            <p className="text-sm text-neutral-500">
              {formatDate(new Date(startDate))} - {formatDate(new Date(endDate))}
            </p>
          </div>
          <span className={`px-2 py-1 rounded-full text-xs font-medium flex items-center ${getStatusColor()}`}>
            {getStatusIcon()}
            {status}
          </span>
        </div>

        <div className="mb-4">
          <p className="text-sm text-neutral-600 mb-1">Original Deposit</p>
          <p className="text-xl font-bold text-neutral-900">
            {formatCurrency(originalAmount, localCurrency)}
          </p>
          <p className="text-xs text-neutral-500">
            ≈ {formatCurrency(usdcAmount, 'USDC')}
          </p>
        </div>

        {(status === 'UNLOCKED' || status === 'WITHDRAWN') && (
          <div className="mb-4">
            <p className="text-sm text-neutral-600 mb-1">
              {status === 'WITHDRAWN' ? 'Withdrawn Value' : 'Current Value'}
            </p>
            <p className="text-xl font-bold text-neutral-900">
              {formatCurrency(currentValue || originalAmount, localCurrency)}
            </p>
            {growth && (
              <p className={`text-xs ${parseFloat(growth) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {parseFloat(growth) >= 0 ? '+' : ''}{growth}% from original
              </p>
            )}
          </div>
        )}

        <div className="mb-4">
          <p className="text-sm text-neutral-600 mb-1">Yield Earned</p>
          <p className="text-lg font-semibold text-green-600">
            +{formatCurrency(yieldEarned, 'USDC')}
          </p>
        </div>

        {isWithdrawable && (
          <div className="mt-4 pt-4 border-t border-neutral-200">
            <p className="text-sm text-green-600 font-medium flex items-center">
              <LockOpenIcon className="h-4 w-4 mr-1" />
              Available for withdrawal
            </p>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default VaultCard;
