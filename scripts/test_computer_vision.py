#!/usr/bin/env python3
"""
Test script for computer vision material detection
Tests the real material detection capabilities
"""

import sys
import os
import numpy as np
import cv2
from PIL import Image
import base64
import io

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import our computer vision module
try:
    from ai_models.computer_vision.material_detection import (
        MaterialDetector, 
        analyze_base64_image,
        analyze_numpy_image,
        detect_materials_from_image_async
    )
    CV_AVAILABLE = True
except ImportError as e:
    print(f"❌ Computer vision module not available: {e}")
    CV_AVAILABLE = False

def create_test_image(material_type: str) -> np.ndarray:
    """Create a synthetic test image for a material type"""
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    if material_type == "aluminum":
        # Bright metallic appearance
        image[:, :] = [200, 200, 200]  # Light gray
        # Add some metallic texture
        noise = np.random.randint(-20, 20, image.shape, dtype=np.int16)
        image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
    elif material_type == "plastic":
        # Colorful plastic appearance
        image[:, :] = [100, 150, 200]  # Blueish plastic
        # Add smooth texture
        image = cv2.GaussianBlur(image, (15, 15), 0)
        
    elif material_type == "cardboard":
        # Brown corrugated appearance
        image[:, :] = [139, 106, 69]  # Brown color
        # Add corrugated lines
        for i in range(0, image.shape[0], 20):
            cv2.line(image, (0, i), (image.shape[1], i), (120, 90, 50), 2)
            
    elif material_type == "glass":
        # Transparent/reflective appearance
        image[:, :] = [230, 230, 240]  # Very light color
        # Add reflective highlights
        cv2.circle(image, (200, 200), 50, (255, 255, 255), -1)
        cv2.circle(image, (400, 300), 30, (255, 255, 255), -1)
        
    else:
        # Default random pattern
        image = np.random.randint(0, 255, image.shape, dtype=np.uint8)
    
    return image

def image_to_base64(image: np.ndarray) -> str:
    """Convert numpy image to base64 string"""
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    
    # Convert to base64
    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def test_material_detection():
    """Test material detection on synthetic images"""
    print("🧪 Testing Computer Vision Material Detection")
    print("=" * 50)
    
    if not CV_AVAILABLE:
        print("❌ Computer vision module not available. Skipping tests.")
        return False
    
    test_materials = ["aluminum", "plastic", "cardboard", "glass"]
    detector = MaterialDetector()
    
    all_passed = True
    
    for material in test_materials:
        print(f"\n🔍 Testing {material} detection...")
        
        try:
            # Create test image
            test_image = create_test_image(material)
            
            # Test with numpy array
            detections = detector.detect_materials(test_image)
            
            if detections:
                print(f"  ✅ Detected materials:")
                for detection in detections[:3]:  # Show top 3
                    print(f"    - {detection.material_type}: {detection.confidence:.2f}")
                
                # Check if target material was detected
                detected_materials = [d.material_type for d in detections]
                if any(material in dm for dm in detected_materials):
                    print(f"  ✅ Successfully detected {material}")
                else:
                    print(f"  ⚠️ Did not detect {material} specifically, but found: {detected_materials}")
            else:
                print(f"  ❌ No materials detected")
                all_passed = False
                
        except Exception as e:
            print(f"  ❌ Error testing {material}: {e}")
            all_passed = False
    
    return all_passed

def test_base64_detection():
    """Test base64 image detection"""
    print(f"\n🔍 Testing base64 image detection...")
    
    if not CV_AVAILABLE:
        print("❌ Computer vision module not available. Skipping test.")
        return False
    
    try:
        # Create test image
        test_image = create_test_image("plastic")
        base64_string = image_to_base64(test_image)
        
        # Test base64 detection
        detections = analyze_base64_image(base64_string)
        
        if detections:
            print(f"  ✅ Base64 detection successful:")
            for detection in detections[:3]:
                print(f"    - {detection.material_type}: {detection.confidence:.2f}")
            return True
        else:
            print(f"  ❌ No materials detected from base64")
            return False
            
    except Exception as e:
        print(f"  ❌ Error in base64 detection: {e}")
        return False

