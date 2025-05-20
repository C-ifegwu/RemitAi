import React, { createContext, useContext, useState, ReactNode } from 'react';
import { walletAPI } from '../services/api';

interface WalletContextType {
  balance: string;
  currency: string;
  loading: boolean;
  error: string | null;
  fetchBalance: () => Promise<void>;
  generateRecoveryPhrase: () => Promise<any>;
  confirmRecoveryPhraseSaved: (userId: string) => Promise<any>;
  linkBiometric: (userId: string, voicePrintId: string) => Promise<any>;
  recoverWithPassphrase: (userId: string, passphraseWords: string[]) => Promise<any>;
  recoverWithBiometric: (userId: string, voiceVerificationToken: string) => Promise<any>;
}

const WalletContext = createContext<WalletContextType | undefined>(undefined);

export const useWallet = () => {
  const context = useContext(WalletContext);
  if (context === undefined) {
    throw new Error('useWallet must be used within a WalletProvider');
  }
  return context;
};

interface WalletProviderProps {
  children: ReactNode;
}

export const WalletProvider: React.FC<WalletProviderProps> = ({ children }) => {
  const [balance, setBalance] = useState<string>('1,350.00');
  const [currency, setCurrency] = useState<string>('USD');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchBalance = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // In a real app, this would be an API call to fetch wallet balance
      // For now, we'll use mock data
      await new Promise(resolve => setTimeout(resolve, 800));
      setBalance('1,350.00');
      setCurrency('USD');
    } catch (err) {
      console.error('Error fetching wallet balance:', err);
      setError('Failed to fetch wallet balance. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const generateRecoveryPhrase = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // In development, we can use the actual API call but handle the response differently
      // const response = await walletAPI.generateRecoveryPhrase();
      
      // For now, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 1000));
      const mockResponse = {
        success: true,
        mnemonic_words: [
          'apple', 'banana', 'cherry', 'date', 'elderberry', 
          'fig', 'grape', 'honeydew', 'kiwi', 'lemon', 
          'mango', 'nectarine'
        ],
        message: 'Recovery phrase generated successfully. Store it securely!'
      };
      
      return mockResponse;
    } catch (err) {
      console.error('Error generating recovery phrase:', err);
      setError('Failed to generate recovery phrase. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const confirmRecoveryPhraseSaved = async (userId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      // In development, we can use the actual API call but handle the response differently
      // const response = await walletAPI.confirmRecoveryPhraseSaved(userId);
      
      // For now, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 800));
      const mockResponse = {
        success: true,
        message: 'Passphrase backup process acknowledged. Store your passphrase securely!'
      };
      
      return mockResponse;
    } catch (err) {
      console.error('Error confirming recovery phrase saved:', err);
      setError('Failed to confirm recovery phrase saved. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const linkBiometric = async (userId: string, voicePrintId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      // In development, we can use the actual API call but handle the response differently
      // const response = await walletAPI.linkBiometric(userId, voicePrintId);
      
      // For now, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 1200));
      const mockResponse = {
        success: true,
        message: 'Biometric assisted recovery setup successful (mock).'
      };
      
      return mockResponse;
    } catch (err) {
      console.error('Error linking biometric:', err);
      setError('Failed to link biometric. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const recoverWithPassphrase = async (userId: string, passphraseWords: string[]) => {
    setLoading(true);
    setError(null);
    
    try {
      // In development, we can use the actual API call but handle the response differently
      // const response = await walletAPI.recoverWithPassphrase(userId, passphraseWords);
      
      // For now, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 1500));
      const mockResponse = {
        success: true,
        message: 'Wallet recovery with passphrase successful (mock).'
      };
      
      return mockResponse;
    } catch (err) {
      console.error('Error recovering with passphrase:', err);
      setError('Failed to recover wallet with passphrase. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const recoverWithBiometric = async (userId: string, voiceVerificationToken: string) => {
    setLoading(true);
    setError(null);
    
    try {
      // In development, we can use the actual API call but handle the response differently
      // const response = await walletAPI.recoverWithBiometric(userId, voiceVerificationToken);
      
      // For now, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 1500));
      const mockResponse = {
        success: true,
        message: 'Wallet recovery with biometric assistance successful (mock).'
      };
      
      return mockResponse;
    } catch (err) {
      console.error('Error recovering with biometric:', err);
      setError('Failed to recover wallet with biometric. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    balance,
    currency,
    loading,
    error,
    fetchBalance,
    generateRecoveryPhrase,
    confirmRecoveryPhraseSaved,
    linkBiometric,
    recoverWithPassphrase,
    recoverWithBiometric
  };

  return <WalletContext.Provider value={value}>{children}</WalletContext.Provider>;
};
