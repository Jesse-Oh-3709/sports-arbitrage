# 📤 Upload Data Feature - Complete Guide

## Overview

The **Upload Data** feature allows you to manually upload odds data in JSON or CSV format for instant arbitrage analysis.

**Use Cases:**
- Test specific arbitrage scenarios
- Import historical odds data
- Work offline without API calls
- Analyze odds from sportsbooks not in The Odds API
- Educational purposes / demonstrations

---

## 📁 Supported File Formats

### 1. **JSON** (Recommended)
- ✅ Most flexible
- ✅ Supports two-way and three-way markets
- ✅ Easy to read and edit

### 2. **CSV**
- ✅ Simple spreadsheet format
- ✅ Good for bulk data
- ⚠️ More limited than JSON

---

## 📊 JSON Format - Complete Structure

### Basic Two-Way Format (NFL, NBA, MLB, NHL)

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

### Three-Way Format (Soccer with Draw)

```json
{
  "games": [
    {
      "match": "Manchester United vs Liverpool",
      "sport": "Soccer",
      "date": "2025-10-20",
      "bookmakers": [
        {
          "name": "Bet365",
          "home": 2.75,
          "draw": 3.40,
          "away": 2.60
        },
        {
          "name": "William Hill",
          "home": 2.80,
          "draw": 3.30,
          "away": 2.55
        }
      ]
    }
  ]
}
```

### Multiple Games Example

```json
{
  "games": [
    {
      "match": "Eagles vs Giants",
      "sport": "NFL",
      "date": "2025-10-15",
      "bookmakers": [
        {"name": "FanDuel", "home": 2.10, "away": 1.82},
        {"name": "DraftKings", "home": 1.95, "away": 2.05},
        {"name": "BetMGM", "home": 2.05, "away": 1.90}
      ]
    },
    {
      "match": "Lakers vs Warriors",
      "sport": "NBA",
      "date": "2025-10-16",
      "bookmakers": [
        {"name": "Caesars", "home": 1.85, "away": 2.15},
        {"name": "FanDuel", "home": 1.90, "away": 2.00}
      ]
    }
  ]
}
```

---

## 📋 Field Descriptions

### Game Level:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `match` | string | Yes | Team names or match description | "Eagles vs Giants" |
| `sport` | string | Yes | Sport name | "NFL", "NBA", "MLB", "Soccer" |
| `date` | string | Optional | Game date (for reference) | "2025-10-15" |
| `bookmakers` | array | Yes | List of sportsbook odds | See below |

### Bookmaker Level:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `name` | string | Yes | Sportsbook name | "DraftKings", "FanDuel" |
| `home` | number | Yes* | Home team odds (decimal) | 2.10 |
| `away` | number | Yes* | Away team odds (decimal) | 1.80 |
| `draw` | number | Optional | Draw odds (soccer only) | 3.40 |

*For two-way markets, you need `home` and `away`. For three-way markets, add `draw`.

---

## 💡 Alternative Field Names

The system accepts multiple naming conventions:

### Home/Away Format:
```json
{
  "name": "DraftKings",
  "home": 2.10,
  "away": 1.80
}
```

### Team 1/Team 2 Format:
```json
{
  "name": "FanDuel",
  "odds1": 2.10,
  "odds2": 1.80
}
```

Both work interchangeably!

---

## 📊 CSV Format

### Basic CSV Structure:
```csv
match,sport,date,sportsbook,home,away
Eagles vs Giants,NFL,2025-10-15,FanDuel,2.10,1.82
Eagles vs Giants,NFL,2025-10-15,DraftKings,1.95,2.05
Lakers vs Warriors,NBA,2025-10-16,FanDuel,1.90,2.00
Lakers vs Warriors,NBA,2025-10-16,DraftKings,1.88,2.05
```

**Note**: CSV format requires one row per sportsbook per game.

---

## 🎯 Examples by Sport

### NFL Example:
```json
{
  "games": [
    {
      "match": "Kansas City Chiefs vs Buffalo Bills",
      "sport": "NFL",
      "date": "2025-10-20",
      "bookmakers": [
        {
          "name": "DraftKings",
          "home": 1.85,
          "away": 2.05
        },
        {
          "name": "FanDuel",
          "home": 1.91,
          "away": 1.95
        },
        {
          "name": "ESPN BET",
          "home": 1.88,
          "away": 2.00
        }
      ]
    }
  ]
}
```

