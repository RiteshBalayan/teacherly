import React from 'react';

function Header() {
  return (
    <nav className="py-6 px-6 flex justify-between items-center border-b border-gray-200">
      <a href="/" className="text-xl font-semibold">Teacherly</a>
      <div className="space-x-6">
        <a href="/" className="px-6 py-3 text-lg font-semibold bg-teal-500 text-white rounded-xl hover:bg-teal-700">Sign up</a>
        <a href="/" className="px-6 py-3 text-lg font-semibold bg-gray-500 text-white rounded-xl hover:bg-gray-700">Log in</a>
      </div>
    </nav>
  );
}

export default Header;
