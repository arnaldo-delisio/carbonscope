#!/usr/bin/env python3
"""
Test script for CarbonScope API
Run this to verify the backend is working correctly
"""

import requests
import json
import sys

API_BASE = "http://localhost:8000"

def test_health_check():
    """Test basic health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.ConnectionError:
        print("❌ Cannot connect to API. Is the backend running?")
        return False

def test_product_scan():
    """Test product scanning endpoint"""
    print("\n🔍 Testing product scan...")
    
    test_data = {
        "barcode": "1234567890123",
        "user_location": "test_location",
        "purchase_context": "online"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/api/v1/products/scan",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Product scan successful")
            print(f"   Product: {data.get('product_name', 'Unknown')}")
            print(f"   Carbon footprint: {data.get('carbon_estimate', {}).get('total_co2_kg', 'N/A')} kg CO₂e")
            print(f"   Confidence: {data.get('carbon_estimate', {}).get('confidence_score', 'N/A')}")
            return True
        else:
            print(f"❌ Product scan failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Product scan error: {e}")
        return False

def test_alternative_barcode():
    """Test with iPhone barcode"""
    print("\n🔍 Testing iPhone barcode...")
    
    test_data = {
        "barcode": "7890123456789",
        "user_location": "california",
        "purchase_context": "retail_store"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/api/v1/products/scan",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ iPhone scan successful")
            print(f"   Product: {data.get('product_name', 'Unknown')}")
            print(f"   Carbon footprint: {data.get('carbon_estimate', {}).get('total_co2_kg', 'N/A')} kg CO₂e")
            
            alternatives = data.get('alternatives', [])
            if alternatives:
                print(f"   Alternatives found: {len(alternatives)}")
                for alt in alternatives[:2]:  # Show first 2
                    print(f"     - {alt.get('name')}: Save {alt.get('savings_kg')} kg CO₂e")
            
            return True
        else:
            print(f"❌ iPhone scan failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ iPhone scan error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 CarbonScope API Test Suite")
    print("=" * 40)
    
    tests = [
        test_health_check,
        test_product_scan,
        test_alternative_barcode
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Start the frontend: cd frontend && npm start")
        print("   2. Visit http://localhost:3000")
        print("   3. Try scanning the test barcodes!")
    else:
        print("❌ Some tests failed. Check the backend setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()
