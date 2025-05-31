#!/bin/bash

# CarbonScope Project Verification Script

echo "🔍 Verifying CarbonScope Project Structure"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ $1/${NC}"
    else
        echo -e "${RED}❌ $1/${NC}"
    fi
}

echo "📁 Checking project structure..."

# Root files
check_file "README.md"
check_file "LICENSE"
check_file "ROADMAP.md"
check_file "PROJECT_SUMMARY.md"
check_file "docker-compose.yml"
check_file ".gitignore"

# Directories
check_dir "backend"
check_dir "frontend"
check_dir "ai-models"
check_dir "mobile"
check_dir "data"
check_dir "docs"
check_dir "scripts"
check_dir ".github"

echo ""
echo "📊 Project Statistics:"
echo "----------------------"

# Count files
total_files=$(find . -type f | wc -l)
total_dirs=$(find . -type d | wc -l)
total_lines=$(find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.md" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')

echo "📄 Total files: $total_files"
echo "📁 Total directories: $total_dirs"
echo "📝 Total lines of code/docs: $total_lines"

echo ""
echo "🛠️ Tech Stack Verification:"
echo "----------------------------"

# Backend files
if [ -f "backend/main.py" ]; then
    echo -e "${GREEN}✅ FastAPI backend${NC}"
else
    echo -e "${RED}❌ FastAPI backend${NC}"
fi

if [ -f "backend/requirements.txt" ]; then
    echo -e "${GREEN}✅ Python dependencies${NC}"
else
    echo -e "${RED}❌ Python dependencies${NC}"
fi

# Frontend files
if [ -f "frontend/package.json" ]; then
    echo -e "${GREEN}✅ React frontend${NC}"
else
    echo -e "${RED}❌ React frontend${NC}"
fi

# AI models
if [ -f "ai-models/computer_vision/material_detection.py" ]; then
    echo -e "${GREEN}✅ AI models structure${NC}"
else
    echo -e "${RED}❌ AI models structure${NC}"
fi

# Documentation
doc_count=$(find docs/ -name "*.md" 2>/dev/null | wc -l)
echo -e "${GREEN}✅ Documentation files: $doc_count${NC}"

# Data
if [ -f "data/datasets/carbon_intensity_materials.csv" ]; then
    echo -e "${GREEN}✅ Sample datasets${NC}"
else
    echo -e "${RED}❌ Sample datasets${NC}"
fi

echo ""
echo "🚀 Ready to Build Features:"
echo "--------------------------"
echo "1. 🔍 Barcode + image scanning (backend/app/api/products.py)"
echo "2. 🤖 Material detection AI (ai-models/computer_vision/)"
echo "3. 📊 Dynamic carbon estimation (ai-models/carbon_estimation/)"
echo "4. 🌐 Web interface (frontend/src/)"
echo "5. 📱 Mobile app (mobile/)"

echo ""
echo -e "${YELLOW}💡 Next Steps:${NC}"
echo "1. Run: chmod +x scripts/setup.sh && ./scripts/setup.sh"
echo "2. Start development with: docker-compose up -d"
echo "3. Visit: http://localhost:3000 (frontend) & http://localhost:8000/docs (API)"

echo ""
echo -e "${GREEN}🎉 CarbonScope project is ready for revolutionary development!${NC}"
