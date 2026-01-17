# 📊 Google Sheets Integration Guide

## Overview

I've added **TWO ways** to use your arbitrage data in Google Sheets:

1. **Export to CSV** (Simple) - One-click export button
2. **Google Apps Script** (Advanced) - Live updates from your API

---

## ✅ Method 1: Export to CSV (Easiest)

### New Feature Added: Export Button

I just added an **"Export to CSV"** button to your dashboard!

### How to Use:

**Step 1: Find Arbitrages**
- Go to http://localhost:3000
- Click "Live Odds (API)" or upload data
- Click "Refresh Odds" to get arbitrages

**Step 2: Export**
- Click **"Export to CSV"** button (top right)
- File downloads automatically: `arbitrage_opportunities_2025-10-10.csv`

**Step 3: Import to Google Sheets**
- Open Google Sheets (sheets.google.com)
- Create new spreadsheet
- Go to **File → Import → Upload**
- Select your downloaded CSV
- Choose "Replace current sheet"
- Click "Import data"

**Done!** Your arbitrage data is now in Google Sheets! 📊

---

## 📋 CSV Format

The exported CSV includes these columns:

| Column | Example | Description |
|--------|---------|-------------|
| Match | Vikings vs Eagles | Game matchup |
| Sport | NFL | Sport type |
| Market | h2h | Market type |
| Game Time | Sun 1:00 PM | When game starts |
| Sportsbook A | DraftKings | First book |
| Outcome A | Eagles | Team/outcome |
| Odds A (American) | -130 | American format |
| Odds A (Decimal) | 1.77 | Decimal format |
| Sportsbook B | ESPN BET | Second book |
| Outcome B | Vikings | Team/outcome |
| Odds B (American) | +130 | American format |
| Odds B (Decimal) | 2.30 | Decimal format |
| Profit % | 0.02% | ROI percentage |
| Implied Probability | 99.98% | Total implied prob |
| Stake A ($1000) | 565.11 | How much to bet on A |
| Stake B ($1000) | 434.89 | How much to bet on B |
| Guaranteed Profit | 0.25 | Profit amount |
| Confidence | low | Confidence tier |
| Warning Message | Low profit margin | Warning text |

---

## 🚀 Method 2: Google Apps Script (Live Updates)

For **automatic live updates** directly from your API to Google Sheets:

### Setup Instructions:

**Step 1: Create Google Sheet**
- Go to sheets.google.com
- Create new blank spreadsheet
- Name it "Sports Arbitrage Tracker"

**Step 2: Open Script Editor**
- Click **Extensions → Apps Script**
- Delete any default code

**Step 3: Copy This Script**

