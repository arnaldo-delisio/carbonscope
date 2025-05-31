import React from 'react';
import './App.css';

function App(): JSX.Element {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🌍 CarbonScope</h1>
        <p>AI-Powered Carbon Footprint Analyzer</p>
        <div className="features">
          <div className="feature">
            <h3>📱 Scan Products</h3>
            <p>Use your camera to scan barcodes and analyze products</p>
          </div>
          <div className="feature">
            <h3>🤖 AI Analysis</h3>
            <p>Advanced computer vision for material detection</p>
          </div>
          <div className="feature">
            <h3>🌐 Real-Time Data</h3>
            <p>Dynamic carbon calculation based on current supply chains</p>
          </div>
          <div className="feature">
            <h3>🤝 Community</h3>
            <p>Crowdsourced verification for improved accuracy</p>
          </div>
        </div>
        <div className="cta">
          <button className="scan-button">
            Start Scanning Products
          </button>
        </div>
      </header>
    </div>
  );
}

export default App;
