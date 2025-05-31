"""
Enhanced product database with more realistic data and external API integration preparation
"""

import httpx
import json
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

class ProductDatabase:
    """Enhanced product database with real-world data"""
    
    def __init__(self):
        self.local_products = {
            # Food & Beverages
            "0123456789012": {
                "name": "Coca-Cola Classic 330ml Can",
                "brand": "Coca-Cola",
                "category": "beverages",
                "weight_grams": 375,
                "materials": ["aluminum", "plastic"],
                "country_origin": "USA",
                "verified": True,
                "carbon_factors": {"production": 0.8, "transport": 1.2}
            },
            "1234567890123": {
                "name": "Coca-Cola Classic 330ml Can", 
                "brand": "Coca-Cola",
                "category": "beverages",
                "weight_grams": 375,
                "materials": ["aluminum", "plastic"],
                "country_origin": "USA",
                "verified": True,
                "carbon_factors": {"production": 0.8, "transport": 1.2}
            },
            "7890123456789": {
                "name": "iPhone 15 Pro 128GB",
                "brand": "Apple",
                "category": "electronics",
                "weight_grams": 187,
                "materials": ["aluminum", "glass", "rare_earth_metals", "lithium"],
                "country_origin": "China",
                "verified": True,
                "carbon_factors": {"production": 18.0, "transport": 2.5}
            },
            "5432109876543": {
                "name": "Organic Bananas 1kg",
                "brand": "Local Farm",
                "category": "food",
                "weight_grams": 1000,
                "materials": ["organic_matter", "plastic"],
                "country_origin": "Ecuador",
                "verified": True,
                "carbon_factors": {"production": 0.7, "transport": 0.5}
            },
            "9876543210987": {
                "name": "Samsung Galaxy S24 Ultra",
                "brand": "Samsung",
                "category": "electronics", 
                "weight_grams": 232,
                "materials": ["aluminum", "glass", "rare_earth_metals", "lithium"],
                "country_origin": "South Korea",
                "verified": True,
                "carbon_factors": {"production": 16.5, "transport": 2.2}
            },
            "1122334455667": {
                "name": "Patagonia Better Sweater Jacket",
                "brand": "Patagonia",
                "category": "clothing",
                "weight_grams": 680,
                "materials": ["recycled_polyester", "polyester"],
                "country_origin": "Vietnam",
                "verified": True,
                "carbon_factors": {"production": 12.0, "transport": 1.8}
            }
        }
    
    async def lookup_product(self, barcode: str) -> Dict:
        """Look up product with enhanced data"""
        
        # Check local database first
        if barcode in self.local_products:
            return self.local_products[barcode]
        
        # Try external APIs (OpenFoodFacts, UPC Database, etc.)
        external_product = await self._try_external_apis(barcode)
        if external_product:
            return external_product
        
        # Generate intelligent mock data based on barcode patterns
        return self._generate_mock_product(barcode)
    
    async def _try_external_apis(self, barcode: str) -> Optional[Dict]:
        """Try external product APIs (OpenFoodFacts, etc.)"""
        try:
            # OpenFoodFacts API
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json",
                    timeout=3.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status") == 1:
                        product = data.get("product", {})
                        
                        return {
                            "name": product.get("product_name", f"Product {barcode[:8]}..."),
                            "brand": product.get("brands", "Unknown Brand"),
                            "category": self._map_category(product.get("categories", "")),
                            "weight_grams": self._extract_weight(product),
                            "materials": self._guess_materials_from_packaging(product),
                            "country_origin": product.get("countries", "Unknown"),
                            "verified": False,
                            "source": "OpenFoodFacts"
                        }
                        
        except Exception as e:
            logger.warning(f"External API failed for {barcode}: {e}")
        
        return None
    
    def _generate_mock_product(self, barcode: str) -> Dict:
        """Generate intelligent mock product based on barcode patterns"""
        
        # Use barcode patterns to guess product type
        first_digit = barcode[0] if barcode else "0"
        
        category_mapping = {
            "0": "food",
            "1": "beverages", 
            "2": "food",
            "3": "electronics",
            "4": "clothing",
            "5": "food",
            "6": "beverages",
            "7": "electronics",
            "8": "household",
            "9": "electronics"
        }
        
        category = category_mapping.get(first_digit, "general")
        
        base_products = {
            "food": {
                "name": f"Food Product {barcode[:8]}...",
                "weight_grams": 250,
                "materials": ["cardboard", "plastic"],
                "country_origin": "USA"
            },
            "beverages": {
                "name": f"Beverage {barcode[:8]}...",
                "weight_grams": 350,
                "materials": ["plastic", "aluminum"],
                "country_origin": "USA"
            },
            "electronics": {
                "name": f"Electronic Device {barcode[:8]}...",
                "weight_grams": 200,
                "materials": ["plastic", "metal", "rare_earth_metals"],
                "country_origin": "China"
            },
            "clothing": {
                "name": f"Clothing Item {barcode[:8]}...",
                "weight_grams": 300,
                "materials": ["cotton", "polyester"],
                "country_origin": "Bangladesh"
            }
        }
        
        base = base_products.get(category, base_products["food"])
        
        return {
            **base,
            "brand": "Unknown Brand",
            "category": category,
            "verified": False,
            "source": "generated"
        }
    
    def _map_category(self, categories_str: str) -> str:
        """Map OpenFoodFacts categories to our categories"""
        categories = categories_str.lower()
        
        if any(word in categories for word in ["beverage", "drink", "soda", "water"]):
            return "beverages"
        elif any(word in categories for word in ["snack", "food", "meal"]):
            return "food"
        else:
            return "food"
    
    def _extract_weight(self, product: Dict) -> int:
        """Extract weight from product data"""
        # Try multiple fields
        for field in ["quantity", "net_weight", "serving_quantity"]:
            if field in product:
                weight_str = str(product[field])
                # Extract numbers
                import re
                numbers = re.findall(r'\d+', weight_str)
                if numbers:
                    return int(numbers[0])
        
        return 100  # Default weight
    
    def _guess_materials_from_packaging(self, product: Dict) -> List[str]:
        """Guess materials from packaging information"""
        packaging = str(product.get("packaging", "")).lower()
        materials = []
        
        if "plastic" in packaging or "bottle" in packaging:
            materials.append("plastic")
        if "aluminum" in packaging or "can" in packaging:
            materials.append("aluminum")
        if "glass" in packaging:
            materials.append("glass")
        if "cardboard" in packaging or "box" in packaging:
            materials.append("cardboard")
        
        return materials if materials else ["unknown"]

# Global instance
product_db = ProductDatabase()

async def lookup_product_by_barcode(barcode: Optional[str]) -> dict:
    """Enhanced product lookup function"""
    if not barcode:
        return {"name": "Unknown Product", "category": "general"}
    
    return await product_db.lookup_product(barcode)
