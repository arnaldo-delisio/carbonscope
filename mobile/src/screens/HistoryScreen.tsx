import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface ScanHistoryItem {
  id: string;
  product_name: string;
  barcode: string;
  total_co2_kg: number;
  impact_level: string;
  timestamp: string;
}

interface HistoryScreenProps {
  navigation: any;
}

const HistoryItem = ({ item, onPress }: {
  item: ScanHistoryItem;
  onPress: () => void;
}) => {
  const getImpactColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'low': return '#10B981';
      case 'medium': return '#F59E0B';
      case 'high': return '#EF4444';
      case 'very high': return '#DC2626';
      default: return '#6B7280';
    }
  };

  const getImpactEmoji = (level: string) => {
    switch (level.toLowerCase()) {
      case 'low': return '🟢';
      case 'medium': return '🟡';
      case 'high': return '🟠';
      case 'very high': return '🔴';
      default: return '⚪';
    }
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <TouchableOpacity style={styles.historyItem} onPress={onPress}>
      <View style={styles.itemHeader}>
        <Text style={styles.productName} numberOfLines={1}>
          {item.product_name}
        </Text>
        <Text style={styles.timestamp}>{formatDate(item.timestamp)}</Text>
      </View>
      
      <View style={styles.itemDetails}>
        <View style={styles.carbonInfo}>
          <Text style={styles.carbonValue}>{item.total_co2_kg} kg CO₂e</Text>
          <View style={styles.impactBadge}>
            <Text style={styles.impactEmoji}>{getImpactEmoji(item.impact_level)}</Text>
            <Text style={[styles.impactText, { color: getImpactColor(item.impact_level) }]}>
              {item.impact_level}
            </Text>
          </View>
        </View>
        
        <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
      </View>
      
      <Text style={styles.barcode}>Barcode: {item.barcode}</Text>
    </TouchableOpacity>
  );
};

const EmptyState = ({ onScanPress }: { onScanPress: () => void }) => (
  <View style={styles.emptyContainer}>
    <Ionicons name="time-outline" size={64} color="#9ca3af" />
    <Text style={styles.emptyTitle}>No Scan History</Text>
    <Text style={styles.emptyDescription}>
      Start scanning products to see your carbon footprint analysis history
    </Text>
    <TouchableOpacity style={styles.scanButton} onPress={onScanPress}>
      <Ionicons name="scan" size={20} color="white" />
      <Text style={styles.scanButtonText}>Start Scanning</Text>
    </TouchableOpacity>
  </View>
);

const StatsCard = ({ title, value, subtitle, color }: {
  title: string;
  value: string;
  subtitle: string;
  color: string;
}) => (
  <View style={[styles.statsCard, { borderLeftColor: color }]}>
    <Text style={styles.statsTitle}>{title}</Text>
    <Text style={[styles.statsValue, { color }]}>{value}</Text>
    <Text style={styles.statsSubtitle}>{subtitle}</Text>
  </View>
);

export default function HistoryScreen({ navigation }: HistoryScreenProps) {
  const [refreshing, setRefreshing] = useState(false);
  
  // Mock data - in real app this would come from API/storage
  const [scanHistory] = useState<ScanHistoryItem[]>([
    // Empty for now - will be populated when user starts scanning
  ]);

  const onRefresh = async () => {
    setRefreshing(true);
    // TODO: Fetch latest scan history from API
    setTimeout(() => setRefreshing(false), 1000);
  };

  const navigateToScan = () => {
    navigation.navigate('Scan');
  };

  const viewScanDetails = (item: ScanHistoryItem) => {
    // TODO: Navigate to detailed view of scan result
    // For now, just show an alert
    console.log('View details for:', item.product_name);
  };

  // Calculate stats from history
  const totalScans = scanHistory.length;
  const totalCO2 = scanHistory.reduce((sum, item) => sum + item.total_co2_kg, 0);
  const avgCO2 = totalScans > 0 ? totalCO2 / totalScans : 0;

  return (
    <View style={styles.container}>
      {/* Stats Section */}
      {totalScans > 0 && (
        <View style={styles.statsContainer}>
          <Text style={styles.sectionTitle}>Your Impact Summary</Text>
          <View style={styles.statsGrid}>
            <StatsCard
              title="Total Scans"
              value={totalScans.toString()}
              subtitle="products analyzed"
              color="#10B981"
            />
            <StatsCard
              title="Total CO₂"
              value={`${totalCO2.toFixed(1)}kg`}
              subtitle="carbon footprint"
              color="#EF4444"
            />
          </View>
          <StatsCard
            title="Average Impact"
            value={`${avgCO2.toFixed(1)}kg`}
            subtitle="CO₂e per product"
            color="#3B82F6"
          />
        </View>
      )}

      {/* History List */}
      <View style={styles.historyContainer}>
        <Text style={styles.sectionTitle}>Scan History</Text>
        
        {scanHistory.length === 0 ? (
          <EmptyState onScanPress={navigateToScan} />
        ) : (
          <FlatList
            data={scanHistory}
            renderItem={({ item }) => (
              <HistoryItem 
                item={item} 
                onPress={() => viewScanDetails(item)} 
              />
            )}
            keyExtractor={(item) => item.id}
            refreshControl={
              <RefreshControl
                refreshing={refreshing}
                onRefresh={onRefresh}
                colors={['#10B981']}
              />
            }
            contentContainerStyle={styles.listContainer}
            showsVerticalScrollIndicator={false}
          />
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  statsContainer: {
    padding: 20,
    backgroundColor: 'white',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 12,
  },
  statsCard: {
    flex: 1,
    backgroundColor: '#f8f9fa',
    padding: 16,
    borderRadius: 8,
    borderLeftWidth: 4,
  },
  statsTitle: {
    fontSize: 12,
    color: '#6b7280',
    textTransform: 'uppercase',
    marginBottom: 4,
  },
  statsValue: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 2,
  },
  statsSubtitle: {
    fontSize: 12,
    color: '#6b7280',
  },
  historyContainer: {
    flex: 1,
    backgroundColor: 'white',
    paddingTop: 20,
  },
  listContainer: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  historyItem: {
    backgroundColor: '#f8f9fa',
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  itemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  productName: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginRight: 8,
  },
  timestamp: {
    fontSize: 12,
    color: '#6b7280',
  },
  itemDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  carbonInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  carbonValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  impactBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'white',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    gap: 4,
  },
  impactEmoji: {
    fontSize: 12,
  },
  impactText: {
    fontSize: 12,
    fontWeight: '600',
  },
  barcode: {
    fontSize: 12,
    color: '#6b7280',
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 60,
    paddingHorizontal: 40,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1f2937',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyDescription: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: 24,
  },
  scanButton: {
    backgroundColor: '#10B981',
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
    gap: 8,
  },
  scanButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});