### NBA Example:
```json
{
  "games": [
    {
      "match": "Los Angeles Lakers vs Boston Celtics",
      "sport": "NBA",
      "date": "2025-10-18",
      "bookmakers": [
        {
          "name": "DraftKings",
          "home": 2.20,
          "away": 1.70
        },
        {
          "name": "FanDuel",
          "home": 2.15,
          "away": 1.75
        }
      ]
    }
  ]
}
```

### MLB Example:
```json
{
  "games": [
    {
      "match": "New York Yankees vs Boston Red Sox",
      "sport": "MLB",
      "date": "2025-10-12",
      "bookmakers": [
        {
          "name": "DraftKings",
          "home": 1.77,
          "away": 2.10
        },
        {
          "name": "BetMGM",
          "home": 1.80,
          "away": 2.05
        }
      ]
    }
  ]
}
```

### Soccer (Three-Way) Example:
```json
{
  "games": [
    {
      "match": "Real Madrid vs Barcelona",
      "sport": "Soccer",
      "date": "2025-10-25",
      "bookmakers": [
        {
          "name": "Bet365",
          "home": 2.10,
          "draw": 3.50,
          "away": 3.20
        },
        {
          "name": "William Hill",
          "home": 2.15,
          "draw": 3.40,
          "away": 3.10
        }
      ]
    }
  ]
}
```

---

## 🔢 Odds Format Support

The system automatically detects and converts odds formats:

### Decimal (Recommended):
```json
{
  "name": "DraftKings",
  "home": 1.91,
  "away": 2.10
}
```

### American Odds (Also Supported):
```json
{
  "name": "FanDuel",
  "home": -110,
  "away": 110
}
```
*Will be auto-converted to decimal (1.91, 2.10)*

### Fractional Odds (Also Supported):
```json
{
  "name": "Bet365",
  "home": "10/11",
  "away": "11/10"
}
```
*Will be auto-converted to decimal (1.91, 2.10)*

---

## 📝 Minimum Requirements

### Minimum Valid JSON:
```json
{
  "games": [
    {
      "match": "Team A vs Team B",
      "sport": "Any Sport",
      "bookmakers": [
        {"name": "Book A", "home": 2.00, "away": 2.00},
        {"name": "Book B", "home": 2.05, "away": 1.95}
      ]
    }
  ]
}
```

**Requirements:**
- ✅ At least 1 game
- ✅ At least 2 bookmakers per game
- ✅ `match`, `sport` fields present
- ✅ Each bookmaker has `name` and odds (`home`/`away`)

---

## 🚫 Sportsbook Filtering

**Important**: The system only uses your 7 whitelisted sportsbooks:
- DraftKings
- FanDuel
- ESPN BET
- BetMGM
- Caesars Sportsbook
- Fanatics Sportsbook
- Bally Bet

**Other sportsbooks will be silently ignored.**

### Example:
```json
{
  "bookmakers": [
    {"name": "DraftKings", "home": 2.10, "away": 1.80},  // ✅ Included
    {"name": "Bovada", "home": 2.20, "away": 1.75},      // ❌ Ignored (offshore)
    {"name": "FanDuel", "home": 1.95, "away": 2.00}      // ✅ Included
  ]
}
```
*Result: Only DraftKings and FanDuel odds will be analyzed*

---

## 🎯 How It Works

### 1. Upload File
- Click **"Upload Data"** tab
- Drag & drop or click to select file
- Accept: `.json` or `.csv`

### 2. Processing
```
Your File → Backend API → Validation → Arbitrage Detection → Results
```

### 3. Analysis
- Filters to whitelisted sportsbooks
- Converts odds to decimal format
- Calculates all possible arbitrage combinations
- Applies validation (odds range, implied probability)
- Assigns confidence tiers

### 4. Results
- Displays arbitrage opportunities found
- Shows in same format as Live Odds
- Includes all validation warnings

---

## 📊 Sample Files Provided

### Pre-made Test File:
```
/data/sample_odds.json
```

**Contains:**
- NFL game (Eagles vs Giants)
- NBA game (Lakers vs Warriors)
- Soccer game with draw (Man United vs Liverpool)

