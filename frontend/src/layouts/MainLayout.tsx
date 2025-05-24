import React from 'react';
import { Outlet } from 'react-router-dom';
import BottomNavigation from '../components/navigation/BottomNavigation';
import Header from '../components/navigation/Header';

const MainLayout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen bg-neutral-50">
      <Header />
      
      <main className="flex-1 container mx-auto px-4 py-6 pb-20 md:pb-6 animate-fadeIn">
        <Outlet />
      </main>
      
      <BottomNavigation />
    </div>
  );
};

export default MainLayout;
