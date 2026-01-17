import React from 'react';
import { TrendingUp, AlertCircle, Clock } from 'lucide-react';
import { decimalToAmerican, formatGameTime } from '../utils/oddsConverter';

const ArbitrageTable = ({ arbitrages, loading, error }) => {
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
          <p className="font-semibold text-red-400">Error Loading Arbitrages</p>
          <p className="text-sm text-red-300">{error}</p>
        </div>
      </div>
    );
  }

  if (!arbitrages || arbitrages.length === 0) {
    return (
      <div className="text-center py-12 text-slate-400">
        <AlertCircle size={48} className="mx-auto mb-4 opacity-50" />
        <p className="text-lg">No arbitrage opportunities found</p>
        <p className="text-sm mt-2">Try adjusting your filters or check back later</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {arbitrages.map((arb, index) => (
        <div 
          key={index}
          className="bg-gradient-to-r from-green-900/40 to-emerald-900/40 border-l-4 border-green-400 rounded-lg overflow-hidden"
        >
          <div className="p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="bg-blue-600 px-3 py-1 rounded text-xs font-semibold">
                    {arb.sport}
                  </span>
                  <span className="bg-slate-700 px-3 py-1 rounded text-xs font-semibold">
                    {arb.market.toUpperCase()}
                  </span>
                  {arb.implied_probability && (
                    <span className="bg-slate-600 px-3 py-1 rounded text-xs">
                      Implied: {(arb.implied_probability * 100).toFixed(2)}%
                    </span>
                  )}
                  {arb.warning && arb.warning.level && (
                    <span className={`px-3 py-1 rounded text-xs font-semibold ${
                      arb.warning.level === 'verify_odds' ? 'bg-yellow-600 text-yellow-100' :
                      arb.warning.level === 'moderate' ? 'bg-orange-600 text-orange-100' :
                      'bg-green-600 text-green-100'
                    }`} title={arb.warning.description || ''}>
                      {arb.warning.emoji} {arb.warning.level.toUpperCase().replace('_', ' ')}
                    </span>
                  )}
                  {arb.commence_time && (
                    <span className="bg-slate-700 px-3 py-1 rounded text-xs flex items-center gap-1">
                      <Clock size={12} />
                      {formatGameTime(arb.commence_time)}
                    </span>
                  )}
                </div>
                <h3 className="text-xl font-bold text-white">{arb.match}</h3>
                
                {/* Warning Message */}
                {arb.warning && (
                  <div className={`mt-2 px-3 py-2 rounded-lg flex items-center gap-2 text-sm ${
                    arb.warning.level === 'critical' ? 'bg-yellow-900/40 border border-yellow-500/50 text-yellow-300' :
                    arb.warning.level === 'moderate' ? 'bg-orange-900/40 border border-orange-500/50 text-orange-300' :
                    'bg-blue-900/40 border border-blue-500/50 text-blue-300'
                  }`}>
                    <span className="text-lg">{arb.warning.emoji}</span>
                    <div>
                      <p className="font-semibold">{arb.warning.message}</p>
                      <p className="text-xs opacity-90">{arb.warning.description}</p>
                    </div>
                  </div>
                )}
              </div>
              <div className="text-right">
                <div className={`flex items-center gap-2 ${
                  arb.warning?.level === 'critical' ? 'text-yellow-400' : 'text-green-400'
                }`}>
                  <TrendingUp size={24} />
                  <span className="text-3xl font-bold">{arb.profit_percentage}%</span>
                </div>
                <p className="text-sm text-slate-300 mt-1">Profit Margin</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div className="bg-slate-800/70 rounded-lg p-4">
                <p className="text-slate-400 text-sm mb-2">
                  Bet on <span className="font-semibold text-white">{arb.outcome_a}</span>
                </p>
                <p className="text-xl font-bold text-white mb-1">{arb.sportsbook_a}</p>
                <div className="flex items-baseline gap-3">
                  <span className="text-3xl font-bold text-green-400">{decimalToAmerican(arb.odds_a)}</span>
                  <span className="text-slate-400 text-sm">({arb.odds_a.toFixed(2)})</span>
                </div>
                <div className="mt-3 pt-3 border-t border-slate-700">
                  <p className="text-slate-400 text-sm">Stake (of $1,000 total)</p>
                  <p className="text-lg font-bold text-green-400">${arb.stake_a}</p>
                </div>
              </div>

              <div className="bg-slate-800/70 rounded-lg p-4">
                <p className="text-slate-400 text-sm mb-2">
                  Bet on <span className="font-semibold text-white">{arb.outcome_b}</span>
                </p>
                <p className="text-xl font-bold text-white mb-1">{arb.sportsbook_b}</p>
                <div className="flex items-baseline gap-3">
                  <span className="text-3xl font-bold text-green-400">{decimalToAmerican(arb.odds_b)}</span>
                  <span className="text-slate-400 text-sm">({arb.odds_b.toFixed(2)})</span>
                </div>
                <div className="mt-3 pt-3 border-t border-slate-700">
                  <p className="text-slate-400 text-sm">Stake (of $1,000 total)</p>
                  <p className="text-lg font-bold text-green-400">${arb.stake_b}</p>
                </div>
              </div>

              {arb.sportsbook_c && (
                <div className="bg-slate-800/70 rounded-lg p-4 md:col-span-2">
                  <p className="text-slate-400 text-sm mb-2">
                    Bet on <span className="font-semibold text-white">{arb.outcome_c}</span>
                  </p>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xl font-bold text-white mb-1">{arb.sportsbook_c}</p>
                      <div className="flex items-baseline gap-3">
                        <span className="text-3xl font-bold text-green-400">{decimalToAmerican(arb.odds_c)}</span>
                        <span className="text-slate-400 text-sm">({arb.odds_c.toFixed(2)})</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-slate-400 text-sm">Stake (of $1,000 total)</p>
                      <p className="text-lg font-bold text-green-400">${arb.stake_c}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="bg-slate-900/50 rounded-lg p-4 border border-green-400/30">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-400 text-sm">Guaranteed Profit</p>
                  <p className="text-2xl font-bold text-green-400">${arb.guaranteed_profit}</p>
                </div>
                <div className="text-right">
                  <p className="text-slate-400 text-sm">Return on Investment</p>
                  <p className="text-xl font-bold text-green-400">
                    {((arb.guaranteed_profit / 1000) * 100).toFixed(2)}%
                  </p>
                </div>
              </div>
            </div>

            {arb.timestamp && (
              <div className="mt-3 text-xs text-slate-500 text-right">
                ⏱️ Data fetched: {new Date(arb.timestamp).toLocaleString()}
                <span className="ml-2 text-yellow-400">
                  ⚠️ Always verify odds on actual sportsbook before betting
                </span>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ArbitrageTable;

