from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import requests
import json
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from utils.arbitrage import (
    calculate_arbitrage_two_way,
    calculate_arbitrage_three_way,
    convert_odds_to_decimal,
    calculate_stakes,
    normalize_odds_data,
    is_arbitrage,
    roi_percent,
    stake_split
)
from utils.filters import filter_prematch, is_game_started
from utils.odds import to_decimal
from utils.matching import same_market, is_valid_two_way_pairing
from utils.validations import (
    validate_odds,
    implied_sum,
    age_seconds,
    confidence_from_roi,
    get_confidence_tooltip
)

# Whitelist: Only include these major regulated US sportsbooks
ALLOWED_SPORTSBOOKS = {
    'DraftKings',
    'FanDuel',
    'ESPN BET',
    'Bally Bet',
    'BetMGM',
    'Caesars Sportsbook',
    'Fanatics Sportsbook'
}

PLAYER_PROP_MARKETS_BY_SPORT: Dict[str, List[str]] = {
    "basketball_nba": [
        "player_points",
        "player_rebounds",
        "player_assists",
        "player_threes",
        "player_points_rebounds_assists",
        "player_points_rebounds",
        "player_points_assists",
        "player_rebounds_assists",
        "player_turnovers"
    ],
    "americanfootball_nfl": [
        "player_pass_yds",
        "player_rush_yds",
        "player_receptions",
        "player_rush_tds",
        "player_anytime_td",
        "player_pass_tds",
        "player_rush_attempts",
        "player_rush_reception_yds"
    ],
    "icehockey_nhl": [
        "player_points",
        "player_assists",
        "player_shots_on_goal",
        "player_goals",
        "player_total_saves"
    ],
    "baseball_mlb": [
        "batter_total_bases",
        "batter_hits",
        "pitcher_strikeouts",
        "batter_home_runs"
    ],
    "soccer_epl": [
        "player_goal_scorer_anytime",
        "player_first_goal_scorer",
        "player_shots_on_target",
        "player_assists"
    ],
    "default": [
        "player_points",
        "player_rebounds",
        "player_assists"
    ]
}

SUPPORTED_PLAYER_PROP_MARKETS = {
    market for markets in PLAYER_PROP_MARKETS_BY_SPORT.values() for market in markets
}

PLAYER_PROP_CACHE_TTL_SECONDS = 120
MAX_PLAYER_PROP_EVENTS = 8
PLAYER_PROP_CACHE: Dict[str, Dict[str, Any]] = {}

app = FastAPI(title="Sports Arbitrage API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class OddsData(BaseModel):
    match: str
    sport: str
    sportsbook: str
    odds: Dict[str, float]
    market_type: str = "h2h"  # h2h, spreads, totals

class ManualOddsUpload(BaseModel):
    games: List[Dict[str, Any]]

class ArbitrageResult(BaseModel):
    match: str
    sport: str
    market: str
    sportsbook_a: str
    odds_a: float
    outcome_a: str
    sportsbook_b: str
    odds_b: float
    outcome_b: str
    profit_percentage: float
    stake_a: float
    stake_b: float
    guaranteed_profit: float
    sportsbook_c: Optional[str] = None
    odds_c: Optional[float] = None
    outcome_c: Optional[str] = None
    stake_c: Optional[float] = None

# Environment variable for API key
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "")
ODDS_API_BASE_URL = "https://api.the-odds-api.com/v4"


def get_player_prop_markets_for_sport(sport: str, requested_markets: Optional[List[str]] = None) -> List[str]:
    """
    Determine which player prop markets to request for a given sport.
    Filters the requested markets to those supported. Falls back to defaults.
    """
    valid_requested = []
    if requested_markets:
        for market in requested_markets:
            if market in SUPPORTED_PLAYER_PROP_MARKETS:
                valid_requested.append(market)

    if valid_requested:
        return valid_requested

    defaults = PLAYER_PROP_MARKETS_BY_SPORT.get(sport)
    if defaults:
        return defaults
    return PLAYER_PROP_MARKETS_BY_SPORT["default"]


