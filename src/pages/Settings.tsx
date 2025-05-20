import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  BellIcon, 
  LanguageIcon, 
  LockClosedIcon, 
  UserIcon, 
  ArrowRightOnRectangleIcon,
  ChevronRightIcon,
  MoonIcon
} from '@heroicons/react/24/outline';

interface SettingsProps {}

const Settings: React.FC<SettingsProps> = () => {
  const [activeTab, setActiveTab] = useState('profile');
  
  // Mock user data
  const user = {
    name: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+1 (555) 123-4567',
    profileImage: null,
    language: 'English',
    notificationsEnabled: true,
    darkModeEnabled: false
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'profile':
        return (
          <div className="space-y-6">
            <div className="flex flex-col items-center mb-6">
              <div className="w-24 h-24 rounded-full bg-neutral-200 flex items-center justify-center mb-4">
                {user.profileImage ? (
                  <img src={user.profileImage} alt={user.name} className="w-full h-full rounded-full" />
                ) : (
                  <span className="text-neutral-600 text-2xl font-medium">
                    {user.name.split(' ').map(n => n[0]).join('')}
                  </span>
                )}
              </div>
              <h3 className="text-xl font-semibold">{user.name}</h3>
              <p className="text-neutral-500">{user.email}</p>
            </div>
            
            <div className="space-y-4">
              <div className="border-b border-neutral-200 pb-4">
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  className="input"
                  value={user.name}
                  onChange={() => {}}
                />
              </div>
              
              <div className="border-b border-neutral-200 pb-4">
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  className="input"
                  value={user.email}
                  onChange={() => {}}
                />
              </div>
              
              <div className="border-b border-neutral-200 pb-4">
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Phone Number
                </label>
                <input
                  type="tel"
                  className="input"
                  value={user.phone}
                  onChange={() => {}}
                />
              </div>
              
              <button className="btn btn-primary w-full">
                Save Changes
              </button>
            </div>
          </div>
        );
        
      case 'notifications':
        return (
          <div className="space-y-6">
            <h3 className="text-xl font-semibold mb-4">Notifications</h3>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-neutral-200">
                <div>
                  <h4 className="font-medium">Push Notifications</h4>
                  <p className="text-sm text-neutral-500">Receive alerts on your device</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    className="sr-only peer" 
                    checked={user.notificationsEnabled}
                    onChange={() => {}}
                  />
                  <div className="w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-neutral-200">
                <div>
                  <h4 className="font-medium">Transaction Alerts</h4>
                  <p className="text-sm text-neutral-500">Get notified about your transactions</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    className="sr-only peer" 
                    checked={true}
                    onChange={() => {}}
                  />
                  <div className="w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-neutral-200">
                <div>
                  <h4 className="font-medium">Marketing Updates</h4>
                  <p className="text-sm text-neutral-500">Receive news and special offers</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    className="sr-only peer" 
                    checked={false}
                    onChange={() => {}}
                  />
                  <div className="w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
                </label>
              </div>
            </div>
          </div>
        );
        
      case 'language':
        return (
          <div className="space-y-6">
            <h3 className="text-xl font-semibold mb-4">Language</h3>
            
            <div className="space-y-4">
              <div className="bg-white rounded-xl border border-neutral-200 overflow-hidden">
                {['English', 'Français', 'Español', 'Yoruba', 'Igbo', 'Hausa', 'العربية', 'Kiswahili'].map((language, index) => (
                  <div 
                    key={language}
                    className={`flex items-center justify-between p-4 ${index !== 0 && 'border-t border-neutral-200'}`}
                  >
                    <span className={user.language === language ? 'font-medium text-primary-500' : ''}>
                      {language}
                    </span>
                    {user.language === language && (
                      <div className="w-5 h-5 rounded-full bg-primary-500 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-white" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
        
      case 'security':
        return (
          <div className="space-y-6">
            <h3 className="text-xl font-semibold mb-4">Security & Privacy</h3>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-neutral-200">
                <div>
                  <h4 className="font-medium">Change Password</h4>
                  <p className="text-sm text-neutral-500">Update your account password</p>
                </div>
                <ChevronRightIcon className="h-5 w-5 text-neutral-400" />
              </div>
              
              <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-neutral-200">
                <div>
                  <h4 className="font-medium">Two-Factor Authentication</h4>
                  <p className="text-sm text-neutral-500">Add an extra layer of security</p>
                </div>
                <ChevronRightIcon className="h-5 w-5 text-neutral-400" />
              </div>
              
              <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-neutral-200">
                <div>
                  <h4 className="font-medium">Biometric Authentication</h4>
                  <p className="text-sm text-neutral-500">Use your voice or fingerprint</p>
                </div>
                <ChevronRightIcon className="h-5 w-5 text-neutral-400" />
              </div>
              
              <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-neutral-200">
                <div>
                  <h4 className="font-medium">Privacy Settings</h4>
                  <p className="text-sm text-neutral-500">Manage your data and privacy</p>
                </div>
                <ChevronRightIcon className="h-5 w-5 text-neutral-400" />
              </div>
            </div>
            
            <button className="btn btn-outline w-full text-red-600 border-red-200 hover:bg-red-50">
              Delete Account
            </button>
          </div>
        );
        
      case 'appearance':
        return (
          <div className="space-y-6">
            <h3 className="text-xl font-semibold mb-4">Appearance</h3>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-neutral-200">
                <div className="flex items-center">
                  <MoonIcon className="h-5 w-5 mr-3 text-neutral-600" />
                  <div>
                    <h4 className="font-medium">Dark Mode</h4>
                    <p className="text-sm text-neutral-500">Use dark theme</p>
                  </div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    className="sr-only peer" 
                    checked={user.darkModeEnabled}
                    onChange={() => {}}
                  />
                  <div className="w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
                </label>
              </div>
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      <motion.div 
        className="card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        {/* Settings Tabs */}
        <div className="flex overflow-x-auto pb-4 mb-6 -mx-5 px-5 scrollbar-hide">
          <button
            className={`flex flex-col items-center px-4 py-2 rounded-xl mr-4 min-w-[80px] ${
              activeTab === 'profile' ? 'bg-primary-100 text-primary-800' : 'text-neutral-600'
            }`}
            onClick={() => setActiveTab('profile')}
          >
            <UserIcon className="h-6 w-6 mb-1" />
            <span className="text-sm">Profile</span>
          </button>
          
          <button
            className={`flex flex-col items-center px-4 py-2 rounded-xl mr-4 min-w-[80px] ${
              activeTab === 'notifications' ? 'bg-primary-100 text-primary-800' : 'text-neutral-600'
            }`}
            onClick={() => setActiveTab('notifications')}
          >
            <BellIcon className="h-6 w-6 mb-1" />
            <span className="text-sm">Notifications</span>
          </button>
          
          <button
            className={`flex flex-col items-center px-4 py-2 rounded-xl mr-4 min-w-[80px] ${
              activeTab === 'language' ? 'bg-primary-100 text-primary-800' : 'text-neutral-600'
            }`}
            onClick={() => setActiveTab('language')}
          >
            <LanguageIcon className="h-6 w-6 mb-1" />
            <span className="text-sm">Language</span>
          </button>
          
          <button
            className={`flex flex-col items-center px-4 py-2 rounded-xl mr-4 min-w-[80px] ${
              activeTab === 'security' ? 'bg-primary-100 text-primary-800' : 'text-neutral-600'
            }`}
            onClick={() => setActiveTab('security')}
          >
            <LockClosedIcon className="h-6 w-6 mb-1" />
            <span className="text-sm">Security</span>
          </button>
          
          <button
            className={`flex flex-col items-center px-4 py-2 rounded-xl mr-4 min-w-[80px] ${
              activeTab === 'appearance' ? 'bg-primary-100 text-primary-800' : 'text-neutral-600'
            }`}
            onClick={() => setActiveTab('appearance')}
          >
            <MoonIcon className="h-6 w-6 mb-1" />
            <span className="text-sm">Appearance</span>
          </button>
        </div>
        
        {/* Tab Content */}
        <div>
          {renderTabContent()}
        </div>
      </motion.div>
      
      {/* Logout Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.2 }}
      >
        <button className="btn btn-outline w-full flex items-center justify-center">
          <ArrowRightOnRectangleIcon className="h-5 w-5 mr-2" />
          <span>Logout</span>
        </button>
      </motion.div>
    </div>
  );
};

export default Settings;
