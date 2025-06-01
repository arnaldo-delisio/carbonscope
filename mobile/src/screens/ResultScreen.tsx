import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Share,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface CarbonEstimate {
  total_co2_kg: number;
  production_co2_kg: number;
  transport_co2_kg: number;
  packaging_co2_kg: number;
  usage_co2_kg?: number;
  confidence_score: number;
  impact_level: string;
  methodology: string;
  factors_applied?: any;
}

interface ProductAnalysis {
  scan_id: string;
  product_name: string;
  barcode: string;
  materials_detected: string[];
  carbon_estimate: CarbonEstimate;
  alternatives: Array<{
    name: string;
    co2_kg: number;
    co2_reduction: number;
    reason: string;
    savings_kg: number;
    availability?: string;
  }>;
  timestamp: string;
}

interface ResultScreenProps {
  route: {
    params: {
      analysisData: ProductAnalysis;
    };
  };
  navigation: any;
}

const ImpactIndicator = ({ level, co2Kg }: { level: string; co2Kg: number }) => {
  const getIndicatorStyle = () => {
    switch (level.toLowerCase()) {
      case 'low':
        return { color: '#10B981', icon: 'leaf' as const, emoji: '🟢' };
      case 'medium':
        return { color: '#F59E0B', icon: 'warning' as const, emoji: '🟡' };
      case 'high':
        return { color: '#EF4444', icon: 'alert-circle' as const, emoji: '🟠' };
      case 'very high':
        return { color: '#DC2626', icon: 'alert' as const, emoji: '🔴' };
      default:
        return { color: '#6B7280', icon: 'help-circle' as const, emoji: '⚪' };
    }
  };

  const style = getIndicatorStyle();

  return (
    <View style={[styles.impactContainer, { borderColor: style.color }]}>
      <View style={styles.impactHeader}>
        <Text style={styles.impactEmoji}>{style.emoji}</Text>
        <Text style={[styles.impactLevel, { color: style.color }]}>
          {level} Impact
        </Text>
      </View>
      <Text style={styles.co2Value}>{co2Kg} kg CO₂e</Text>
    </View>
  );
};

const BreakdownItem = ({ label, value, percentage }: {
  label: string;
  value: number;
  percentage: number;
}) => (
  <View style={styles.breakdownItem}>
    <View style={styles.breakdownHeader}>
      <Text style={styles.breakdownLabel}>{label}</Text>
      <Text style={styles.breakdownValue}>{value} kg</Text>
    </View>
    <View style={styles.progressBar}>
      <View style={[styles.progressFill, { width: `${percentage}%` }]} />
    </View>
  </View>
);

const AlternativeCard = ({ alternative }: {
  alternative: {
    name: string;
    co2_kg: number;
    co2_reduction: number;
    reason: string;
    savings_kg: number;
    availability?: string;
  };
}) => (
  <View style={styles.alternativeCard}>
    <View style={styles.alternativeHeader}>
      <Text style={styles.alternativeName}>{alternative.name}</Text>
      <View style={styles.savingsContainer}>
        <Text style={styles.savingsText}>
          -{alternative.savings_kg} kg CO₂e
        </Text>
        <Text style={styles.savingsPercentage}>
          ({Math.round(alternative.co2_reduction * 100)}% less)
        </Text>
      </View>
    </View>
    <Text style={styles.alternativeReason}>{alternative.reason}</Text>
    {alternative.availability && (
      <Text style={styles.alternativeAvailability}>
        Available: {alternative.availability}
      </Text>
    )}
  </View>
);

