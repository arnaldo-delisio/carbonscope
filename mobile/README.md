# CarbonScope Mobile App

React Native mobile application for CarbonScope - AI-powered carbon footprint analysis.

## Features

### 🔍 **Product Scanning**
- **Barcode Scanner**: Camera-based barcode scanning with real-time detection
- **Manual Entry**: Manual barcode input for quick analysis
- **Image Analysis**: Photo capture for material detection (coming soon)

### 📊 **Carbon Analysis**
- **Real-time Calculation**: Instant carbon footprint analysis
- **Detailed Breakdown**: Production, transport, packaging emissions
- **Impact Classification**: Low/Medium/High/Very High impact levels
- **Confidence Scoring**: Transparency about estimate reliability

### 💡 **Smart Alternatives**
- **Lower-carbon Options**: Eco-friendly product suggestions
- **Savings Calculation**: Exact CO₂ reduction amounts
- **Availability Info**: Where to find alternatives

### 📱 **Mobile-Optimized UX**
- **Bottom Tab Navigation**: Easy access to all features
- **Native Performance**: Smooth 60fps animations
- **Offline Capability**: Basic functionality without internet
- **Share Results**: Share carbon analysis with friends

## Tech Stack

- **React Native 0.72** - Cross-platform mobile framework
- **Expo 49** - Development and deployment platform
- **TypeScript** - Type-safe development
- **React Navigation 6** - Navigation library
- **Expo Camera/Barcode Scanner** - Camera functionality
- **Vector Icons** - Consistent iconography

## Setup

### Prerequisites
- Node.js 18+
- Expo CLI
- iOS Simulator (macOS) or Android Studio

### Installation

1. **Install dependencies**:
   ```bash
   cd mobile
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm start
   ```

3. **Run on device/simulator**:
   ```bash
   # iOS (requires macOS and Xcode)
   npm run ios
   
   # Android (requires Android Studio)
   npm run android
   
   # Web (for testing)
   npm run web
   ```

## App Structure

```
mobile/
├── App.tsx                 # Main app component with navigation
├── src/
│   └── screens/
│       ├── HomeScreen.tsx      # Welcome screen with features overview
│       ├── ScanScreen.tsx      # Barcode scanning interface
│       ├── ResultScreen.tsx    # Analysis results display
│       ├── HistoryScreen.tsx   # Scan history and statistics
│       └── ProfileScreen.tsx   # Settings and user profile
├── assets/                 # Images, icons, and other assets
├── app.json               # Expo configuration
└── package.json           # Dependencies and scripts
```

## Key Features

### Camera Integration
- **Barcode Scanner**: Real-time barcode detection using device camera
- **Image Capture**: Photo capture for future material analysis
- **Permissions**: Proper camera and photo library permissions

### Navigation
- **Tab Navigation**: Bottom tabs for main screens
- **Stack Navigation**: Nested navigation for scan flow
- **Type Safety**: Full TypeScript navigation types

### Connectivity
- **API Integration**: Connects to CarbonScope backend API
- **Error Handling**: Graceful handling of network issues
- **Loading States**: Smooth loading indicators

### User Experience
- **Native Feel**: Platform-specific design patterns
- **Accessibility**: Screen reader and accessibility support
- **Performance**: Optimized for smooth 60fps performance

## API Integration

The mobile app connects to the CarbonScope backend API at `http://localhost:8000` for development.

### Endpoints Used
- `POST /api/v1/products/scan` - Product carbon analysis
- `GET /api/v1/products/history` - Scan history (future)
- `POST /api/v1/community/verify` - Community verification (future)

## Development

### Testing Barcodes
- `1234567890123` - Coca-Cola 330ml (Low impact)
- `7890123456789` - iPhone 15 Pro (Very High impact)
- `5432109876543` - Organic Bananas (Medium impact)

### Adding New Screens
1. Create screen component in `src/screens/`
2. Add navigation types
3. Update navigation configuration in `App.tsx`

### Styling
- Uses React Native StyleSheet API
- Consistent color scheme with web app
- Responsive design for different screen sizes

## Future Enhancements

### Phase 3 Features
- **Computer Vision**: Real-time material detection from camera
- **AR Visualization**: Augmented reality carbon visualization
- **Offline Mode**: Full functionality without internet
- **Push Notifications**: Carbon-saving tips and reminders

### Community Features
- **User Accounts**: Profile creation and sync
- **Data Sharing**: Contribute to community database
- **Leaderboards**: Community carbon reduction tracking
- **Social Sharing**: Share results on social media

## Build and Deployment

### Development Build
```bash
expo build:android
expo build:ios
```

### Production Build
```bash
expo build:android --type app-bundle
expo build:ios --type archive
```

### App Store Submission
- Configure app.json with store metadata
- Add required assets (icons, splash screens)
- Follow platform-specific guidelines

## Performance

- **Bundle Size**: Optimized for minimal download size
- **Memory Usage**: Efficient memory management
- **Battery Life**: Optimized camera and API usage
- **Startup Time**: Fast app initialization

---

**Ready to scan products and analyze their carbon footprint on mobile!** 📱🌍