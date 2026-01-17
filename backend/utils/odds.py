"""
Odds format detection and conversion utilities
"""
from typing import Union


def to_decimal(odd: Union[int, float, str]) -> float:
    """
    Convert odds from any format to decimal
    Auto-detects: American, Fractional, or Decimal
    
    Args:
        odd: Odds value in any format
    
    Returns:
        Decimal odds (e.g., 1.91, 2.50)
    
    Raises:
        ValueError: If format cannot be determined
    """
    # Handle string input
    if isinstance(odd, str):
        odd = odd.strip()
        
        # Check for fractional (e.g., "13/8", "5/2")
        if "/" in odd:
            try:
                num, den = odd.split("/")
                return float(num) / float(den) + 1
            except (ValueError, ZeroDivisionError):
                raise ValueError(f"Invalid fractional odds: {odd}")
        
        # Try to convert to number
        try:
            odd = float(odd)
        except ValueError:
            raise ValueError(f"Cannot parse odds value: {odd}")
    
    # Now we have a number
    if not isinstance(odd, (int, float)):
        raise ValueError(f"Odds must be numeric, got {type(odd)}")
    
    # Decimal odds (1.01 to 100)
    if 1.01 <= odd <= 100:
        return float(odd)
    
    # American odds (positive)
    if odd >= 100:
        return (odd / 100) + 1
    
    # American odds (negative)
    if odd <= -100:
        return (100 / abs(odd)) + 1
    
    # Invalid range
    raise ValueError(f"Odds {odd} outside valid ranges")


def detect_format(odd: Union[int, float, str]) -> str:
    """
    Detect odds format
    
    Args:
        odd: Odds value
    
    Returns:
        Format type: 'american', 'fractional', or 'decimal'
    """
    if isinstance(odd, str):
        if "/" in odd:
            return "fractional"
        try:
            odd = float(odd)
        except ValueError:
            return "unknown"
    
    if isinstance(odd, (int, float)):
        if odd >= 100 or odd <= -100:
            return "american"
        if 1.01 <= odd <= 100:
            return "decimal"
    
    return "unknown"


def american_to_decimal(american_odds: Union[int, float]) -> float:
    """
    Convert American odds to decimal
    
    Args:
        american_odds: American odds (e.g., -110, +150)
    
    Returns:
        Decimal odds
    """
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return (100 / abs(american_odds)) + 1


def decimal_to_american(decimal_odds: float) -> int:
    """
    Convert decimal odds to American
    
    Args:
        decimal_odds: Decimal odds (e.g., 1.91, 2.50)
    
    Returns:
        American odds (e.g., -110, +150)
    """
    if decimal_odds >= 2.0:
        return int(round((decimal_odds - 1) * 100))
    else:
        return int(round(-100 / (decimal_odds - 1)))

