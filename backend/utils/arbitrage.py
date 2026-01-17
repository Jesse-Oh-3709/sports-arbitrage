"""
Arbitrage calculation utilities for sports betting
Enhanced with validation, sanity checks, and warning systems
"""
from typing import Dict, List, Tuple, Union, Optional
from datetime import datetime, timedelta
import re


def is_arbitrage(o1: float, o2: float) -> bool:
    """
    Check if arbitrage exists for two-way market
    
    Args:
        o1: Decimal odds for outcome 1
        o2: Decimal odds for outcome 2
    
    Returns:
        True if arbitrage exists
    """
    return (1/o1 + 1/o2) < 1


def roi_percent(o1: float, o2: float) -> float:
    """
    Calculate ROI percentage for two-way arbitrage
    
    Formula: ROI% = (1 / (1/o1 + 1/o2) - 1) * 100
    
    Args:
        o1: Decimal odds for outcome 1
        o2: Decimal odds for outcome 2
    
    Returns:
        ROI percentage
    """
    return (1 / (1/o1 + 1/o2) - 1) * 100


def stake_split(total: float, o1: float, o2: float) -> Tuple[float, float]:
    """
    Calculate optimal stake distribution
    Normalize by implied probability, then round
    
    Args:
        total: Total stake amount
        o1: Decimal odds for outcome 1
        o2: Decimal odds for outcome 2
    
    Returns:
        Tuple of (stake1, stake2) rounded to cents
    """
    inv_sum = (1/o1 + 1/o2)
    s1 = total * (1/o1) / inv_sum
    s2 = total - s1
    return round(s1, 2), round(s2, 2)


def detect_odds_format(odds_value: Union[float, str]) -> str:
    """
    Auto-detect odds format from value
    
    Args:
        odds_value: The odds value (can be string or number)
    
    Returns:
        Format type: 'american', 'fractional', or 'decimal'
    """
    if isinstance(odds_value, str):
        # Check for fractional (e.g., "3/1", "5/2")
        if '/' in odds_value:
            return "fractional"
        # Try to convert to float
        try:
            odds_value = float(odds_value)
        except ValueError:
            raise ValueError(f"Cannot parse odds value: {odds_value}")
    
    # American odds are typically +100 or greater, or -100 or less
    if isinstance(odds_value, (int, float)):
        if odds_value >= 100 or odds_value <= -100:
            return "american"
        # Decimal odds are typically between 1.01 and 100
        elif 1.0 <= odds_value <= 100:
            return "decimal"
    
    return "decimal"  # Default to decimal


def convert_odds_to_decimal(odds: Union[float, str], format_type: str = "decimal") -> float:
    """
    Convert odds from various formats to decimal
    
    Args:
        odds: The odds value
        format_type: Format type ('american', 'fractional', 'decimal')
    
    Returns:
        Decimal odds
    """
    if format_type == "decimal":
        return float(odds)
    
    elif format_type == "american":
        if odds > 0:
            return (odds / 100) + 1
        else:
            return (100 / abs(odds)) + 1
    
    elif format_type == "fractional":
        # Assumes format like "3/1" or "5/2"
        if isinstance(odds, str):
            numerator, denominator = map(float, odds.split("/"))
            return (numerator / denominator) + 1
        else:
            # If already a float, assume it's the fractional value
            return odds + 1
    
    else:
        raise ValueError(f"Unsupported format type: {format_type}")


