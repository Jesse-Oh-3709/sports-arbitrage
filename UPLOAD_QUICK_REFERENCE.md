# 📤 Upload Data - Quick Reference Card

## 🎯 What It Does

Upload a JSON or CSV file with sportsbook odds → Get instant arbitrage analysis

**No API key required!** Perfect for testing and offline use.

---

## ⚡ Quick Example - Copy & Paste Ready

### Minimal Working Example:
```json
{
  "games": [
    {
      "match": "Team A vs Team B",
      "sport": "NBA",
      "bookmakers": [
        {"name": "DraftKings", "home": 2.08, "away": 1.80},
        {"name": "FanDuel", "home": 1.90, "away": 2.06}
      ]
    }
  ]
}
```

**Save as**: `my_odds.json`  
**Upload**: Go to "Upload Data" tab → Upload file  
**Result**: Instant arbitrage analysis!

---

## 📋 Required Fields

### JSON Structure:
```
{
  "games": [                    ← Array of games
    {
      "match": "...",            ← Game name (required)
      "sport": "...",            ← Sport type (required)
      "date": "...",             ← Optional
      "bookmakers": [            ← Array of sportsbooks (min 2)
        {
          "name": "...",         ← Sportsbook name (required)
          "home": X.XX,          ← Home odds (required)
          "away": X.XX           ← Away odds (required)
        }
      ]
    }
  ]
}
```

---

## 🏈 Sport-Specific Examples

### NFL:
```json
{
  "games": [{
    "match": "Chiefs vs Bills",
    "sport": "NFL",
    "bookmakers": [
      {"name": "DraftKings", "home": 1.91, "away": 1.95},
      {"name": "FanDuel", "home": 1.88, "away": 2.00}
    ]
  }]
}
```

### NBA:
```json
{
  "games": [{
    "match": "Lakers vs Celtics",
    "sport": "NBA",
    "bookmakers": [
      {"name": "DraftKings", "home": 2.20, "away": 1.70},
      {"name": "ESPN BET", "home": 2.15, "away": 1.75}
    ]
  }]
}
```

### MLB:
```json
{
  "games": [{
    "match": "Yankees vs Red Sox",
    "sport": "MLB",
    "bookmakers": [
      {"name": "DraftKings", "home": 1.77, "away": 2.10},
      {"name": "BetMGM", "home": 1.80, "away": 2.05}
    ]
  }]
}
```

### Soccer (3-Way):
```json
{
  "games": [{
    "match": "Real Madrid vs Barcelona",
    "sport": "Soccer",
    "bookmakers": [
      {"name": "Bet365", "home": 2.10, "draw": 3.50, "away": 3.20}
    ]
  }]
}
```

---

## 🔢 Odds Format - All Supported

### Decimal (Recommended):
```json
{"name": "DraftKings", "home": 1.91, "away": 2.10}
```

### American:
```json
{"name": "FanDuel", "home": -110, "away": 110}
```

### Fractional:
```json
{"name": "Bet365", "home": "10/11", "away": "11/10"}
```

### Mixed (All Work Together):
```json
{"name": "DraftKings", "home": 1.91, "away": 2.10},
{"name": "FanDuel", "home": -110, "away": "+110"},
{"name": "BetMGM", "home": "10/11", "away": "21/20"}
```

---

## ✅ Whitelisted Sportsbooks Only

**These will be analyzed:**
- DraftKings ✅
- FanDuel ✅
- ESPN BET ✅
- BetMGM ✅
- Caesars Sportsbook ✅
- Fanatics Sportsbook ✅
- Bally Bet ✅

**All others will be ignored** (offshore, regional, etc.)

---

## 📊 CSV Format Cheat Sheet

### Template:
```csv
match,sport,date,sportsbook,home,away
[Game Name],[Sport],[Date],[Book Name],[Home Odds],[Away Odds]
```

### Example:
```csv
match,sport,date,sportsbook,home,away
Chiefs vs Bills,NFL,2025-10-20,DraftKings,1.91,1.95
Chiefs vs Bills,NFL,2025-10-20,FanDuel,1.88,2.00
Lakers vs Celtics,NBA,2025-10-18,DraftKings,2.20,1.70
Lakers vs Celtics,NBA,2025-10-18,FanDuel,2.15,1.75
```

**Rules:**
- Header row required
- One row per sportsbook per game
- Comma-separated values
- Quotes optional for text fields

---

## 🧪 Test File Included

**Location**: `data/sample_odds.json`

**Try it now:**
1. Open http://localhost:3000
2. Click "Upload Data"
3. Upload `sample_odds.json` from data folder
4. See instant arbitrage analysis!

---

## ⚠️ Common Errors & Fixes

### Error: "Only JSON and CSV files are supported"
**Fix**: Make sure file has `.json` or `.csv` extension

### Error: No arbitrages found
**Possible causes:**
- Using non-whitelisted sportsbooks
- Odds don't create arbitrage (implied prob > 1)
- Less than 2 bookmakers per game
**Fix**: Check your odds and sportsbook names

### Error: Invalid JSON
**Possible causes:**
- Missing commas
- Extra commas
- Unmatched brackets
**Fix**: Validate at https://jsonlint.com

---

## 💡 Quick Tips

### ✅ DO:
- Use decimal odds (1.91, 2.10) - easiest
- Include 3+ sportsbooks per game
- Use whitelisted sportsbooks only
- Validate JSON before uploading
- Keep odds realistic (1.5 - 3.0)

### ❌ DON'T:
- Use only 1 sportsbook (need min 2)
- Forget required fields (match, sport)
- Use non-whitelisted books
- Upload invalid JSON
- Use odds outside 1.1 - 15.0 range

---

## 🎨 UI Preview

```
╔═══════════════════════════════════════╗
║  📤 Upload Odds Data                  ║
╠═══════════════════════════════════════╣
║                                       ║
║  ┌─────────────────────────────────┐ ║
║  │  📤                              │ ║
║  │  Click to upload or drag & drop │ ║
║  │  JSON or CSV files only         │ ║
║  └─────────────────────────────────┘ ║
║                                       ║
║  📄 sample_odds.json    ✕            ║
║     3.24 KB                          ║
║                                       ║
║  [Upload and Analyze]                ║
║                                       ║
║  Expected JSON format:               ║
║  {                                   ║
║    "games": [...]                    ║
║  }                                   ║
╚═══════════════════════════════════════╝
```

---

## 🚀 Try It Now!

**3 Steps:**
1. Copy the minimal example above
2. Save as `test.json`
3. Upload at http://localhost:3000 → Upload Data

**Or use the included sample:**
- Navigate to "Upload Data" tab
- Upload `data/sample_odds.json`
- See 3 games analyzed instantly!

---

## 📖 Full Documentation

For complete details, see: [UPLOAD_DATA_GUIDE.md](UPLOAD_DATA_GUIDE.md)

---

## ✅ Summary

**Supported Formats**: JSON, CSV  
**Required Fields**: match, sport, bookmakers (with name, home, away)  
**Odds Formats**: Decimal, American, Fractional (auto-detected)  
**Validation**: Same hardened engine as Live Odds  
**Sportsbooks**: Only your 7 whitelisted books analyzed  

**Perfect for**: Testing, offline use, manual data, historical analysis

---

**Upload your first file in seconds!** 📤

