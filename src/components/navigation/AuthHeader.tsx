import React from 'react';
import { Link } from 'react-router-dom';

const AuthHeader: React.FC = () => {
  return (
    <header className="bg-white py-6 px-4">
      <div className="container mx-auto flex justify-center">
        <Link to="/" className="flex items-center">
          <span className="font-display font-bold text-2xl text-primary-500">RemitAI</span>
        </Link>
      </div>
    </header>
  );
};

export default AuthHeader;