def validate_odds(odds_a: float, odds_b: float, odds_c: Optional[float] = None) -> Dict[str, Union[bool, str]]:
    """
    Validate odds values and implied probability for sanity
    
    Args:
        odds_a: First odds value
        odds_b: Second odds value
        odds_c: Optional third odds value (for 3-way markets)
    
    Returns:
        Dictionary with validation results
    """
    # Check odds range (realistic bounds)
    MIN_ODDS = 1.01
    MAX_ODDS = 15.0
    
    all_odds = [odds_a, odds_b]
    if odds_c is not None:
        all_odds.append(odds_c)
    
    # Validate range
    for odds in all_odds:
        if not (MIN_ODDS <= odds <= MAX_ODDS):
            return {
                "valid": False,
                "error": f"Odds {odds} outside valid range [{MIN_ODDS}, {MAX_ODDS}]",
                "warning_level": "critical"
            }
    
    # Calculate implied probability sum
    implied_sum = sum(1/o for o in all_odds)
    
    # Sanity check: implied probability sum
    # Normal markets: 0.97 - 1.10 (with bookmaker margin)
    # Arbitrage: < 1.0
    # Too low: likely data error
    if implied_sum < 0.80:
        return {
            "valid": False,
            "error": f"Implied probability sum too low ({implied_sum:.3f}). Likely stale or mismatched odds.",
            "warning_level": "critical",
            "implied_sum": implied_sum
        }
    
    if implied_sum > 1.10:
        return {
            "valid": False,
            "error": f"Implied probability sum too high ({implied_sum:.3f}). Check for data errors.",
            "warning_level": "critical",
            "implied_sum": implied_sum
        }
    
    return {
        "valid": True,
        "implied_sum": implied_sum,
        "warning_level": "none"
    }


def validate_timestamp(timestamp: Optional[str], max_age_seconds: int = 30) -> bool:
    """
    Validate that odds timestamp is recent enough
    
    Args:
        timestamp: ISO format timestamp string
        max_age_seconds: Maximum age in seconds (default 30)
    
    Returns:
        True if timestamp is valid and recent
    """
    if not timestamp:
        return False
    
    try:
        odds_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        current_time = datetime.now(odds_time.tzinfo)
        age = (current_time - odds_time).total_seconds()
        return age <= max_age_seconds
    except (ValueError, AttributeError):
        return False


def get_warning_level(roi: float) -> Dict[str, str]:
    """
    Determine warning level based on ROI percentage
    
    Args:
        roi: Return on investment percentage
    
    Returns:
        Dictionary with warning level and message
    """
    if roi > 5.0:
        return {
            "level": "critical",
            "emoji": "⚠️",
            "message": "VERIFY ODDS - ROI suspiciously high",
            "description": "ROI > 5% is extremely rare. Double-check odds on actual sportsbook sites."
        }
    elif roi > 2.0:
        return {
            "level": "moderate",
            "emoji": "⚡",
            "message": "High ROI - Act quickly",
            "description": "ROI 2-5% is rare but possible. Verify and execute immediately."
        }
    elif roi > 0.5:
        return {
            "level": "low",
            "emoji": "✅",
            "message": "Valid arbitrage opportunity",
            "description": "ROI 0.5-2% is typical for arbitrage betting."
        }
    else:
        return {
            "level": "minimal",
            "emoji": "ℹ️",
            "message": "Low profit margin",
            "description": "ROI < 0.5% may not cover transaction costs."
        }


def calculate_arbitrage_two_way(
    odds_a: float, 
    odds_b: float,
    validate: bool = True
) -> Dict[str, Union[bool, float, str, Dict]]:
    """
    Calculate if arbitrage exists for two-way market with validation
    
    Formula:
        Implied probability = 1/odds_a + 1/odds_b
        Arbitrage exists if implied_prob < 1
        Profit % = (1 / implied_prob - 1) * 100
    
    Args:
        odds_a: Decimal odds for outcome A
        odds_b: Decimal odds for outcome B
        validate: Whether to run validation checks
    
    Returns:
        Dictionary with arbitrage info and validation results
    """
    # Validate odds if requested
    validation = {"valid": True} if not validate else validate_odds(odds_a, odds_b)
    
    if not validation["valid"]:
        return {
            "exists": False,
            "implied_probability": sum(1/o for o in [odds_a, odds_b]),
            "profit_percentage": 0,
            "validation": validation,
            "warning": validation.get("error", "")
        }
    
    # Calculate using correct formula
    implied_prob = (1 / odds_a) + (1 / odds_b)
    arb_exists = implied_prob < 1.0
    
    if arb_exists:
        # Correct ROI formula
        profit_pct = ((1 / implied_prob) - 1) * 100
    else:
        profit_pct = 0
    
    # Get warning level
    warning = get_warning_level(profit_pct) if arb_exists else None
    
    return {
        "exists": arb_exists,
        "implied_probability": round(implied_prob, 6),
        "profit_percentage": round(profit_pct, 4),
        "validation": validation,
        "warning": warning
    }


