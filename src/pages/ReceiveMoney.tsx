import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { QrCodeIcon, ShareIcon } from '@heroicons/react/24/outline';
import { useWallet } from '../contexts/WalletContext';

interface ReceiveMoneyProps {}

const ReceiveMoney: React.FC<ReceiveMoneyProps> = () => {
  const { balance, currency } = useWallet();
  const [amount, setAmount] = useState('');
  const [selectedCurrency, setSelectedCurrency] = useState('USD');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSharing, setIsSharing] = useState(false);
  const [qrGenerated, setQrGenerated] = useState(false);
  
  // Mock QR code data - in a real app, this would be generated from backend
  const [qrCodeUrl, setQrCodeUrl] = useState('https://via.placeholder.com/300x300?text=RemitAI+QR+Code');
  
  const handleGenerateQR = async () => {
    setIsGenerating(true);
    try {
      // Simulate API call to generate QR code
      await new Promise(resolve => setTimeout(resolve, 1200));
      
      // Update QR code with amount if specified
      if (amount) {
        setQrCodeUrl(`https://via.placeholder.com/300x300?text=RemitAI+${amount}+${selectedCurrency}`);
      }
      
      setQrGenerated(true);
    } catch (error) {
      console.error('Error generating QR code:', error);
    } finally {
      setIsGenerating(false);
    }
  };
  
  const handleShare = async () => {
    setIsSharing(true);
    try {
      // Simulate sharing functionality
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // In a real app, this would use the Web Share API or a custom sharing solution
      alert('Payment link copied to clipboard!');
    } catch (error) {
      console.error('Error sharing payment link:', error);
    } finally {
      setIsSharing(false);
    }
  };

  // Generate QR code on initial load
  useEffect(() => {
    handleGenerateQR();
  }, []);

  return (
    <div className="space-y-6">
      <motion.div 
        className="card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <h2 className="text-xl font-semibold mb-4">Receive Money</h2>
        
        {/* QR Code Display */}
        <div className="flex flex-col items-center mb-6">
          <div className="bg-white p-4 rounded-xl border border-neutral-200 mb-4">
            {isGenerating ? (
              <div className="w-64 h-64 flex items-center justify-center">
                <svg className="animate-spin h-10 w-10 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
            ) : (
              <img 
                src={qrCodeUrl} 
                alt="Payment QR Code" 
                className="w-64 h-64 mx-auto"
              />
            )}
          </div>
          <p className="text-sm text-neutral-600 text-center">
            This QR code can be scanned by anyone using RemitAI to send you money instantly
          </p>
        </div>
        
        {/* Optional Amount Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Request Amount (Optional)
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
        </div>
        
        {/* Action Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            className="btn btn-primary flex items-center justify-center"
            onClick={handleGenerateQR}
            disabled={isGenerating}
          >
            {isGenerating ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-neutral-900" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating...
              </>
            ) : (
              <>
                <QrCodeIcon className="mr-2 h-5 w-5" />
                <span>Generate QR Code</span>
              </>
            )}
          </button>
          
          <button
            className="btn btn-outline flex items-center justify-center"
            onClick={handleShare}
            disabled={isSharing || !qrGenerated}
          >
            {isSharing ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-neutral-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Sharing...
              </>
            ) : (
              <>
                <ShareIcon className="mr-2 h-5 w-5" />
                <span>Share Payment Link</span>
              </>
            )}
          </button>
        </div>
      </motion.div>
      
      {/* Payment Instructions */}
      <motion.div 
        className="card bg-neutral-50"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.2 }}
      >
        <h3 className="font-semibold mb-3">How to receive money</h3>
        <ol className="list-decimal pl-5 space-y-2 text-sm text-neutral-700">
          <li>Share your QR code or payment link with the sender</li>
          <li>They can scan the QR code using their RemitAI app</li>
          <li>Once they confirm the payment, you'll receive a notification</li>
          <li>Funds will be instantly available in your RemitAI wallet</li>
        </ol>
      </motion.div>
    </div>
  );
};

export default ReceiveMoney;
