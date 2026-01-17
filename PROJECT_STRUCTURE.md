# 📁 Project Structure

```
Sports Arbitrage/
│
├── 📄 README.md                    # Complete documentation
├── 📄 QUICKSTART.md                # 5-minute setup guide
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 🔧 setup.sh                     # Automated setup script
├── 📄 .gitignore                   # Git ignore rules
│
├── 🔙 backend/                     # Python FastAPI Backend
│   ├── 📄 app.py                   # Main FastAPI application
│   ├── 📄 requirements.txt         # Python dependencies
│   └── 📁 utils/
│       └── 📄 arbitrage.py         # Arbitrage calculation utilities
│
├── 🎨 frontend/                    # React/Next.js Frontend
│   ├── 📄 package.json             # Node.js dependencies
│   ├── 📄 next.config.js           # Next.js configuration
│   ├── 📄 tailwind.config.js       # Tailwind CSS config
│   ├── 📄 postcss.config.js        # PostCSS config
│   ├── 📄 SportsArbitrageApp.jsx   # Main application component
│   │
│   ├── 📁 pages/                   # Next.js pages
│   │   ├── 📄 _app.js              # App wrapper
│   │   └── 📄 index.js             # Homepage
│   │
│   ├── 📁 components/              # React components
│   │   ├── 📄 ArbitrageTable.jsx   # Display arbitrage results
│   │   ├── 📄 FilterPanel.jsx      # Filtering controls
│   │   └── 📄 UploadOdds.jsx       # File upload component
│   │
│   └── 📁 styles/                  # CSS styles
│       └── 📄 globals.css          # Global styles
│
└── 📊 data/                        # Sample data
    └── 📄 sample_odds.json         # Example odds data for testing
```

## 🔑 Key Files Explained

### Backend Files

**`backend/app.py`** (Main API)
- FastAPI application with CORS support
- Endpoints for live odds, file upload, odds conversion
- Integration with The Odds API
- Health checks and sports listing

**`backend/utils/arbitrage.py`** (Utilities)
- Odds conversion (American/Fractional → Decimal)
- Two-way arbitrage calculation
- Three-way arbitrage calculation
- Stake distribution algorithms
- Kelly Criterion and EV calculations

**`backend/requirements.txt`**
- fastapi: Web framework
- uvicorn: ASGI server
- pydantic: Data validation
- requests: HTTP client
- python-multipart: File uploads

### Frontend Files

**`frontend/SportsArbitrageApp.jsx`** (Main App)
- View mode tabs (Live/Manual/Upload)
- API integration
- Auto-refresh functionality
- Manual game entry
- State management

**`frontend/components/ArbitrageTable.jsx`**
- Displays arbitrage opportunities
- Profit visualization
- Stake recommendations
- Three-way support

**`frontend/components/FilterPanel.jsx`**
- Sport selection
- Market type filters
- Region selection
- Min profit threshold
- Auto-refresh toggle

**`frontend/components/UploadOdds.jsx`**
- Drag-and-drop file upload
- JSON/CSV support
- Format examples
- Instant analysis

### Configuration Files

**`frontend/package.json`**
- Next.js 14
- React 18
- Tailwind CSS 3
- Lucide React icons

**`frontend/tailwind.config.js`**
- Custom colors (slate-750)
- Content paths for purging
- Responsive utilities

**`frontend/next.config.js`**
- React strict mode enabled
- Production optimizations

### Documentation Files

**`README.md`**
- Complete feature list
- Architecture overview
- API documentation
- Deployment guide
- Mathematical formulas

**`QUICKSTART.md`**
- 5-minute setup guide
- Step-by-step instructions
- Troubleshooting tips
- Quick tips for best results

### Data Files

**`data/sample_odds.json`**
- Example NFL game (Eagles vs Giants)
- Example NBA game (Lakers vs Warriors)
- Example Soccer game with 3-way odds
- Ready to upload and test

## 🚀 Startup Commands

### Option 1: Automated Setup
```bash
./setup.sh
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export ODDS_API_KEY="your_key"
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🌐 URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (automatic Swagger UI)
- **Health Check**: http://localhost:8000/health

## 📊 Data Flow

```
┌─────────────┐
│  The Odds   │
│     API     │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│   FastAPI   │◄─────┤   User File  │
│   Backend   │      │    Upload    │
└──────┬──────┘      └──────────────┘
       │
       │ (REST API)
       │
       ▼
┌─────────────┐
│   Next.js   │
│   Frontend  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Browser   │
│     UI      │
└─────────────┘
```

## 🔧 Tech Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14 | React framework with SSR |
| Styling | Tailwind CSS | Utility-first CSS |
| Icons | Lucide React | Modern icon library |
| Backend | FastAPI | High-performance Python API |
| Server | Uvicorn | ASGI server |
| Data Source | The Odds API | Live sports odds |
| Validation | Pydantic | Type checking and validation |

## 📈 Feature Checklist

- ✅ Live odds fetching from The Odds API
- ✅ Two-way arbitrage detection
- ✅ Three-way arbitrage detection (soccer draws)
- ✅ Multiple input methods (API, manual, upload)
- ✅ CSV/JSON file upload support
- ✅ Odds format conversion (American/Fractional/Decimal)
- ✅ Real-time profit calculations
- ✅ Optimal stake distribution
- ✅ Multi-sport support (NFL, NBA, MLB, NHL, Soccer, etc.)
- ✅ Multi-market support (Moneyline, Spreads, Totals)
- ✅ Multi-region support (US, UK, EU, AU)
- ✅ Filtering by sport, market, and profit threshold
- ✅ Auto-refresh every 60 seconds
- ✅ Beautiful, responsive UI
- ✅ API request tracking
- ✅ Health monitoring
- ✅ Comprehensive documentation

## 🔜 Potential Enhancements

- [ ] Redis caching for odds data
- [ ] PostgreSQL for historical tracking
- [ ] User authentication (JWT)
- [ ] Saved preferences and alerts
- [ ] Email/Discord notifications
- [ ] WebSocket for real-time updates
- [ ] Historical analytics dashboard
- [ ] Machine learning predictions
- [ ] Mobile app (React Native)
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline
- [ ] Unit and integration tests
- [ ] Rate limiting and throttling
- [ ] Multi-currency support
- [ ] Bankroll management tools

