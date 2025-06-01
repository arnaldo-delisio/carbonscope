"""
Product and carbon footprint models
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import uuid

class Product(Base):
    """
    Product information model
    """
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    barcode = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    brand = Column(String)
    category = Column(String, nullable=False)
    
    # Physical properties
    weight_grams = Column(Integer)
    dimensions = Column(JSON)  # {"length": x, "width": y, "height": z}
    
    # Origin and manufacturing
    country_origin = Column(String)
    manufacturer = Column(String)
    manufacturing_process = Column(String)
    
    # Materials
    materials = Column(JSON)  # List of material types
    material_composition = Column(JSON)  # Detailed composition percentages
    
    # Carbon data
    production_co2_kg = Column(Float)
    transport_co2_kg = Column(Float)
    packaging_co2_kg = Column(Float)
    usage_co2_kg = Column(Float)
    total_co2_kg = Column(Float)
    
    # Metadata
    verified = Column(Boolean, default=False)
    verification_count = Column(Integer, default=0)
    data_source = Column(String)  # "manual", "api", "community"
    confidence_score = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    scans = relationship("ProductScan", back_populates="product")
    verifications = relationship("CommunityVerification", back_populates="product")

class ProductScan(Base):
    """
    Individual product scan records
    """
    __tablename__ = "product_scans"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Product reference
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    barcode = Column(String, nullable=False, index=True)
    
    # Scan context
    user_id = Column(String, index=True)  # Anonymous user tracking
    user_location = Column(String)
    purchase_context = Column(String)  # "retail_store", "online", etc.
    scan_method = Column(String)  # "barcode", "image", "manual"
    
    # Analysis results
    materials_detected = Column(JSON)  # Materials found via CV
    carbon_estimate = Column(JSON)  # Full carbon breakdown
    alternatives_suggested = Column(JSON)  # Alternative products
    
    # Image data (if applicable)
    image_analysis = Column(JSON)  # CV analysis results
    image_hash = Column(String)  # For deduplication
    
    # Timestamps
    scanned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="scans")

class MaterialType(Base):
    """
    Material types and their carbon intensities
    """
    __tablename__ = "material_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)  # "plastic", "metal", "organic", etc.
    
    # Carbon properties
    carbon_intensity_kg_per_kg = Column(Float, nullable=False)
    production_method = Column(String)
    recyclable = Column(Boolean, default=False)
    biodegradable = Column(Boolean, default=False)
    
    # Physical properties
    density_kg_per_m3 = Column(Float)
    melting_point_celsius = Column(Float)
    
    # Metadata
    data_source = Column(String)
    verified = Column(Boolean, default=False)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

class CarbonFootprintCache(Base):
    """
    Cache for carbon footprint calculations
    """
    __tablename__ = "carbon_footprint_cache"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Cache key components
    product_category = Column(String, nullable=False)
    materials_hash = Column(String, nullable=False)  # Hash of materials list
    country_origin = Column(String)
    context_hash = Column(String)  # Hash of purchase context
    
    # Cached results
    production_co2_kg = Column(Float, nullable=False)
    transport_co2_kg = Column(Float, nullable=False)
    packaging_co2_kg = Column(Float, nullable=False)
    usage_co2_kg = Column(Float, default=0.0)
    total_co2_kg = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    
    # Cache metadata
    calculation_method = Column(String, nullable=False)
    factors_applied = Column(JSON)
    hit_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))

class ProductAlternative(Base):
    """
    Lower-carbon alternatives for products
    """
    __tablename__ = "product_alternatives"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Original product
    original_product_id = Column(String, ForeignKey("products.id"))
    original_category = Column(String, nullable=False)
    
    # Alternative product
    alternative_name = Column(String, nullable=False)
    alternative_brand = Column(String)
    alternative_barcode = Column(String)
    
    # Comparison data
    co2_reduction_kg = Column(Float, nullable=False)
    co2_reduction_percentage = Column(Float, nullable=False)
    reason = Column(Text, nullable=False)
    availability = Column(String)
    
    # Quality metrics
    similarity_score = Column(Float)  # How similar to original
    popularity_score = Column(Float)  # How often suggested
    success_rate = Column(Float)  # How often users choose this
    
    # Metadata
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())