import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useAuth } from './AuthContext';

// Types
export interface Vault {
  id: string;
  localCurrency: string;
  originalLocalAmount: number;
  usdcAmount: number;
  startDate: string;
  endDate: string;
  status: string;
  mockYieldEarned: number;
  isWithdrawable: boolean;
  mockCurrentWithdrawalValueLocal: number | null;
}

interface VaultContextType {
  vaults: Vault[];
  isLoading: boolean;
  error: string | null;
  createVault: (localCurrency: string, localAmount: number, lockDurationDays: number) => Promise<Vault | null>;
  fetchVaults: () => Promise<void>;
  getVaultStatus: (vaultId: string) => Promise<Vault | null>;
  withdrawVault: (vaultId: string) => Promise<{ success: boolean; message: string; withdrawnAmount?: number }>;
}

// Create context
const VaultContext = createContext<VaultContextType | undefined>(undefined);

// Provider component
export const VaultProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [vaults, setVaults] = useState<Vault[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { token, isAuthenticated } = useAuth();

  // Mock API URL - would be replaced with real API in production
  const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

  // Fetch all vaults for the current user
  const fetchVaults = async (): Promise<void> => {
    if (!isAuthenticated || !token) {
      setError('Authentication required');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/vault/list`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch vaults: ${response.status}`);
      }

      const data = await response.json();
      
      // Transform API response to match our frontend model
      const transformedVaults: Vault[] = data.map((vault: any) => ({
        id: vault.id,
        localCurrency: vault.local_currency,
        originalLocalAmount: vault.original_local_amount,
        usdcAmount: vault.usdc_amount,
        startDate: vault.start_date,
        endDate: vault.end_date,
        status: vault.status,
        mockYieldEarned: vault.mock_yield_earned,
        isWithdrawable: vault.is_withdrawable,
        mockCurrentWithdrawalValueLocal: vault.mock_current_withdrawal_value_local,
      }));

      setVaults(transformedVaults);
    } catch (err) {
      console.error('Error fetching vaults:', err);
      setError('Failed to load vaults. Please try again later.');
      
      // For development/demo: Create mock data if API fails
      if (import.meta.env.DEV) {
        const mockVaults: Vault[] = [
          {
            id: '1',
            localCurrency: 'NGN',
            originalLocalAmount: 50000,
            usdcAmount: 33.33,
            startDate: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(),
            endDate: new Date(Date.now() + 15 * 24 * 60 * 60 * 1000).toISOString(),
            status: 'LOCKED',
            mockYieldEarned: 0.25,
            isWithdrawable: false,
            mockCurrentWithdrawalValueLocal: null,
          },
          {
            id: '2',
            localCurrency: 'NGN',
            originalLocalAmount: 100000,
            usdcAmount: 66.67,
            startDate: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000).toISOString(),
            endDate: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
            status: 'UNLOCKED',
            mockYieldEarned: 1.25,
            isWithdrawable: true,
            mockCurrentWithdrawalValueLocal: 105000,
          },
        ];
        setVaults(mockVaults);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Get status of a specific vault
  const getVaultStatus = async (vaultId: string): Promise<Vault | null> => {
    if (!isAuthenticated || !token) {
      setError('Authentication required');
      return null;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/vault/${vaultId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch vault status: ${response.status}`);
      }

      const data = await response.json();
      
      // Transform API response to match our frontend model
      const vault: Vault = {
        id: data.id,
        localCurrency: data.local_currency,
        originalLocalAmount: data.original_local_amount,
        usdcAmount: data.usdc_amount,
        startDate: data.start_date,
        endDate: data.end_date,
        status: data.status,
        mockYieldEarned: data.mock_yield_earned,
        isWithdrawable: data.is_withdrawable,
        mockCurrentWithdrawalValueLocal: data.mock_current_withdrawal_value_local,
      };

      return vault;
    } catch (err) {
      console.error('Error fetching vault status:', err);
      setError('Failed to load vault status. Please try again later.');
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  // Create a new vault
  const createVault = async (
    localCurrency: string,
    localAmount: number,
    lockDurationDays: number
  ): Promise<Vault | null> => {
    if (!isAuthenticated || !token) {
      setError('Authentication required');
      return null;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/vault/create`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          local_currency: localCurrency,
          local_amount: localAmount,
          lock_duration_days: lockDurationDays,
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to create vault: ${response.status}`);
      }

      const data = await response.json();
      
      // Transform API response to match our frontend model
      const newVault: Vault = {
        id: data.id,
        localCurrency: data.local_currency,
        originalLocalAmount: data.original_local_amount,
        usdcAmount: data.usdc_amount,
        startDate: data.start_date,
        endDate: data.end_date,
        status: data.status,
        mockYieldEarned: data.mock_yield_earned,
        isWithdrawable: data.is_withdrawable,
        mockCurrentWithdrawalValueLocal: data.mock_current_withdrawal_value_local,
      };

      // Update local state
      setVaults(prevVaults => [...prevVaults, newVault]);
      
      return newVault;
    } catch (err) {
      console.error('Error creating vault:', err);
      setError('Failed to create vault. Please try again later.');
      
      // For development/demo: Create mock data if API fails
      if (import.meta.env.DEV) {
        const mockVault: Vault = {
          id: Math.random().toString(36).substring(2, 9),
          localCurrency: localCurrency,
          originalLocalAmount: localAmount,
          usdcAmount: localCurrency === 'NGN' ? localAmount / 1500 : localAmount / 130,
          startDate: new Date().toISOString(),
          endDate: new Date(Date.now() + lockDurationDays * 24 * 60 * 60 * 1000).toISOString(),
          status: 'LOCKED',
          mockYieldEarned: 0,
          isWithdrawable: false,
          mockCurrentWithdrawalValueLocal: null,
        };
        
        setVaults(prevVaults => [...prevVaults, mockVault]);
        return mockVault;
      }
      
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  // Withdraw from a vault
  const withdrawVault = async (vaultId: string): Promise<{ success: boolean; message: string; withdrawnAmount?: number }> => {
    if (!isAuthenticated || !token) {
      setError('Authentication required');
      return { success: false, message: 'Authentication required' };
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/vault/withdraw`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          vault_id: vaultId,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Failed to withdraw: ${response.status}`);
      }

      const data = await response.json();
      
      // Update local state
      setVaults(prevVaults => 
        prevVaults.map(vault => 
          vault.id === vaultId 
            ? { ...vault, status: 'WITHDRAWN', isWithdrawable: false } 
            : vault
        )
      );
      
      return { 
        success: true, 
        message: data.message || 'Withdrawal successful',
        withdrawnAmount: data.mock_final_local_amount
      };
    } catch (err: any) {
      console.error('Error withdrawing from vault:', err);
      setError(err.message || 'Failed to withdraw. Please try again later.');
      
      // For development/demo: Mock successful withdrawal if API fails
      if (import.meta.env.DEV) {
        const vaultToWithdraw = vaults.find(v => v.id === vaultId);
        
        if (vaultToWithdraw && vaultToWithdraw.isWithdrawable) {
          setVaults(prevVaults => 
            prevVaults.map(vault => 
              vault.id === vaultId 
                ? { ...vault, status: 'WITHDRAWN', isWithdrawable: false } 
                : vault
            )
          );
          
          return { 
            success: true, 
            message: 'Withdrawal successful (mock)',
            withdrawnAmount: vaultToWithdraw.mockCurrentWithdrawalValueLocal || vaultToWithdraw.originalLocalAmount
          };
        }
        
        return { 
          success: false, 
          message: vaultToWithdraw?.isWithdrawable === false 
            ? 'This vault is not yet available for withdrawal' 
            : 'Vault not found'
        };
      }
      
      return { success: false, message: err.message || 'Failed to withdraw' };
    } finally {
      setIsLoading(false);
    }
  };

  // Load vaults when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      fetchVaults();
    }
  }, [isAuthenticated]);

  const value = {
    vaults,
    isLoading,
    error,
    createVault,
    fetchVaults,
    getVaultStatus,
    withdrawVault,
  };

  return <VaultContext.Provider value={value}>{children}</VaultContext.Provider>;
};

// Custom hook to use the vault context
export const useVault = (): VaultContextType => {
  const context = useContext(VaultContext);
  if (context === undefined) {
    throw new Error('useVault must be used within a VaultProvider');
  }
  return context;
};
