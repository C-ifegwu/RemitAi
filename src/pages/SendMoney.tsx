import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowUpRightIcon, UserCircleIcon } from '@heroicons/react/24/outline';
import { useTransactions } from '../contexts/TransactionContext';
import { useNLP } from '../contexts/NLPContext';

interface SendMoneyProps {}

const SendMoney: React.FC<SendMoneyProps> = () => {
  const { initiateOffRamp, assessTransactionRisk, loading } = useTransactions();
  const { parseIntent } = useNLP();
  
  const [amount, setAmount] = useState('');
  const [selectedCurrency, setSelectedCurrency] = useState('USD');
  const [recipient, setRecipient] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Mock exchange rates
  const exchangeRates = {
    USD: 1,
    NGN: 1510.25,
    KES: 129.85,
    GHS: 15.42,
    ZAR: 18.65
  };
  
  // Calculate converted amount
  const calculateConvertedAmount = () => {
    const numAmount = parseFloat(amount.replace(/,/g, '')) || 0;
    return (numAmount * exchangeRates[selectedCurrency as keyof typeof exchangeRates]).toLocaleString();
  };
  
  const handleContinue = async () => {
    setIsProcessing(true);
    setError(null);
    
    try {
      // 1. Parse the intent to validate the transaction
      const parsedIntent = await parseIntent('mock-user-id', `Send ${amount} ${selectedCurrency} to ${recipient}`, 'en');
      
      // 2. Assess transaction risk
      const numAmount = parseFloat(amount.replace(/,/g, '')) || 0;
      const riskAssessment = await assessTransactionRisk('mock-user-id', `Send ${amount} ${selectedCurrency} to ${recipient}`, numAmount, 'recipient-id');
      
      // 3. If suspicious, show warning or block
      if (riskAssessment.is_suspicious) {
        setError(`This transaction appears suspicious (Risk score: ${riskAssessment.risk_score}). Please verify the details and try again.`);
        setIsProcessing(false);
        return;
      }
      
      // 4. Initiate the transaction
      const result = await initiateOffRamp(
        'mock-user-id',
        numAmount,
        selectedCurrency,
        { name: recipient, account_type: 'mobile_money' },
        'RemitAI Default Provider'
      );
      
      // 5. Handle success - in a real app, would redirect to confirmation page
      console.log('Transaction initiated:', result);
      alert(`Transaction initiated successfully! ID: ${result.transaction_id}`);
      
      // Reset form
      setAmount('');
      setRecipient('');
      
    } catch (err: any) {
      console.error('Error processing transaction:', err);
      setError(err.message || 'Failed to process transaction. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };
  
  const recentRecipients = [
    { id: '1', name: 'John Doe', avatar: null },
    { id: '2', name: 'Sarah Smith', avatar: null },
    { id: '3', name: 'Mike Johnson', avatar: null },
    { id: '4', name: 'Emma Wilson', avatar: null },
    { id: '5', name: 'David Brown', avatar: null },
  ];

  return (
    <div className="space-y-6">
      <motion.div 
        className="card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <h2 className="text-xl font-semibold mb-4">Send Money</h2>
        
        {/* Error message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}
        
        {/* Recipient Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Recipient
          </label>
          <div className="flex items-center border border-neutral-300 rounded-xl p-3 mb-4">
            <UserCircleIcon className="h-6 w-6 text-neutral-400 mr-3" />
            <input
              type="text"
              placeholder="Enter name or phone number"
              className="flex-1 outline-none bg-transparent"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
            />
          </div>
          
          <div className="mb-2">
            <p className="text-sm text-neutral-600 mb-3">Recent Recipients</p>
            <div className="flex space-x-4 overflow-x-auto pb-2">
              {recentRecipients.map((person) => (
                <button
                  key={person.id}
                  className="flex flex-col items-center min-w-[60px]"
                  onClick={() => setRecipient(person.name)}
                >
                  <div className="w-12 h-12 rounded-full bg-neutral-200 flex items-center justify-center mb-1">
                    {person.avatar ? (
                      <img src={person.avatar} alt={person.name} className="w-full h-full rounded-full" />
                    ) : (
                      <span className="text-neutral-600 font-medium">
                        {person.name.split(' ').map(n => n[0]).join('')}
                      </span>
                    )}
                  </div>
                  <span className="text-xs text-center truncate w-full">{person.name}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
        
        {/* Amount Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Amount
          </label>
          <div className="flex items-center">
            <div className="relative flex-1">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span className="text-neutral-500 sm:text-sm">$</span>
              </div>
              <input
                type="text"
                className="input pl-8"
                placeholder="0.00"
                value={amount}
                onChange={(e) => {
                  // Allow only numbers and commas
                  const value = e.target.value.replace(/[^0-9.,]/g, '');
                  setAmount(value);
                }}
              />
            </div>
            <div className="ml-3">
              <select
                className="input py-3 px-4"
                value={selectedCurrency}
                onChange={(e) => setSelectedCurrency(e.target.value)}
              >
                <option value="USD">USD</option>
                <option value="NGN">NGN</option>
                <option value="KES">KES</option>
                <option value="GHS">GHS</option>
                <option value="ZAR">ZAR</option>
              </select>
            </div>
          </div>
          
          {/* Converted amount display */}
          {amount && (
            <div className="mt-2 text-sm text-neutral-600">
              Recipient gets approximately: {calculateConvertedAmount()} {selectedCurrency}
            </div>
          )}
        </div>
        
        {/* Fee information */}
        <div className="bg-neutral-50 rounded-xl p-4 mb-6">
          <div className="flex justify-between mb-2">
            <span className="text-sm text-neutral-600">Transfer Fee</span>
            <span className="text-sm font-medium">$0.00</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-neutral-600">Exchange Rate</span>
            <span className="text-sm font-medium">
              1 USD = {exchangeRates[selectedCurrency as keyof typeof exchangeRates]} {selectedCurrency}
            </span>
          </div>
        </div>
        
        {/* Continue Button */}
        <button
          className="btn btn-primary w-full flex items-center justify-center"
          onClick={handleContinue}
          disabled={!amount || !recipient || isProcessing}
        >
          {isProcessing ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-neutral-900" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing...
            </>
          ) : (
            <>
              <span>Continue</span>
              <ArrowUpRightIcon className="ml-2 h-5 w-5" />
            </>
          )}
        </button>
      </motion.div>
    </div>
  );
};

export default SendMoney;
