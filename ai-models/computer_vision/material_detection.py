"""
Material Detection Model
Uses computer vision to identify materials from product images.
Focuses on practical, achievable material classification through image analysis.
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple
import tensorflow as tf
from dataclasses import dataclass

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
        Fallback material detection using traditional CV methods
        """
        # Simple color-based material detection
        detections = []
        
        # Convert to HSV for better color analysis
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Example: Detect plastic based on color characteristics
        # This is a simplified approach - real implementation would be more sophisticated
        
        return detections
    
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
    Convenience function to analyze a product image
    
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