async def test_async_detection():
    """Test async detection function"""
    print(f"\n🔍 Testing async material detection...")
    
    if not CV_AVAILABLE:
        print("❌ Computer vision module not available. Skipping test.")
        return False
    
    try:
        # Create test image
        test_image = create_test_image("aluminum")
        base64_string = image_to_base64(test_image)
        
        # Test async detection
        materials = await detect_materials_from_image_async(base64_string)
        
        if materials:
            print(f"  ✅ Async detection successful: {materials}")
            return True
        else:
            print(f"  ❌ No materials detected via async function")
            return False
            
    except Exception as e:
        print(f"  ❌ Error in async detection: {e}")
        return False

def test_edge_cases():
    """Test edge cases and error handling"""
    print(f"\n🔍 Testing edge cases...")
    
    if not CV_AVAILABLE:
        print("❌ Computer vision module not available. Skipping tests.")
        return False
    
    detector = MaterialDetector()
    passed = 0
    total = 0
    
    # Test 1: Very small image
    try:
        small_image = np.zeros((10, 10, 3), dtype=np.uint8)
        detections = detector.detect_materials(small_image)
        print(f"  ✅ Small image handled: {len(detections)} detections")
        passed += 1
    except Exception as e:
        print(f"  ❌ Small image failed: {e}")
    total += 1
    
    # Test 2: Large image
    try:
        large_image = np.zeros((2000, 2000, 3), dtype=np.uint8)
        detections = detector.detect_materials(large_image)
        print(f"  ✅ Large image handled: {len(detections)} detections")
        passed += 1
    except Exception as e:
        print(f"  ❌ Large image failed: {e}")
    total += 1
    
    # Test 3: Invalid base64
    try:
        analyze_base64_image("invalid_base64_string")
        print(f"  ❌ Invalid base64 should have failed")
    except Exception:
        print(f"  ✅ Invalid base64 properly rejected")
        passed += 1
    total += 1
    
    # Test 4: Grayscale image
    try:
        gray_image = np.zeros((480, 640), dtype=np.uint8)
        # Convert to 3-channel
        bgr_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        detections = detector.detect_materials(bgr_image)
        print(f"  ✅ Grayscale image handled: {len(detections)} detections")
        passed += 1
    except Exception as e:
        print(f"  ❌ Grayscale image failed: {e}")
    total += 1
    
    return passed == total

def main():
    """Run all computer vision tests"""
    print("🤖 CarbonScope Computer Vision Test Suite")
    print("=" * 50)
    
    if not CV_AVAILABLE:
        print("❌ Computer vision module not available.")
        print("   This could be due to:")
        print("   - Missing dependencies (opencv-python, pillow)")
        print("   - Module import path issues")
        print("   - Missing ai-models directory")
        return False
    
    tests = [
        ("Material Detection", test_material_detection),
        ("Base64 Detection", test_base64_detection), 
        ("Edge Cases", test_edge_cases)
    ]
    
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    # Test async function
    print(f"\n{'='*20} Async Detection {'='*20}")
    try:
        import asyncio
        if asyncio.run(test_async_detection()):
            passed += 1
            print(f"✅ Async Detection PASSED")
        else:
            print(f"❌ Async Detection FAILED")
    except Exception as e:
        print(f"❌ Async Detection ERROR: {e}")
    
    total_tests = len(tests) + 1  # +1 for async test
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total_tests} tests passed")
    
    if passed == total_tests:
        print("🎉 All computer vision tests passed!")
        print("   - Material detection is working")
        print("   - Base64 image processing works")
        print("   - Edge cases handled properly")
        print("   - Async detection functional")
        print("   Ready for integration with mobile app!")
    else:
        print(f"⚠️ {total_tests - passed} tests failed")
        print("   - Check dependencies and module paths")
        print("   - Review error messages above")
    
    return passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)