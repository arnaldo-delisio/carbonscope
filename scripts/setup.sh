#!/bin/bash

echo "🌍 Setting up CarbonScope - AI-Powered Carbon Footprint Analyzer"
echo "================================================================="

# Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.9+ is required"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js 18+ is required"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "⚠️ Docker is recommended for PostgreSQL"
fi

echo "✅ Prerequisites check passed!"

# Create environment files
echo "📝 Creating environment files..."
if [ ! -f backend/.env ]; then
    cat > backend/.env << EOF
DATABASE_URL=postgresql://carbonscope:carbonscope@localhost:5432/carbonscope
REDIS_URL=redis://localhost:6379
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=true
EOF
    echo "✅ Created backend/.env"
fi

if [ ! -f frontend/.env ]; then
    cat > frontend/.env << EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
EOF
    echo "✅ Created frontend/.env"
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies  
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Install mobile dependencies
echo "📦 Installing mobile dependencies..."
cd mobile
npm install
cd ..

# Start PostgreSQL if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Starting PostgreSQL with Docker..."
    docker run -d \
        --name carbonscope-postgres \
        -e POSTGRES_USER=carbonscope \
        -e POSTGRES_PASSWORD=carbonscope \
        -e POSTGRES_DB=carbonscope \
        -p 5432:5432 \
        postgres:15-alpine || echo "PostgreSQL container already running or failed to start"
    
    # Wait for PostgreSQL to be ready
    echo "⏳ Waiting for PostgreSQL to be ready..."
    sleep 5
    
    # Run database migrations
    echo "🗄️ Setting up database..."
    cd backend
    source venv/bin/activate
    alembic upgrade head
    cd ..
fi

echo "✅ Setup complete! CarbonScope is ready for development."
echo ""
echo "🚀 Next steps:"
echo ""
echo "Backend API:"
echo "  cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  📖 API docs: http://localhost:8000/docs"
echo ""
echo "Frontend Web App:"
echo "  cd frontend && npm start" 
echo "  🌐 App: http://localhost:3000"
echo ""
echo "Mobile App:"
echo "  cd mobile && npm start"
echo "  📱 Follow Expo instructions for device/simulator"
echo ""
echo "🧪 Test the enhanced API:"
echo "  python scripts/test_enhanced_api.py"
echo ""
echo "📊 What's been implemented:"
echo "  ✅ Enhanced backend API with intelligent carbon calculation"
echo "  ✅ Real computer vision material detection"
echo "  ✅ Complete React Native mobile app"
echo "  ✅ PostgreSQL database with comprehensive models"
echo "  ✅ Community verification and contribution system"
echo "  ✅ Advanced alternatives intelligence"
echo "  ✅ Context-aware calculations (shipping, seasonal factors)"
echo "  ✅ Confidence scoring and transparency"
echo ""
echo "🌟 Ready to revolutionize carbon footprint analysis!"
echo "🌍 Build the future of sustainable consumption!"
