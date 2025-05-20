import React from 'react';
import { motion } from 'framer-motion';

interface TransactionItemProps {
  type: 'sent' | 'received';
  amount: string;
  currency: string;
  recipient: string;
  date: string;
  status?: 'completed' | 'pending' | 'failed';
  icon?: React.ReactNode;
}

const TransactionItem: React.FC<TransactionItemProps> = ({
  type,
  amount,
  currency,
  recipient,
  date,
  status = 'completed',
  icon
}) => {
  const getStatusBadge = () => {
    switch (status) {
      case 'completed':
        return <span className="badge badge-success">Completed</span>;
      case 'pending':
        return <span className="badge badge-pending">Pending</span>;
      case 'failed':
        return <span className="badge bg-red-100 text-red-800">Failed</span>;
      default:
        return null;
    }
  };

  return (
    <motion.div 
      className="flex items-center p-4 border-b border-neutral-200 last:border-b-0"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="w-10 h-10 rounded-full bg-neutral-100 flex items-center justify-center mr-4">
        {icon || (
          type === 'sent' ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-neutral-600" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-neutral-600" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          )
        )}
      </div>
      
      <div className="flex-1">
        <div className="flex justify-between items-start">
          <div>
            <p className="font-medium">{type === 'sent' ? `To ${recipient}` : `From ${recipient}`}</p>
            <p className="text-sm text-neutral-500">{date}</p>
          </div>
          <div className="text-right">
            <p className={`font-semibold ${type === 'sent' ? 'text-neutral-800' : 'text-secondary-600'}`}>
              {type === 'sent' ? '-' : '+'}{amount} {currency}
            </p>
            <div className="mt-1">
              {getStatusBadge()}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default TransactionItem;
