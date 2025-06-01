import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Switch,
  Alert,
  Linking,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface ProfileScreenProps {
  navigation: any;
}

const SettingItem = ({ 
  icon, 
  title, 
  subtitle, 
  onPress, 
  rightElement 
}: {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  subtitle?: string;
  onPress?: () => void;
  rightElement?: React.ReactNode;
}) => (
  <TouchableOpacity 
    style={styles.settingItem} 
    onPress={onPress}
    disabled={!onPress}
  >
    <View style={styles.settingLeft}>
      <Ionicons name={icon} size={24} color="#10B981" />
      <View style={styles.settingTextContainer}>
        <Text style={styles.settingTitle}>{title}</Text>
        {subtitle && <Text style={styles.settingSubtitle}>{subtitle}</Text>}
      </View>
    </View>
    {rightElement || (onPress && <Ionicons name="chevron-forward" size={20} color="#9ca3af" />)}
  </TouchableOpacity>
);

const StatCard = ({ icon, value, label, color }: {
  icon: keyof typeof Ionicons.glyphMap;
  value: string;
  label: string;
  color: string;
}) => (
  <View style={styles.statCard}>
    <Ionicons name={icon} size={24} color={color} />
    <Text style={[styles.statValue, { color }]}>{value}</Text>
    <Text style={styles.statLabel}>{label}</Text>
  </View>
);

export default function ProfileScreen({ navigation }: ProfileScreenProps) {
  const [notifications, setNotifications] = useState(true);
  const [autoUpload, setAutoUpload] = useState(false);
  const [shareData, setShareData] = useState(true);

  const handleShare = () => {
    Alert.alert(
      'Share CarbonScope',
      'Help others reduce their carbon footprint!',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Share', 
          onPress: () => {
            // TODO: Implement sharing functionality
            console.log('Share app');
          }
        },
      ]
    );
  };

  const handleFeedback = () => {
    Alert.alert(
      'Send Feedback',
      'Help us improve CarbonScope',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Email', 
          onPress: () => {
            Linking.openURL('mailto:feedback@carbonscope.app?subject=CarbonScope Feedback');
          }
        },
      ]
    );
  };

  const handleAbout = () => {
    Alert.alert(
      'About CarbonScope',
      'Version 1.0.0\n\nAI-powered carbon footprint analysis for sustainable consumption.\n\nMade with ❤️ for the planet.',
      [{ text: 'OK' }]
    );
  };

  const handlePrivacy = () => {
    // TODO: Navigate to privacy policy
    Alert.alert('Privacy Policy', 'Privacy policy content would go here.');
  };

  const handleTerms = () => {
    // TODO: Navigate to terms of service
    Alert.alert('Terms of Service', 'Terms of service content would go here.');
  };

  return (
    <ScrollView style={styles.container}>
      {/* Profile Header */}
      <View style={styles.header}>
        <View style={styles.avatarContainer}>
          <Ionicons name="person" size={40} color="white" />
        </View>
        <Text style={styles.userName}>Anonymous User</Text>
        <Text style={styles.userSubtitle}>Making a difference, one scan at a time</Text>
      </View>

      {/* Stats */}
      <View style={styles.statsContainer}>
        <Text style={styles.sectionTitle}>Your Impact</Text>
        <View style={styles.statsGrid}>
          <StatCard
            icon="scan"
            value="0"
            label="Products Scanned"
            color="#10B981"
          />
          <StatCard
            icon="leaf"
            value="0.0kg"
            label="CO₂ Avoided"
            color="#3B82F6"
          />
          <StatCard
            icon="people"
            value="0"
            label="Community Contributions"
            color="#8B5CF6"
          />
        </View>
      </View>

      {/* Settings */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Settings</Text>
        
        <SettingItem
          icon="notifications"
          title="Notifications"
          subtitle="Get alerts about carbon-saving tips"
          rightElement={
            <Switch
              value={notifications}
              onValueChange={setNotifications}
              trackColor={{ false: '#e5e7eb', true: '#10B981' }}
              thumbColor={notifications ? '#ffffff' : '#f4f3f4'}
            />
          }
        />
        
        <SettingItem
          icon="cloud-upload"
          title="Auto Upload Scans"
          subtitle="Help improve community data"
          rightElement={
            <Switch
              value={autoUpload}
              onValueChange={setAutoUpload}
              trackColor={{ false: '#e5e7eb', true: '#10B981' }}
              thumbColor={autoUpload ? '#ffffff' : '#f4f3f4'}
            />
          }
        />
        
        <SettingItem
          icon="analytics"
          title="Share Anonymous Data"
          subtitle="Help improve AI accuracy"
          rightElement={
            <Switch
              value={shareData}
              onValueChange={setShareData}
              trackColor={{ false: '#e5e7eb', true: '#10B981' }}
              thumbColor={shareData ? '#ffffff' : '#f4f3f4'}
            />
          }
        />
      </View>

      {/* Community */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Community</Text>
        
        <SettingItem
          icon="share-social"
          title="Share CarbonScope"
          subtitle="Help friends reduce their carbon footprint"
          onPress={handleShare}
        />
        
        <SettingItem
          icon="chatbubble"
          title="Send Feedback"
          subtitle="Help us improve the app"
          onPress={handleFeedback}
        />
        
        <SettingItem
          icon="star"
          title="Rate the App"
          subtitle="Show your support"
          onPress={() => {
            // TODO: Navigate to app store rating
            Alert.alert('Rate CarbonScope', 'Thank you for your support!');
          }}
        />
      </View>

      {/* About */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>
        
        <SettingItem
          icon="information-circle"
          title="About CarbonScope"
          subtitle="Version 1.0.0"
          onPress={handleAbout}
        />
        
        <SettingItem
          icon="shield-checkmark"
          title="Privacy Policy"
          subtitle="How we protect your data"
          onPress={handlePrivacy}
        />
        
        <SettingItem
          icon="document-text"
          title="Terms of Service"
          subtitle="App usage terms"
          onPress={handleTerms}
        />
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>
          🌍 Made with ❤️ for the planet
        </Text>
        <Text style={styles.footerSubtext}>
          Open source • Community driven • Privacy first
        </Text>
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
    backgroundColor: '#10B981',
    alignItems: 'center',
    paddingVertical: 30,
    paddingHorizontal: 20,
  },
  avatarContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 4,
  },
  userSubtitle: {
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center',
  },
  statsContainer: {
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
  statsGrid: {
    flexDirection: 'row',
    gap: 16,
  },
  statCard: {
    flex: 1,
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 8,
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 12,
    color: '#6b7280',
    textAlign: 'center',
  },
  section: {
    backgroundColor: 'white',
    marginBottom: 12,
    paddingTop: 20,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#f3f4f6',
  },
  settingLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  settingTextContainer: {
    marginLeft: 16,
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#1f2937',
  },
  settingSubtitle: {
    fontSize: 14,
    color: '#6b7280',
    marginTop: 2,
  },
  footer: {
    alignItems: 'center',
    padding: 30,
  },
  footerText: {
    fontSize: 16,
    color: '#1f2937',
    marginBottom: 4,
  },
  footerSubtext: {
    fontSize: 12,
    color: '#6b7280',
    textAlign: 'center',
  },
});