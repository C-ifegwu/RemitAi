import React from 'react';
import { Outlet } from 'react-router-dom';
import AuthHeader from '../components/navigation/AuthHeader';

const AuthLayout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <AuthHeader />
      
      <main className="flex-1 flex items-center justify-center p-4 animate-fadeIn">
        <div className="w-full max-w-md">
          <Outlet />
        </div>
      </main>
      
      <footer className="py-4 text-center text-neutral-500 text-sm">
        <p>© {new Date().getFullYear()} RemitAI. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default AuthLayout;
