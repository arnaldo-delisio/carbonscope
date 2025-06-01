from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.community import User, CommunityVerification, CommunityContribution
from app.models.product import Product, ProductScan
import uuid

router = APIRouter()

# Request/Response Models
class VerificationRequest(BaseModel):
    scan_id: str
    product_id: str
    verification_type: str = Field(..., regex="^(accuracy|materials|origin|alternatives)$")
    is_accurate: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    materials_feedback: Optional[Dict[str, Any]] = None
    carbon_feedback: Optional[Dict[str, Any]] = None
    alternative_feedback: Optional[Dict[str, Any]] = None
    verification_method: Optional[str] = None
    evidence_provided: Optional[str] = None
    user_id: str

class ContributionRequest(BaseModel):
    contribution_type: str = Field(..., regex="^(product|alternative|correction|material_data)$")
    data: Dict[str, Any]
    original_data: Optional[Dict[str, Any]] = None
    user_id: str

class CommunityInsight(BaseModel):
    product_name: str
    barcode: str
    average_co2: float
    scan_count: int
    verified_scans: int
    community_rating: float
    accuracy_score: float
    last_verified: Optional[datetime] = None
    top_materials: List[str]
    verification_trends: Dict[str, int]

class UserProfile(BaseModel):
    id: str
    display_name: Optional[str]
    verification_count: int
    contribution_score: float
    reputation_score: float
    accuracy_rating: float
    total_scans: int
    co2_saved_kg: float
    joined_at: datetime
    rank: Optional[int] = None

class LeaderboardEntry(BaseModel):
    user: UserProfile
    metric_value: float
    rank: int