def calculate_arbitrage_three_way(
    odds_a: float, 
    odds_b: float, 
    odds_c: float,
    validate: bool = True
) -> Dict[str, Union[bool, float, str, Dict]]:
    """
    Calculate if arbitrage exists for three-way market with validation
    
    Formula:
        Implied probability = 1/odds_a + 1/odds_b + 1/odds_c
        Arbitrage exists if implied_prob < 1
    
    Args:
        odds_a: Decimal odds for outcome A (e.g., home win)
        odds_b: Decimal odds for outcome B (e.g., draw)
        odds_c: Decimal odds for outcome C (e.g., away win)
        validate: Whether to run validation checks
    
    Returns:
        Dictionary with arbitrage info and validation results
    """
    # Validate odds if requested
    validation = {"valid": True} if not validate else validate_odds(odds_a, odds_b, odds_c)
    
    if not validation["valid"]:
        return {
            "exists": False,
            "implied_probability": sum(1/o for o in [odds_a, odds_b, odds_c]),
            "profit_percentage": 0,
            "validation": validation,
            "warning": validation.get("error", "")
        }
    
    # Calculate using correct formula
    implied_prob = (1 / odds_a) + (1 / odds_b) + (1 / odds_c)
    arb_exists = implied_prob < 1.0
    
    if arb_exists:
        profit_pct = ((1 / implied_prob) - 1) * 100
    else:
        profit_pct = 0
    
    # Get warning level
    warning = get_warning_level(profit_pct) if arb_exists else None
    
    return {
        "exists": arb_exists,
        "implied_probability": round(implied_prob, 6),
        "profit_percentage": round(profit_pct, 4),
        "validation": validation,
        "warning": warning
    }


def calculate_stakes(*odds: float, total_stake: float = 1000) -> Dict[str, float]:
    """
    Calculate optimal stake distribution for arbitrage betting
    Uses correct formula with normalization before rounding
    
    For two-way:
        Normalize by implied probability sum, then allocate
    
    For three-way:
        Each stake proportional to inverse of odds
    
    Args:
        *odds: Variable number of decimal odds
        total_stake: Total amount to bet
    
    Returns:
        Dictionary with stake amounts and guaranteed profit
    """
    if len(odds) == 2:
        odds_a, odds_b = odds
        
        # Correct formula: normalize by implied probability
        inv_a = 1 / odds_a
        inv_b = 1 / odds_b
        inv_sum = inv_a + inv_b
        
        # Allocate stakes proportional to implied probability
        stake_a = (inv_a / inv_sum) * total_stake
        stake_b = (inv_b / inv_sum) * total_stake
        
        # Calculate guaranteed return (should be equal for both outcomes)
        return_a = stake_a * odds_a
        return_b = stake_b * odds_b
        profit = min(return_a, return_b) - total_stake
        
        return {
            "stake_a": round(stake_a, 2),
            "stake_b": round(stake_b, 2),
            "profit": round(profit, 2),
            "return_a": round(return_a, 2),
            "return_b": round(return_b, 2)
        }
    
    elif len(odds) == 3:
        # Three-way calculation
        odds_a, odds_b, odds_c = odds
        
        # Calculate inverse odds (implied probability)
        inv_a = 1 / odds_a
        inv_b = 1 / odds_b
        inv_c = 1 / odds_c
        total_inv = inv_a + inv_b + inv_c
        
        # Calculate stakes proportional to inverse odds (normalize first)
        stake_a = (inv_a / total_inv) * total_stake
        stake_b = (inv_b / total_inv) * total_stake
        stake_c = (inv_c / total_inv) * total_stake
        
        # Calculate guaranteed return (should be equal for all outcomes)
        return_a = stake_a * odds_a
        return_b = stake_b * odds_b
        return_c = stake_c * odds_c
        profit = min(return_a, return_b, return_c) - total_stake
        
        return {
            "stake_a": round(stake_a, 2),
            "stake_b": round(stake_b, 2),
            "stake_c": round(stake_c, 2),
            "profit": round(profit, 2),
            "return_a": round(return_a, 2),
            "return_b": round(return_b, 2),
            "return_c": round(return_c, 2)
        }
    
    else:
        raise ValueError("Stakes calculation supports only 2-way or 3-way markets")


