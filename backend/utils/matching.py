"""
Market matching utilities to ensure odds are from the same market
"""
from typing import Dict, Optional


def same_market(market1: Dict, market2: Dict) -> bool:
    """
    Check if two markets are the same (for valid arbitrage comparison)
    
    For spreads/totals, the point value must match exactly
    For h2h, just the market key needs to match
    
    Args:
        market1: First market dict with 'key' and optional 'point'
        market2: Second market dict with 'key' and optional 'point'
    
    Returns:
        True if markets match, False otherwise
    """
    # Market keys must match
    if market1.get("key") != market2.get("key"):
        return False
    
    # For spreads and totals, point values must match exactly
    if market1.get("key") in ("spreads", "totals"):
        point1 = market1.get("point")
        point2 = market2.get("point")
        
        # Both must have point values
        if point1 is None or point2 is None:
            return False
        
        # Points must match (with small tolerance for float comparison)
        try:
            return abs(float(point1) - float(point2)) < 0.01
        except (ValueError, TypeError):
            return False
    
    # For h2h (moneyline), just matching key is enough
    return True


def get_market_identifier(market: Dict) -> str:
    """
    Get a unique identifier for a market
    
    Args:
        market: Market dict with 'key' and optional 'point'
    
    Returns:
        String identifier (e.g., "h2h", "spreads_-1.5", "totals_45.5")
    """
    key = market.get("key", "unknown")
    
    if key in ("spreads", "totals"):
        point = market.get("point")
        if point is not None:
            return f"{key}_{point}"
    
    return key


def extract_opposite_outcome(market: Dict, outcome_name: str) -> Optional[str]:
    """
    For two-way markets, get the opposite outcome name
    
    Args:
        market: Market dict with 'outcomes' list
        outcome_name: Name of one outcome
    
    Returns:
        Name of opposite outcome, or None if not found
    """
    outcomes = market.get("outcomes", [])
    outcome_names = [o.get("name") for o in outcomes]
    
    if len(outcome_names) == 2:
        return outcome_names[0] if outcome_names[1] == outcome_name else outcome_names[1]
    
    return None


def is_valid_two_way_pairing(
    market1: Dict, 
    outcome1: str, 
    market2: Dict, 
    outcome2: str
) -> bool:
    """
    Check if two outcomes from different markets form a valid arbitrage pair
    
    Args:
        market1: First market
        outcome1: Outcome name from first market
        market2: Second market
        outcome2: Outcome name from second market
    
    Returns:
        True if valid pairing for arbitrage
    """
    # Markets must be the same
    if not same_market(market1, market2):
        return False
    
    # Outcomes must be different (opposite sides)
    if outcome1 == outcome2:
        return False
    
    # Both outcomes must exist in their respective markets
    market1_outcomes = [o.get("name") for o in market1.get("outcomes", [])]
    market2_outcomes = [o.get("name") for o in market2.get("outcomes", [])]
    
    if outcome1 not in market1_outcomes or outcome2 not in market2_outcomes:
        return False
    
    return True

