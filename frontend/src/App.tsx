import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { TransactionProvider } from './contexts/TransactionContext';
import { WalletProvider } from './contexts/WalletContext';
import { NLPProvider } from './contexts/NLPContext';
import { VaultProvider } from './contexts/VaultContext';

// Layouts
import MainLayout from './layouts/MainLayout';
import AuthLayout from './layouts/AuthLayout';

// Pages
import Dashboard from './pages/Dashboard';
import SendMoney from './pages/SendMoney';
import ReceiveMoney from './pages/ReceiveMoney';
import TransactionHistory from './pages/TransactionHistory';
import Settings from './pages/Settings';
import Login from './pages/Login';
import Register from './pages/Register';
import VerifyIdentity from './pages/VerifyIdentity';
import NotFound from './pages/NotFound';
import Vault from './pages/Vault';

// Protected Route Component
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  // In a real app, this would check authentication state from context
  const isAuthenticated = localStorage.getItem('remitai_token') !== null;
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

function App() {
  return (
    <AuthProvider>
      <TransactionProvider>
        <WalletProvider>
          <VaultProvider>
            <NLPProvider>
              <Router>
                <Routes>
                  {/* Auth routes */}
                  <Route element={<AuthLayout />}>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/verify" element={<VerifyIdentity />} />
                  </Route>
                  
                  {/* Main app routes - protected */}
                  <Route element={<MainLayout />}>
                    <Route path="/" element={
                      <ProtectedRoute>
                        <Dashboard />
                      </ProtectedRoute>
                    } />
                    <Route path="/send" element={
                      <ProtectedRoute>
                        <SendMoney />
                      </ProtectedRoute>
                    } />
                    <Route path="/receive" element={
                      <ProtectedRoute>
                        <ReceiveMoney />
                      </ProtectedRoute>
                    } />
                    <Route path="/history" element={
                      <ProtectedRoute>
                        <TransactionHistory />
                      </ProtectedRoute>
                    } />
                    <Route path="/vault" element={
                      <ProtectedRoute>
                        <Vault />
                      </ProtectedRoute>
                    } />
                    <Route path="/settings" element={
                      <ProtectedRoute>
                        <Settings />
                      </ProtectedRoute>
                    } />
                  </Route>
                  
                  {/* 404 route */}
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </Router>
            </NLPProvider>
          </VaultProvider>
        </WalletProvider>
      </TransactionProvider>
    </AuthProvider>
  );
}

export default App;
