import React, { createContext, useContext, useState, ReactNode } from 'react';
import { nlpAPI } from '../services/api';

interface NLPContextType {
  loading: boolean;
  error: string | null;
  parseIntent: (userId: string, text: string, language: string) => Promise<any>;
}

const NLPContext = createContext<NLPContextType | undefined>(undefined);

export const useNLP = () => {
  const context = useContext(NLPContext);
  if (context === undefined) {
    throw new Error('useNLP must be used within an NLPProvider');
  }
  return context;
};

interface NLPProviderProps {
  children: ReactNode;
}

export const NLPProvider: React.FC<NLPProviderProps> = ({ children }) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const parseIntent = async (userId: string, text: string, language: string) => {
    setLoading(true);
    setError(null);
    
    try {
      // In development, we can use the actual API call but handle the response differently
      // const response = await nlpAPI.parseIntent(userId, text, language);
      
      // For now, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock intent parsing based on text content
      let intent = 'unknown';
      let parsedData: any = {
        original_text: text,
        detected_language: language,
        parsed_text_language: 'en'
      };
      
      // Simple intent detection based on keywords
      if (text.toLowerCase().includes('send') || text.toLowerCase().includes('transfer')) {
        intent = 'payment';
        
        // Extract amount if present (simple regex for numbers)
        const amountMatch = text.match(/\d+(\.\d+)?/);
        const amount = amountMatch ? parseFloat(amountMatch[0]) : null;
        
        // Extract currency if present
        const currencies = ['USD', 'NGN', 'KES', 'GHS', 'ZAR'];
        let currency = null;
        for (const curr of currencies) {
          if (text.toUpperCase().includes(curr)) {
            currency = curr;
            break;
          }
        }
        
        // Extract recipient name (simple heuristic - words after "to")
        let recipientName = null;
        const toIndex = text.toLowerCase().indexOf(' to ');
        if (toIndex !== -1) {
          recipientName = text.substring(toIndex + 4).trim();
          // Remove any trailing punctuation
          recipientName = recipientName.replace(/[.,;!?]$/, '');
        }
        
        parsedData = {
          ...parsedData,
          amount,
          currency: currency || 'USD',
          recipient_name: recipientName
        };
      } else if (text.toLowerCase().includes('receive') || text.toLowerCase().includes('request')) {
        intent = 'request';
        
        // Extract amount if present (simple regex for numbers)
        const amountMatch = text.match(/\d+(\.\d+)?/);
        const amount = amountMatch ? parseFloat(amountMatch[0]) : null;
        
        // Extract currency if present
        const currencies = ['USD', 'NGN', 'KES', 'GHS', 'ZAR'];
        let currency = null;
        for (const curr of currencies) {
          if (text.toUpperCase().includes(curr)) {
            currency = curr;
            break;
          }
        }
        
        // Extract sender name (simple heuristic - words after "from")
        let senderName = null;
        const fromIndex = text.toLowerCase().indexOf(' from ');
        if (fromIndex !== -1) {
          senderName = text.substring(fromIndex + 6).trim();
          // Remove any trailing punctuation
          senderName = senderName.replace(/[.,;!?]$/, '');
        }
        
        parsedData = {
          ...parsedData,
          amount,
          currency: currency || 'USD',
          sender_name: senderName
        };
      } else if (text.toLowerCase().includes('balance') || text.toLowerCase().includes('wallet')) {
        intent = 'balance';
      } else if (text.toLowerCase().includes('history') || text.toLowerCase().includes('transactions')) {
        intent = 'history';
      }
      
      const mockResponse = {
        user_id: userId,
        original_text: text,
        language_detected: language,
        translated_text: language === 'en' ? null : 'Translated text would appear here',
        intent,
        parsed_data: parsedData
      };
      
      return mockResponse;
    } catch (err) {
      console.error('Error parsing intent:', err);
      setError('Failed to parse intent. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    loading,
    error,
    parseIntent
  };

  return <NLPContext.Provider value={value}>{children}</NLPContext.Provider>;
};
