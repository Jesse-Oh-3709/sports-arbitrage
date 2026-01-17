"""
Filtering utilities for games and markets
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional


def filter_prematch(
    games: List[Dict], 
    now: Optional[datetime] = None, 
    grace_min: int = 0, 
    include_live: bool = False
) -> List[Dict]:
    """
    Filter games to only include pre-match (upcoming) games
    
    Args:
        games: List of game data
        now: Current time (defaults to UTC now)
        grace_min: Exclude games starting within this many minutes
        include_live: Whether to include live games (default False)
    
    Returns:
        Filtered list of upcoming games only
    """
    now = now or datetime.now(timezone.utc)
    out = []
    
    for game in games:
        # Exclude live games unless explicitly included
        if not include_live and game.get("live", False):
            continue
        
        # Parse commence time
        commence_str = game.get("commence_time", "")
        if not commence_str:
            continue
        
        try:
            start = datetime.fromisoformat(commence_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            continue
        
        # Ensure start is timezone-aware
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        
        # Ensure now is timezone-aware
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        
        # Exclude games that have already started
        if start <= now:
            continue
        
        # Exclude games starting too soon (grace period)
        if grace_min and (start - now).total_seconds() < grace_min * 60:
            continue
        
        out.append(game)
    
    return out


def is_game_started(commence_time: str, now: Optional[datetime] = None) -> bool:
    """
    Check if a game has already started
    
    Args:
        commence_time: ISO format time string
        now: Current time (defaults to UTC now)
    
    Returns:
        True if game has started, False otherwise
    """
    now = now or datetime.now(timezone.utc)
    
    try:
        start = datetime.fromisoformat(commence_time.replace("Z", "+00:00"))
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        
        return start <= now
    except (ValueError, AttributeError):
        return False


def get_time_until_game(commence_time: str, now: Optional[datetime] = None) -> int:
    """
    Get seconds until game starts
    
    Args:
        commence_time: ISO format time string
        now: Current time (defaults to UTC now)
    
    Returns:
        Seconds until game starts (negative if already started)
    """
    now = now or datetime.now(timezone.utc)
    
    try:
        start = datetime.fromisoformat(commence_time.replace("Z", "+00:00"))
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        
        return int((start - now).total_seconds())
    except (ValueError, AttributeError):
        return 0

