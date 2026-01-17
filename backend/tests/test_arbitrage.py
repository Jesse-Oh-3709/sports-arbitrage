"""
Unit tests for arbitrage calculation utilities
"""
import pytest
import math
from utils.arbitrage import is_arbitrage, roi_percent, stake_split
from utils.odds import to_decimal
from utils.validations import validate_odds, implied_sum, confidence_from_roi


def test_odds_conversion():
    """Test odds conversion from various formats to decimal"""
    # Decimal (unchanged)
    assert math.isclose(to_decimal(1.91), 1.91)
    
    # American positive
    assert math.isclose(to_decimal(110), 2.10, rel_tol=1e-6)
    assert math.isclose(to_decimal("+110"), 2.10, rel_tol=1e-6)
    
    # American negative
    assert math.isclose(to_decimal(-130), 1 + 100/130, rel_tol=1e-6)
    assert math.isclose(to_decimal("-130"), 1.769230769, rel_tol=1e-6)
    
    # Fractional
    assert math.isclose(to_decimal("13/8"), 1 + 13/8, rel_tol=1e-6)
    assert math.isclose(to_decimal("5/2"), 3.5, rel_tol=1e-6)


def test_is_arbitrage_positive_case():
    """Test detection of valid arbitrage opportunity"""
    # Actual small arb - realistic scenario
    # Need implied prob < 1: 1/2.08 + 1/2.06 = 0.4808 + 0.4854 = 0.9662 < 1
    o1, o2 = 2.08, 2.06
    
    # This should be a valid arbitrage
    assert is_arbitrage(o1, o2) is True
    
    # Calculate ROI
    roi = roi_percent(o1, o2)
    
    # This creates ~3.5% arbitrage (moderate range)
    assert 2.0 < roi < 5.0


def test_is_arbitrage_negative_case():
    """Test detection of no arbitrage (normal market with vig)"""
    o1, o2 = 1.60, 2.10
    
    # Implied prob = 1/1.60 + 1/2.10 = 0.625 + 0.476 = 1.101 > 1
    # No arbitrage exists
    assert is_arbitrage(o1, o2) is False


def test_stake_split_rounding():
    """Test stake allocation rounds correctly and sums to total"""
    o1, o2, total = 1.77, 2.10, 1000
    s1, s2 = stake_split(total, o1, o2)
    
    # Stakes should sum to total (within rounding tolerance)
    assert round(s1 + s2, 2) == 1000.00
    
    # Both stakes should be positive
    assert s1 > 0
    assert s2 > 0
    
    # Verify guaranteed return is equal for both outcomes
    return1 = s1 * o1
    return2 = s2 * o2
    assert math.isclose(return1, return2, rel_tol=0.01)


def test_validate_odds_range():
    """Test odds validation rejects out-of-range values"""
    # Valid range: 1.1 to 15.0
    assert validate_odds(1.2) is True
    assert validate_odds(2.0) is True
    assert validate_odds(10.0) is True
    
    # Invalid - too low
    assert validate_odds(0.5) is False
    assert validate_odds(1.0) is False
    
    # Invalid - too high
    assert validate_odds(20.0) is False
    assert validate_odds(100.0) is False


def test_implied_sum_reasonable_band():
    """Test implied probability sum for realistic markets"""
    # Normal market (no arb) - typical MLB with vig
    s_no_arb = implied_sum(1.77, 2.10)
    assert s_no_arb > 1.0  # Has bookmaker margin
    assert 1.00 < s_no_arb < 1.10  # Within realistic band
    
    # Arbitrage market
    s_arb = implied_sum(2.08, 2.06)
    assert s_arb < 1.0  # Arbitrage exists
    assert 0.95 < s_arb < 1.00  # Within realistic arb band


