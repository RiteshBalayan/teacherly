import React from 'react';

function Footer() {
  return (
    <footer className="py-6 px-6 flex justify-between bg-gray-800">
      <div className="w-2/3 pr-10">
        <h3 className="mb-5 font-semibold text-gray-400">About</h3>
        <p className="text-lg text-gray-500">Lorem ipsum bla bla bla</p>
      </div>
      <div className="w-1/3">
        <h3 className="mb-5 font-semibold text-gray-400">Menu</h3>
        <ul className="space-y-2">
          <li><a href="#" className="text-lg text-teal-500 hover:text-teal-700">About</a></li>
          <li><a href="#" className="text-lg text-teal-500 hover:text-teal-700">Contact</a></li>
          <li><a href="#" className="text-lg text-teal-500 hover:text-teal-700">Privacy Policy</a></li>
          <li><a href="#" className="text-lg text-teal-500 hover:text-teal-700">Terms of use</a></li>
        </ul>
      </div>
    </footer>
  );
}

export default Footer;
