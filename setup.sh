#!/bin/bash

echo "🎯 Sports Arbitrage Dashboard Setup"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 16 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python and Node.js are installed${NC}"
echo ""

# Backend Setup
echo -e "${BLUE}📦 Setting up Backend...${NC}"
cd backend

# Create virtual environment
python3 -m venv venv
echo -e "${GREEN}✅ Virtual environment created${NC}"

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo -e "${GREEN}✅ Backend dependencies installed${NC}"
echo ""

# Deactivate for now
deactivate

cd ..

# Frontend Setup
echo -e "${BLUE}📦 Setting up Frontend...${NC}"
cd frontend

# Install dependencies
npm install
echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
echo ""

cd ..

# Done
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo ""
echo "📋 Next Steps:"
echo "1. Get your free API key from: https://the-odds-api.com"
echo "2. Set your API key:"
echo "   export ODDS_API_KEY='your_key_here'"
echo ""
echo "3. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "4. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "5. Open http://localhost:3000 in your browser"
echo ""
echo -e "${GREEN}Happy arbitrage hunting! 🎰💰${NC}"

