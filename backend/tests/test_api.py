import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct response"""
    response = client.get("/")
    assert response.status_code == 200
    assert "CarbonScope API" in response.json()["message"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_scan_product():
    """Test product scanning endpoint"""
    test_data = {
        "barcode": "1234567890123",
        "user_location": "test_location"
    }
    
    response = client.post("/api/v1/products/scan", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "scan_id" in data
    assert "carbon_estimate" in data
    assert data["carbon_estimate"]["total_co2_kg"] > 0

def test_upload_image():
    """Test image upload endpoint"""
    # Create a dummy image file
    from io import BytesIO
    import tempfile
    
    dummy_content = b"fake image content"
    
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(dummy_content)
        tmp.seek(0)
        
        response = client.post(
            "/api/v1/products/upload-image",
            files={"file": ("test.jpg", dummy_content, "image/jpeg")}
        )
    
    assert response.status_code == 200
    assert "Image uploaded successfully" in response.json()["message"]