export default function ResultScreen({ route, navigation }: ResultScreenProps) {
  const { analysisData } = route.params;
  const { carbon_estimate, alternatives, product_name, materials_detected } = analysisData;

  const shareResults = async () => {
    try {
      const message = `🌍 Carbon Footprint Analysis

Product: ${product_name}
Impact: ${carbon_estimate.total_co2_kg} kg CO₂e (${carbon_estimate.impact_level})

Breakdown:
• Production: ${carbon_estimate.production_co2_kg} kg
• Transport: ${carbon_estimate.transport_co2_kg} kg
• Packaging: ${carbon_estimate.packaging_co2_kg} kg

Analyzed with CarbonScope - AI-powered carbon footprint analysis`;

      await Share.share({
        message,
        title: 'Carbon Footprint Analysis',
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to share results');
    }
  };

  const total = carbon_estimate.total_co2_kg;
  const production = carbon_estimate.production_co2_kg;
  const transport = carbon_estimate.transport_co2_kg;
  const packaging = carbon_estimate.packaging_co2_kg;
  const usage = carbon_estimate.usage_co2_kg || 0;

  return (
    <ScrollView style={styles.container}>
      {/* Product Header */}
      <View style={styles.header}>
        <Text style={styles.productName}>{product_name}</Text>
        <Text style={styles.barcode}>Barcode: {analysisData.barcode}</Text>
        {materials_detected.length > 0 && (
          <Text style={styles.materials}>
            Materials: {materials_detected.join(', ')}
          </Text>
        )}
      </View>

      {/* Impact Indicator */}
      <View style={styles.section}>
        <ImpactIndicator 
          level={carbon_estimate.impact_level} 
          co2Kg={carbon_estimate.total_co2_kg} 
        />
      </View>

      {/* Breakdown */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Carbon Footprint Breakdown</Text>
        <View style={styles.breakdown}>
          <BreakdownItem 
            label="Production" 
            value={production} 
            percentage={(production / total) * 100} 
          />
          <BreakdownItem 
            label="Transport" 
            value={transport} 
            percentage={(transport / total) * 100} 
          />
          <BreakdownItem 
            label="Packaging" 
            value={packaging} 
            percentage={(packaging / total) * 100} 
          />
          {usage > 0 && (
            <BreakdownItem 
              label="Usage" 
              value={usage} 
              percentage={(usage / total) * 100} 
            />
          )}
        </View>
      </View>

      {/* Confidence */}
      <View style={styles.section}>
        <View style={styles.confidenceContainer}>
          <Text style={styles.confidenceLabel}>Confidence Score</Text>
          <Text style={styles.confidenceValue}>
            {Math.round(carbon_estimate.confidence_score * 100)}%
          </Text>
        </View>
        <Text style={styles.methodology}>
          Method: {carbon_estimate.methodology}
        </Text>
      </View>

      {/* Alternatives */}
      {alternatives.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>💡 Better Alternatives</Text>
          {alternatives.map((alt, index) => (
            <AlternativeCard key={index} alternative={alt} />
          ))}
        </View>
      )}

      {/* Actions */}
      <View style={styles.actions}>
        <TouchableOpacity style={styles.shareButton} onPress={shareResults}>
          <Ionicons name="share-social" size={20} color="white" />
          <Text style={styles.shareButtonText}>Share Results</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={styles.scanAgainButton}
          onPress={() => navigation.navigate('ScanMain')}
        >
          <Ionicons name="scan" size={20} color="#10B981" />
          <Text style={styles.scanAgainButtonText}>Scan Another</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    backgroundColor: 'white',
    padding: 20,
    marginBottom: 12,
  },
  productName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
  },
  barcode: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 4,
  },
  materials: {
    fontSize: 14,
    color: '#6b7280',
  },
  section: {
    backgroundColor: 'white',
    padding: 20,
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 16,
  },
  impactContainer: {
    borderWidth: 2,
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
  },
  impactHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  impactEmoji: {
    fontSize: 24,
    marginRight: 8,
  },
  impactLevel: {
    fontSize: 18,
    fontWeight: '600',
  },
  co2Value: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  breakdown: {
    gap: 16,
  },
  breakdownItem: {
    gap: 8,
  },
  breakdownHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  breakdownLabel: {
    fontSize: 16,
    color: '#374151',
  },
  breakdownValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
  },
  progressBar: {
    height: 6,
    backgroundColor: '#e5e7eb',
    borderRadius: 3,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#10B981',
  },
  confidenceContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  confidenceLabel: {
    fontSize: 16,
    color: '#374151',
  },
  confidenceValue: {
    fontSize: 18,
    fontWeight: '600',
    color: '#10B981',
  },
  methodology: {
    fontSize: 14,
    color: '#6b7280',
  },
  alternativeCard: {
    backgroundColor: '#f0fdf4',
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#10B981',
  },
  alternativeHeader: {
    marginBottom: 8,
  },
  alternativeName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 4,
  },
  savingsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  savingsText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#10B981',
  },
  savingsPercentage: {
    fontSize: 12,
    color: '#059669',
  },
  alternativeReason: {
    fontSize: 14,
    color: '#374151',
    marginBottom: 4,
  },
  alternativeAvailability: {
    fontSize: 12,
    color: '#6b7280',
    fontStyle: 'italic',
  },
  actions: {
    padding: 20,
    gap: 12,
  },
  shareButton: {
    backgroundColor: '#3b82f6',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: 8,
  },
  shareButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  scanAgainButton: {
    backgroundColor: 'white',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#10B981',
  },
  scanAgainButtonText: {
    color: '#10B981',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
});