```javascript
// Sports Arbitrage API to Google Sheets
// Update these settings:
const API_URL = 'http://localhost:8000/arbitrage/live';
const SPORT = 'americanfootball_nfl';
const REGIONS = 'us,us2';
const MARKETS = 'h2h';
const MIN_PROFIT = 0;

function fetchArbitrages() {
  const url = `${API_URL}?sport=${SPORT}&regions=${REGIONS}&markets=${MARKETS}&min_profit=${MIN_PROFIT}&include_live=false`;
  
  try {
    const response = UrlFetchApp.fetch(url);
    const data = JSON.parse(response.getContentText());
    
    return data.arbitrages || [];
  } catch (error) {
    Logger.log('Error fetching data: ' + error);
    return [];
  }
}

function decimalToAmerican(decimal) {
  if (decimal >= 2.0) {
    return '+' + Math.round((decimal - 1) * 100);
  } else {
    return Math.round(-100 / (decimal - 1));
  }
}

function formatGameTime(isoTime) {
  if (!isoTime) return '';
  const date = new Date(isoTime);
  return Utilities.formatDate(date, Session.getScriptTimeZone(), 'MMM dd, h:mm a');
}

function updateArbitrageSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Fetch arbitrage data
  const arbitrages = fetchArbitrages();
  
  // Clear existing data
  sheet.clear();
  
  // Set headers
  const headers = [
    'Match', 'Sport', 'Market', 'Game Time',
    'Sportsbook A', 'Outcome A', 'Odds A (American)', 'Odds A (Decimal)',
    'Sportsbook B', 'Outcome B', 'Odds B (American)', 'Odds B (Decimal)',
    'Profit %', 'Implied Prob', 'Stake A', 'Stake B', 'Profit $', 'Confidence'
  ];
  
  sheet.appendRow(headers);
  
  // Format header row
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setFontWeight('bold');
  headerRange.setBackground('#1e293b');
  headerRange.setFontColor('#ffffff');
  
  // Add data rows
  arbitrages.forEach(arb => {
    sheet.appendRow([
      arb.match || '',
      arb.sport || '',
      arb.market || '',
      formatGameTime(arb.commence_time),
      arb.sportsbook_a || '',
      arb.outcome_a || '',
      decimalToAmerican(arb.odds_a),
      arb.odds_a ? arb.odds_a.toFixed(2) : '',
      arb.sportsbook_b || '',
      arb.outcome_b || '',
      decimalToAmerican(arb.odds_b),
      arb.odds_b ? arb.odds_b.toFixed(2) : '',
      arb.profit_percentage ? arb.profit_percentage.toFixed(2) + '%' : '',
      arb.implied_probability ? (arb.implied_probability * 100).toFixed(2) + '%' : '',
      arb.stake_a || '',
      arb.stake_b || '',
      arb.guaranteed_profit || '',
      arb.warning ? arb.warning.level : ''
    ]);
  });
  
  // Auto-resize columns
  sheet.autoResizeColumns(1, headers.length);
  
  // Add timestamp
  sheet.getRange(sheet.getLastRow() + 2, 1).setValue('Last Updated: ' + new Date());
  
  // Color code by confidence
  const dataRange = sheet.getRange(2, 1, sheet.getLastRow() - 1, headers.length);
  const values = dataRange.getValues();
  
  values.forEach((row, index) => {
    const confidence = row[17]; // Confidence column
    const rowRange = sheet.getRange(index + 2, 1, 1, headers.length);
    
    if (confidence === 'verify_odds') {
      rowRange.setBackground('#fef3c7'); // Yellow
    } else if (confidence === 'moderate') {
      rowRange.setBackground('#fed7aa'); // Orange
    } else if (confidence === 'low') {
      rowRange.setBackground('#d1fae5'); // Green
    }
  });
  
  SpreadsheetApp.getUi().alert(`Updated! Found ${arbitrages.length} arbitrage opportunit${arbitrages.length === 1 ? 'y' : 'ies'}`);
}

// Add menu item
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('⚡ Arbitrage')
    .addItem('🔄 Refresh Arbitrages', 'updateArbitrageSheet')
    .addItem('⚙️ Settings', 'showSettings')
    .addToUi();
}

function showSettings() {
  const html = `
    <div>
      <h3>Current Settings:</h3>
      <p>Sport: ${SPORT}</p>
      <p>Regions: ${REGIONS}</p>
      <p>Markets: ${MARKETS}</p>
      <p>Min Profit: ${MIN_PROFIT}%</p>
      <br>
      <p>To change settings, edit the script variables at the top.</p>
    </div>
  `;
  
  SpreadsheetApp.getUi().showModalDialog(
    HtmlService.createHtmlOutput(html).setWidth(300).setHeight(200),
    'Arbitrage Settings'
  );
}
```

**Step 4: Save Script**
- Click Save icon (💾)
- Name it "Arbitrage Updater"

**Step 5: Authorize**
- Click Run → "updateArbitrageSheet"
- Click "Review permissions"
- Authorize the script

**Step 6: Use It!**
- Go back to your sheet
- You'll see new menu: **"⚡ Arbitrage"**
- Click **"⚡ Arbitrage → 🔄 Refresh Arbitrages"**
- Data updates automatically!

---

## ⚙️ Google Apps Script Configuration

Edit these variables at the top of the script:

