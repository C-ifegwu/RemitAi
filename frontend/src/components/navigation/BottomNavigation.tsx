import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { HomeIcon, ArrowUpRightIcon, QrCodeIcon, ClockIcon, UserIcon, BanknotesIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';

const BottomNavigation: React.FC = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: HomeIcon, label: 'Home' },
    { path: '/send', icon: ArrowUpRightIcon, label: 'Send' },
    { path: '/receive', icon: QrCodeIcon, label: 'Receive' },
    { path: '/vault', icon: BanknotesIcon, label: 'Vault' },
    { path: '/history', icon: ClockIcon, label: 'History' },
    { path: '/settings', icon: UserIcon, label: 'Profile' },
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-neutral-200 md:hidden z-10">
      <nav className="flex justify-around items-center h-16">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex flex-col items-center justify-center w-full h-full ${
                isActive ? 'text-primary-500' : 'text-neutral-500'
              }`}
            >
              <div className="relative">
                <item.icon className="w-6 h-6" />
                {isActive && (
                  <motion.div
                    layoutId="bottomNavIndicator"
                    className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-primary-500 rounded-full"
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  />
                )}
              </div>
              <span className="text-xs mt-1">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
};

export default BottomNavigation;
