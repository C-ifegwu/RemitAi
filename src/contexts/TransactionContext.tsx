import React, { createContext, useContext, useState, ReactNode } from 'react';
import { transactionsAPI } from '../services/api';

interface TransactionContextType {
  transactions: any[];
  loading: boolean;
  error: string | null;
  fetchTransactions: () => Promise<void>;
  initiateOnRamp: (userId: string, fiatAmount: number, fiatCurrency: string, provider: string) => Promise<any>;
  initiateOffRamp: (userId: string, usdcAmount: number, targetCurrency: string, recipientDetails: any, provider: string) => Promise<any>;
  checkTransactionStatus: (transactionId: string, type: 'onramp' | 'offramp') => Promise<any>;
  assessTransactionRisk: (userId: string, commandText: string, amount: number, recipientId: string) => Promise<any>;
}

const TransactionContext = createContext<TransactionContextType | undefined>(undefined);

export const useTransactions = () => {
  const context = useContext(TransactionContext);
  if (context === undefined) {
    throw new Error('useTransactions must be used within a TransactionProvider');
  }
  return context;
};

interface TransactionProviderProps {
  children: ReactNode;
}

export const TransactionProvider: React.FC<TransactionProviderProps> = ({ children }) => {
  const [transactions, setTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Mock transaction data for development
  const mockTransactions = [
    {
      id: '1',
      type: 'sent',
      amount: '250.00',
      currency: 'USD',
      recipient: 'John Doe',
      date: 'Today, 2:30 PM',
      status: 'completed'
    },
    {
      id: '2',
      type: 'received',
      amount: '1,000.00',
      currency: 'NGN',
      recipient: 'Sarah Smith',
      date: 'Yesterday, 10:15 AM',
      status: 'completed'
    },
    {
      id: '3',
      type: 'sent',
      amount: '75.50',
      currency: 'USD',
      recipient: 'Mike Johnson',
      date: 'May 18, 2025',
      status: 'pending'
    }
  ];

  const fetchTransactions = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // In a real app, this would be an API call to fetch transactions
      // For now, we'll use mock data
      await new Promise(resolve => setTimeout(resolve, 1000));
      setTransactions(mockTransactions);
    } catch (err) {
      console.error('Error fetching transactions:', err);
      setError('Failed to fetch transactions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const initiateOnRamp = async (userId: string, fiatAmount: number, fiatCurrency: string, provider: string) => {
    setLoading(true);
    setError(null);
    
    try {
      // In development, we can use the actual API call but handle the response differently
      // const response = await transactionsAPI.initiateOnRamp(userId, fiatAmount, fiatCurrency, provider);
      
      // For now, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 1500));
      const mockResponse = {
        success: true,
        transaction_id: `tx_${Date.now()}`,
        status: 'pending',
        details: {
          transaction_id: `tx_${Date.now()}`,
          status: 'pending',
          provider: 'RemitAI Mock Provider',
          amount: fiatAmount,
          currency: fiatCurrency,
          fees: fiatAmount * 0.005,
          exchange_rate: fiatCurrency === 'USD' ? 1 : 0.0077,
          usdc_amount: fiatCurrency === 'USD' ? fiatAmount : fiatAmount * 0.0077,
          recipient_address: `USER_SMART_WALLET_ADDRESS_FOR_${userId}`,
          payment_method: 'Bank Transfer',
          payment_instructions: {
            account_name: 'RemitAI Payment Processor',
            account_number: '1234567890',
            bank_name: 'Mock Bank',
            reference: `tx_${Date.now()}`
          },
          estimated_completion_time: '1-5 minutes',
          created_at: new Date().toISOString(),
          expires_at: new Date(Date.now() + 3600000).toISOString()
        }
      };
      
      return mockResponse;
    } catch (err) {
      console.error('Error initiating on-ramp:', err);
      setError('Failed to initiate transaction. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const initiateOffRamp = async (userId: string, usdcAmount: number, targetCurrency: string, recipientDetails: any, provider: string) => {
    setLoading(true);
    setError(null);
    
    try {
      // In development, we can use the actual API call but handle the response differently
      // const response = await transactionsAPI.initiateOffRamp(userId, usdcAmount, targetCurrency, recipientDetails, provider);
      
      // For now, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Mock exchange rates
      const exchangeRates: Record<string, number> = {
        'USD': 1,
        'NGN': 1510.25,
        'KES': 129.85,
        'GHS': 15.42,
        'ZAR': 18.65
      };
      
      const rate = exchangeRates[targetCurrency] || 1;
      const estimatedFiatPayout = usdcAmount * rate;
      
      const mockResponse = {
        success: true,
        transaction_id: `offtx_${Date.now()}`,
        status: 'pending_usdc_transfer',
        details: {
          transaction_id: `offtx_${Date.now()}`,
          status: 'pending_usdc_transfer',
          provider: `${provider} (Mock)`,
          usdc_amount_due: usdcAmount,
          target_currency: targetCurrency,
          estimated_fiat_payout: estimatedFiatPayout,
          fees_in_usdc: usdcAmount * 0.018,
          payout_method: 'Bank Transfer',
          payout_details_provided: recipientDetails,
          deposit_address_for_usdc: 'STELLAR_ADDRESS_FOR_MOCK_DEPOSITS',
          memo_required: `REMITAI_offtx_${Date.now()}`,
          estimated_completion_time: '15-60 minutes',
          created_at: new Date().toISOString(),
          expires_at: new Date(Date.now() + 3600000).toISOString()
        }
      };
      
      return mockResponse;
    } catch (err) {
      console.error('Error initiating off-ramp:', err);
      setError('Failed to initiate withdrawal. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const checkTransactionStatus = async (transactionId: string, type: 'onramp' | 'offramp') => {
    setLoading(true);
    setError(null);
    
    try {
      // In development, we can use the actual API call but handle the response differently
      // const response = type === 'onramp' 
      //   ? await transactionsAPI.checkOnRampStatus(transactionId)
      //   : await transactionsAPI.checkOffRampStatus(transactionId);
      
      // For now, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Randomly select a status for demonstration
      const statuses = type === 'onramp' 
        ? ['pending', 'processing', 'completed', 'failed']
        : ['pending_usdc_transfer', 'usdc_received_processing_fiat', 'completed', 'failed'];
        
      const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
      
      const mockResponse = {
        transaction_id: transactionId,
        status: randomStatus,
        details: {
          transaction_id: transactionId,
          status: randomStatus,
          message: `Transaction ${randomStatus === 'completed' ? 'completed successfully' : 'is being processed'}`,
          last_updated: new Date().toISOString()
        }
      };
      
      return mockResponse;
    } catch (err) {
      console.error('Error checking transaction status:', err);
      setError('Failed to check transaction status. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const assessTransactionRisk = async (userId: string, commandText: string, amount: number, recipientId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      // In development, we can use the actual API call but handle the response differently
      // const response = await transactionsAPI.assessTransactionRisk(userId, commandText, amount, recipientId);
      
      // For now, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Simulate risk assessment based on amount
      const isSuspicious = amount > 5000;
      const riskScore = isSuspicious ? 75 : 0;
      const reasons = isSuspicious ? ['Unusually large transaction amount'] : [];
      
      const mockResponse = {
        user_id: userId,
        is_suspicious: isSuspicious,
        risk_score: riskScore,
        reasons: reasons,
        timestamp: Date.now() / 1000
      };
      
      return mockResponse;
    } catch (err) {
      console.error('Error assessing transaction risk:', err);
      setError('Failed to assess transaction risk. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    transactions,
    loading,
    error,
    fetchTransactions,
    initiateOnRamp,
    initiateOffRamp,
    checkTransactionStatus,
    assessTransactionRisk
  };

  return <TransactionContext.Provider value={value}>{children}</TransactionContext.Provider>;
};
