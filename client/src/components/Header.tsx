import React from "react";

interface HeaderProps {
  onLogout: () => void;
}

const Header: React.FC<HeaderProps> = ({ onLogout }) => {
  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3 sm:px-6">
      <div>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div>
              <img
                src="images/header.jpeg"
                alt="Smart City Logo"
                className="h-14 w-auto mr-8"
              />
            </div>
          </div>
          
          <div className="flex items-center">
            <button
              onClick={onLogout}
              className=" cursor-pointer flex items-center gap-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors duration-200 font-medium text-sm"
            >
              <svg 
                className="w-4 h-4" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" 
                />
              </svg>
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
