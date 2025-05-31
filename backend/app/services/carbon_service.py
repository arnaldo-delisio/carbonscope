"""
Advanced carbon calculation engine with real-world factors and supply chain modeling
"""

import math
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class CarbonCalculationEngine:
    """Advanced carbon footprint calculation with real-world factors"""
    
    def __init__(self):
        # Material carbon intensities (kg CO2e per kg) - based on IPCC data
        self.material_factors = {
            "aluminum": 11.5,
            "plastic": 3.4,
            "plastic_pet": 3.4,
            "plastic_hdpe": 2.1,
            "glass": 0.9,
            "steel": 2.3,
            "cardboard": 1.1,
            "paper": 1.3,
            "cotton": 5.9,
            "polyester": 9.5,
            "recycled_polyester": 4.2,
            "rare_earth_metals": 25.0,
            "lithium": 15.0,
            "organic_matter": 0.3,
            "unknown": 5.0
        }
        
        # Category base factors (kg CO2e per unit)
        self.category_factors = {
            "beverages": 0.8,
            "food": 2.0,
            "electronics": 15.0,
            "clothing": 8.0,
            "household": 3.5,
            "general": 3.0
        }
        
        # Transport factors by origin (multiplier)
        self.transport_factors = {
            "USA": 1.0,
            "Canada": 1.1,
            "Mexico": 1.2,
            "China": 1.8,
            "South Korea": 1.7,
            "Japan": 1.6,
            "Germany": 1.3,
            "France": 1.3,
            "UK": 1.2,
            "Vietnam": 1.9,
            "Bangladesh": 2.0,
            "India": 1.8,
            "Ecuador": 1.5,
            "Brazil": 1.6,
            "Unknown": 1.5
        }
        
        # Seasonal factors (month-based multipliers)
        self.seasonal_factors = self._calculate_seasonal_factors()
    
    def _calculate_seasonal_factors(self) -> Dict[int, float]:
        """Calculate seasonal transport factors"""
        # Higher emissions in winter due to heating, storms affecting shipping
        return {
            1: 1.2,   # January - winter storms
            2: 1.15,  # February
            3: 1.05,  # March
            4: 1.0,   # April - baseline
            5: 1.0,   # May
            6: 1.1,   # June - hurricane season begins
            7: 1.15,  # July - peak summer, more energy for cooling
            8: 1.15,  # August
            9: 1.1,   # September
            10: 1.05, # October
            11: 1.1,  # November
            12: 1.2   # December - holiday shipping surge
        }
    
    async def calculate_footprint(
        self,
        product_info: Dict,
        location: Optional[str] = None,
        context: Optional[str] = None
    ) -> Dict:
        """Calculate comprehensive carbon footprint"""
        
        try:
            # Base calculations
            production_co2 = await self._calculate_production_emissions(product_info)
            transport_co2 = await self._calculate_transport_emissions(product_info, location)
            packaging_co2 = await self._calculate_packaging_emissions(product_info)
            usage_co2 = await self._calculate_usage_emissions(product_info)
            
            # Apply contextual factors
            context_multiplier = self._get_context_multiplier(context)
            seasonal_multiplier = self._get_seasonal_multiplier()
            
            # Total calculation
            base_total = production_co2 + transport_co2 + packaging_co2 + usage_co2
            total_co2 = base_total * context_multiplier * seasonal_multiplier
            
            # Confidence calculation
            confidence = self._calculate_confidence(product_info)
            
            # Impact classification
            impact_level = self._classify_impact(total_co2)
            
            return {
                "total_co2_kg": round(total_co2, 3),
                "production_co2_kg": round(production_co2 * context_multiplier, 3),
                "transport_co2_kg": round(transport_co2 * seasonal_multiplier, 3),
                "packaging_co2_kg": round(packaging_co2, 3),
                "usage_co2_kg": round(usage_co2, 3),
                "confidence_score": confidence,
                "impact_level": impact_level,
                "methodology": "Enhanced Multi-Factor Analysis",
                "factors_applied": {
                    "context_multiplier": context_multiplier,
                    "seasonal_multiplier": seasonal_multiplier,
                    "verified_data": product_info.get("verified", False)
                }
            }
            
        except Exception as e:
            logger.error(f"Carbon calculation error: {e}")
            # Fallback calculation
            return await self._fallback_calculation(product_info)
    
    async def _calculate_production_emissions(self, product_info: Dict) -> float:
        """Calculate production-phase emissions"""
        
        category = product_info.get("category", "general")
        materials = product_info.get("materials", ["unknown"])
        weight_kg = product_info.get("weight_grams", 100) / 1000
        
        # Method 1: Category-based calculation
        category_co2 = self.category_factors.get(category, 3.0)
        
        # Method 2: Material-based calculation
        material_co2 = 0
        for material in materials:
            material_intensity = self.material_factors.get(material, 5.0)
            material_co2 += material_intensity * (weight_kg / len(materials))
        
        # Method 3: Use custom factors if available
        custom_factors = product_info.get("carbon_factors", {})
        if "production" in custom_factors:
            custom_co2 = custom_factors["production"]
            # Weighted average of all methods
            production_co2 = (category_co2 + material_co2 + custom_co2) / 3
        else:
            # Use max of category and material methods
            production_co2 = max(category_co2, material_co2)
        
        return production_co2
    
    async def _calculate_transport_emissions(self, product_info: Dict, location: Optional[str]) -> float:
        """Calculate transport emissions with route optimization"""
        
        origin = product_info.get("country_origin", "Unknown")
        transport_multiplier = self.transport_factors.get(origin, 1.5)
        
        # Base transport emissions (typically 20-30% of production)
        production_estimate = await self._calculate_production_emissions(product_info)
        base_transport = production_estimate * 0.25
        
        # Apply distance multiplier
        transport_co2 = base_transport * transport_multiplier
        
        # Local products get bonus reduction
        if location and any(term in location.lower() for term in ["local", "same", "nearby"]):
            transport_co2 *= 0.3  # 70% reduction for local
        
        return transport_co2
    
    async def _calculate_packaging_emissions(self, product_info: Dict) -> float:
        """Calculate packaging emissions"""
        
        materials = product_info.get("materials", ["unknown"])
        weight_kg = product_info.get("weight_grams", 100) / 1000
        
        # Packaging typically 5-15% of total product weight
        packaging_weight = weight_kg * 0.1
        
        packaging_co2 = 0
        for material in materials:
            if material in ["cardboard", "plastic", "aluminum", "glass"]:
                material_intensity = self.material_factors.get(material, 3.0)
                packaging_co2 += material_intensity * (packaging_weight / len(materials))
        
        return max(packaging_co2, 0.05)  # Minimum packaging impact
    
    async def _calculate_usage_emissions(self, product_info: Dict) -> float:
        """Calculate usage-phase emissions (important for electronics)"""
        
        category = product_info.get("category", "general")
        
        if category == "electronics":
            # Electronics have significant usage emissions
            weight_kg = product_info.get("weight_grams", 100) / 1000
            # Estimate based on device size/power consumption
            return weight_kg * 2.0  # Simplified usage factor
        
        # Other products have minimal usage emissions
        return 0.0
    
    def _get_context_multiplier(self, context: Optional[str]) -> float:
        """Get multiplier based on purchase context"""
        
        if not context:
            return 1.0
        
        context_factors = {
            "express_shipping": 1.5,
            "overnight_shipping": 2.0,
            "same_day_delivery": 3.0,
            "retail_store": 0.9,
            "online": 1.1,
            "bulk_purchase": 0.8,
            "subscription": 0.85
        }
        
        return context_factors.get(context, 1.0)
    
    def _get_seasonal_multiplier(self) -> float:
        """Get current seasonal multiplier"""
        current_month = datetime.now().month
        return self.seasonal_factors.get(current_month, 1.0)
    
    def _calculate_confidence(self, product_info: Dict) -> float:
        """Calculate confidence score for the estimate"""
        
        confidence = 0.5  # Base confidence
        
        # Boost confidence for verified products
        if product_info.get("verified", False):
            confidence += 0.3
        
        # Boost for known brands/products
        if not product_info.get("name", "").startswith("Product"):
            confidence += 0.2
        
        # Boost for detailed material information
        materials = product_info.get("materials", [])
        if len(materials) > 1 and "unknown" not in materials:
            confidence += 0.1
        
        # Boost for custom carbon factors
        if "carbon_factors" in product_info:
            confidence += 0.1
        
        return min(confidence, 0.95)  # Cap at 95%
    
    def _classify_impact(self, total_co2: float) -> str:
        """Classify environmental impact level"""
        
        if total_co2 < 1.0:
            return "Low"
        elif total_co2 < 5.0:
            return "Medium"
        elif total_co2 < 15.0:
            return "High"
        else:
            return "Very High"
    
    async def _fallback_calculation(self, product_info: Dict) -> Dict:
        """Fallback calculation if main method fails"""
        
        category = product_info.get("category", "general")
        base_co2 = self.category_factors.get(category, 3.0)
        
        return {
            "total_co2_kg": base_co2,
            "production_co2_kg": base_co2 * 0.6,
            "transport_co2_kg": base_co2 * 0.3,
            "packaging_co2_kg": base_co2 * 0.1,
            "usage_co2_kg": 0.0,
            "confidence_score": 0.3,
            "impact_level": self._classify_impact(base_co2),
            "methodology": "Fallback Category-Based",
            "factors_applied": {"fallback": True}
        }

# Global instance
carbon_engine = CarbonCalculationEngine()

async def calculate_carbon_estimate(
    product_info: dict,
    location: Optional[str] = None,
    context: Optional[str] = None
) -> Dict:
    """Enhanced carbon estimation function"""
    return await carbon_engine.calculate_footprint(product_info, location, context)
