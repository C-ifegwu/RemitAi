import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from '../services/api';

interface AuthContextType {
  isAuthenticated: boolean;
  user: any | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (userData: any) => Promise<void>;
  requestOTP: (userId: string, phoneNumber: string, method: string) => Promise<any>;
  verifyOTP: (userId: string, otpCode: string) => Promise<any>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Check if user is logged in on initial load
    const checkAuthStatus = async () => {
      const token = localStorage.getItem('remitai_token');
      const userData = localStorage.getItem('remitai_user');
      
      if (token && userData) {
        try {
          // In a real app, you would validate the token with the backend
          setUser(JSON.parse(userData));
          setIsAuthenticated(true);
        } catch (error) {
          console.error('Error parsing user data:', error);
          localStorage.removeItem('remitai_token');
          localStorage.removeItem('remitai_user');
        }
      }
      
      setLoading(false);
    };
    
    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await authAPI.login(email, password);
      const { token, user } = response.data;
      
      localStorage.setItem('remitai_token', token);
      localStorage.setItem('remitai_user', JSON.stringify(user));
      
      setUser(user);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('remitai_token');
    localStorage.removeItem('remitai_user');
    setUser(null);
    setIsAuthenticated(false);
  };

  const register = async (userData: any) => {
    setLoading(true);
    try {
      const response = await authAPI.register(userData);
      const { token, user } = response.data;
      
      localStorage.setItem('remitai_token', token);
      localStorage.setItem('remitai_user', JSON.stringify(user));
      
      setUser(user);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const requestOTP = async (userId: string, phoneNumber: string, method: string) => {
    try {
      const response = await authAPI.requestOTP(userId, phoneNumber, method);
      return response.data;
    } catch (error) {
      console.error('OTP request error:', error);
      throw error;
    }
  };

  const verifyOTP = async (userId: string, otpCode: string) => {
    try {
      const response = await authAPI.verifyOTP(userId, otpCode);
      return response.data;
    } catch (error) {
      console.error('OTP verification error:', error);
      throw error;
    }
  };

  const value = {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    register,
    requestOTP,
    verifyOTP
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