def test_confidence_tiers():
    """Test confidence tier assignment based on ROI"""
    # Low confidence: ≤2%
    assert confidence_from_roi(0.9) == "low"
    assert confidence_from_roi(1.5) == "low"
    assert confidence_from_roi(2.0) == "low"
    
    # Moderate confidence: 2-5%
    assert confidence_from_roi(2.1) == "moderate"
    assert confidence_from_roi(3.1) == "moderate"
    assert confidence_from_roi(4.9) == "moderate"
    
    # Verify odds: >5%
    assert confidence_from_roi(5.1) == "verify_odds"
    assert confidence_from_roi(9.0) == "verify_odds"
    assert confidence_from_roi(15.0) == "verify_odds"


def test_realistic_mlb_scenario():
    """Test realistic MLB arbitrage scenario"""
    # DraftKings: Team A @ 2.08 (slight underdog)
    # BetMGM: Team B @ 2.06 (slight underdog)
    # This can happen when books disagree on which team is favorite
    dk_odds = 2.08
    betmgm_odds = 2.06
    
    # Should be small arbitrage
    assert is_arbitrage(dk_odds, betmgm_odds) is True
    
    roi = roi_percent(dk_odds, betmgm_odds)
    
    # Should be realistic (2-4% range)
    assert 2.0 < roi < 5.0
    
    # Verify stakes
    s1, s2 = stake_split(1000, dk_odds, betmgm_odds)
    assert s1 + s2 == 1000.00


def test_impossible_scenario_both_underdogs():
    """Test that both underdogs scenario is rejected"""
    # Both odds suggest underdogs (impossible)
    o1, o2 = 2.46, 2.95
    
    # This creates artificially high ROI
    # Should be flagged in validation
    imp_sum = implied_sum(o1, o2)
    
    # Implied sum too low (both underdogs)
    assert imp_sum < 0.80
    
    # If someone tries to calculate ROI anyway
    if is_arbitrage(o1, o2):
        roi = roi_percent(o1, o2)
        confidence = confidence_from_roi(roi)
        # Should be flagged for verification
        assert confidence == "verify_odds"


def test_zero_vig_line():
    """Test perfectly balanced no-vig line"""
    # Perfect 50/50 line with no vig
    o1, o2 = 2.0, 2.0
    
    # This is an arbitrage (implied prob = 1.0)
    # In reality, this would be even money
    imp_sum = implied_sum(o1, o2)
    assert imp_sum == 1.0
    
    # Technically right at the edge
    # Not an arbitrage (need < 1.0, not <=)
    assert is_arbitrage(o1, o2) is False


def test_heavy_favorite_scenario():
    """Test heavy favorite odds (common in sports)"""
    # Heavy favorite: -500 (1.20 decimal)
    # Underdog: +350 (4.50 decimal)
    favorite = to_decimal(-500)
    underdog = to_decimal(350)
    
    assert math.isclose(favorite, 1.20, rel_tol=0.01)
    assert math.isclose(underdog, 4.50, rel_tol=0.01)
    
    # These shouldn't create arbitrage (normal vig market)
    assert is_arbitrage(favorite, underdog) is False
    
    # Implied sum should be > 1 (bookmaker margin)
    imp_sum = implied_sum(favorite, underdog)
    assert imp_sum > 1.0


def test_fractional_odds_conversion():
    """Test fractional odds commonly used in UK"""
    # 5/2 (fractional) = 3.5 (decimal)
    assert math.isclose(to_decimal("5/2"), 3.5)
    
    # 6/4 (fractional) = 2.5 (decimal)
    assert math.isclose(to_decimal("6/4"), 2.5)
    
    # 13/8 (fractional) = 2.625 (decimal)
    assert math.isclose(to_decimal("13/8"), 2.625)


def test_stake_split_guarantees_equal_return():
    """Test that stake split guarantees equal return on both outcomes"""
    o1, o2 = 2.05, 2.08
    s1, s2 = stake_split(1000, o1, o2)
    
    # Calculate returns
    return1 = s1 * o1
    return2 = s2 * o2
    
    # Returns should be equal (within rounding)
    assert math.isclose(return1, return2, abs_tol=0.01)
    
    # Profit should be same regardless of outcome
    profit1 = return1 - 1000
    profit2 = return2 - 1000
    assert math.isclose(profit1, profit2, abs_tol=0.01)

