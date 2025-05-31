import React, { useState } from 'react';

interface CarbonEstimate {
  total_co2_kg: number;
  production_co2_kg: number;
  transport_co2_kg: number;
  packaging_co2_kg: number;
  confidence_score: number;
  methodology: string;
}

interface ProductAnalysis {
  scan_id: string;
  product_name: string;
  barcode: string;
  materials_detected: string[];
  carbon_estimate: CarbonEstimate;
  alternatives: Array<{
    name: string;
    co2_kg: number;
    co2_reduction: number;
    reason: string;
    savings_kg: number;
  }>;
  timestamp: string;
}

const BarcodeScanner: React.FC = () => {
  const [barcode, setBarcode] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<ProductAnalysis | null>(null);
  const [error, setError] = useState<string>('');

  const handleScan = async (): Promise<void> => {
    if (!barcode.trim()) {
      setError('Please enter a barcode');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('/api/v1/products/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          barcode: barcode.trim(),
          user_location: 'test_location',
          purchase_context: 'online'
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ProductAnalysis = await response.json();
      setResult(data);
    } catch (err) {
      setError(`Failed to analyze product: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const getCarbonLevel = (co2Kg: number): { level: string; color: string } => {
    if (co2Kg < 1) return { level: 'Low', color: 'text-green-600' };
    if (co2Kg < 5) return { level: 'Medium', color: 'text-yellow-600' };
    return { level: 'High', color: 'text-red-600' };
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">🔍 Scan Product</h2>
      
      {/* Input Section */}
      <div className="mb-6">
        <label htmlFor="barcode" className="block text-sm font-medium text-gray-700 mb-2">
          Barcode
        </label>
        <div className="flex gap-2">
          <input
            id="barcode"
            type="text"
            value={barcode}
            onChange={(e) => setBarcode(e.target.value)}
            placeholder="Enter barcode (e.g., 1234567890123)"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            onKeyPress={(e) => e.key === 'Enter' && handleScan()}
          />
          <button
            onClick={handleScan}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? '...' : 'Scan'}
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          Try: 1234567890123 (Coca-Cola) or 7890123456789 (iPhone)
        </p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="space-y-4">
          {/* Product Info */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-lg">{result.product_name}</h3>
            <p className="text-sm text-gray-600">Barcode: {result.barcode}</p>
            {result.materials_detected.length > 0 && (
              <p className="text-sm text-gray-600">
                Materials: {result.materials_detected.join(', ')}
              </p>
            )}
          </div>

          {/* Carbon Footprint */}
          <div className="p-4 bg-blue-50 rounded-lg">
            <h4 className="font-semibold mb-2">🌍 Carbon Footprint</h4>
            <div className={`text-2xl font-bold ${getCarbonLevel(result.carbon_estimate.total_co2_kg).color}`}>
              {result.carbon_estimate.total_co2_kg} kg CO₂e
            </div>
            <div className={`text-sm ${getCarbonLevel(result.carbon_estimate.total_co2_kg).color}`}>
              {getCarbonLevel(result.carbon_estimate.total_co2_kg).level} Impact
            </div>
            
            <div className="mt-3 space-y-1 text-sm">
              <div>Production: {result.carbon_estimate.production_co2_kg} kg</div>
              <div>Transport: {result.carbon_estimate.transport_co2_kg} kg</div>
              <div>Packaging: {result.carbon_estimate.packaging_co2_kg} kg</div>
            </div>
            
            <div className="mt-2 text-xs text-gray-600">
              Confidence: {Math.round(result.carbon_estimate.confidence_score * 100)}%
            </div>
          </div>

          {/* Alternatives */}
          {result.alternatives.length > 0 && (
            <div className="p-4 bg-green-50 rounded-lg">
              <h4 className="font-semibold mb-2">💡 Better Alternatives</h4>
              <div className="space-y-2">
                {result.alternatives.map((alt, index) => (
                  <div key={index} className="text-sm">
                    <div className="font-medium">{alt.name}</div>
                    <div className="text-green-600">
                      Save {alt.savings_kg} kg CO₂e ({Math.round(alt.co2_reduction * 100)}% less)
                    </div>
                    <div className="text-gray-600 text-xs">{alt.reason}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default BarcodeScanner;
