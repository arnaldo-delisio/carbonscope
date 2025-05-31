# Development Setup

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- Git

## Local Development

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/carbonscope.git
cd carbonscope
```

### 2. Environment Setup

Create environment files:

```bash
# Backend environment
cp backend/.env.example backend/.env

# Frontend environment  
cp frontend/.env.example frontend/.env
```

### 3. Database Setup

Start PostgreSQL and Redis:

```bash
docker-compose up -d db redis
```

### 4. Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload
```

### 5. Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 6. AI Models Setup

```bash
cd ai-models

# Install ML dependencies
pip install -r requirements.txt

# Download pre-trained models
python scripts/download_models.py

# Start model service
python model_server.py
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Code Quality

### Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

### Linting
```bash
# Backend
flake8 backend/
black backend/

# Frontend
npm run lint
npm run format
```