**To Use:**
1. Go to "Upload Data" tab
2. Upload `/data/sample_odds.json`
3. See instant arbitrage analysis!

---

## 🧪 Testing Examples

### Example 1: Simple Arbitrage
```json
{
  "games": [{
    "match": "Test Game",
    "sport": "NBA",
    "bookmakers": [
      {"name": "DraftKings", "home": 2.08, "away": 1.80},
      {"name": "FanDuel", "home": 1.90, "away": 2.06}
    ]
  }]
}
```
*Expected: Should find arbitrage between DK away (1.80) vs FD away (2.06)... wait, checking math... 1/1.80 + 1/2.06 = 1.04 > 1, no arb*

### Example 2: Known Arbitrage
```json
{
  "games": [{
    "match": "Arbitrage Test",
    "sport": "Test",
    "bookmakers": [
      {"name": "DraftKings", "home": 2.08, "away": 1.80},
      {"name": "FanDuel", "home": 1.90, "away": 2.06}
    ]
  }]
}
```
*Will check: DK home (2.08) vs FD away (2.06): 1/2.08 + 1/2.06 = 0.9662 < 1 ✅ Arbitrage!*

### Example 3: Mixed Formats
```json
{
  "games": [{
    "match": "Format Test",
    "sport": "NFL",
    "bookmakers": [
      {"name": "DraftKings", "home": -110, "away": -110},
      {"name": "FanDuel", "home": 2.10, "away": "10/11"},
      {"name": "ESPN BET", "home": "+105", "away": 1.91}
    ]
  }]
}
```
*All formats auto-converted to decimal!*

---

## ⚠️ Common Mistakes

### ❌ Mistake 1: Single Bookmaker
```json
{
  "games": [{
    "match": "Bad Example",
    "sport": "NBA",
    "bookmakers": [
      {"name": "DraftKings", "home": 2.10, "away": 1.80}
    ]
  }]
}
```
**Error**: Need at least 2 bookmakers for arbitrage detection

### ❌ Mistake 2: Missing Required Fields
```json
{
  "games": [{
    "match": "Lakers vs Celtics",
    "bookmakers": [
      {"name": "DraftKings", "home": 2.10}
    ]
  }]
}
```
**Error**: Missing `sport` field and `away` odds

### ❌ Mistake 3: Non-Whitelisted Sportsbooks
```json
{
  "games": [{
    "match": "Test",
    "sport": "NBA",
    "bookmakers": [
      {"name": "UnknownBook", "home": 2.10, "away": 1.80},
      {"name": "AnotherBook", "home": 1.95, "away": 2.05}
    ]
  }]
}
```
**Result**: Both sportsbooks ignored (not whitelisted), no arbitrage found

---

## ✅ Best Practices

### 1. **Use Decimal Odds** (Easiest)
```json
"home": 1.91,
"away": 2.10
```

### 2. **Include Multiple Books** (More Opportunities)
```json
"bookmakers": [
  {"name": "DraftKings", "home": 2.10, "away": 1.80},
  {"name": "FanDuel", "home": 1.95, "away": 1.95},
  {"name": "BetMGM", "home": 2.05, "away": 1.85},
  {"name": "ESPN BET", "home": 2.08, "away": 1.82}
]
```

### 3. **Use Whitelisted Sportsbooks**
Only these will be analyzed:
- DraftKings
- FanDuel
- ESPN BET
- BetMGM
- Caesars Sportsbook
- Fanatics Sportsbook
- Bally Bet

### 4. **Validate JSON Before Upload**
Use a JSON validator: https://jsonlint.com

---

## 📝 CSV Format

### Structure:
```
match, sport, date, sportsbook, home, away
```

### Example CSV:
```csv
match,sport,date,sportsbook,home,away
Eagles vs Giants,NFL,2025-10-15,FanDuel,2.10,1.82
Eagles vs Giants,NFL,2025-10-15,DraftKings,1.95,2.05
Eagles vs Giants,NFL,2025-10-15,BetMGM,2.05,1.90
Lakers vs Warriors,NBA,2025-10-16,FanDuel,1.90,2.00
Lakers vs Warriors,NBA,2025-10-16,DraftKings,1.88,2.05
```

**Note**: Each row is one sportsbook for one game. Multiple rows for same game = multiple sportsbooks.

