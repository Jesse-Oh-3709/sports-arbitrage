# Player Props Implementation Guide

## Overview
This document describes the implementation of player prop markets in the Sports Arbitrage Finder application.

## Backend Changes

### 1. API Endpoint Updates (`backend/app.py`)

The `/arbitrage/live` endpoint has been extended with:
- **New Parameter**: `include_player_props` (boolean) - Enables fetching player prop markets
- **Market Detection**: Automatically detects and separates game markets from player prop markets
- **Player Prop Markets Supported**:
  - `player_points` (NBA, etc.)
  - `player_assists` (NBA)
  - `player_rebounds` (NBA)
  - `player_touchdowns` (NFL)
  - `player_passing_yards` (NFL)
  - `player_receiving_yards` (NFL)
  - `player_rushing_yards` (NFL)

### 2. Arbitrage Detection Logic

**Game Markets** (unchanged):
- Processes h2h, spreads, totals markets
- Two-way and three-way arbitrage detection
- Market type set to `"game"`

**Player Prop Markets** (new):
- Extracts player name from outcome descriptions
- Groups Over/Under outcomes by player
- Compares odds across bookmakers for same player/prop
- Creates arbitrage opportunities when:
  - Over at Book A + Under at Book B creates arbitrage
  - Under at Book A + Over at Book B creates arbitrage
- Market type set to `"player_prop"`
- Includes additional fields:
  - `player_name`: Name of the player
  - `prop_type`: Type of prop (points, assists, etc.)
  - `prop_line`: The line value (e.g., 25.5 for points)

### 3. Response Structure

All arbitrage records now include:
```json
{
  "market_type": "game" | "player_prop",
  "player_name": "LeBron James",  // Only for player_prop
  "prop_type": "points",          // Only for player_prop
  "prop_line": 25.5,              // Only for player_prop
  // ... other standard fields
}
```

## Frontend Changes

### 1. New Components

**`PlayerPropsTable.jsx`**:
- Displays player prop arbitrage opportunities
- Groups props by player name and prop type
- Shows player name, prop type, line value prominently
- Displays Over/Under outcomes with bookmaker odds
- Includes stake recommendations and profit calculations

### 2. Updated Components

**`FilterPanel.jsx`**:
- Added checkbox: "Include Player Props"
- Enables/disables player prop market fetching

**`SportsArbitrageApp.jsx`**:
- Added `marketTypeView` state: 'game', 'player_props', 'all'
- Added toggle buttons to switch between views
- Filters arbitrages by market type for display
- Automatically resets view when player props disabled

### 3. Type Definitions

**`utils/types.js`**:
- JSDoc type definitions for TypeScript-style documentation
- Defines `ArbitrageOpportunity` and `PlayerPropArbitrage` types

## Usage

### Enabling Player Props

1. **In the UI**:
   - Go to "Live Odds (API)" view
   - Check "Include Player Props" in the Filters panel
   - Select a sport that supports player props (NBA, NFL, etc.)
   - Click "Refresh Odds"

2. **Via API**:
   ```bash
   curl "http://localhost:8000/arbitrage/live?sport=basketball_nba&include_player_props=true&regions=us,us2"
   ```

### Viewing Results

- **Game Odds**: Shows only traditional game markets (h2h, spreads, totals)
- **Player Props**: Shows only player prop arbitrages
- **All**: Shows both types grouped separately

## API Response Example

```json
{
  "count": 2,
  "arbitrages": [
    {
      "match": "Lakers vs Warriors",
      "sport": "NBA",
      "market": "player_points",
      "market_type": "player_prop",
      "player_name": "LeBron James",
      "prop_type": "points",
      "prop_line": 25.5,
      "sportsbook_a": "DraftKings",
      "odds_a": 1.90,
      "outcome_a": "Over 25.5",
      "sportsbook_b": "FanDuel",
      "odds_b": 1.95,
      "outcome_b": "Under 25.5",
      "profit_percentage": 1.11,
      "stake_a": 506.33,
      "stake_b": 493.67,
      "guaranteed_profit": 11.11
    }
  ]
}
```

## Notes

1. **Player Prop Availability**: Player props are only available for certain sports (primarily NBA and NFL) and may not be available for all games.

2. **Line Matching**: The current implementation attempts to match player props across bookmakers. If lines differ slightly, arbitrage may still be possible but requires manual verification.

3. **API Rate Limits**: Fetching player props increases API calls. Monitor your API request count.

4. **Data Structure**: The Odds API player prop structure may vary. The implementation includes flexible parsing to handle different formats.

## Testing

To test player props:
1. Ensure backend server is running with API key configured
2. Select NBA or NFL sport
3. Enable "Include Player Props" checkbox
4. Click "Refresh Odds"
5. Check if player prop arbitrages appear

If no player props appear:
- Verify the sport supports player props
- Check API request count hasn't been exceeded
- Ensure games are upcoming (not live/started)
- Try different regions (us, us2)

## Future Enhancements

- [ ] Add prop line matching tolerance (e.g., 25.5 vs 26.0)
- [ ] Support more prop types (first basket, player combos)
- [ ] Add prop line filtering (only show props above/below certain lines)
- [ ] Cache player prop data to reduce API calls
- [ ] Add player search/filter functionality

