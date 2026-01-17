"""
Unit tests for market matching utilities
"""
import pytest
from utils.matching import same_market, get_market_identifier, is_valid_two_way_pairing


def test_same_market_h2h():
    """Test market matching for head-to-head (moneyline)"""
    market1 = {"key": "h2h"}
    market2 = {"key": "h2h"}
    
    # Same market
    assert same_market(market1, market2) is True
    
    # Different market
    market3 = {"key": "spreads"}
    assert same_market(market1, market3) is False


def test_same_market_spreads_matching_point():
    """Test spread markets with same point value"""
    market1 = {"key": "spreads", "point": -1.5}
    market2 = {"key": "spreads", "point": -1.5}
    
    # Same spread
    assert same_market(market1, market2) is True


def test_same_market_spreads_different_point():
    """Test spread markets with different point values are NOT same"""
    market1 = {"key": "spreads", "point": -1.5}
    market2 = {"key": "spreads", "point": -2.5}
    
    # Different spreads - NOT the same market!
    assert same_market(market1, market2) is False


def test_same_market_totals_matching():
    """Test totals markets with same total value"""
    market1 = {"key": "totals", "point": 45.5}
    market2 = {"key": "totals", "point": 45.5}
    
    assert same_market(market1, market2) is True
    
    # Different totals
    market3 = {"key": "totals", "point": 46.5}
    assert same_market(market1, market3) is False


def test_get_market_identifier():
    """Test market identifier generation"""
    # H2H
    assert get_market_identifier({"key": "h2h"}) == "h2h"
    
    # Spreads with point
    assert get_market_identifier({"key": "spreads", "point": -1.5}) == "spreads_-1.5"
    
    # Totals with point
    assert get_market_identifier({"key": "totals", "point": 45.5}) == "totals_45.5"


def test_is_valid_two_way_pairing():
    """Test validation of outcome pairings"""
    market1 = {
        "key": "h2h",
        "outcomes": [
            {"name": "Team A", "price": 1.91},
            {"name": "Team B", "price": 2.10}
        ]
    }
    
    market2 = {
        "key": "h2h",
        "outcomes": [
            {"name": "Team A", "price": 1.95},
            {"name": "Team B", "price": 2.05}
        ]
    }
    
    # Valid: Team A from market1 vs Team B from market2
    assert is_valid_two_way_pairing(market1, "Team A", market2, "Team B") is True
    
    # Invalid: Same outcome from both markets
    assert is_valid_two_way_pairing(market1, "Team A", market2, "Team A") is False
    
    # Invalid: Different market keys
    market3 = {"key": "spreads", "point": -1.5, "outcomes": market1["outcomes"]}
    assert is_valid_two_way_pairing(market1, "Team A", market3, "Team B") is False


def test_spread_market_requires_exact_point_match():
    """Test that spread arbitrage requires exact same handicap"""
    # Dodgers -1.5 from two books
    market1 = {
        "key": "spreads",
        "point": -1.5,
        "outcomes": [
            {"name": "Dodgers", "price": 1.91},
            {"name": "Phillies", "price": 2.00}
        ]
    }
    
    # Same spread (-1.5)
    market2 = {
        "key": "spreads",
        "point": -1.5,
        "outcomes": [
            {"name": "Dodgers", "price": 1.95},
            {"name": "Phillies", "price": 1.96}
        ]
    }
    
    # Different spread (-2.5) - NOT VALID for arbitrage!
    market3 = {
        "key": "spreads",
        "point": -2.5,
        "outcomes": [
            {"name": "Dodgers", "price": 2.20},
            {"name": "Phillies", "price": 1.75}
        ]
    }
    
    # Same spread = valid
    assert is_valid_two_way_pairing(market1, "Dodgers", market2, "Phillies") is True
    
    # Different spread = invalid
    assert is_valid_two_way_pairing(market1, "Dodgers", market3, "Phillies") is False