### CSV with Draw (Soccer):
```csv
match,sport,date,sportsbook,home,draw,away
Man United vs Liverpool,Soccer,2025-10-20,Bet365,2.75,3.40,2.60
Man United vs Liverpool,Soccer,2025-10-20,William Hill,2.80,3.30,2.55
```

---

## 🔄 Processing Flow

```
1. Upload File
   ↓
2. Detect Format (JSON or CSV)
   ↓
3. Parse Content
   ↓
4. Filter to Whitelisted Sportsbooks
   ↓
5. Convert All Odds to Decimal
   ↓
6. Find All Possible Arbitrage Pairs
   ↓
7. Apply Validation:
   - Odds range (1.1 - 15.0)
   - Implied probability (0.80 - 1.10)
   - Confidence tier assignment
   ↓
8. Return Results
   ↓
9. Display in UI
```

---

## 📤 Upload Process

### Step-by-Step:

**1. Navigate to Upload Tab**
- Open http://localhost:3000
- Click **"Upload Data"** tab

**2. Select File**
- Drag & drop your JSON/CSV file
- Or click to browse and select

**3. Verify File**
- File name and size shown
- Green checkmark if valid format

**4. Upload**
- Click **"Upload and Analyze"**
- Processing happens instantly

**5. View Results**
- Automatically switches to results view
- Shows all arbitrage opportunities found
- Same display as Live Odds

---

## 🎨 UI Features

### Drag & Drop Area:
```
┌─────────────────────────────────────┐
│  📤                                  │
│  Click to upload or drag and drop   │
│  JSON or CSV files only             │
└─────────────────────────────────────┘
```

### File Preview:
```
┌─────────────────────────────────────┐
│ 📄 sample_odds.json    ✕            │
│    3.24 KB                          │
└─────────────────────────────────────┘
```

### Format Example (Built-in):
Shows complete JSON format example in the UI for reference.

---

## 🧮 Example: What Gets Analyzed

### Your Upload:
```json
{
  "games": [{
    "match": "Eagles vs Giants",
    "sport": "NFL",
    "bookmakers": [
      {"name": "FanDuel", "home": 2.10, "away": 1.82},
      {"name": "DraftKings", "home": 1.95, "away": 2.05},
      {"name": "BetMGM", "home": 2.05, "away": 1.90}
    ]
  }]
}
```

### System Checks:
```
Possible combinations:
1. FanDuel home (2.10) vs DraftKings away (2.05)
2. FanDuel home (2.10) vs BetMGM away (1.90)
3. FanDuel away (1.82) vs DraftKings home (1.95)
4. FanDuel away (1.82) vs BetMGM home (2.05)
5. DraftKings home (1.95) vs BetMGM away (1.90)
6. DraftKings away (2.05) vs BetMGM home (2.05)

For each combination:
✅ Convert odds to decimal
✅ Check: 1/o1 + 1/o2 < 1?
✅ Validate odds range
✅ Validate implied probability
✅ Calculate stakes
✅ Assign confidence tier
```

### Result:
```
Found 1 arbitrage:
FanDuel: Eagles @ 2.10
DraftKings: Giants @ 2.05
ROI: 3.7%
Confidence: Moderate ⚡
```

---

## 💾 Sample File Location

Your project includes a ready-to-use sample:

**Path**: `/Users/jesseoh/Desktop/Sports Arbitrage/data/sample_odds.json`

**Contains:**
- NFL game with 3 sportsbooks
- NBA game with 3 sportsbooks
- Soccer game with 3 sportsbooks (includes draw)

**To Use:**
1. Go to "Upload Data" tab
2. Click to upload
3. Navigate to `data/sample_odds.json`
4. Click "Open"
5. Click "Upload and Analyze"
6. See results instantly!

---

## 🎯 Response Format

### Success Response:
```json
{
  "success": true,
  "count": 2,
  "arbitrages": [
    {
      "match": "Eagles vs Giants",
      "sport": "NFL",
      "market": "h2h",
      "sportsbook_a": "FanDuel",
      "odds_a": 2.10,
      "outcome_a": "Home/Team A",
      "sportsbook_b": "DraftKings",
      "odds_b": 2.05,
      "outcome_b": "Away/Team B",
      "profit_percentage": 3.7,
      "implied_probability": 0.9638,
      "stake_a": 493.97,
      "stake_b": 506.03,
      "guaranteed_profit": 37.00,
      "warning": {
        "level": "moderate",
        "emoji": "⚡",
        "message": "High ROI - Act quickly"
      }
    }
  ]
}
```