def fetch_player_prop_event_odds(
    sport: str,
    event_id: str,
    markets: List[str],
    regions: str
) -> Optional[Dict[str, Any]]:
    """
    Fetch player prop odds for a specific event, with simple in-memory caching.
    """
    cache_key = f"{sport}:{event_id}:{','.join(sorted(markets))}:{regions}"
    cached = PLAYER_PROP_CACHE.get(cache_key)
    now = datetime.now(timezone.utc)

    if cached and (now - cached["timestamp"]).total_seconds() < PLAYER_PROP_CACHE_TTL_SECONDS:
        return cached["data"]

    try:
        response = requests.get(
            f"{ODDS_API_BASE_URL}/sports/{sport}/events/{event_id}/odds",
            params={
                "apiKey": ODDS_API_KEY,
                "regions": regions,
                "markets": ",".join(markets),
                "oddsFormat": "decimal"
            },
            timeout=10
        )
        response.raise_for_status()
        event_data = response.json()
        PLAYER_PROP_CACHE[cache_key] = {
            "timestamp": now,
            "data": event_data
        }
        return event_data
    except requests.exceptions.RequestException:
        return None


def build_player_prop_arbitrages(
    event_data: Dict[str, Any],
    game_info: Dict[str, Any],
    player_prop_markets: List[str],
    min_profit: float
) -> List[Dict[str, Any]]:
    """
    Generate player prop arbitrage opportunities for a single event.
    """
    bookmakers = event_data.get("bookmakers", [])
    if not bookmakers:
        return []

    player_market_book_data: Dict[tuple, Dict[str, Dict[str, Any]]] = {}

    for bookmaker in bookmakers:
        title = bookmaker.get("title")
        if title not in ALLOWED_SPORTSBOOKS:
            continue

        for market in bookmaker.get("markets", []):
            market_key = market.get("key")
            if market_key not in player_prop_markets:
                continue

            for outcome in market.get("outcomes", []):
                outcome_name = (outcome.get("name") or "").lower()
                if outcome_name not in {"over", "under"}:
                    continue

                player_name = (outcome.get("description") or outcome.get("player_name") or "").strip()
                if not player_name:
                    continue

                price = outcome.get("price")
                point = outcome.get("point")
                if price is None or point is None:
                    continue

                key = (player_name, market_key, round(float(point), 4))
                entry = player_market_book_data.setdefault(key, {})
                book_entry = entry.setdefault(title, {"point": point})
                book_entry[outcome_name] = price

    arbitrages: List[Dict[str, Any]] = []

    for (player_name, market_key, point), bookmaker_data in player_market_book_data.items():
        book_titles = list(bookmaker_data.keys())
        if len(book_titles) < 2:
            continue

        for i in range(len(book_titles)):
            book1 = book_titles[i]
            data1 = bookmaker_data[book1]
            for j in range(i + 1, len(book_titles)):
                book2 = book_titles[j]
                data2 = bookmaker_data[book2]

                # Over (book1) vs Under (book2)
                if "over" in data1 and "under" in data2:
                    odds_a = data1["over"]
                    odds_b = data2["under"]
                    arb = calculate_arbitrage_two_way(odds_a, odds_b, validate=True)
                    if arb.get("validation", {}).get("valid", True) and arb["exists"] and arb["profit_percentage"] >= min_profit:
                        stakes = calculate_stakes(odds_a, odds_b, total_stake=1000)
                        arbitrages.append({
                            "match": game_info["match_name"],
                            "sport": game_info["sport_name"],
                            "market": market_key,
                            "market_type": "player_prop",
                            "player_name": player_name,
                            "prop_type": market_key.replace("player_", ""),
                            "prop_line": point,
                            "commence_time": game_info["commence_time"],
                            "sportsbook_a": book1,
                            "odds_a": odds_a,
                            "outcome_a": f"Over {point}",
                            "sportsbook_b": book2,
                            "odds_b": odds_b,
                            "outcome_b": f"Under {point}",
                            "profit_percentage": round(arb["profit_percentage"], 2),
                            "implied_probability": round(arb["implied_probability"], 4),
                            "stake_a": stakes["stake_a"],
                            "stake_b": stakes["stake_b"],
                            "guaranteed_profit": round(stakes["profit"], 2),
                            "timestamp": datetime.now().isoformat()
                        })

                # Under (book1) vs Over (book2)
                if "under" in data1 and "over" in data2:
                    odds_a = data1["under"]
                    odds_b = data2["over"]
                    arb = calculate_arbitrage_two_way(odds_a, odds_b, validate=True)
                    if arb.get("validation", {}).get("valid", True) and arb["exists"] and arb["profit_percentage"] >= min_profit:
                        stakes = calculate_stakes(odds_a, odds_b, total_stake=1000)
                        arbitrages.append({
                            "match": game_info["match_name"],
                            "sport": game_info["sport_name"],
                            "market": market_key,
                            "market_type": "player_prop",
                            "player_name": player_name,
                            "prop_type": market_key.replace("player_", ""),
                            "prop_line": point,
                            "commence_time": game_info["commence_time"],
                            "sportsbook_a": book1,
                            "odds_a": odds_a,
                            "outcome_a": f"Under {point}",
                            "sportsbook_b": book2,
                            "odds_b": odds_b,
                            "outcome_b": f"Over {point}",
                            "profit_percentage": round(arb["profit_percentage"], 2),
                            "implied_probability": round(arb["implied_probability"], 4),
                            "stake_a": stakes["stake_a"],
                            "stake_b": stakes["stake_b"],
                            "guaranteed_profit": round(stakes["profit"], 2),
                            "timestamp": datetime.now().isoformat()
                        })

    return arbitrages