def normalize_odds_data(raw_data: List[Dict]) -> List[Dict]:
    """
    Normalize odds data from various sources to a standard format
    
    Args:
        raw_data: List of raw odds data
    
    Returns:
        Normalized odds data
    """
    normalized = []
    
    for item in raw_data:
        # Convert odds if needed
        odds = item.get("odds", {})
        normalized_odds = {}
        
        odds_format = item.get("odds_format", "decimal")
        
        for outcome, value in odds.items():
            normalized_odds[outcome] = convert_odds_to_decimal(value, odds_format)
        
        normalized.append({
            "match": item.get("match", ""),
            "sport": item.get("sport", ""),
            "sportsbook": item.get("sportsbook", ""),
            "odds": normalized_odds,
            "market_type": item.get("market_type", "h2h"),
            "timestamp": item.get("timestamp", "")
        })
    
    return normalized


def find_best_arbitrage_combinations(games_data: List[Dict]) -> List[Dict]:
    """
    Find all arbitrage combinations across multiple games and sportsbooks
    
    Args:
        games_data: List of game data with odds from multiple bookmakers
    
    Returns:
        List of arbitrage opportunities sorted by profit percentage
    """
    arbitrages = []
    
    for game in games_data:
        bookmakers = game.get("bookmakers", [])
        
        if len(bookmakers) < 2:
            continue
        
        # Check all pairs of bookmakers
        for i, book1 in enumerate(bookmakers):
            for book2 in bookmakers[i+1:]:
                # Two-way markets
                if "home" in book1 and "away" in book2:
                    odds_a = book1["home"]
                    odds_b = book2["away"]
                    
                    arb = calculate_arbitrage_two_way(odds_a, odds_b)
                    
                    if arb["exists"]:
                        stakes = calculate_stakes(odds_a, odds_b)
                        
                        arbitrages.append({
                            "game": game.get("match", ""),
                            "sport": game.get("sport", ""),
                            "book_a": book1.get("name", ""),
                            "odds_a": odds_a,
                            "book_b": book2.get("name", ""),
                            "odds_b": odds_b,
                            "profit_pct": arb["profit_percentage"],
                            "stakes": stakes
                        })
    
    # Sort by profit percentage
    arbitrages.sort(key=lambda x: x["profit_pct"], reverse=True)
    
    return arbitrages


def calculate_implied_probability(odds: float) -> float:
    """
    Calculate implied probability from decimal odds
    
    Args:
        odds: Decimal odds
    
    Returns:
        Implied probability as percentage
    """
    return (1 / odds) * 100


def calculate_expected_value(
    odds: float,
    true_probability: float,
    stake: float = 100
) -> float:
    """
    Calculate expected value of a bet
    
    Args:
        odds: Decimal odds
        true_probability: Your estimated probability of outcome (0-1)
        stake: Bet amount
    
    Returns:
        Expected value
    """
    win_amount = (odds - 1) * stake
    lose_amount = -stake
    
    ev = (true_probability * win_amount) + ((1 - true_probability) * lose_amount)
    
    return round(ev, 2)


def calculate_kelly_criterion(
    odds: float,
    true_probability: float,
    bankroll: float
) -> float:
    """
    Calculate optimal bet size using Kelly Criterion
    
    Formula: f = (bp - q) / b
    Where:
        f = fraction of bankroll to bet
        b = decimal odds - 1
        p = probability of winning
        q = probability of losing (1 - p)
    
    Args:
        odds: Decimal odds
        true_probability: Your estimated probability of outcome (0-1)
        bankroll: Total bankroll
    
    Returns:
        Recommended bet size
    """
    b = odds - 1
    p = true_probability
    q = 1 - p
    
    f = (b * p - q) / b
    
    # Don't bet if edge is negative
    if f <= 0:
        return 0
    
    # Conservative: use fractional Kelly (e.g., 25% of full Kelly)
    f = f * 0.25
    
    return round(f * bankroll, 2)

