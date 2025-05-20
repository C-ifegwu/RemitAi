import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BellIcon, Bars3Icon } from '@heroicons/react/24/outline';
import { motion, AnimatePresence } from 'framer-motion';

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();
  
  // Get page title based on current route
  const getPageTitle = () => {
    switch (location.pathname) {
      case '/':
        return 'Home';
      case '/send':
        return 'Send Money';
      case '/receive':
        return 'Receive Money';
      case '/history':
        return 'Transaction History';
      case '/settings':
        return 'Settings';
      default:
        return 'RemitAI';
    }
  };

  return (
    <header className="bg-white border-b border-neutral-200 sticky top-0 z-20">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Left section - Logo or back button */}
        <div className="flex items-center">
          {location.pathname !== '/' ? (
            <button 
              onClick={() => window.history.back()}
              className="mr-4 p-2 rounded-full hover:bg-neutral-100"
              aria-label="Go back"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </button>
          ) : (
            <Link to="/" className="flex items-center">
              <span className="font-display font-bold text-xl text-primary-500">RemitAI</span>
            </Link>
          )}
        </div>
        
        {/* Center section - Page title */}
        <h1 className="text-lg font-medium hidden md:block">{getPageTitle()}</h1>
        
        {/* Right section - Notifications and menu */}
        <div className="flex items-center space-x-4">
          <button 
            className="p-2 rounded-full hover:bg-neutral-100 relative"
            aria-label="Notifications"
          >
            <BellIcon className="h-6 w-6 text-neutral-700" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-secondary-500 rounded-full"></span>
          </button>
          
          <button 
            className="p-2 rounded-full hover:bg-neutral-100 md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Menu"
          >
            <Bars3Icon className="h-6 w-6 text-neutral-700" />
          </button>
          
          {/* Profile avatar - visible on desktop */}
          <div className="hidden md:flex items-center space-x-3">
            <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
              <span className="font-medium text-primary-800">JD</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Mobile menu */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.2 }}
            className="absolute top-16 left-0 right-0 bg-white border-b border-neutral-200 shadow-lg z-10 md:hidden"
          >
            <nav className="container mx-auto py-4 px-4">
              <ul className="space-y-2">
                <li>
                  <Link 
                    to="/settings" 
                    className="flex items-center p-3 rounded-xl hover:bg-neutral-100"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <UserIcon className="h-5 w-5 mr-3 text-neutral-600" />
                    <span>Profile</span>
                  </Link>
                </li>
                <li>
                  <Link 
                    to="/settings?tab=security" 
                    className="flex items-center p-3 rounded-xl hover:bg-neutral-100"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <LockClosedIcon className="h-5 w-5 mr-3 text-neutral-600" />
                    <span>Security</span>
                  </Link>
                </li>
                <li>
                  <Link 
                    to="/settings?tab=language" 
                    className="flex items-center p-3 rounded-xl hover:bg-neutral-100"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <LanguageIcon className="h-5 w-5 mr-3 text-neutral-600" />
                    <span>Language</span>
                  </Link>
                </li>
                <li>
                  <button 
                    className="flex items-center w-full p-3 rounded-xl hover:bg-neutral-100 text-red-600"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <ArrowRightOnRectangleIcon className="h-5 w-5 mr-3" />
                    <span>Logout</span>
                  </button>
                </li>
              </ul>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
};

// Import these icons at the top of the file
import { UserIcon, LockClosedIcon, LanguageIcon, ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline';

export default Header;
