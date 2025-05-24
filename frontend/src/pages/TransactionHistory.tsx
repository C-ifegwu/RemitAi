import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import TransactionItem from '../components/transactions/TransactionItem';
import { FunnelIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useTransactions } from '../contexts/TransactionContext';

interface TransactionHistoryProps {}

const TransactionHistory: React.FC<TransactionHistoryProps> = () => {
  const { transactions, fetchTransactions } = useTransactions();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterOpen, setFilterOpen] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    const loadTransactions = async () => {
      setIsLoading(true);
      try {
        await fetchTransactions();
      } catch (error) {
        console.error('Error loading transactions:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadTransactions();
  }, [fetchTransactions]);
  
  // Filter transactions based on search query and selected filter
  const filteredTransactions = transactions.filter((transaction: any) => {
    const matchesSearch = 
      transaction.recipient.toLowerCase().includes(searchQuery.toLowerCase()) ||
      transaction.amount.includes(searchQuery) ||
      transaction.currency.toLowerCase().includes(searchQuery.toLowerCase());
      
    const matchesFilter = 
      selectedFilter === 'all' ||
      (selectedFilter === 'sent' && transaction.type === 'sent') ||
      (selectedFilter === 'received' && transaction.type === 'received') ||
      (selectedFilter === 'pending' && transaction.status === 'pending') ||
      (selectedFilter === 'completed' && transaction.status === 'completed') ||
      (selectedFilter === 'failed' && transaction.status === 'failed');
      
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="space-y-6">
      <motion.div 
        className="card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Transaction History</h2>
          <button 
            className="p-2 rounded-full hover:bg-neutral-100"
            onClick={() => setFilterOpen(!filterOpen)}
            aria-label="Filter transactions"
          >
            <FunnelIcon className="h-5 w-5 text-neutral-700" />
          </button>
        </div>
        
        {/* Search Bar */}
        <div className="relative mb-4">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <MagnifyingGlassIcon className="h-5 w-5 text-neutral-400" />
          </div>
          <input
            type="text"
            className="input pl-10"
            placeholder="Search transactions..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        
        {/* Filters */}
        {filterOpen && (
          <motion.div 
            className="mb-4 p-4 bg-neutral-50 rounded-xl"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <p className="text-sm font-medium mb-2">Filter by:</p>
            <div className="flex flex-wrap gap-2">
              <button 
                className={`px-3 py-1 rounded-full text-sm ${selectedFilter === 'all' ? 'bg-primary-500 text-neutral-900' : 'bg-white border border-neutral-300'}`}
                onClick={() => setSelectedFilter('all')}
              >
                All
              </button>
              <button 
                className={`px-3 py-1 rounded-full text-sm ${selectedFilter === 'sent' ? 'bg-primary-500 text-neutral-900' : 'bg-white border border-neutral-300'}`}
                onClick={() => setSelectedFilter('sent')}
              >
                Sent
              </button>
              <button 
                className={`px-3 py-1 rounded-full text-sm ${selectedFilter === 'received' ? 'bg-primary-500 text-neutral-900' : 'bg-white border border-neutral-300'}`}
                onClick={() => setSelectedFilter('received')}
              >
                Received
              </button>
              <button 
                className={`px-3 py-1 rounded-full text-sm ${selectedFilter === 'pending' ? 'bg-primary-500 text-neutral-900' : 'bg-white border border-neutral-300'}`}
                onClick={() => setSelectedFilter('pending')}
              >
                Pending
              </button>
              <button 
                className={`px-3 py-1 rounded-full text-sm ${selectedFilter === 'completed' ? 'bg-primary-500 text-neutral-900' : 'bg-white border border-neutral-300'}`}
                onClick={() => setSelectedFilter('completed')}
              >
                Completed
              </button>
              <button 
                className={`px-3 py-1 rounded-full text-sm ${selectedFilter === 'failed' ? 'bg-primary-500 text-neutral-900' : 'bg-white border border-neutral-300'}`}
                onClick={() => setSelectedFilter('failed')}
              >
                Failed
              </button>
            </div>
          </motion.div>
        )}
        
        {/* Transactions List */}
        <div className="divide-y divide-neutral-200">
          {isLoading ? (
            <div className="py-4 space-y-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="flex items-center p-4">
                  <div className="w-10 h-10 rounded-full bg-neutral-200 animate-pulse mr-4"></div>
                  <div className="flex-1">
                    <div className="h-4 bg-neutral-200 rounded animate-pulse mb-2 w-3/4"></div>
                    <div className="h-3 bg-neutral-200 rounded animate-pulse w-1/2"></div>
                  </div>
                  <div className="text-right">
                    <div className="h-4 bg-neutral-200 rounded animate-pulse mb-2 w-20 ml-auto"></div>
                    <div className="h-3 bg-neutral-200 rounded animate-pulse w-16 ml-auto"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : filteredTransactions.length > 0 ? (
            filteredTransactions.map((transaction: any) => (
              <TransactionItem 
                key={transaction.id}
                type={transaction.type}
                amount={transaction.amount}
                currency={transaction.currency}
                recipient={transaction.recipient}
                date={transaction.date}
                status={transaction.status}
              />
            ))
          ) : (
            <div className="py-8 text-center text-neutral-500">
              <p>No transactions found</p>
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
};

export default TransactionHistory;
