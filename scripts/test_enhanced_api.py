#!/usr/bin/env python3
"""
Enhanced test script for CarbonScope API
Tests all enhanced features and realistic scenarios
"""

import requests
import json
import sys
import time
from typing import Dict, List

API_BASE = "http://localhost:8000"

def print_header(title: str):
    """Print formatted test section header"""
    print(f"\n{'='*50}")
    print(f"🧪 {title}")
    print('='*50)

def print_result(test_name: str, success: bool, details: str = ""):
    """Print formatted test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"   {details}")

def test_health_check() -> bool:
    """Test basic health check endpoint"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        success = response.status_code == 200
        data = response.json() if success else {}
        
        print_result(
            "Health Check", 
            success,
            f"Status: {data.get('status', 'Unknown')}" if success else f"HTTP {response.status_code}"
        )
        return success
    except requests.ConnectionError:
        print_result("Health Check", False, "Cannot connect to API. Is the backend running?")
        return False
    except Exception as e:
        print_result("Health Check", False, f"Error: {e}")
        return False

def test_enhanced_barcode_scan(barcode: str, expected_product: str) -> bool:
    """Test enhanced barcode scanning with specific expectations"""
    try:
        test_data = {
            "barcode": barcode,
            "user_location": "California",
            "purchase_context": "retail_store"
        }
        
        response = requests.post(
            f"{API_BASE}/api/v1/products/scan",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code != 200:
            print_result(f"Barcode Scan ({barcode})", False, f"HTTP {response.status_code}")
            return False
        
        data = response.json()
        
        # Validate response structure
        required_fields = ["scan_id", "product_name", "carbon_estimate", "alternatives"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            print_result(f"Barcode Scan ({barcode})", False, f"Missing fields: {missing_fields}")
            return False
        
        # Validate carbon estimate structure
        carbon_est = data["carbon_estimate"]
        required_carbon_fields = ["total_co2_kg", "confidence_score", "impact_level", "methodology"]
        missing_carbon_fields = [field for field in required_carbon_fields if field not in carbon_est]
        
        if missing_carbon_fields:
            print_result(f"Barcode Scan ({barcode})", False, f"Missing carbon fields: {missing_carbon_fields}")
            return False
        
        # Print detailed results
        product_name = data["product_name"]
        total_co2 = carbon_est["total_co2_kg"]
        confidence = carbon_est["confidence_score"]
        impact_level = carbon_est["impact_level"]
        alternatives_count = len(data["alternatives"])
        
        details = f"""
   Product: {product_name}
   Carbon: {total_co2} kg CO₂e ({impact_level} impact)
   Confidence: {confidence:.1%}
   Alternatives: {alternatives_count} found
   Materials: {data.get('materials_detected', [])}"""
        
        print_result(f"Barcode Scan ({barcode})", True, details)
        
        # Validate alternatives have required fields
        if alternatives_count > 0:
            alt = data["alternatives"][0]
            alt_required = ["name", "co2_kg", "savings_kg", "reason"]
            missing_alt_fields = [field for field in alt_required if field not in alt]
            
            if missing_alt_fields:
                print_result("Alternative Structure", False, f"Missing: {missing_alt_fields}")
                return False
            
            print_result("Alternative Structure", True, f"Best: {alt['name']} saves {alt['savings_kg']} kg CO₂e")
        
        return True
        
    except Exception as e:
        print_result(f"Barcode Scan ({barcode})", False, f"Error: {e}")
        return False

def test_purchase_context_effects() -> bool:
    """Test that purchase context affects carbon calculations"""
    try:
        base_request = {
            "barcode": "1234567890123",
            "user_location": "California"
        }
        
        contexts = ["retail_store", "express_shipping", "same_day_delivery"]
        results = {}
        
        for context in contexts:
            request_data = {**base_request, "purchase_context": context}
            response = requests.post(
                f"{API_BASE}/api/v1/products/scan",
                json=request_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results[context] = data["carbon_estimate"]["total_co2_kg"]
            else:
                print_result("Context Effects", False, f"Failed for context: {context}")
                return False
        
        # Verify that different contexts produce different results
        unique_values = len(set(results.values()))
        if unique_values > 1:
            details = "\n".join([f"   {ctx}: {co2:.2f} kg CO₂e" for ctx, co2 in results.items()])
            print_result("Context Effects", True, f"Different contexts produce different results:\n{details}")
            return True
        else:
            print_result("Context Effects", False, "All contexts produced same result")
            return False
            
    except Exception as e:
        print_result("Context Effects", False, f"Error: {e}")
        return False

def test_confidence_scoring() -> bool:
    """Test confidence scoring for different product types"""
    try:
        test_cases = [
            ("1234567890123", "Known product (Coca-Cola)"),
            ("9999999999999", "Unknown product"),
        ]
        
        confidences = {}
        
        for barcode, description in test_cases:
            response = requests.post(
                f"{API_BASE}/api/v1/products/scan",
                json={"barcode": barcode},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                confidence = data["carbon_estimate"]["confidence_score"]
                confidences[description] = confidence
            else:
                print_result("Confidence Scoring", False, f"Failed for: {description}")
                return False
        
        # Known products should have higher confidence
        known_conf = confidences.get("Known product (Coca-Cola)", 0)
        unknown_conf = confidences.get("Unknown product", 1)
        
        if known_conf > unknown_conf:
            details = f"\n   Known product: {known_conf:.1%}\n   Unknown product: {unknown_conf:.1%}"
            print_result("Confidence Scoring", True, f"Confidence varies appropriately:{details}")
            return True
        else:
            print_result("Confidence Scoring", False, "Confidence scoring not working properly")
            return False
            
    except Exception as e:
        print_result("Confidence Scoring", False, f"Error: {e}")
        return False

def test_api_performance() -> bool:
    """Test API performance and response times"""
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE}/api/v1/products/scan",
            json={"barcode": "1234567890123"},
            timeout=15
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200 and response_time < 5.0:  # Should respond in under 5 seconds
            print_result("API Performance", True, f"Response time: {response_time:.2f}s")
            return True
        else:
            status = "slow" if response_time >= 5.0 else f"HTTP {response.status_code}"
            print_result("API Performance", False, f"Response time: {response_time:.2f}s ({status})")
            return False
            
    except Exception as e:
        print_result("API Performance", False, f"Error: {e}")
        return False

def test_error_handling() -> bool:
    """Test error handling for invalid inputs"""
    try:
        # Test invalid barcode
        response = requests.post(
            f"{API_BASE}/api/v1/products/scan",
            json={"barcode": ""},  # Empty barcode
            timeout=10
        )
        
        # Should handle gracefully, not crash
        handles_empty = response.status_code in [200, 400, 422]
        
        # Test malformed request
        response2 = requests.post(
            f"{API_BASE}/api/v1/products/scan",
            json={"invalid_field": "test"},
            timeout=10
        )
        
        handles_malformed = response2.status_code in [200, 400, 422]
        
        if handles_empty and handles_malformed:
            print_result("Error Handling", True, "Gracefully handles invalid inputs")
            return True
        else:
            print_result("Error Handling", False, "Does not handle invalid inputs properly")
            return False
            
    except Exception as e:
        print_result("Error Handling", False, f"Error: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("🚀 CarbonScope Enhanced API Test Suite")
    print("=" * 50)
    
    test_functions = [
        ("Health Check", test_health_check),
        ("Enhanced Barcode - Coca-Cola", lambda: test_enhanced_barcode_scan("1234567890123", "Coca-Cola")),
        ("Enhanced Barcode - iPhone", lambda: test_enhanced_barcode_scan("7890123456789", "iPhone")),
        ("Enhanced Barcode - Bananas", lambda: test_enhanced_barcode_scan("5432109876543", "Bananas")),
        ("Purchase Context Effects", test_purchase_context_effects),
        ("Confidence Scoring", test_confidence_scoring),
        ("API Performance", test_api_performance),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_name, test_func in test_functions:
        print_header(test_name)
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print_result(test_name, False, f"Unexpected error: {e}")
    
    print_header("FINAL RESULTS")
    print(f"📊 Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your enhanced API is working perfectly.")
        print("\n💡 What's working:")
        print("   ✅ Smart carbon calculation with multiple factors")
        print("   ✅ Purchase context awareness")
        print("   ✅ Confidence scoring")
        print("   ✅ Enhanced alternatives with savings")
        print("   ✅ Proper error handling")
        print("   ✅ Good performance")
        print("\n🚀 Ready for frontend testing and computer vision!")
    else:
        print(f"❌ {total - passed} tests failed. Check the issues above.")
        if passed >= total * 0.7:
            print("   Most features working - minor issues to fix")
        else:
            print("   Major issues detected - check backend setup")
        sys.exit(1)

if __name__ == "__main__":
    main()
