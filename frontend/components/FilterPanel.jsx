import React from 'react';
import { Filter, RefreshCw } from 'lucide-react';

const FilterPanel = ({ 
  filters, 
  onFilterChange, 
  onRefresh, 
  isRefreshing,
  apiKeyConfigured 
}) => {
  const sports = [
    { value: 'upcoming', label: 'All Upcoming' },
    { value: 'americanfootball_nfl', label: 'NFL' },
    { value: 'basketball_nba', label: 'NBA' },
    { value: 'baseball_mlb', label: 'MLB' },
    { value: 'icehockey_nhl', label: 'NHL' },
    { value: 'soccer_epl', label: 'EPL Soccer' },
    { value: 'soccer_uefa_champs_league', label: 'UEFA Champions League' }
  ];

  const markets = [
    { value: 'h2h', label: 'Moneyline (H2H)' },
    { value: 'spreads', label: 'Spreads' },
    { value: 'totals', label: 'Totals (O/U)' },
    { value: 'h2h,spreads', label: 'Moneyline + Spreads' },
    { value: 'h2h,totals', label: 'Moneyline + Totals' },
    { value: 'h2h,spreads,totals', label: 'All Markets' }
  ];

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold flex items-center gap-2">
          <Filter size={20} />
          Filters
        </h2>
        <button
          onClick={onRefresh}
          disabled={isRefreshing || !apiKeyConfigured}
          className={`flex items-center gap-2 px-4 py-2 rounded font-semibold transition ${
            isRefreshing || !apiKeyConfigured
              ? 'bg-slate-600 cursor-not-allowed'
              : 'bg-green-600 hover:bg-green-700'
          }`}
        >
          <RefreshCw size={18} className={isRefreshing ? 'animate-spin' : ''} />
          {isRefreshing ? 'Refreshing...' : 'Refresh Odds'}
        </button>
      </div>

      {!apiKeyConfigured && (
        <div className="bg-yellow-900/30 border border-yellow-500/50 rounded-lg p-3 mb-4">
          <p className="text-yellow-400 text-sm">
            ⚠️ API key not configured. Live odds fetching is disabled. 
            <a 
              href="https://the-odds-api.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="underline ml-1 hover:text-yellow-300"
            >
              Get your free API key
            </a>
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Sport
          </label>
          <select
            value={filters.sport}
            onChange={(e) => onFilterChange('sport', e.target.value)}
            className="w-full bg-slate-700 rounded px-3 py-2 border border-slate-600 focus:border-green-400 focus:outline-none"
          >
            {sports.map(sport => (
              <option key={sport.value} value={sport.value}>
                {sport.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Markets
          </label>
          <select
            value={filters.markets}
            onChange={(e) => onFilterChange('markets', e.target.value)}
            className="w-full bg-slate-700 rounded px-3 py-2 border border-slate-600 focus:border-green-400 focus:outline-none"
          >
            {markets.map(market => (
              <option key={market.value} value={market.value}>
                {market.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Min Profit %
          </label>
          <input
            type="number"
            step="0.1"
            min="0"
            max="100"
            value={filters.minProfit}
            onChange={(e) => onFilterChange('minProfit', e.target.value)}
            className="w-full bg-slate-700 rounded px-3 py-2 border border-slate-600 focus:border-green-400 focus:outline-none"
            placeholder="0.0"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Region
          </label>
          <select
            value={filters.regions}
            onChange={(e) => onFilterChange('regions', e.target.value)}
            className="w-full bg-slate-700 rounded px-3 py-2 border border-slate-600 focus:border-green-400 focus:outline-none"
          >
            <option value="us">US (Primary Books)</option>
            <option value="us2">US (Regional Books)</option>
            <option value="us,us2">US (All Books) ⭐</option>
            <option value="uk">United Kingdom</option>
            <option value="eu">Europe</option>
            <option value="au">Australia</option>
            <option value="us,us2,uk">US + UK (Best)</option>
            <option value="us,us2,uk,eu,au">All Regions (Max Coverage)</option>
          </select>
        </div>
      </div>

      <div className="mt-4 flex flex-col gap-2">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={filters.autoRefresh}
            onChange={(e) => onFilterChange('autoRefresh', e.target.checked)}
            className="w-4 h-4 rounded border-slate-600 bg-slate-700 text-green-600 focus:ring-green-500"
          />
          <span className="text-sm text-slate-300">Auto-refresh every 60 seconds</span>
        </label>
        
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={!filters.includeLive}
            onChange={(e) => onFilterChange('includeLive', !e.target.checked)}
            className="w-4 h-4 rounded border-slate-600 bg-slate-700 text-green-600 focus:ring-green-500"
          />
          <span className="text-sm text-slate-300">
            Show only upcoming games (exclude live/started games)
            <span className="ml-2 text-xs text-green-400">✅ Recommended</span>
          </span>
        </label>

        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={filters.includePlayerProps || false}
            onChange={(e) => onFilterChange('includePlayerProps', e.target.checked)}
            className="w-4 h-4 rounded border-slate-600 bg-slate-700 text-green-600 focus:ring-green-500"
          />
          <span className="text-sm text-slate-300">
            Include Player Props (Points, Assists, Rebounds, etc.)
            <span className="ml-2 text-xs text-blue-400">🏀 New</span>
          </span>
        </label>
      </div>
    </div>
  );
};

export default FilterPanel;

