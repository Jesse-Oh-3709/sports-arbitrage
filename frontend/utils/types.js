/**
 * TypeScript-style type definitions for the Sports Arbitrage App
 * Note: This is a .js file for compatibility, but includes JSDoc type annotations
 */

/**
 * @typedef {Object} ArbitrageOpportunity
 * @property {string} match - Game/match identifier
 * @property {string} sport - Sport name
 * @property {string} market - Market type (h2h, spreads, totals, player_points, etc.)
 * @property {('game'|'player_prop')} market_type - Type of market
 * @property {string} [player_name] - Player name (for player props)
 * @property {string} [prop_type] - Prop type (points, assists, rebounds, etc.)
 * @property {number} [prop_line] - Prop line value (e.g., 25.5 for points)
 * @property {string} commence_time - Game start time
 * @property {string} sportsbook_a - First sportsbook name
 * @property {number} odds_a - Odds at first sportsbook
 * @property {string} outcome_a - Outcome at first sportsbook
 * @property {string} sportsbook_b - Second sportsbook name
 * @property {number} odds_b - Odds at second sportsbook
 * @property {string} outcome_b - Outcome at second sportsbook
 * @property {string} [sportsbook_c] - Third sportsbook (for 3-way markets)
 * @property {number} [odds_c] - Odds at third sportsbook
 * @property {string} [outcome_c] - Outcome at third sportsbook
 * @property {number} profit_percentage - Profit percentage
 * @property {number} implied_probability - Implied probability
 * @property {number} stake_a - Recommended stake at first sportsbook
 * @property {number} stake_b - Recommended stake at second sportsbook
 * @property {number} [stake_c] - Recommended stake at third sportsbook
 * @property {number} guaranteed_profit - Guaranteed profit amount
 * @property {string} timestamp - Timestamp of data fetch
 * @property {Object} [warning] - Warning information if applicable
 */

/**
 * @typedef {Object} PlayerPropArbitrage
 * @property {string} match - Game/match identifier
 * @property {string} sport - Sport name
 * @property {string} player_name - Player name
 * @property {string} prop_type - Type of prop (points, assists, rebounds, etc.)
 * @property {number} prop_line - Prop line value
 * @property {string} sportsbook_a - First sportsbook
 * @property {number} odds_a - Odds at first sportsbook
 * @property {string} outcome_a - Outcome (Over/Under)
 * @property {string} sportsbook_b - Second sportsbook
 * @property {number} odds_b - Odds at second sportsbook
 * @property {string} outcome_b - Outcome (Over/Under)
 * @property {number} profit_percentage - Profit percentage
 * @property {number} guaranteed_profit - Guaranteed profit
 */

export {};

