import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { PlusIcon, ArrowPathIcon } from '@heroicons/react/24/outline';
import { useVault } from '../contexts/VaultContext';
import VaultCard from '../components/dashboard/VaultCard';
import VaultDepositForm from '../components/dashboard/VaultDepositForm';
import { Button } from '../components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Skeleton } from '../components/ui/skeleton';
import { useToast } from '../components/ui/use-toast';

const Vault: React.FC = () => {
  const { vaults, isLoading, error, fetchVaults, withdrawVault } = useVault();
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [selectedVaultId, setSelectedVaultId] = useState<string | null>(null);
  const [isWithdrawing, setIsWithdrawing] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    fetchVaults();
  }, [fetchVaults]);

  const handleRefresh = () => {
    fetchVaults();
  };

  const handleCreateVault = () => {
    setIsCreateDialogOpen(true);
  };

  const handleVaultCreated = () => {
    setIsCreateDialogOpen(false);
    fetchVaults();
  };

  const handleVaultClick = (vaultId: string) => {
    setSelectedVaultId(vaultId);
  };

  const handleCloseVaultDetail = () => {
    setSelectedVaultId(null);
  };

  const handleWithdraw = async () => {
    if (!selectedVaultId) return;
    
    setIsWithdrawing(true);
    try {
      const result = await withdrawVault(selectedVaultId);
      if (result.success) {
        toast({
          title: "Withdrawal Successful",
          description: `${result.message}. You've received ${result.withdrawnAmount} in your wallet.`,
          variant: "default",
        });
        setSelectedVaultId(null);
        fetchVaults();
      } else {
        toast({
          title: "Withdrawal Failed",
          description: result.message,
          variant: "destructive",
        });
      }
    } catch (error) {
      console.error('Error withdrawing from vault:', error);
      toast({
        title: "Withdrawal Failed",
        description: "There was an error processing your withdrawal. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsWithdrawing(false);
    }
  };

  const selectedVault = selectedVaultId ? vaults.find(v => v.id === selectedVaultId) : null;

  const activeVaults = vaults.filter(v => v.status !== 'WITHDRAWN');
  const completedVaults = vaults.filter(v => v.status === 'WITHDRAWN');

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Savings Vault</h1>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm" onClick={handleRefresh}>
            <ArrowPathIcon className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button size="sm" onClick={handleCreateVault}>
            <PlusIcon className="h-4 w-4 mr-2" />
            New Vault
          </Button>
        </div>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <div className="bg-white rounded-lg p-6 shadow-sm">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-8">
            <h2 className="text-xl font-semibold mb-2">Protect Your Money from Inflation</h2>
            <p className="text-neutral-600">
              Save your local currency in USDC to protect against depreciation and inflation.
              Earn interest while your money is locked and withdraw at the current exchange rate.
            </p>
          </div>

          <Tabs defaultValue="active" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="active">Active Vaults</TabsTrigger>
              <TabsTrigger value="completed">Completed</TabsTrigger>
            </TabsList>
            
            <TabsContent value="active" className="mt-6">
              {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {[1, 2].map((i) => (
                    <div key={i} className="rounded-lg overflow-hidden">
                      <Skeleton className="h-48 w-full" />
                    </div>
                  ))}
                </div>
              ) : activeVaults.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {activeVaults.map((vault) => (
                    <VaultCard
                      key={vault.id}
                      localCurrency={vault.localCurrency}
                      originalAmount={vault.originalLocalAmount}
                      usdcAmount={vault.usdcAmount}
                      currentValue={vault.mockCurrentWithdrawalValueLocal}
                      yieldEarned={vault.mockYieldEarned}
                      startDate={vault.startDate}
                      endDate={vault.endDate}
                      status={vault.status}
                      isWithdrawable={vault.isWithdrawable}
                      onClick={() => handleVaultClick(vault.id)}
                    />
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <p className="text-neutral-500 mb-4">You don't have any active vaults</p>
                  <Button onClick={handleCreateVault}>Create Your First Vault</Button>
                </div>
              )}
            </TabsContent>
            
            <TabsContent value="completed" className="mt-6">
              {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <Skeleton className="h-48 w-full" />
                </div>
              ) : completedVaults.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {completedVaults.map((vault) => (
                    <VaultCard
                      key={vault.id}
                      localCurrency={vault.localCurrency}
                      originalAmount={vault.originalLocalAmount}
                      usdcAmount={vault.usdcAmount}
                      currentValue={vault.mockCurrentWithdrawalValueLocal}
                      yieldEarned={vault.mockYieldEarned}
                      startDate={vault.startDate}
                      endDate={vault.endDate}
                      status={vault.status}
                      isWithdrawable={vault.isWithdrawable}
                      onClick={() => handleVaultClick(vault.id)}
                    />
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <p className="text-neutral-500">No completed vaults yet</p>
                </div>
              )}
            </TabsContent>
          </Tabs>
        </div>
      </div>

      {/* Create Vault Dialog */}
      <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Create New Vault</DialogTitle>
          </DialogHeader>
          <VaultDepositForm onSuccess={handleVaultCreated} />
        </DialogContent>
      </Dialog>

      {/* Vault Detail Dialog */}
      <Dialog open={!!selectedVaultId} onOpenChange={(open) => !open && handleCloseVaultDetail()}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Vault Details</DialogTitle>
          </DialogHeader>
          
          {selectedVault && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-neutral-500">Original Amount</p>
                  <p className="text-lg font-semibold">{selectedVault.originalLocalAmount} {selectedVault.localCurrency}</p>
                </div>
                <div>
                  <p className="text-sm text-neutral-500">USDC Value</p>
                  <p className="text-lg font-semibold">{selectedVault.usdcAmount.toFixed(2)} USDC</p>
                </div>
                <div>
                  <p className="text-sm text-neutral-500">Start Date</p>
                  <p className="text-base">{new Date(selectedVault.startDate).toLocaleDateString()}</p>
                </div>
                <div>
                  <p className="text-sm text-neutral-500">End Date</p>
                  <p className="text-base">{new Date(selectedVault.endDate).toLocaleDateString()}</p>
                </div>
                <div>
                  <p className="text-sm text-neutral-500">Status</p>
                  <p className="text-base capitalize">{selectedVault.status.toLowerCase()}</p>
                </div>
                <div>
                  <p className="text-sm text-neutral-500">Yield Earned</p>
                  <p className="text-base text-green-600">+{selectedVault.mockYieldEarned.toFixed(2)} USDC</p>
                </div>
              </div>

              {selectedVault.isWithdrawable && (
                <div className="pt-4 border-t">
                  <div className="mb-4">
                    <p className="text-sm text-neutral-500">Current Value (if withdrawn now)</p>
                    <p className="text-xl font-bold">
                      {selectedVault.mockCurrentWithdrawalValueLocal} {selectedVault.localCurrency}
                    </p>
                    <p className="text-xs text-green-600">
                      Protected from currency depreciation
                    </p>
                  </div>
                  <Button 
                    className="w-full" 
                    onClick={handleWithdraw}
                    disabled={isWithdrawing}
                  >
                    {isWithdrawing ? 'Processing...' : 'Withdraw Funds'}
                  </Button>
                </div>
              )}

              {selectedVault.status === 'LOCKED' && !selectedVault.isWithdrawable && (
                <div className="pt-4 border-t">
                  <Alert>
                    <AlertDescription>
                      This vault is locked until {new Date(selectedVault.endDate).toLocaleDateString()}. 
                      You cannot withdraw funds before this date.
                    </AlertDescription>
                  </Alert>
                </div>
              )}

              {selectedVault.status === 'WITHDRAWN' && (
                <div className="pt-4 border-t">
                  <Alert>
                    <AlertDescription>
                      This vault has been withdrawn. The funds have been returned to your wallet.
                    </AlertDescription>
                  </Alert>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Vault;
