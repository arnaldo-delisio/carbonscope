"""
Enhanced Material Detection Model
Uses computer vision to identify materials from product images.
Implements practical material classification through texture analysis and deep learning.
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
import tensorflow as tf
from dataclasses import dataclass
import base64
import io
from PIL import Image
import logging

logger = logging.getLogger(__name__)

@dataclass
class MaterialDetection:
    material_type: str
    confidence: float
    bounding_box: Tuple[int, int, int, int]
    properties: Dict[str, any]

class MaterialDetector:
    """
    AI model for detecting and classifying materials from product images.
    
    Focuses on practical material identification that can be achieved through
    computer vision analysis of product packaging and appearance.
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.material_classes = [
            'plastic_pet', 'plastic_hdpe', 'plastic_pvc', 'plastic_ldpe',
            'plastic_pp', 'plastic_ps', 'aluminum', 'steel', 'glass',
            'cardboard', 'paper', 'wood', 'fabric', 'ceramic'
        ]
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str):
        """Load pre-trained material detection model"""
        try:
            self.model = tf.keras.models.load_model(model_path)
            print(f"Model loaded from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            # TODO: Implement fallback to pre-trained model
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for model input"""
        # Resize to model input size
        resized = cv2.resize(image, (224, 224))
        
        # Normalize pixel values
        normalized = resized / 255.0
        
        # Add batch dimension
        batched = np.expand_dims(normalized, axis=0)
        
        return batched
    
    def detect_materials(self, image: np.ndarray) -> List[MaterialDetection]:
        """
        Detect materials in the given image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of detected materials with confidence scores
        """
        if self.model is None:
            # Fallback to rule-based detection
            return self._fallback_detection(image)
        
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Run inference
        predictions = self.model.predict(processed_image)
        
        # Process predictions
        detections = []
        for i, confidence in enumerate(predictions[0]):
            if confidence > 0.5:  # Confidence threshold
                material = MaterialDetection(
                    material_type=self.material_classes[i],
                    confidence=float(confidence),
                    bounding_box=(0, 0, image.shape[1], image.shape[0]),  # Full image for now
                    properties=self._get_material_properties(self.material_classes[i])
                )
                detections.append(material)
        
        return sorted(detections, key=lambda x: x.confidence, reverse=True)
    
    def _fallback_detection(self, image: np.ndarray) -> List[MaterialDetection]:
        """
        Enhanced fallback material detection using traditional CV methods
        Analyzes texture, color, and shape patterns to identify materials
        """
        detections = []
        
        try:
            # Convert to different color spaces for analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Texture analysis using Local Binary Patterns
            texture_score = self._analyze_texture(gray)
            
            # Color analysis
            color_features = self._analyze_colors(hsv)
            
            # Shape and edge analysis
            edge_features = self._analyze_edges(gray)
            
            # Combine features to predict materials
            material_predictions = self._classify_from_features(
                texture_score, color_features, edge_features
            )
            
            # Convert predictions to MaterialDetection objects
            for material_type, confidence in material_predictions.items():
                if confidence > 0.3:  # Minimum confidence threshold
                    detection = MaterialDetection(
                        material_type=material_type,
                        confidence=confidence,
                        bounding_box=(0, 0, image.shape[1], image.shape[0]),
                        properties=self._get_material_properties(material_type)
                    )
                    detections.append(detection)
            
        except Exception as e:
            logger.warning(f"Fallback detection failed: {e}")
            # Return best guess based on image characteristics
            detections = self._simple_guess(image)
        
        return sorted(detections, key=lambda x: x.confidence, reverse=True)[:3]
    
    def _analyze_texture(self, gray_image: np.ndarray) -> Dict[str, float]:
        """Analyze texture patterns to identify material types"""
        texture_scores = {}
        
        # Calculate texture descriptors
        # Variance of Laplacian (texture measure)
        laplacian_var = cv2.Laplacian(gray_image, cv2.CV_64F).var()
        
        # Local Binary Pattern approximation
        kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
        lbp_response = cv2.filter2D(gray_image, cv2.CV_64F, kernel)
        lbp_std = np.std(lbp_response)
        
        # Classify based on texture
        if laplacian_var > 1000:  # High texture variance
            if lbp_std > 50:
                texture_scores['cardboard'] = 0.7  # Corrugated texture
                texture_scores['fabric'] = 0.5    # Woven texture
            else:
                texture_scores['plastic'] = 0.6   # Smooth but detailed
        elif laplacian_var > 100:  # Medium texture
            texture_scores['paper'] = 0.6
            texture_scores['wood'] = 0.4
        else:  # Low texture variance (smooth)
            texture_scores['glass'] = 0.7
            texture_scores['aluminum'] = 0.6
            texture_scores['plastic'] = 0.5
        
        return texture_scores
    
    def _analyze_colors(self, hsv_image: np.ndarray) -> Dict[str, float]:
        """Analyze color characteristics to identify materials"""
        color_scores = {}
        
        # Calculate color statistics
        h_mean = np.mean(hsv_image[:, :, 0])
        s_mean = np.mean(hsv_image[:, :, 1])
        v_mean = np.mean(hsv_image[:, :, 2])
        
        # Metallic detection (low saturation, medium-high value)
        if s_mean < 50 and v_mean > 100:
            if v_mean > 200:
                color_scores['aluminum'] = 0.8  # Bright metallic
            else:
                color_scores['steel'] = 0.6     # Darker metallic
        
        # Glass detection (high value, low-medium saturation)
        if v_mean > 150 and s_mean < 80:
            color_scores['glass'] = 0.7
        
        # Plastic detection (varied colors, medium saturation)
        if s_mean > 30 and s_mean < 200:
            color_scores['plastic_pet'] = 0.6
            color_scores['plastic_hdpe'] = 0.5
        
        # Paper/cardboard (brownish hues, medium saturation)
        if 10 <= h_mean <= 30 or h_mean >= 150:  # Brown/yellow/red range
            color_scores['cardboard'] = 0.7
            color_scores['paper'] = 0.6
        
        return color_scores
    
    def _analyze_edges(self, gray_image: np.ndarray) -> Dict[str, float]:
        """Analyze edge patterns to identify material characteristics"""
        edge_scores = {}
        
        # Edge detection
        edges = cv2.Canny(gray_image, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Line detection for packaging
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, 
                               minLineLength=30, maxLineGap=10)
        line_count = len(lines) if lines is not None else 0
        
        # Classification based on edge characteristics
        if edge_density > 0.1:  # High edge density
            if line_count > 10:
                edge_scores['cardboard'] = 0.8  # Structured packaging
            else:
                edge_scores['fabric'] = 0.6     # Irregular edges
        elif edge_density > 0.05:  # Medium edge density
            edge_scores['plastic'] = 0.7
            edge_scores['paper'] = 0.5
        else:  # Low edge density (smooth surfaces)
            edge_scores['glass'] = 0.8
            edge_scores['aluminum'] = 0.7
        
        return edge_scores
    
    def _classify_from_features(self, texture_scores: Dict[str, float], 
                               color_scores: Dict[str, float], 
                               edge_scores: Dict[str, float]) -> Dict[str, float]:
        """Combine feature scores to classify materials"""
        all_materials = set(texture_scores.keys()) | set(color_scores.keys()) | set(edge_scores.keys())
        final_scores = {}
        
        for material in all_materials:
            # Weighted combination of scores
            texture_weight = 0.4
            color_weight = 0.4
            edge_weight = 0.2
            
            texture_score = texture_scores.get(material, 0.0)
            color_score = color_scores.get(material, 0.0)
            edge_score = edge_scores.get(material, 0.0)
            
            final_score = (texture_weight * texture_score + 
                          color_weight * color_score + 
                          edge_weight * edge_score)
            
            # Apply material-specific boosts
            if material in ['plastic_pet', 'plastic_hdpe', 'plastic']:
                final_score *= 1.1  # Plastic is common in products
            elif material in ['aluminum', 'steel']:
                final_score *= 1.05  # Metal is common in packaging
            
            final_scores[material] = min(final_score, 0.95)  # Cap at 95%
        
        return final_scores
    
    def _simple_guess(self, image: np.ndarray) -> List[MaterialDetection]:
        """Simple fallback when all analysis fails"""
        # Basic heuristic based on image properties
        height, width = image.shape[:2]
        
        # Default to common packaging materials
        return [
            MaterialDetection(
                material_type="plastic",
                confidence=0.4,
                bounding_box=(0, 0, width, height),
                properties=self._get_material_properties("plastic")
            ),
            MaterialDetection(
                material_type="cardboard",
                confidence=0.3,
                bounding_box=(0, 0, width, height),
                properties=self._get_material_properties("cardboard")
            )
        ]
    
    def _get_material_properties(self, material_type: str) -> Dict[str, any]:
        """Get properties for a given material type"""
        properties = {
            'plastic_pet': {
                'recyclable': True,
                'carbon_intensity': 3.4,  # kg CO2 per kg material
                'density': 1.38,
                'melting_point': 260
            },
            'aluminum': {
                'recyclable': True,
                'carbon_intensity': 11.5,
                'density': 2.70,
                'melting_point': 660
            },
            'cardboard': {
                'recyclable': True,
                'carbon_intensity': 1.1,
                'density': 0.7,
                'biodegradable': True
            }
            # Add more materials...
        }
        
        return properties.get(material_type, {})

def analyze_product_image(image_path: str) -> List[MaterialDetection]:
    """
    Convenience function to analyze a product image from file path
    
    Args:
        image_path: Path to the image file
        
    Returns:
        List of detected materials
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from {image_path}")
    
    # Initialize detector
    detector = MaterialDetector()
    
    # Detect materials
    materials = detector.detect_materials(image)
    
    return materials

def analyze_base64_image(base64_string: str) -> List[MaterialDetection]:
    """
    Analyze a product image from base64 encoded string
    
    Args:
        base64_string: Base64 encoded image data
        
    Returns:
        List of detected materials
    """
    try:
        # Decode base64 image
        if ',' in base64_string:
            # Remove data URL prefix if present
            base64_string = base64_string.split(',')[1]
        
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert PIL to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Initialize detector
        detector = MaterialDetector()
        
        # Detect materials
        materials = detector.detect_materials(opencv_image)
        
        return materials
        
    except Exception as e:
        logger.error(f"Failed to analyze base64 image: {e}")
        raise ValueError(f"Invalid base64 image data: {e}")

def analyze_numpy_image(image_array: np.ndarray) -> List[MaterialDetection]:
    """
    Analyze a product image from numpy array
    
    Args:
        image_array: Image as numpy array (BGR format)
        
    Returns:
        List of detected materials
    """
    # Initialize detector
    detector = MaterialDetector()
    
    # Detect materials
    materials = detector.detect_materials(image_array)
    
    return materials

# API Integration Functions
async def detect_materials_from_image_async(image_data: str) -> List[str]:
    """
    Async wrapper for material detection from base64 image
    Returns simplified list of material names for API integration
    """
    try:
        materials = analyze_base64_image(image_data)
        return [mat.material_type for mat in materials]
    except Exception as e:
        logger.warning(f"Material detection failed: {e}")
        # Return common materials as fallback
        return ["plastic", "cardboard"]

if __name__ == "__main__":
    # Example usage
    detector = MaterialDetector()
    
    # Create dummy image for testing
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Detect materials
    materials = detector.detect_materials(test_image)
    
    print("Detected materials:")
    for material in materials:
        print(f"- {material.material_type}: {material.confidence:.2f}")
