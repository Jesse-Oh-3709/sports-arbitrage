"""
Validation utilities for odds and arbitrage calculations
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any


def validate_odds(odds: float) -> bool:
    """
    Validate that odds are within realistic range
    
    Args:
        odds: Decimal odds value
    
    Returns:
        True if valid, False otherwise
    """
    return 1.1 <= odds <= 15.0


def implied_sum(*odds: float) -> float:
    """
    Calculate implied probability sum
    
    Args:
        *odds: Variable number of decimal odds
    
    Returns:
        Sum of implied probabilities (1/odds for each)
    """
    return sum(1/o for o in odds)


def age_seconds(ts_iso: str, now: Optional[datetime] = None) -> float:
    """
    Calculate age of odds data in seconds
    
    Args:
        ts_iso: ISO format timestamp
        now: Current time (defaults to UTC now)
    
    Returns:
        Age in seconds (0 if parsing fails)
    """
    now = now or datetime.now(timezone.utc)
    
    try:
        ts = datetime.fromisoformat(ts_iso.replace("Z", "+00:00"))
        
        # Ensure both are timezone-aware
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        
        return max(0, (now - ts).total_seconds())
    except (ValueError, AttributeError):
        return 0


def confidence_from_roi(roi: float) -> str:
    """
    Determine confidence level from ROI percentage
    
    Args:
        roi: Return on investment percentage
    
    Returns:
        Confidence tier: "low", "moderate", or "verify_odds"
    """
    if roi > 5.0:
        return "verify_odds"
    elif roi > 2.0:
        return "moderate"
    else:
        return "low"


def get_confidence_tooltip(confidence: str) -> str:
    """
    Get tooltip text for confidence level
    
    Args:
        confidence: Confidence tier
    
    Returns:
        Tooltip text
    """
    tooltips = {
        "low": "Pre-match arb within realistic range (≤2%).",
        "moderate": "Verify quickly; odds may move (2–5%).",
        "verify_odds": "Unusually high ROI—confirm lines & timestamps."
    }
    return tooltips.get(confidence, "Unknown confidence level")


def validate_arbitrage_data(
    odds_a: float,
    odds_b: float,
    timestamp_a: Optional[str] = None,
    timestamp_b: Optional[str] = None,
    max_age_seconds: int = 30
) -> Dict[str, Any]:
    """
    Comprehensive validation for arbitrage data
    
    Args:
        odds_a: First odds value
        odds_b: Second odds value
        timestamp_a: Timestamp for first odds
        timestamp_b: Timestamp for second odds
        max_age_seconds: Maximum acceptable age for odds data
    
    Returns:
        Dictionary with validation results
    """
    errors = []
    
    # Validate odds ranges
    if not validate_odds(odds_a):
        errors.append(f"Odds A ({odds_a}) outside valid range [1.1, 15.0]")
    if not validate_odds(odds_b):
        errors.append(f"Odds B ({odds_b}) outside valid range [1.1, 15.0]")
    
    # Calculate implied probability sum
    imp_sum = implied_sum(odds_a, odds_b)
    
    # Check for realistic implied probability
    if imp_sum < 0.80:
        errors.append(f"Implied probability sum too low ({imp_sum:.3f}). Likely stale or mismatched odds.")
    elif imp_sum > 1.10:
        errors.append(f"Implied probability sum too high ({imp_sum:.3f}). Check for data errors.")
    
    # Check timestamp freshness
    if timestamp_a:
        age_a = age_seconds(timestamp_a)
        if age_a > max_age_seconds:
            errors.append(f"Odds A is stale ({age_a:.0f}s old, max {max_age_seconds}s)")
    
    if timestamp_b:
        age_b = age_seconds(timestamp_b)
        if age_b > max_age_seconds:
            errors.append(f"Odds B is stale ({age_b:.0f}s old, max {max_age_seconds}s)")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "implied_sum": imp_sum,
        "warnings": []
    }

