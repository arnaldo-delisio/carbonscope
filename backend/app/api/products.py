from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

router = APIRouter()

class ProductScanRequest(BaseModel):
    barcode: Optional[str] = None
    image_base64: Optional[str] = None
    user_location: Optional[str] = None
    purchase_context: Optional[str] = None  # e.g., "grocery_store", "online"

class CarbonEstimate(BaseModel):
    total_co2_kg: float
    production_co2_kg: float
    transport_co2_kg: float
    packaging_co2_kg: float
    confidence_score: float
    methodology: str

class ProductAnalysis(BaseModel):
    scan_id: str
    product_name: Optional[str]
    barcode: Optional[str]
    materials_detected: List[str]
    carbon_estimate: CarbonEstimate
    alternatives: List[dict]
    timestamp: datetime

@router.post("/scan", response_model=ProductAnalysis)
async def scan_product(request: ProductScanRequest):
    """
    Analyze a product's carbon footprint using AI-powered estimation:
    - Barcode scanning for product identification
    - Computer vision analysis for material detection
    - Real-time supply chain modeling
    - Dynamic carbon calculation
    """
    # Generate unique scan ID
    scan_id = str(uuid.uuid4())
    
    # Basic product lookup from barcode (mock for now)
    product_info = await lookup_product_by_barcode(request.barcode)
    
    # Estimate carbon footprint based on available data
    carbon_estimate = await calculate_carbon_estimate(
        product_info=product_info,
        location=request.user_location,
        context=request.purchase_context
    )
    
    # Detect materials if image provided
    materials = []
    if request.image_base64:
        materials = await detect_materials_from_image(request.image_base64)
    
    # Find alternatives
    alternatives = await find_alternatives(product_info, carbon_estimate.total_co2_kg)
    
    analysis = ProductAnalysis(
        scan_id=scan_id,
        product_name=product_info.get("name", "Unknown Product"),
        barcode=request.barcode,
        materials_detected=materials,
        carbon_estimate=carbon_estimate,
        alternatives=alternatives,
        timestamp=datetime.now()
    )
    
    return analysis

@router.post("/upload-image")
async def upload_product_image(file: UploadFile = File(...)):
    """
    Upload and analyze product image for material composition
    """
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid image format")
    
    # TODO: Implement computer vision analysis
    
    return {
        "message": "Image uploaded successfully",
        "filename": file.filename,
        "analysis_status": "pending"
    }

@router.get("/history")
async def get_scan_history(limit: int = 10):
    """
    Get user's scan history
    """
    # TODO: Implement database query
    return {"scans": [], "total": 0}

# Helper functions for product analysis

async def lookup_product_by_barcode(barcode: Optional[str]) -> dict:
    """
    Look up product information by barcode
    Currently uses mock data, will integrate with real APIs later
    """
    if not barcode:
        return {"name": "Unknown Product", "category": "general"}
    
    # Mock product database - replace with real API calls
    mock_products = {
        "1234567890123": {
            "name": "Coca-Cola 330ml Can",
            "brand": "Coca-Cola",
            "category": "beverages",
            "weight_grams": 375,
            "materials": ["aluminum", "plastic"],
            "country_origin": "USA"
        },
        "7890123456789": {
            "name": "iPhone 15 Pro",
            "brand": "Apple", 
            "category": "electronics",
            "weight_grams": 187,
            "materials": ["aluminum", "glass", "rare_earth_metals"],
            "country_origin": "China"
        }
    }
    
    return mock_products.get(barcode, {
        "name": f"Product {barcode[:8]}...",
        "category": "general",
        "weight_grams": 100,
        "materials": ["unknown"],
        "country_origin": "unknown"
    })

