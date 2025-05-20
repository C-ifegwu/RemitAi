import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import BalanceCard from '../components/dashboard/BalanceCard';
import ActionButton from '../components/common/ActionButton';
import TransactionItem from '../components/transactions/TransactionItem';
import { ArrowUpRightIcon, QrCodeIcon, BanknotesIcon, CreditCardIcon } from '@heroicons/react/24/outline';
import { Link } from 'react-router-dom';
import { useWallet } from '../contexts/WalletContext';
import { useTransactions } from '../contexts/TransactionContext';

const Dashboard: React.FC = () => {
  const { balance, currency, loading: walletLoading, fetchBalance } = useWallet();
  const { transactions, loading: transactionsLoading, fetchTransactions } = useTransactions();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      setIsLoading(true);
      try {
        await Promise.all([
          fetchBalance(),
          fetchTransactions()
        ]);
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, [fetchBalance, fetchTransactions]);

  return (
    <div className="space-y-6">
      {/* Balance Card */}
      {isLoading ? (
        <div className="card bg-gradient-to-br from-primary-500 to-primary-400 text-neutral-900 h-32 animate-pulse"></div>
      ) : (
        <BalanceCard 
          balance={balance} 
          currency={currency} 
          lastUpdated="Today, 7:30 AM"
        />
      )}
      
      {/* Quick Actions */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 gap-4">
          <Link to="/send">
            <ActionButton 
              icon={<ArrowUpRightIcon className="h-6 w-6" />}
              label="Send Money"
              onClick={() => {}}
              color="primary"
            />
          </Link>
          <Link to="/receive">
            <ActionButton 
              icon={<QrCodeIcon className="h-6 w-6" />}
              label="Receive Money"
              onClick={() => {}}
              color="secondary"
            />
          </Link>
          <ActionButton 
            icon={<BanknotesIcon className="h-6 w-6" />}
            label="Add Money"
            onClick={() => {}}
            color="neutral"
          />
          <ActionButton 
            icon={<CreditCardIcon className="h-6 w-6" />}
            label="Virtual Card"
            onClick={() => {}}
            color="neutral"
          />
        </div>
      </section>
      
      {/* Recent Transactions */}
      <section>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Recent Transactions</h2>
          <Link to="/history" className="text-primary-500 text-sm font-medium">
            View All
          </Link>
        </div>
        
        <motion.div 
          className="card divide-y divide-neutral-200"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          {isLoading ? (
            <div className="py-4 space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center p-4">
                  <div className="w-10 h-10 rounded-full bg-neutral-200 animate-pulse mr-4"></div>
                  <div className="flex-1">
                    <div className="h-4 bg-neutral-200 rounded animate-pulse mb-2 w-3/4"></div>
                    <div className="h-3 bg-neutral-200 rounded animate-pulse w-1/2"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : transactions.length > 0 ? (
            transactions.map((transaction: any) => (
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
              <p>No recent transactions</p>
            </div>
          )}
        </motion.div>
      </section>
      
      {/* Financial Insights */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Financial Insights</h2>
        <motion.div 
          className="card bg-white p-5"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <div className="text-center py-4">
            <p className="text-neutral-600 mb-2">You've saved approximately</p>
            <p className="text-2xl font-bold text-secondary-500">$45.30</p>
            <p className="text-neutral-500 text-sm mt-1">in transfer fees this month</p>
          </div>
        </motion.div>
      </section>
    </div>
  );
};

export default Dashboard;