# Verification Endpoints
@router.post("/verify")
async def submit_verification(
    verification: VerificationRequest,
    db: Session = Depends(get_db)
):
    """
    Submit community verification of product data
    """
    try:
        # Get or create user
        user = get_or_create_user(verification.user_id, db)
        
        # Verify product and scan exist
        product = db.query(Product).filter(Product.id == verification.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        scan = db.query(ProductScan).filter(ProductScan.id == verification.scan_id).first()
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        
        # Create verification record
        community_verification = CommunityVerification(
            user_id=user.id,
            product_id=verification.product_id,
            scan_id=verification.scan_id,
            verification_type=verification.verification_type,
            is_accurate=verification.is_accurate,
            confidence=verification.confidence,
            materials_feedback=verification.materials_feedback,
            carbon_feedback=verification.carbon_feedback,
            alternative_feedback=verification.alternative_feedback,
            verification_method=verification.verification_method,
            evidence_provided=verification.evidence_provided
        )
        
        db.add(community_verification)
        
        # Update user metrics
        user.verification_count += 1
        user.contribution_score += calculate_verification_score(verification)
        
        # Update product verification metrics
        product.verification_count += 1
        if verification.is_accurate:
            product.confidence_score = min(0.95, product.confidence_score * 1.05)
        else:
            product.confidence_score = max(0.1, product.confidence_score * 0.95)
        
        db.commit()
        
        return {
            "message": "Verification submitted successfully",
            "verification_id": community_verification.id,
            "impact": f"Improved accuracy by {calculate_accuracy_improvement(verification)}%",
            "user_score": user.contribution_score
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit verification: {str(e)}")

@router.post("/contribute")
async def submit_contribution(
    contribution: ContributionRequest,
    db: Session = Depends(get_db)
):
    """
    Submit community contribution to improve database
    """
    try:
        # Get or create user
        user = get_or_create_user(contribution.user_id, db)
        
        # Create contribution record
        community_contribution = CommunityContribution(
            user_id=user.id,
            contribution_type=contribution.contribution_type,
            data=contribution.data,
            original_data=contribution.original_data,
            quality_score=assess_contribution_quality(contribution)
        )
        
        db.add(community_contribution)
        
        # Update user metrics
        user.contribution_score += calculate_contribution_score(contribution)
        
        db.commit()
        
        return {
            "message": "Contribution submitted successfully",
            "contribution_id": community_contribution.id,
            "status": "pending_review",
            "estimated_impact": calculate_estimated_impact(contribution)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit contribution: {str(e)}")

# Insights Endpoints
@router.get("/insights/{barcode}")
async def get_community_insights(
    barcode: str,
    db: Session = Depends(get_db)
) -> CommunityInsight:
    """
    Get community-driven insights for a product
    """
    try:
        # Get product data
        product = db.query(Product).filter(Product.barcode == barcode).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get scan statistics
        scans = db.query(ProductScan).filter(ProductScan.barcode == barcode).all()
        verifications = db.query(CommunityVerification).filter(
            CommunityVerification.product_id == product.id
        ).all()
        
        # Calculate insights
        scan_count = len(scans)
        verified_scans = len([v for v in verifications if v.is_accurate])
        
        # Calculate average CO2 from scans
        if scans:
            total_co2 = sum([scan.carbon_estimate.get('total_co2_kg', 0) for scan in scans if scan.carbon_estimate])
            average_co2 = total_co2 / len(scans) if scans else 0
        else:
            average_co2 = product.total_co2_kg or 0
        
        # Calculate community rating
        if verifications:
            accuracy_scores = [v.confidence for v in verifications if v.is_accurate]
            community_rating = sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else 0.5
        else:
            community_rating = 0.5
        
        # Get material trends
        all_materials = []
        for scan in scans:
            if scan.materials_detected:
                all_materials.extend(scan.materials_detected)
        
        top_materials = get_top_materials(all_materials)
        
        # Verification trends
        verification_trends = {
            "accurate": len([v for v in verifications if v.is_accurate]),
            "inaccurate": len([v for v in verifications if not v.is_accurate]),
            "pending": 0  # Would be from pending verifications
        }
        
        return CommunityInsight(
            product_name=product.name,
            barcode=barcode,
            average_co2=round(average_co2, 2),
            scan_count=scan_count,
            verified_scans=verified_scans,
            community_rating=round(community_rating * 5, 1),  # Convert to 5-star scale
            accuracy_score=round(product.confidence_score, 2),
            last_verified=max([v.created_at for v in verifications]) if verifications else None,
            top_materials=top_materials,
            verification_trends=verification_trends
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get insights: {str(e)}")

# User and Leaderboard Endpoints
@router.get("/profile/{user_id}")
async def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db)
) -> UserProfile:
    """
    Get user community profile
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate rank
    rank = calculate_user_rank(user, db)
    
    return UserProfile(
        id=user.id,
        display_name=user.display_name,
        verification_count=user.verification_count,
        contribution_score=user.contribution_score,
        reputation_score=user.reputation_score,
        accuracy_rating=user.accuracy_rating,
        total_scans=user.total_scans,
        co2_saved_kg=user.co2_saved_kg,
        joined_at=user.joined_at,
        rank=rank
    )

@router.get("/leaderboard")
async def get_leaderboard(
    metric: str = "contribution_score",
    limit: int = 10,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get community leaderboard
    """
    try:
        # Validate metric
        valid_metrics = ["contribution_score", "verification_count", "co2_saved_kg", "accuracy_rating"]
        if metric not in valid_metrics:
            raise HTTPException(status_code=400, detail=f"Invalid metric. Must be one of: {valid_metrics}")
        
        # Get top users
        users_query = db.query(User).filter(User.verification_count > 0)
        
        if metric == "contribution_score":
            users_query = users_query.order_by(User.contribution_score.desc())
        elif metric == "verification_count":
            users_query = users_query.order_by(User.verification_count.desc())
        elif metric == "co2_saved_kg":
            users_query = users_query.order_by(User.co2_saved_kg.desc())
        elif metric == "accuracy_rating":
            users_query = users_query.order_by(User.accuracy_rating.desc())
        
        top_users = users_query.limit(limit).all()
        
        # Calculate community totals
        total_verifications = db.query(CommunityVerification).count()
        total_co2_saved = db.query(User).with_entities(db.func.sum(User.co2_saved_kg)).scalar() or 0
        total_users = db.query(User).count()
        
        # Build leaderboard entries
        leaderboard = []
        for i, user in enumerate(top_users, 1):
            metric_value = getattr(user, metric)
            leaderboard.append(LeaderboardEntry(
                user=UserProfile(
                    id=user.id,
                    display_name=user.display_name or f"User {user.id[:8]}",
                    verification_count=user.verification_count,
                    contribution_score=user.contribution_score,
                    reputation_score=user.reputation_score,
                    accuracy_rating=user.accuracy_rating,
                    total_scans=user.total_scans,
                    co2_saved_kg=user.co2_saved_kg,
                    joined_at=user.joined_at
                ),
                metric_value=metric_value,
                rank=i
            ))
        
        return {
            "leaderboard": leaderboard,
            "metric": metric,
            "community_stats": {
                "total_users": total_users,
                "total_verifications": total_verifications,
                "total_co2_saved_kg": round(total_co2_saved, 2),
                "avg_accuracy": calculate_community_avg_accuracy(db)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get leaderboard: {str(e)}")

# Helper Functions
def get_or_create_user(user_id: str, db: Session) -> User:
    """Get existing user or create new one"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(
            id=user_id,
            anonymous_id=user_id,
            display_name=f"User {user_id[:8]}"
        )
        db.add(user)
        db.flush()
    return user

def calculate_verification_score(verification: VerificationRequest) -> float:
    """Calculate score for a verification"""
    base_score = 1.0
    confidence_bonus = verification.confidence * 0.5
    detail_bonus = 0.5 if verification.evidence_provided else 0.0
    return base_score + confidence_bonus + detail_bonus

def calculate_contribution_score(contribution: ContributionRequest) -> float:
    """Calculate score for a contribution"""
    base_scores = {
        "product": 5.0,
        "alternative": 3.0,
        "correction": 2.0,
        "material_data": 1.0
    }
    return base_scores.get(contribution.contribution_type, 1.0)

def calculate_accuracy_improvement(verification: VerificationRequest) -> float:
    """Calculate estimated accuracy improvement"""
    return verification.confidence * 2.5 if verification.is_accurate else 0.0

def assess_contribution_quality(contribution: ContributionRequest) -> float:
    """Assess quality of a contribution"""
    # Simple heuristic - could be enhanced with ML
    data_completeness = len(contribution.data) / 10.0  # Assume 10 fields is complete
    has_evidence = 0.2 if contribution.original_data else 0.0
    return min(1.0, data_completeness + has_evidence)

def calculate_estimated_impact(contribution: ContributionRequest) -> str:
    """Calculate estimated impact of contribution"""
    impact_map = {
        "product": "High - New product data",
        "alternative": "Medium - Better recommendations", 
        "correction": "Medium - Improved accuracy",
        "material_data": "Low - Enhanced material analysis"
    }
    return impact_map.get(contribution.contribution_type, "Low")

def get_top_materials(materials_list: List[str]) -> List[str]:
    """Get most common materials"""
    from collections import Counter
    if not materials_list:
        return []
    
    material_counts = Counter(materials_list)
    return [material for material, count in material_counts.most_common(5)]

def calculate_user_rank(user: User, db: Session) -> int:
    """Calculate user's rank in community"""
    higher_score_users = db.query(User).filter(
        User.contribution_score > user.contribution_score
    ).count()
    return higher_score_users + 1

def calculate_community_avg_accuracy(db: Session) -> float:
    """Calculate community average accuracy"""
    avg_accuracy = db.query(User).with_entities(
        db.func.avg(User.accuracy_rating)
    ).scalar()
    return round(avg_accuracy or 0.5, 2)