async def calculate_carbon_estimate(
    product_info: dict, 
    location: Optional[str] = None,
    context: Optional[str] = None
) -> CarbonEstimate:
    """
    Calculate carbon footprint estimate based on product information
    """
    # Base carbon factors (kg CO2e per unit)
    category_factors = {
        "beverages": 0.8,
        "electronics": 15.0,
        "food": 2.0,
        "clothing": 8.0,
        "general": 3.0
    }
    
    # Material carbon intensity (kg CO2e per kg)
    material_factors = {
        "aluminum": 11.5,
        "plastic": 3.4,
        "glass": 0.9,
        "cardboard": 1.1,
        "rare_earth_metals": 25.0,
        "unknown": 5.0
    }
    
    # Base calculation
    category = product_info.get("category", "general")
    base_co2 = category_factors.get(category, 3.0)
    
    # Add material-based calculation
    materials = product_info.get("materials", ["unknown"])
    weight_kg = product_info.get("weight_grams", 100) / 1000
    
    material_co2 = sum(
        material_factors.get(material, 5.0) * (weight_kg / len(materials))
        for material in materials
    )
    
    # Production footprint (60% of total)
    production_co2 = max(base_co2, material_co2) * 0.6
    
    # Transport footprint based on origin
    transport_multiplier = {
        "USA": 1.0,
        "China": 1.5,
        "Europe": 1.2,
        "unknown": 1.3
    }
    origin = product_info.get("country_origin", "unknown")
    transport_co2 = production_co2 * 0.3 * transport_multiplier.get(origin, 1.3)
    
    # Packaging (10% of total)
    packaging_co2 = production_co2 * 0.1
    
    total_co2 = production_co2 + transport_co2 + packaging_co2
    
    # Confidence score based on data availability
    confidence = 0.5  # Base confidence
    if product_info.get("name", "").startswith("Product"):
        confidence = 0.3  # Lower for unknown products
    else:
        confidence = 0.8  # Higher for known products
    
    return CarbonEstimate(
        total_co2_kg=round(total_co2, 2),
        production_co2_kg=round(production_co2, 2),
        transport_co2_kg=round(transport_co2, 2),
        packaging_co2_kg=round(packaging_co2, 2),
        confidence_score=confidence,
        methodology="Basic Category + Material Analysis"
    )

async def detect_materials_from_image(image_base64: str) -> List[str]:
    """
    Detect materials from product image
    Currently returns mock data, will implement computer vision later
    """
    # Mock material detection - replace with actual CV model
    import random
    
    possible_materials = [
        "plastic_pet", "aluminum", "cardboard", "glass", 
        "plastic_hdpe", "paper", "steel"
    ]
    
    # Return 1-3 random materials for now
    num_materials = random.randint(1, 3)
    return random.sample(possible_materials, num_materials)

async def find_alternatives(product_info: dict, current_co2: float) -> List[dict]:
    """
    Find lower-carbon alternatives to the scanned product
    """
    category = product_info.get("category", "general")
    
    # Mock alternatives based on category
    alternatives_db = {
        "beverages": [
            {"name": "Local Brand Alternative", "co2_reduction": 0.3, "reason": "Shorter transport distance"},
            {"name": "Glass Bottle Version", "co2_reduction": 0.2, "reason": "Recyclable packaging"},
        ],
        "electronics": [
            {"name": "Refurbished Option", "co2_reduction": 0.7, "reason": "No new manufacturing"},
            {"name": "Energy Efficient Model", "co2_reduction": 0.2, "reason": "Lower lifetime energy use"},
        ],
        "general": [
            {"name": "Local Alternative", "co2_reduction": 0.25, "reason": "Reduced shipping"},
        ]
    }
    
    base_alternatives = alternatives_db.get(category, alternatives_db["general"])
    
    # Calculate actual CO2 values
    alternatives = []
    for alt in base_alternatives:
        new_co2 = current_co2 * (1 - alt["co2_reduction"])
        alternatives.append({
            "name": alt["name"],
            "co2_kg": round(new_co2, 2),
            "co2_reduction": alt["co2_reduction"],
            "reason": alt["reason"],
            "savings_kg": round(current_co2 - new_co2, 2)
        })
    
    return alternatives
