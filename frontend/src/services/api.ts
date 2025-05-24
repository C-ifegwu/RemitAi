import axios from 'axios';

// Base URL for API calls
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('remitai_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for handling common errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized errors (token expired)
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('remitai_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email: string, password: string) => 
    apiClient.post('/auth/login', { email, password }),
  
  register: (userData: any) => 
    apiClient.post('/auth/register', userData),
  
  requestOTP: (userId: string, phoneNumber: string, method: string) => 
    apiClient.post('/auth/request-otp', { user_id: userId, phone_number: phoneNumber, method }),
  
  verifyOTP: (userId: string, otpCode: string) => 
    apiClient.post('/auth/verify-otp', { user_id: userId, otp_code: otpCode }),
};

// NLP API
export const nlpAPI = {
  parseIntent: (userId: string, text: string, language: string) => 
    apiClient.post('/nlp/parse-intent', { user_id: userId, text, language }),
};

// Transactions API
export const transactionsAPI = {
  // On-ramp operations
  initiateOnRamp: (userId: string, fiatAmount: number, fiatCurrency: string, provider: string) => 
    apiClient.post('/transactions/onramp/initiate', { 
      user_id: userId, 
      fiat_amount: fiatAmount, 
      fiat_currency: fiatCurrency, 
      provider 
    }),
  
  checkOnRampStatus: (transactionId: string) => 
    apiClient.get(`/transactions/onramp/status/${transactionId}`),
  
  // Off-ramp operations
  initiateOffRamp: (userId: string, usdcAmount: number, targetCurrency: string, recipientDetails: any, provider: string) => 
    apiClient.post('/transactions/offramp/initiate', { 
      user_id: userId, 
      usdc_amount: usdcAmount, 
      target_currency: targetCurrency, 
      recipient_details: recipientDetails, 
      provider 
    }),
  
  checkOffRampStatus: (transactionId: string) => 
    apiClient.get(`/transactions/offramp/status/${transactionId}`),
  
  // Withdrawal confirmation
  confirmWithdrawal: (userId: string, transactionId: string) => 
    apiClient.post('/transactions/withdrawal/confirm-on-contract', { 
      user_id: userId, 
      transaction_id: transactionId 
    }),
  
  // Risk assessment
  assessTransactionRisk: (userId: string, commandText: string, amount: number, recipientId: string) => 
    apiClient.post('/transactions/assess-risk', { 
      user_id: userId, 
      command_text: commandText, 
      amount, 
      recipient_id: recipientId 
    }),
};

// Wallet API
export const walletAPI = {
  generateRecoveryPhrase: () => 
    apiClient.post('/wallet/backup/generate-phrase'),
  
  confirmRecoveryPhraseSaved: (userId: string) => 
    apiClient.post('/wallet/backup/confirm-saved', { user_id: userId }),
  
  linkBiometric: (userId: string, voicePrintId: string) => 
    apiClient.post('/wallet/backup/link-biometric', { 
      user_id: userId, 
      voice_print_id: voicePrintId 
    }),
  
  recoverWithPassphrase: (userId: string, passphraseWords: string[]) => 
    apiClient.post('/wallet/recover/passphrase', { 
      user_id: userId, 
      passphrase_words: passphraseWords 
    }),
  
  recoverWithBiometric: (userId: string, voiceVerificationToken: string) => 
    apiClient.post('/wallet/recover/biometric', { 
      user_id: userId, 
      voice_verification_token: voiceVerificationToken 
    }),
};

// Voice Biometrics API
export const voiceAPI = {
  registerVoice: (userId: string, audioSamplePaths: string[]) => 
    apiClient.post('/voice/register', { 
      user_id: userId, 
      audio_sample_paths: audioSamplePaths 
    }),
  
  verifyVoice: (userId: string, audioSamplePath: string, attemptLivenessCheck: boolean = true) => 
    apiClient.post('/voice/verify', { 
      user_id: userId, 
      audio_sample_path: audioSamplePath, 
      attempt_liveness_check: attemptLivenessCheck 
    }),
};

export default apiClient;