### Error Response:
```json
{
  "detail": "Only JSON and CSV files are supported"
}
```

---

## 🔍 Validation Applied

All uploaded data goes through the same hardened validation:

✅ **Odds Range**: 1.1 - 15.0  
✅ **Implied Probability**: 0.80 - 1.10  
✅ **Sportsbook Whitelist**: Only 7 approved books  
✅ **Format Detection**: Auto-converts American/Fractional  
✅ **Confidence Tiers**: Low/Moderate/Verify  

**Bad data is rejected automatically!**

---

## 📚 Use Cases

### 1. **Testing Specific Scenarios**
Create custom odds to test arbitrage calculations

### 2. **Historical Analysis**
Upload past odds data to analyze historical opportunities

### 3. **Offline Work**
No API key needed for upload feature

### 4. **Manual Data Entry**
If you have odds from sportsbooks not in the API

### 5. **Education/Demonstrations**
Show how arbitrage works with controlled examples

---

## 💡 Pro Tips

### Tip 1: Test with Known Arbitrage
```json
{
  "bookmakers": [
    {"name": "DraftKings", "home": 2.08, "away": 1.80},
    {"name": "FanDuel", "home": 1.85, "away": 2.06}
  ]
}
```
*Checking: 1/2.08 + 1/2.06 = 0.9662 < 1 ✅ Arbitrage exists!*

### Tip 2: Include Many Sportsbooks
More books = more combinations = higher chance of finding arbitrage

### Tip 3: Use Realistic Odds
Keep odds in realistic ranges (1.5 - 3.0 for most sports)

### Tip 4: Save Templates
Create JSON templates for different sports to reuse

---

## 🚀 Quick Test

### Download sample file:
```bash
# File is already in your project
cat "/Users/jesseoh/Desktop/Sports Arbitrage/data/sample_odds.json"
```

### Upload via UI:
1. Go to http://localhost:3000
2. Click **"Upload Data"**
3. Upload `data/sample_odds.json`
4. See arbitrage analysis!

### Upload via API:
```bash
curl -X POST \
  http://localhost:8000/upload \
  -F "file=@/Users/jesseoh/Desktop/Sports Arbitrage/data/sample_odds.json"
```

---

## 📊 Expected Results from Sample File

When you upload `sample_odds.json`, you should see:

### NFL Game (Eagles vs Giants):
- Analyzes 3 books: FanDuel, DraftKings, BetMGM
- Finds arbitrage opportunities (if any)
- Shows in American odds format

### NBA Game (Lakers vs Warriors):
- Analyzes 3 books: Caesars, FanDuel, DraftKings
- Calculates all combinations
- Validates all results

### Soccer Game (Man United vs Liverpool):
- Three-way market (home/draw/away)
- More complex combinations
- Higher potential for arbitrage

---

## 📖 API Documentation

**Endpoint**: `POST /upload`

**Content-Type**: `multipart/form-data`

**Parameters**:
- `file`: JSON or CSV file

**Example with curl**:
```bash
curl -X POST \
  http://localhost:8000/upload \
  -F "file=@my_odds.json"
```

**Example with Python**:
```python
import requests

with open('my_odds.json', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload',
        files={'file': f}
    )
    data = response.json()
    print(f"Found {data['count']} arbitrages")
```

---

## ✅ Summary

**Upload Data Feature:**
- ✅ Accepts JSON and CSV files
- ✅ Auto-detects and converts odds formats
- ✅ Filters to whitelisted sportsbooks
- ✅ Applies full validation
- ✅ Instant arbitrage analysis
- ✅ Same display as Live Odds
- ✅ No API key required

**Format Requirements:**
- At least 1 game
- At least 2 bookmakers per game
- Required fields: match, sport, bookmakers
- Each bookmaker needs: name, home, away (and draw for soccer)

**Validation:**
- Same hardened engine as Live Odds
- Confidence tiers applied
- Invalid data rejected
- Clear error messages

---

**Ready to test? Upload `data/sample_odds.json` right now!** 📤

http://localhost:3000 → Upload Data tab → Upload file → See results!

