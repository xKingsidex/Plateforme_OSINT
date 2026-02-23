#!/bin/bash
# Setup script for OSINT Platform

set -e

echo "🚀 Setting up OSINT Platform..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.9+ required. Current: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo "🧠 Downloading spaCy model..."
python -m spacy download en_core_web_lg

# Create .env from example if not exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
fi

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/raw data/processed data/models logs

# Create .gitkeep files
touch data/raw/.gitkeep data/processed/.gitkeep logs/.gitkeep

# Start Docker services
echo "🐳 Starting Docker services..."
docker-compose up -d postgres neo4j redis

# Wait for services
echo "⏳ Waiting for services to be ready..."
sleep 10

# Create database tables
echo "🗄️  Creating database tables..."
cd backend
python -c "
from models.database import engine, Base
from models.models import Investigation, CollectedData, Alert
Base.metadata.create_all(bind=engine)
print('✅ Database tables created')
"
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📌 Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Activate venv: source venv/bin/activate"
echo "3. Start API: cd backend && uvicorn api.main:app --reload"
echo "4. Open http://localhost:8000/docs"
echo ""
echo "🔗 Useful URLs:"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Neo4j Browser: http://localhost:7474"
echo "   - Flower (Celery): http://localhost:5555 (when enabled)"