```javascript
const API_URL = 'http://localhost:8000/arbitrage/live';
const SPORT = 'americanfootball_nfl';  // or 'basketball_nba', 'baseball_mlb', etc.
const REGIONS = 'us,us2';              // or 'us,us2,uk,eu,au'
const MARKETS = 'h2h';                 // or 'h2h,spreads,totals'
const MIN_PROFIT = 0;                  // Minimum profit percentage
```

**Note**: For localhost to work, your computer must be running the backend server and accessible from Google's servers. For production, deploy your backend to a public URL (Render, Fly.io, etc.)

---

## 🎨 What You'll Get in Google Sheets

### Formatted Spreadsheet:
```
┌────────────────────────────────────────────────────────────────┐
│ Match       │ Sport │ Sportsbook A │ Odds  │ Profit % │ ...  │
├────────────────────────────────────────────────────────────────┤
│ Vikings vs  │ NFL   │ DraftKings   │ -130  │ 0.02%    │ ...  │
│ Eagles      │       │              │(1.77) │          │      │
└────────────────────────────────────────────────────────────────┘
```

### Color Coding:
- 🟢 **Green**: Low confidence (≤2% ROI) - Safe
- 🟠 **Orange**: Moderate (2-5% ROI) - Verify quickly
- 🟡 **Yellow**: Verify odds (>5% ROI) - Double check

### Features:
- ✅ Auto-formatted columns
- ✅ Color-coded by confidence
- ✅ Both American and decimal odds
- ✅ Timestamp of last update
- ✅ Custom menu for easy refresh

---

## 🔄 Auto-Refresh (Optional)

### Add Time-Based Trigger:

**In Apps Script Editor:**
1. Click **Triggers** (clock icon on left)
2. Click **"+ Add Trigger"**
3. Settings:
   - Function: `updateArbitrageSheet`
   - Event source: `Time-driven`
   - Type: `Minutes timer`
   - Interval: `Every 5 minutes` (or your preference)
4. Click **Save**

Now your Google Sheet will **auto-update every 5 minutes**! 🔄

---

## 🌐 Production Deployment (For Live Google Sheets)

Google Sheets can't access `localhost`. For live updates, you need to deploy your backend:

### Option 1: Render.com (Free Tier)
```bash
# Deploy backend to Render
# Get public URL: https://your-app.onrender.com

# Update script:
const API_URL = 'https://your-app.onrender.com/arbitrage/live';
```

### Option 2: Fly.io
```bash
# Deploy to Fly.io
# Get URL: https://your-app.fly.dev

# Update script:
const API_URL = 'https://your-app.fly.dev/arbitrage/live';
```

**See README.md deployment section** for detailed instructions.

---

## 📊 Example Google Sheet Output

```
| Match                     | Sport | Market | Game Time    | Book A      | Odds A | Book B    | Odds B | Profit % |
|---------------------------|-------|--------|--------------|-------------|--------|-----------|--------|----------|
| Vikings vs Eagles         | NFL   | h2h    | Sun 1:00 PM  | DraftKings  | -130   | ESPN BET  | +130   | 0.02%    |
| Lakers vs Celtics         | NBA   | h2h    | Oct 19 7:00  | FanDuel     | +105   | DraftKings| -110   | 0.85%    |
| Yankees vs Red Sox        | MLB   | h2h    | Oct 15 2:00  | BetMGM      | -145   | FanDuel   | +140   | 1.20%    |
```

---

## 🎯 Use Cases

### 1. **Daily Tracking**
- Export daily arbitrages to Google Sheets
- Track historical opportunities
- Analyze patterns over time

### 2. **Team Collaboration**
- Share Google Sheet with betting partners
- Everyone sees same data
- Real-time updates

### 3. **Record Keeping**
- Document arbitrages found
- Track which ones you executed
- Calculate actual ROI

### 4. **Analysis**
- Use Google Sheets formulas
- Create charts and graphs
- Pivot tables for insights

---

## 💡 Pro Tips

