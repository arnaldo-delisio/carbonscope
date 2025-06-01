import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface HomeScreenProps {
  navigation: any;
}

const FeatureCard = ({ icon, title, description, onPress }: {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  description: string;
  onPress: () => void;
}) => (
  <TouchableOpacity style={styles.featureCard} onPress={onPress}>
    <View style={styles.featureIcon}>
      <Ionicons name={icon} size={32} color="#10B981" />
    </View>
    <Text style={styles.featureTitle}>{title}</Text>
    <Text style={styles.featureDescription}>{description}</Text>
  </TouchableOpacity>
);

const StatCard = ({ value, label, color }: {
  value: string;
  label: string;
  color: string;
}) => (
  <View style={[styles.statCard, { borderLeftColor: color }]}>
    <Text style={[styles.statValue, { color }]}>{value}</Text>
    <Text style={styles.statLabel}>{label}</Text>
  </View>
);

export default function HomeScreen({ navigation }: HomeScreenProps) {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.welcomeText}>Welcome to</Text>
        <Text style={styles.title}>🌍 CarbonScope</Text>
        <Text style={styles.subtitle}>
          AI-powered carbon footprint analysis for every product
        </Text>
      </View>

      {/* Quick Stats */}
      <View style={styles.statsContainer}>
        <Text style={styles.sectionTitle}>Your Impact</Text>
        <View style={styles.statsGrid}>
          <StatCard value="0" label="Products Scanned" color="#10B981" />
          <StatCard value="0.0kg" label="CO₂ Saved" color="#3b82f6" />
        </View>
      </View>

      {/* Features */}
      <View style={styles.featuresContainer}>
        <Text style={styles.sectionTitle}>What Can You Do?</Text>
        <View style={styles.featuresGrid}>
          <FeatureCard
            icon="scan"
            title="Scan Products"
            description="Use your camera to scan barcodes and get instant carbon analysis"
            onPress={() => navigation.navigate('Scan')}
          />
          <FeatureCard
            icon="analytics"
            title="AI Analysis"
            description="Smart algorithms calculate real-time carbon estimates"
            onPress={() => navigation.navigate('Scan')}
          />
          <FeatureCard
            icon="leaf"
            title="Find Alternatives"
            description="Discover lower-carbon options with savings calculations"
            onPress={() => navigation.navigate('Scan')}
          />
          <FeatureCard
            icon="people"
            title="Community Data"
            description="Help improve accuracy through crowdsourced verification"
            onPress={() => navigation.navigate('Profile')}
          />
        </View>
      </View>

      {/* Quick Actions */}
      <View style={styles.actionsContainer}>
        <TouchableOpacity 
          style={styles.primaryAction}
          onPress={() => navigation.navigate('Scan')}
        >
          <Ionicons name="scan" size={24} color="white" />
          <Text style={styles.primaryActionText}>Start Scanning</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={styles.secondaryAction}
          onPress={() => navigation.navigate('History')}
        >
          <Ionicons name="time" size={20} color="#10B981" />
          <Text style={styles.secondaryActionText}>View History</Text>
        </TouchableOpacity>
      </View>

      {/* Recent Activity */}
      <View style={styles.recentContainer}>
        <Text style={styles.sectionTitle}>Recent Scans</Text>
        <View style={styles.emptyState}>
          <Ionicons name="scan-outline" size={48} color="#9ca3af" />
          <Text style={styles.emptyStateText}>No scans yet</Text>
          <Text style={styles.emptyStateSubtext}>
            Start by scanning a product to see your carbon impact
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    alignItems: 'center',
    paddingVertical: 30,
    paddingHorizontal: 20,
    backgroundColor: 'white',
    marginBottom: 20,
  },
  welcomeText: {
    fontSize: 16,
    color: '#6b7280',
    marginBottom: 4,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 22,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 16,
  },
  statsContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  statsGrid: {
    flexDirection: 'row',
    gap: 12,
  },
  statCard: {
    flex: 1,
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 14,
    color: '#6b7280',
  },
  featuresContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  featuresGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  featureCard: {
    width: (width - 52) / 2,
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  featureIcon: {
    marginBottom: 12,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 6,
    textAlign: 'center',
  },
  featureDescription: {
    fontSize: 12,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 16,
  },
  actionsContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
    gap: 12,
  },
  primaryAction: {
    backgroundColor: '#10B981',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    borderRadius: 12,
    shadowColor: '#10B981',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  primaryActionText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 8,
  },
  secondaryAction: {
    backgroundColor: 'white',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#10B981',
  },
  secondaryActionText: {
    color: '#10B981',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 6,
  },
  recentContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  emptyState: {
    backgroundColor: 'white',
    padding: 40,
    borderRadius: 12,
    alignItems: 'center',
  },
  emptyStateText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#4b5563',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyStateSubtext: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 20,
  },
});