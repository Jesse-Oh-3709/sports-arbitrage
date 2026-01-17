# Sports Arbitrage Detection Dashboard

A lightweight, browser-based arbitrage detection dashboard that finds risk-free betting opportunities across major sportsbooks.

## Features

- **Live Odds Fetching**: Integrates with The Odds API to fetch real-time odds from major sportsbooks
- **Arbitrage Detection**: Automatically detects 2-way and 3-way arbitrage opportunities
- **Multiple Input Methods**: 
  - Live API data fetching
  - Manual odds entry
  - CSV/JSON file upload
- **Smart Calculations**: 
  - Profit margin calculation
  - Optimal stake distribution
  - Guaranteed profit estimates
- **Filtering & Sorting**: Filter by sport, market type, profit threshold, and region
- **Auto-Refresh**: Optional auto-refresh every 60 seconds for live opportunities
- **Beautiful UI**: Modern, responsive dashboard with real-time updates

## Architecture

```
sports-arb-app/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── utils/
│   │   └── arbitrage.py       # Arbitrage calculation utilities
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── SportsArbitrageApp.jsx # Main React application
│   ├── components/
│   │   ├── ArbitrageTable.jsx # Display arbitrage opportunities
│   │   ├── FilterPanel.jsx    # Filtering controls
│   │   └── UploadOdds.jsx     # File upload component
│   └── package.json           # Node dependencies
├── data/
│   └── sample_odds.json       # Sample data for testing
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- The Odds API key (free tier available at https://the-odds-api.com)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   export ODDS_API_KEY="your_api_key_here"
   # On Windows: set ODDS_API_KEY=your_api_key_here
   ```

5. **Run the backend server**:
   ```bash
   python app.py
   # or
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

## API Endpoints

### Backend API

- `GET /` - API information and available endpoints
- `GET /health` - Health check and API key status
- `GET /sports` - List available sports from The Odds API
- `GET /arbitrage/live` - Fetch live odds and find arbitrage opportunities
  - Query params: `sport`, `regions`, `markets`, `min_profit`
- `POST /upload` - Upload CSV/JSON file with manual odds data
- `POST /convert-odds` - Convert odds between formats

### Example Usage

**Fetch live arbitrage opportunities:**
```bash
curl "http://localhost:8000/arbitrage/live?sport=americanfootball_nfl&markets=h2h&regions=us&min_profit=1.0"
```

**Upload manual odds data:**
```bash
curl -X POST -F "file=@data/sample_odds.json" http://localhost:8000/upload
```

## Arbitrage Calculation

### Two-Way Markets (Moneyline)

For two outcomes (Team A vs Team B):

**Arbitrage Condition:**
```
1/Odds_A + 1/Odds_B < 1
```

**Profit Percentage:**
```
Profit% = (1 / (1/Odds_A + 1/Odds_B) - 1) × 100
```

**Example:**
- DraftKings: Team A @ 2.10
- FanDuel: Team B @ 2.05
- Calculation: 1/2.10 + 1/2.05 = 0.964 < 1
- Profit: 3.7%

### Three-Way Markets (Soccer with Draw)

For three outcomes (Home, Draw, Away):

**Arbitrage Condition:**
```
1/Odds_Home + 1/Odds_Draw + 1/Odds_Away < 1
```

### Stake Distribution

**Two-Way:**
```
Stake_A = Total / (1 + Odds_A/Odds_B)
Stake_B = Total - Stake_A
```

**Three-Way:**
```
Each stake proportional to 1/odds (inverse of odds)
```

## Supported Markets

- **h2h** (Head-to-Head / Moneyline): Which team will win
- **spreads**: Point spread betting
- **totals**: Over/Under total points

## Supported Regions

- **US**: American sportsbooks (DraftKings, FanDuel, BetMGM, Caesars, etc.)
- **UK**: British bookmakers (Bet365, William Hill, Ladbrokes, etc.)
- **EU**: European bookmakers
- **AU**: Australian bookmakers

## Data Format

### JSON Upload Format

```json
{
  "games": [
    {
      "match": "Team A vs Team B",
      "sport": "NBA",
      "date": "2025-10-15",
      "bookmakers": [
        {
          "name": "DraftKings",
          "home": 2.10,
          "away": 1.80
        },
        {
          "name": "FanDuel",
          "home": 1.95,
          "away": 1.95
        }
      ]
    }
  ]
}
```

### Three-Way (Soccer) Format

```json
{
  "name": "Bet365",
  "home": 2.75,
  "draw": 3.40,
  "away": 2.60
}
```

## UI Features

### Live Odds View
- Real-time odds from The Odds API
- Auto-refresh every 60 seconds (optional)
- Filter by sport, market, region, and minimum profit
- API request tracking

### Manual Entry View
- Add games manually with custom odds
- Support for multiple sportsbooks per game
- Real-time arbitrage calculation
- Visual profit indicators

### Upload View
- Drag-and-drop file upload
- Support for JSON and CSV formats
- Instant arbitrage analysis
- Detailed formatting examples

## Utilities

The `backend/utils/arbitrage.py` module provides:

- `convert_odds_to_decimal()` - Convert American/Fractional odds to Decimal
- `calculate_arbitrage_two_way()` - Detect 2-way arbitrage
- `calculate_arbitrage_three_way()` - Detect 3-way arbitrage
- `calculate_stakes()` - Optimal stake distribution
- `calculate_implied_probability()` - Get implied probability from odds
- `calculate_kelly_criterion()` - Kelly Criterion bet sizing

## Deployment

### Backend (Python/FastAPI)

**Recommended platforms:**
- **Render**: Free tier available, easy deployment
- **Fly.io**: Global edge deployment
- **Railway**: Simple setup with free tier
- **Heroku**: Classic PaaS option

### Frontend (React/Next.js)

**Recommended platforms:**
- **Vercel**: Optimized for Next.js, free tier
- **Netlify**: Easy deployment, free tier
- **Cloudflare Pages**: Fast global CDN

## Environment Variables

```bash
# Backend
ODDS_API_KEY=your_api_key_here

# Frontend (if using API in production)
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## Future Enhancements

- [ ] Historical arbitrage tracking and analytics
- [ ] Email/Discord alerts for high-profit opportunities
- [ ] User authentication and saved preferences
- [ ] Bankroll management calculator
- [ ] Machine learning for arbitrage prediction
- [ ] Mobile app (React Native)
- [ ] WebSocket for real-time updates
- [ ] Multi-currency support
- [ ] Odds movement tracking

## Disclaimer

**This tool is for educational and informational purposes only.**

- Always check local gambling laws and regulations
- Most sportsbooks prohibit arbitrage betting in their terms of service
- Account limitations or closures may occur
- Odds can change rapidly; execute quickly
- This is not financial advice
- Gamble responsibly

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions:
- Create an issue in the repository
- Check The Odds API documentation: https://the-odds-api.com/liveapi/guides/v4/

## Acknowledgments

- **The Odds API** for providing sports betting odds data
- **FastAPI** for the excellent Python web framework
- **Next.js** and **React** for the frontend framework
- **Tailwind CSS** for styling
- **Lucide React** for icons

---

**Built for sports betting enthusiasts**

