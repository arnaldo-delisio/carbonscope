#!/bin/bash

# CarbonScope Project Setup Script

echo "🌍 Setting up CarbonScope - AI-Powered Carbon Footprint Analyzer"
echo "================================================================="

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Setup backend
echo "Setting up backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "✅ Backend setup complete!"

# Setup frontend
echo "Setting up frontend..."
cd ../frontend

# Install dependencies
npm install

echo "✅ Frontend setup complete!"

# Create environment files
echo "Creating environment files..."

# Backend .env
cat > ../backend/.env << EOF
DATABASE_URL=postgresql://carbonscope:carbonscope_dev@localhost:5432/carbonscope
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
DEBUG=True
EOF

# Frontend .env
cat > .env << EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
EOF

echo "✅ Environment files created!"

# Start services
echo "Starting services with Docker Compose..."
cd ..
docker-compose up -d

echo "🚀 CarbonScope is ready!"
echo ""
echo "📍 Access points:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔧 Development commands:"
echo "   Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "   Frontend: cd frontend && npm start"
echo ""
echo "📚 Documentation: Check the docs/ folder for detailed guides"
echo ""
echo "Happy coding! 🌱"
