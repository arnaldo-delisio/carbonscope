"""
Community verification and contribution models
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import uuid

class User(Base):
    """
    User accounts for community features
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic info (all optional for privacy)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    anonymous_id = Column(String, unique=True, nullable=False)  # For anonymous tracking
    
    # Profile
    display_name = Column(String)
    avatar_url = Column(String)
    bio = Column(Text)
    location = Column(String)  # General location for context
    
    # Community metrics
    verification_count = Column(Integer, default=0)
    contribution_score = Column(Float, default=0.0)
    reputation_score = Column(Float, default=1.0)
    accuracy_rating = Column(Float, default=0.5)
    
    # Preferences
    privacy_level = Column(String, default="anonymous")  # "anonymous", "public", "private"
    notification_preferences = Column(JSON)
    
    # Statistics
    total_scans = Column(Integer, default=0)
    co2_saved_kg = Column(Float, default=0.0)
    alternatives_chosen = Column(Integer, default=0)
    
    # Timestamps
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    verifications = relationship("CommunityVerification", back_populates="user")
    contributions = relationship("CommunityContribution", back_populates="user")

class CommunityVerification(Base):
    """
    Community verification of product carbon data
    """
    __tablename__ = "community_verifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # References
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    scan_id = Column(String, ForeignKey("product_scans.id"))
    
    # Verification data
    verification_type = Column(String, nullable=False)  # "accuracy", "materials", "origin"
    is_accurate = Column(Boolean, nullable=False)
    confidence = Column(Float, nullable=False)  # User's confidence in their verification
    
    # Detailed feedback
    materials_feedback = Column(JSON)  # Corrections to material detection
    carbon_feedback = Column(JSON)    # Corrections to carbon calculations
    alternative_feedback = Column(JSON)  # Feedback on alternatives
    
    # Context
    verification_method = Column(String)  # "visual", "packaging", "research"
    evidence_provided = Column(Text)
    image_evidence = Column(JSON)  # References to evidence images
    
    # Quality metrics
    helpful_votes = Column(Integer, default=0)
    total_votes = Column(Integer, default=0)
    moderator_approved = Column(Boolean)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="verifications")
    product = relationship("Product", back_populates="verifications")

class CommunityContribution(Base):
    """
    Community contributions to the database
    """
    __tablename__ = "community_contributions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # References
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Contribution type
    contribution_type = Column(String, nullable=False)  # "product", "alternative", "correction"
    status = Column(String, default="pending")  # "pending", "approved", "rejected"
    
    # Contribution data
    data = Column(JSON, nullable=False)  # Flexible storage for different contribution types
    original_data = Column(JSON)  # Original data being modified (for corrections)
    
    # Quality assessment
    quality_score = Column(Float)
    community_votes = Column(Integer, default=0)
    moderator_notes = Column(Text)
    
    # Attribution
    credit_given = Column(Boolean, default=True)
    impact_score = Column(Float, default=0.0)  # How much this improved the database
    
    # Timestamps
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True))
    approved_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="contributions")

class CommunityChallenge(Base):
    """
    Community challenges to improve data quality
    """
    __tablename__ = "community_challenges"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Challenge details
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    challenge_type = Column(String, nullable=False)  # "verification", "data_entry", "research"
    
    # Target criteria
    target_category = Column(String)  # Product category to focus on
    target_count = Column(Integer)    # Target number of contributions
    target_quality = Column(Float)    # Target quality score
    
    # Rewards
    reward_type = Column(String)      # "points", "badge", "recognition"
    reward_amount = Column(Float)
    
    # Status
    status = Column(String, default="active")  # "active", "completed", "expired"
    participants_count = Column(Integer, default=0)
    completions_count = Column(Integer, default=0)
    
    # Timestamps
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DataQualityMetric(Base):
    """
    Track data quality metrics over time
    """
    __tablename__ = "data_quality_metrics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Scope
    metric_type = Column(String, nullable=False)  # "accuracy", "completeness", "freshness"
    scope = Column(String, nullable=False)        # "global", "category", "product"
    scope_identifier = Column(String)             # Category name or product ID
    
    # Metric data
    value = Column(Float, nullable=False)
    sample_size = Column(Integer, nullable=False)
    confidence_interval = Column(JSON)  # {"lower": x, "upper": y}
    
    # Context
    measurement_method = Column(String, nullable=False)
    contributing_factors = Column(JSON)
    
    # Timestamps
    measured_at = Column(DateTime(timezone=True), server_default=func.now())
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))