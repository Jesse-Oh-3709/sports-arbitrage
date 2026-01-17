import React from 'react';
import { TrendingUp, AlertCircle, User, Target } from 'lucide-react';
import { decimalToAmerican, formatGameTime } from '../utils/oddsConverter';

/**
 * PlayerPropsTable Component
 * Displays arbitrage opportunities for player prop markets
 * 
 * @param {Object} props
 * @param {Array} props.playerProps - Array of player prop arbitrage opportunities
 * @param {boolean} props.loading - Loading state
 * @param {string} props.error - Error message if any
 */
const PlayerPropsTable = ({ playerProps, loading, error }) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-400"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/30 border border-red-500 rounded-lg p-4 flex items-center gap-3">
        <AlertCircle className="text-red-400" size={24} />
        <div>
          <p className="font-semibold text-red-400">Error Loading Player Props</p>
          <p className="text-sm text-red-300">{error}</p>
        </div>
      </div>
    );
  }

  if (!playerProps || playerProps.length === 0) {
    return (
      <div className="text-center py-12 text-slate-400">
        <Target size={48} className="mx-auto mb-4 opacity-50" />
        <p className="text-lg">No player prop arbitrage opportunities found</p>
        <div className="bg-yellow-900/30 border border-yellow-500/50 rounded-lg p-4 mt-4 max-w-2xl mx-auto">
          <p className="text-yellow-400 text-sm font-semibold mb-2">⚠️ Player Props Not Available</p>
          <p className="text-yellow-300 text-sm">
            The Odds API does not currently support player prop markets in their standard API. 
            Player props may require a paid subscription tier or may not be available at all.
          </p>
          <p className="text-yellow-200 text-xs mt-2">
            The code is ready to process player props when/if they become available in the API.
          </p>
        </div>
      </div>
    );
  }

  // Group player props by player name for better organization
  const groupedProps = {};
  playerProps.forEach(prop => {
    const key = `${prop.player_name}_${prop.prop_type}`;
    if (!groupedProps[key]) {
      groupedProps[key] = [];
    }
    groupedProps[key].push(prop);
  });

  return (
    <div className="space-y-4">
      {Object.entries(groupedProps).map(([key, props]) => {
        const firstProp = props[0];
        return (
          <div 
            key={key}
            className="bg-gradient-to-r from-blue-900/40 to-indigo-900/40 border-l-4 border-blue-400 rounded-lg overflow-hidden"
          >
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <User className="text-blue-400" size={20} />
                    <span className="bg-blue-600 px-3 py-1 rounded text-xs font-semibold">
                      {firstProp.sport}
                    </span>
                    <span className="bg-slate-700 px-3 py-1 rounded text-xs font-semibold">
                      {firstProp.prop_type.toUpperCase()}
                    </span>
                    {firstProp.prop_line && (
                      <span className="bg-purple-600 px-3 py-1 rounded text-xs">
                        Line: {firstProp.prop_line}
                      </span>
                    )}
                    {firstProp.commence_time && (
                      <span className="bg-slate-700 px-3 py-1 rounded text-xs flex items-center gap-1">
                        <Target size={12} />
                        {formatGameTime(firstProp.commence_time)}
                      </span>
                    )}
                  </div>
                  
                  <h3 className="text-xl font-bold text-white mb-1">
                    {firstProp.player_name}
                  </h3>
                  <p className="text-sm text-slate-400 mb-2">
                    {firstProp.match}
                  </p>
                </div>
                
                <div className="text-right">
                  <div className="flex items-center gap-2 text-blue-400">
                    <TrendingUp size={24} />
                    <span className="text-3xl font-bold">
                      {firstProp.profit_percentage}%
                    </span>
                  </div>
                  <p className="text-sm text-slate-300 mt-1">Profit Margin</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                {props.map((prop, idx) => (
                  <div key={idx} className="bg-slate-800/70 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs text-slate-400">Opportunity #{idx + 1}</span>
                      <span className="text-xs text-green-400 font-semibold">
                        {prop.profit_percentage}% profit
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <p className="text-slate-400 text-xs mb-1">
                          Bet <span className="font-semibold text-white">{prop.outcome_a}</span>
                        </p>
                        <p className="text-lg font-bold text-white mb-1">{prop.sportsbook_a}</p>
                        <div className="flex items-baseline gap-2">
                          <span className="text-2xl font-bold text-blue-400">
                            {decimalToAmerican(prop.odds_a)}
                          </span>
                          <span className="text-slate-400 text-xs">({prop.odds_a.toFixed(2)})</span>
                        </div>
                        <div className="mt-2 pt-2 border-t border-slate-700">
                          <p className="text-slate-400 text-xs">Stake</p>
                          <p className="text-sm font-bold text-green-400">${prop.stake_a}</p>
                        </div>
                      </div>

                      <div>
                        <p className="text-slate-400 text-xs mb-1">
                          Bet <span className="font-semibold text-white">{prop.outcome_b}</span>
                        </p>
                        <p className="text-lg font-bold text-white mb-1">{prop.sportsbook_b}</p>
                        <div className="flex items-baseline gap-2">
                          <span className="text-2xl font-bold text-blue-400">
                            {decimalToAmerican(prop.odds_b)}
                          </span>
                          <span className="text-slate-400 text-xs">({prop.odds_b.toFixed(2)})</span>
                        </div>
                        <div className="mt-2 pt-2 border-t border-slate-700">
                          <p className="text-slate-400 text-xs">Stake</p>
                          <p className="text-sm font-bold text-green-400">${prop.stake_b}</p>
                        </div>
                      </div>
                    </div>

                    <div className="mt-3 pt-3 border-t border-slate-700 bg-slate-900/50 rounded p-2">
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-slate-400">Guaranteed Profit</span>
                        <span className="text-lg font-bold text-green-400">
                          ${prop.guaranteed_profit}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {firstProp.timestamp && (
                <div className="mt-3 text-xs text-slate-500 text-right">
                  ⏱️ Data fetched: {new Date(firstProp.timestamp).toLocaleString()}
                  <span className="ml-2 text-yellow-400">
                    ⚠️ Always verify odds on actual sportsbook before betting
                  </span>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default PlayerPropsTable;

