import React, { useState } from 'react';
import BarcodeScanner from './components/BarcodeScanner';
import './App.css';

function App(): JSX.Element {
  const [activeTab, setActiveTab] = useState<'home' | 'scan'>('home');

  return (
    <div className="App min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-gray-900">🌍 CarbonScope</h1>
              <span className="ml-3 text-sm text-gray-500">AI-Powered Carbon Analysis</span>
            </div>
            <nav className="flex space-x-4">
              <button
                onClick={() => setActiveTab('home')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === 'home' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Home
              </button>
              <button
                onClick={() => setActiveTab('scan')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === 'scan' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Scan Product
              </button>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {activeTab === 'home' && (
          <div className="px-4 py-6 sm:px-0">
            <div className="text-center">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Revolutionary Carbon Footprint Analysis
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Use AI to instantly calculate the carbon impact of any product
              </p>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-12">
                <div className="bg-white p-6 rounded-lg shadow-md">
                  <div className="text-3xl mb-4">📱</div>
                  <h3 className="text-lg font-semibold mb-2">Scan Products</h3>
                  <p className="text-gray-600">Enter barcodes to analyze carbon footprint instantly</p>
                </div>
                
                <div className="bg-white p-6 rounded-lg shadow-md">
                  <div className="text-3xl mb-4">🤖</div>
                  <h3 className="text-lg font-semibold mb-2">AI Analysis</h3>
                  <p className="text-gray-600">Smart algorithms calculate real-time carbon estimates</p>
                </div>
                
                <div className="bg-white p-6 rounded-lg shadow-md">
                  <div className="text-3xl mb-4">🌐</div>
                  <h3 className="text-lg font-semibold mb-2">Real-Time Data</h3>
                  <p className="text-gray-600">Dynamic calculation based on current supply chains</p>
                </div>
                
                <div className="bg-white p-6 rounded-lg shadow-md">
                  <div className="text-3xl mb-4">💡</div>
                  <h3 className="text-lg font-semibold mb-2">Smart Alternatives</h3>
                  <p className="text-gray-600">Get suggestions for lower-carbon options</p>
                </div>
              </div>
              
              <div className="mt-8">
                <button
                  onClick={() => setActiveTab('scan')}
                  className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
                >
                  Start Scanning Products
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'scan' && (
          <div className="px-4 py-6 sm:px-0">
            <BarcodeScanner />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
