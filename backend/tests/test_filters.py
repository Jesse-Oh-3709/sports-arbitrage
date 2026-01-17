"""
Unit tests for game filtering utilities
"""
import pytest
from datetime import datetime, timedelta, timezone
from utils.filters import filter_prematch, is_game_started, get_time_until_game


def test_filter_prematch_excludes_live_and_started():
    """Test that live and already-started games are excluded by default"""
    now = datetime(2025, 10, 9, 22, 0, 0, tzinfo=timezone.utc)
    
    games = [
        # Started 1 minute ago
        {
            "commence_time": (now - timedelta(minutes=1)).isoformat(),
            "live": False
        },
        # Live game (in progress)
        {
            "commence_time": (now + timedelta(minutes=1)).isoformat(),
            "live": True
        },
        # Valid upcoming game
        {
            "commence_time": (now + timedelta(hours=1)).isoformat(),
            "live": False
        },
    ]
    
    out = filter_prematch(games, now=now, include_live=False)
    
    # Should only include the valid upcoming game
    assert len(out) == 1
    assert out[0]["commence_time"] == games[2]["commence_time"]


def test_filter_prematch_with_grace_period():
    """Test grace period excludes games starting too soon"""
    now = datetime(2025, 10, 9, 22, 0, 0, tzinfo=timezone.utc)
    
    games = [
        # Starting in 30 seconds
        {
            "commence_time": (now + timedelta(seconds=30)).isoformat(),
            "live": False
        },
        # Starting in 10 minutes
        {
            "commence_time": (now + timedelta(minutes=10)).isoformat(),
            "live": False
        },
    ]
    
    # With 5-minute grace period
    out = filter_prematch(games, now=now, grace_min=5, include_live=False)
    
    # Should only include game starting in 10 minutes
    assert len(out) == 1


def test_filter_prematch_includes_live_when_requested():
    """Test that live games are included when include_live=True"""
    now = datetime(2025, 10, 9, 22, 0, 0, tzinfo=timezone.utc)
    
    games = [
        # Live game
        {
            "commence_time": (now + timedelta(minutes=1)).isoformat(),
            "live": True
        },
    ]
    
    # With include_live=False (default)
    out_no_live = filter_prematch(games, now=now, include_live=False)
    assert len(out_no_live) == 0
    
    # With include_live=True
    out_with_live = filter_prematch(games, now=now, include_live=True)
    assert len(out_with_live) == 1


def test_is_game_started():
    """Test game start detection"""
    now = datetime(2025, 10, 9, 22, 0, 0, tzinfo=timezone.utc)
    
    # Game started 10 minutes ago
    past_game = (now - timedelta(minutes=10)).isoformat()
    assert is_game_started(past_game, now) is True
    
    # Game starting in 1 hour
    future_game = (now + timedelta(hours=1)).isoformat()
    assert is_game_started(future_game, now) is False
    
    # Game starting right now (edge case)
    now_game = now.isoformat()
    assert is_game_started(now_game, now) is True


def test_get_time_until_game():
    """Test time-until-game calculation"""
    now = datetime(2025, 10, 9, 22, 0, 0, tzinfo=timezone.utc)
    
    # Game in 1 hour
    future_game = (now + timedelta(hours=1)).isoformat()
    time_until = get_time_until_game(future_game, now)
    assert time_until == 3600  # 1 hour in seconds
    
    # Game started 30 minutes ago
    past_game = (now - timedelta(minutes=30)).isoformat()
    time_until = get_time_until_game(past_game, now)
    assert time_until == -1800  # Negative = already started


def test_filter_handles_missing_commence_time():
    """Test filter gracefully handles missing commence_time"""
    games = [
        {"live": False},  # No commence_time
        {"commence_time": "", "live": False},  # Empty commence_time
    ]
    
    out = filter_prematch(games)
    
    # Should exclude both (no valid commence_time)
    assert len(out) == 0


def test_filter_handles_invalid_timestamps():
    """Test filter handles malformed timestamps"""
    games = [
        {"commence_time": "invalid-timestamp", "live": False},
        {"commence_time": "2025-99-99T99:99:99Z", "live": False},
    ]
    
    out = filter_prematch(games)
    
    # Should exclude both (invalid timestamps)
    assert len(out) == 0