### Tip 1: Create Multiple Sheets
```
Sheet 1: NFL Arbitrages
Sheet 2: NBA Arbitrages
Sheet 3: Historical Data
Sheet 4: Executed Bets
```

### Tip 2: Add Your Own Columns
After export, add:
- "Executed?" (Yes/No)
- "Actual Profit"
- "Notes"
- "Book Account Status"

### Tip 3: Use Filters
Google Sheets filters to:
- Show only Profit % > 1%
- Filter by sport
- Sort by game time
- Show only specific books

### Tip 4: Conditional Formatting
Highlight cells:
- Profit > 2%: Green
- Profit > 5%: Yellow
- Confidence "verify_odds": Red border

---

## 🔧 Troubleshooting

### Export Button Not Showing?
- Refresh page (Ctrl+R or Cmd+R)
- Make sure you have arbitrages displayed
- Check browser console (F12) for errors

### Google Apps Script Can't Connect?
- **Localhost won't work from Google's servers**
- Need to deploy backend to public URL
- Or use Export to CSV instead

### CSV Import Issues?
- Make sure to select "Comma" as separator
- Choose "Replace current sheet" or "Insert new sheet"
- Check encoding is UTF-8

---

## 📱 Mobile Access

### Google Sheets Mobile App:
- ✅ View exported arbitrages
- ✅ Filter and sort
- ✅ Share with team
- ✅ Access anywhere

### Workflow:
1. Export from desktop dashboard
2. Import to Google Sheets
3. Access on mobile
4. Place bets from phone

---

## 🎨 Sample Spreadsheet Template

### Create This Structure:

**Sheet 1: Live Arbitrages**
```
Imported data from Export to CSV button
```

**Sheet 2: Execution Tracker**
```
| Match | Book A | Bet A | Book B | Bet B | Executed? | Actual Profit |
```

**Sheet 3: ROI Analysis**
```
=AVERAGE(Profit %)
=SUM(Guaranteed Profit)
=COUNT(Executed Bets)
```

---

## 🌟 Advanced: Real-Time Dashboard

### Using Google Data Studio:
1. Export arbitrages to Google Sheets
2. Connect Google Data Studio to your sheet
3. Create dashboard with:
   - Arbitrage count over time
   - Average ROI by sport
   - Most profitable sportsbook pairs
   - Game time distribution

---

## ✅ What's Available Now

**In Your Dashboard (http://localhost:3000):**
- ✅ **"Export to CSV"** button (new!)
- ✅ **"Google Sheets"** info button (new!)
- ✅ One-click export functionality
- ✅ Formatted for Google Sheets import

**Features:**
- ✅ Includes all arbitrage data
- ✅ Both American and decimal odds
- ✅ Confidence levels
- ✅ Warning messages
- ✅ Ready to import to Google Sheets

---

## 🚀 Try It Now!

**Step-by-Step:**

1. Go to http://localhost:3000
2. Click "Live Odds (API)"
3. Click "Refresh Odds"
4. Click **"Export to CSV"** button (top right, next to title)
5. Open the downloaded file in Google Sheets

**You'll have a professional arbitrage tracking spreadsheet!** 📊

---

## 📖 Alternative: The Odds API Google Sheets Add-On

The official add-on you mentioned is a **separate product** that:
- Fetches raw odds data (not arbitrage calculations)
- Requires The Odds API subscription
- No arbitrage detection built-in

**Our solution is BETTER because:**
- ✅ Includes arbitrage calculations
- ✅ Validation and confidence tiers
- ✅ Filtered to your 7 sportsbooks
- ✅ American odds formatting
- ✅ One-click export

---

## 🎉 Summary

**New Features Added:**
1. ✅ Export to CSV button
2. ✅ Google Sheets import instructions
3. ✅ Google Apps Script for live updates
4. ✅ Formatted for spreadsheet use

**How to Use:**
- **Simple**: Click "Export to CSV" → Import to Google Sheets
- **Advanced**: Use Google Apps Script for auto-updates

---

**Export your first arbitrage sheet right now!** 📊

http://localhost:3000 → Export to CSV → Import to Google Sheets

