# 🚀 Quick Start Guide

Get your Sports Arbitrage Dashboard running in 5 minutes!

## Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd "Sports Arbitrage/backend"

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your API key (optional for testing)
export ODDS_API_KEY="your_key_here"  # Windows: set ODDS_API_KEY=your_key_here

# Start the backend server
python app.py
```

✅ Backend should be running at `http://localhost:8000`

## Step 2: Frontend Setup (2 minutes)

Open a new terminal:

```bash
# Navigate to frontend directory
cd "Sports Arbitrage/frontend"

# Install dependencies
npm install

# Start the development server
npm run dev
```

✅ Frontend should be running at `http://localhost:3000`

## Step 3: Get Your Free API Key (1 minute)

1. Visit: https://the-odds-api.com
2. Sign up for a free account
3. Get your API key (500 requests/month free)
4. Set it in your backend terminal:
   ```bash
   export ODDS_API_KEY="your_actual_key"
   ```
5. Restart the backend server

## 🎯 You're Done!

Open `http://localhost:3000` in your browser and start finding arbitrage opportunities!

### Quick Tips:

- **No API Key?** Use the "Manual Entry" or "Upload Data" tabs
- **Sample Data**: Upload `data/sample_odds.json` to test
- **Auto-Refresh**: Enable in filters for live updates every 60 seconds
- **Best Results**: Try NFL, NBA, or EPL Soccer with "All Regions"

## 🔧 Troubleshooting

**Backend won't start?**
- Check Python version: `python --version` (need 3.8+)
- Try: `python3` instead of `python`

**Frontend won't start?**
- Check Node version: `node --version` (need 16+)
- Delete `node_modules` and run `npm install` again

**No arbitrages found?**
- Arbitrage opportunities are rare (1-5% of markets)
- Try different sports or lower the min profit filter
- Use manual entry to test with known arbitrage scenarios

**API errors?**
- Verify your API key is set correctly
- Check your request limit (500/month on free tier)
- Visit http://localhost:8000/health to check status

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore different markets (h2h, spreads, totals)
- Try uploading custom odds data
- Set up auto-refresh for live monitoring

---

Happy arbitrage hunting! 🎰💰