@app.get("/")
def read_root():
    return {
        "message": "Sports Arbitrage API",
        "version": "1.0.0",
        "endpoints": {
            "/arbitrage": "Find all arbitrage opportunities",
            "/arbitrage/live": "Fetch live odds and find arbitrage",
            "/upload": "Upload manual odds data",
            "/sports": "List available sports",
            "/convert-odds": "Convert odds between formats"
        }
    }

@app.get("/sports")
def get_available_sports():
    """Get list of available sports from The Odds API"""
    if not ODDS_API_KEY:
        return {"error": "API key not configured", "sports": []}
    
    try:
        response = requests.get(
            f"{ODDS_API_BASE_URL}/sports",
            params={"apiKey": ODDS_API_KEY}
        )
        response.raise_for_status()
        return {"sports": response.json()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sports: {str(e)}")

@app.get("/arbitrage/live")
def find_live_arbitrage(
    sport: str = "upcoming",
    regions: str = "us",
    markets: str = "h2h",
    min_profit: float = 0.0,
    include_live: bool = False,
    grace_minutes: int = 0,
    include_player_props: bool = False
):
    """
    Fetch live odds from The Odds API and calculate arbitrage opportunities
    
    Parameters:
    - sport: Sport key (e.g., 'americanfootball_nfl', 'basketball_nba')
    - regions: Comma-separated regions (us, us2, uk, eu, au)
    - markets: Comma-separated markets (h2h, spreads, totals, player_points, player_assists, etc.)
    - min_profit: Minimum profit percentage to return
    - include_live: Include live/in-progress games (default: False)
    - grace_minutes: Exclude games starting within N minutes (default: 0)
    - include_player_props: Include player prop markets (default: False)
    """
    if not ODDS_API_KEY:
        return {
            "error": "ODDS_API_KEY not configured. Please set your API key.",
            "arbitrages": [],
            "message": "Get your free API key at https://the-odds-api.com"
        }
    
    try:
        # Determine which markets to fetch
        # The /sports/{sport}/odds endpoint does not return player props,
        # so we filter them out of the initial request but keep track of what was requested.
        incoming_markets = [m.strip() for m in markets.split(",") if m.strip()]
        game_markets = [m for m in incoming_markets if m not in [
            "player_points", "player_assists", "player_rebounds", "player_touchdowns",
            "player_passing_yards", "player_receiving_yards", "player_rushing_yards"
        ]]
        player_prop_markets = [m for m in incoming_markets if m in [
            "player_points", "player_assists", "player_rebounds", "player_touchdowns",
            "player_passing_yards", "player_receiving_yards", "player_rushing_yards"
        ]]
        
        # Only request game markets (player props are called via event endpoint)
        all_markets = ",".join(game_markets) if game_markets else "h2h"
        
        # Fetch odds data
        response = requests.get(
            f"{ODDS_API_BASE_URL}/sports/{sport}/odds",
            params={
                "apiKey": ODDS_API_KEY,
                "regions": regions,
                "markets": all_markets,
                "oddsFormat": "decimal"
            }
        )
        response.raise_for_status()
        data = response.json()
        
        # Filter to pre-match games only (unless include_live=True)
        filtered_games = filter_prematch(data, include_live=include_live, grace_min=grace_minutes)
        
        arbitrages = []
        current_time = datetime.now(timezone.utc)
        event_lookup: Dict[str, Dict[str, Any]] = {}
        
        for game in filtered_games:
            if not game.get("bookmakers"):
                continue
                
            match_name = f"{game['home_team']} vs {game['away_team']}"
            sport_name = game.get("sport_title", sport)
            commence_time = game.get("commence_time", "")
            event_id = game.get("id")
            if event_id:
                event_lookup[event_id] = {
                    "match_name": match_name,
                    "sport_name": sport_name,
                    "commence_time": commence_time
                }
            
            # Process each market type
            markets_to_process = game_markets if game_markets else markets.split(",")
            for market_key in markets_to_process:
                market_odds = {}
                
                # Collect odds from all bookmakers for this market (only allowed books)
                for bookmaker in game["bookmakers"]:
                    # Only include whitelisted sportsbooks
                    if bookmaker["title"] not in ALLOWED_SPORTSBOOKS:
                        continue
                    for market in bookmaker.get("markets", []):
                        if market["key"] == market_key:
                            bookmaker_name = bookmaker["title"]
                            outcomes = {}
                            for outcome in market["outcomes"]:
                                outcomes[outcome["name"]] = outcome["price"]
                            market_odds[bookmaker_name] = outcomes
                
                if len(market_odds) < 2:
                    continue
                
                # Find arbitrage opportunities
                # Two-way markets (most common)
                bookmaker_names = list(market_odds.keys())
                outcome_names = list(next(iter(market_odds.values())).keys())
                
                if len(outcome_names) == 2:
                    # Two-way arbitrage
                    for i, book1 in enumerate(bookmaker_names):
                        for book2 in bookmaker_names[i+1:]:
                            for outcome_a in outcome_names:
                                for outcome_b in outcome_names:
                                    if outcome_a != outcome_b:
                                        odds_a = market_odds[book1].get(outcome_a)
                                        odds_b = market_odds[book2].get(outcome_b)
                                        
                                        if odds_a and odds_b:
                                            arb = calculate_arbitrage_two_way(odds_a, odds_b, validate=True)
                                            
                                            # Skip if validation failed
                                            if not arb.get("validation", {}).get("valid", True):
                                                continue
                                            
                                            if arb["exists"] and arb["profit_percentage"] >= min_profit:
                                                stakes = calculate_stakes(odds_a, odds_b, total_stake=1000)
                                                
                                                # Build arbitrage record with validation info
                                                arb_record = {
                                                    "match": match_name,
                                                    "sport": sport_name,
                                                    "market": market_key,
                                                    "market_type": "game",
                                                    "commence_time": commence_time,
                                                    "sportsbook_a": book1,
                                                    "odds_a": odds_a,
                                                    "outcome_a": outcome_a,
                                                    "sportsbook_b": book2,
                                                    "odds_b": odds_b,
                                                    "outcome_b": outcome_b,
                                                    "profit_percentage": round(arb["profit_percentage"], 2),
                                                    "implied_probability": round(arb["implied_probability"], 4),
                                                    "stake_a": stakes["stake_a"],
                                                    "stake_b": stakes["stake_b"],
                                                    "guaranteed_profit": round(stakes["profit"], 2),
                                                    "timestamp": datetime.now().isoformat()
                                                }
                                                
                                                # Add warning if present
                                                if arb.get("warning"):
                                                    arb_record["warning"] = arb["warning"]
                                                
                                                arbitrages.append(arb_record)
                
                elif len(outcome_names) == 3:
                    # Three-way arbitrage (e.g., soccer with draw)
                    for i, book1 in enumerate(bookmaker_names):
                        for j, book2 in enumerate(bookmaker_names):
                            if i >= j:
                                continue
                            for book3 in bookmaker_names[j+1:]:
                                outcomes = list(outcome_names)
                                if len(outcomes) == 3:
                                    odds = [
                                        market_odds[book1].get(outcomes[0]),
                                        market_odds[book2].get(outcomes[1]),
                                        market_odds[book3].get(outcomes[2])
                                    ]
                                    
                                    if all(odds):
                                        arb = calculate_arbitrage_three_way(*odds, validate=True)
                                        
                                        # Skip if validation failed
                                        if not arb.get("validation", {}).get("valid", True):
                                            continue
                                        
                                        if arb["exists"] and arb["profit_percentage"] >= min_profit:
                                            stakes = calculate_stakes(*odds, total_stake=1000)
                                            
                                            # Build arbitrage record with validation info
                                            arb_record = {
                                                "match": match_name,
                                                "sport": sport_name,
                                                "market": market_key,
                                                "market_type": "game",
                                                "commence_time": commence_time,
                                                "sportsbook_a": book1,
                                                "odds_a": odds[0],
                                                "outcome_a": outcomes[0],
                                                "sportsbook_b": book2,
                                                "odds_b": odds[1],
                                                "outcome_b": outcomes[1],
                                                "sportsbook_c": book3,
                                                "odds_c": odds[2],
                                                "outcome_c": outcomes[2],
                                                "profit_percentage": round(arb["profit_percentage"], 2),
                                                "implied_probability": round(arb["implied_probability"], 4),
                                                "stake_a": stakes["stake_a"],
                                                "stake_b": stakes["stake_b"],
                                                "stake_c": stakes.get("stake_c"),
                                                "guaranteed_profit": round(stakes["profit"], 2),
                                                "timestamp": datetime.now().isoformat()
                                            }
                                            
                                            # Add warning if present
                                            if arb.get("warning"):
                                                arb_record["warning"] = arb["warning"]
                                            
                                            arbitrages.append(arb_record)
            
        player_props_note: Optional[str] = None
        if include_player_props:
            prop_markets_to_use = get_player_prop_markets_for_sport(sport, player_prop_markets)
            events_to_process = list(event_lookup.items())[:MAX_PLAYER_PROP_EVENTS]
            player_prop_events_processed = 0
            player_prop_arbitrages: List[Dict[str, Any]] = []

            for event_id, game_info in events_to_process:
                event_data = fetch_player_prop_event_odds(sport, event_id, prop_markets_to_use, regions)
                if not event_data:
                    continue
                player_prop_events_processed += 1
                player_prop_arbitrages.extend(
                    build_player_prop_arbitrages(
                        event_data,
                        game_info,
                        prop_markets_to_use,
                        min_profit
                    )
                )

            if player_prop_arbitrages:
                arbitrages.extend(player_prop_arbitrages)
                player_props_note = (
                    f"Player props analyzed for {player_prop_events_processed} events "
                    f"({len(prop_markets_to_use)} markets)."
                )
            else:
                if player_prop_events_processed == 0:
                    player_props_note = (
                        "No player prop data was returned for the requested sport and regions. "
                        "Try again closer to game time or verify your Odds API plan includes player props."
                    )
                else:
                    player_props_note = (
                        "Player props were fetched but no arbitrage opportunities met the minimum profit threshold."
                    )

        # Sort by profit percentage (highest first)
        arbitrages.sort(key=lambda x: x["profit_percentage"], reverse=True)
        
        result = {
            "count": len(arbitrages),
            "arbitrages": arbitrages,
            "api_requests_remaining": response.headers.get("x-requests-remaining", "unknown")
        }
        
        # Include player prop note if applicable
        if include_player_props and player_props_note:
            result["player_props_note"] = player_props_note
        
        return result
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch odds: {str(e)}")

@app.post("/upload")
async def upload_manual_odds(file: UploadFile = File(...)):
    """
    Upload CSV or JSON file with manual odds data
    
    Expected JSON format:
    {
        "games": [
            {
                "match": "Team A vs Team B",
                "sport": "NBA",
                "date": "2025-10-15",
                "bookmakers": [
                    {"name": "DraftKings", "home": 2.10, "away": 1.80},
                    {"name": "FanDuel", "home": 1.95, "away": 1.95}
                ]
            }
        ]
    }
    """
    try:
        content = await file.read()
        
        if file.filename.endswith(".json"):
            data = json.loads(content)
        elif file.filename.endswith(".csv"):
            # Parse CSV (simple implementation)
            import csv
            import io
            csv_data = csv.DictReader(io.StringIO(content.decode()))
            data = {"games": list(csv_data)}
        else:
            raise HTTPException(status_code=400, detail="Only JSON and CSV files are supported")
        
        # Process uploaded data and find arbitrages
        arbitrages = []
        
        for game in data.get("games", []):
            match_name = game.get("match", "Unknown Match")
            sport_name = game.get("sport", "Unknown Sport")
            bookmakers = game.get("bookmakers", [])
            
            # Only include whitelisted sportsbooks
            bookmakers = [b for b in bookmakers if b.get("name") in ALLOWED_SPORTSBOOKS]
            
            if len(bookmakers) < 2:
                continue
            
            # Find arbitrage opportunities
            for i, book1 in enumerate(bookmakers):
                for book2 in bookmakers[i+1:]:
                    odds_a = book1.get("home") or book1.get("odds1")
                    odds_b = book2.get("away") or book2.get("odds2")
                    
                    if odds_a and odds_b:
                        arb = calculate_arbitrage_two_way(odds_a, odds_b)
                        
                        if arb["exists"]:
                            stakes = calculate_stakes(odds_a, odds_b, total_stake=1000)
                            
                            arbitrages.append({
                                "match": match_name,
                                "sport": sport_name,
                                "market": "h2h",
                                "sportsbook_a": book1.get("name", "Unknown"),
                                "odds_a": odds_a,
                                "outcome_a": "Home/Team A",
                                "sportsbook_b": book2.get("name", "Unknown"),
                                "odds_b": odds_b,
                                "outcome_b": "Away/Team B",
                                "profit_percentage": round(arb["profit_percentage"], 2),
                                "stake_a": stakes["stake_a"],
                                "stake_b": stakes["stake_b"],
                                "guaranteed_profit": round(stakes["profit"], 2)
                            })
        
        arbitrages.sort(key=lambda x: x["profit_percentage"], reverse=True)
        
        return {
            "success": True,
            "count": len(arbitrages),
            "arbitrages": arbitrages
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/convert-odds")
def convert_odds(odds_value: float, from_format: str, to_format: str = "decimal"):
    """
    Convert odds between different formats
    
    Supported formats: american, decimal, fractional
    """
    try:
        result = convert_odds_to_decimal(odds_value, from_format)
        
        if to_format == "decimal":
            return {"original": odds_value, "format": from_format, "decimal": result}
        else:
            return {
                "error": "Currently only conversion to decimal is supported",
                "decimal": result
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_key_configured": bool(ODDS_API_KEY)
    }

@app.get("/debug/nba")
def debug_nba():
    """Debug endpoint to see what NBA data is being processed"""
    if not ODDS_API_KEY:
        return {"error": "API key not configured"}
    
    try:
        response = requests.get(
            f"{ODDS_API_BASE_URL}/sports/basketball_nba/odds",
            params={
                "apiKey": ODDS_API_KEY,
                "regions": "us,us2",
                "markets": "h2h",
                "oddsFormat": "decimal"
            }
        )
        response.raise_for_status()
        data = response.json()
        
        filtered_games = filter_prematch(data, include_live=False, grace_min=0)
        
        debug_info = {
            "total_games": len(data),
            "filtered_games": len(filtered_games),
            "allowed_sportsbooks": list(ALLOWED_SPORTSBOOKS),
            "sample_game": {}
        }
        
        if filtered_games:
            game = filtered_games[0]
            debug_info["sample_game"] = {
                "match": f"{game['home_team']} vs {game['away_team']}",
                "commence_time": game.get("commence_time"),
                "total_bookmakers": len(game.get("bookmakers", [])),
                "allowed_bookmakers": []
            }
            
            # Check which bookmakers are in the game and allowed
            for bookmaker in game.get("bookmakers", []):
                book_name = bookmaker["title"]
                is_allowed = book_name in ALLOWED_SPORTSBOOKS
                if is_allowed:
                    market_data = {}
                    for market in bookmaker.get("markets", []):
                        if market.get("key") == "h2h":
                            outcomes = {outcome["name"]: outcome["price"] for outcome in market.get("outcomes", [])}
                            market_data["h2h"] = outcomes
                    debug_info["sample_game"]["allowed_bookmakers"].append({
                        "name": book_name,
                        "markets": market_data
                    })
        
        return debug_info
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/debug/player-props")
def debug_player_props():
    """Debug endpoint to check player prop data structure"""
    if not ODDS_API_KEY:
        return {"error": "API key not configured"}
    
    try:
        response = requests.get(
            f"{ODDS_API_BASE_URL}/sports/basketball_nba/odds",
            params={
                "apiKey": ODDS_API_KEY,
                "regions": "us,us2",
                "markets": "player_points",
                "oddsFormat": "decimal"
            }
        )
        response.raise_for_status()
        data = response.json()
        
        filtered_games = filter_prematch(data, include_live=False, grace_min=0)
        
        debug_info = {
            "total_games": len(data),
            "filtered_games": len(filtered_games),
            "player_prop_markets_found": False,
            "sample_data": {}
        }
        
        if filtered_games:
            game = filtered_games[0]
            debug_info["sample_data"] = {
                "match": f"{game['home_team']} vs {game['away_team']}",
                "bookmakers_checked": 0,
                "player_prop_details": []
            }
            
            for bookmaker in game.get("bookmakers", []):
                book_name = bookmaker.get("title", "")
                if book_name not in ALLOWED_SPORTSBOOKS:
                    continue
                
                debug_info["sample_data"]["bookmakers_checked"] += 1
                
                for market in bookmaker.get("markets", []):
                    market_key = market.get("key", "")
                    if "player" in market_key.lower():
                        debug_info["player_prop_markets_found"] = True
                        prop_info = {
                            "bookmaker": book_name,
                            "market_key": market_key,
                            "outcomes_count": len(market.get("outcomes", [])),
                            "sample_outcomes": []
                        }
                        
                        for outcome in market.get("outcomes", [])[:3]:
                            prop_info["sample_outcomes"].append({
                                "name": outcome.get("name"),
                                "description": outcome.get("description"),
                                "price": outcome.get("price"),
                                "point": outcome.get("point")
                            })
                        
                        debug_info["sample_data"]["player_prop_details"].append(prop_info)
                        break  # Only show first player prop market per bookmaker
        
        return debug_info
        
    except Exception as e:
        return {"error": str(e), "traceback": str(e.__traceback__)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

