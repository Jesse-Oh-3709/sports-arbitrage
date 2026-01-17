import React, { useState, useEffect, useCallback } from 'react';
import { TrendingUp, AlertCircle, Plus, Trash2, Search, Upload as UploadIcon } from 'lucide-react';
import ArbitrageTable from './components/ArbitrageTable';
import PlayerPropsTable from './components/PlayerPropsTable';
import FilterPanel from './components/FilterPanel';
import UploadOdds from './components/UploadOdds';
import ExportButton from './components/ExportButton';
import { decimalToAmerican } from './utils/oddsConverter';

const SportsArbitrageApp = () => {
  // State for API-fetched arbitrages
  const [liveArbitrages, setLiveArbitrages] = useState([]);
  const [loadingLive, setLoadingLive] = useState(false);
  const [errorLive, setErrorLive] = useState(null);
  const [playerPropsNote, setPlayerPropsNote] = useState(null);
  const [apiKeyConfigured, setApiKeyConfigured] = useState(false);
  const [apiRequestsRemaining, setApiRequestsRemaining] = useState(null);

  // State for manually entered games
  const [manualGames, setManualGames] = useState([
    {
      id: 1,
      sport: 'NBA',
      team1: 'Lakers',
      team2: 'Celtics',
      date: '2025-10-15',
      sportsbooks: [
        { name: 'DraftKings', odds1: 2.10, odds2: 1.80 },
        { name: 'FanDuel', odds1: 1.95, odds2: 1.95 },
        { name: 'BetMGM', odds1: 2.05, odds2: 1.85 }
      ]
    },
    {
      id: 2,
      sport: 'NFL',
      team1: 'Chiefs',
      team2: '49ers',
      date: '2025-10-12',
      sportsbooks: [
        { name: 'DraftKings', odds1: 1.75, odds2: 2.20 },
        { name: 'FanDuel', odds1: 1.80, odds2: 2.10 },
        { name: 'Caesars', odds1: 1.72, odds2: 2.25 }
      ]
    }
  ]);

  const [newGame, setNewGame] = useState({
    sport: '',
    team1: '',
    team2: '',
    date: '',
    sportsbooks: []
  });

  const [newOdds, setNewOdds] = useState({
    sportsbook: '',
    odds1: '',
    odds2: ''
  });

  // Filter state
  const [filters, setFilters] = useState({
    sport: 'upcoming',
    markets: 'h2h',
    minProfit: 0,
    regions: 'us,us2',  // Use both US regions by default
    autoRefresh: false,
    includeLive: false,  // Exclude live/started games by default
    includePlayerProps: false  // Include player prop markets
  });

  // View mode
  const [viewMode, setViewMode] = useState('live'); // 'live', 'manual', 'upload'
  
  // Market type view (game odds vs player props)
  const [marketTypeView, setMarketTypeView] = useState('game'); // 'game', 'player_props', 'all'

  // Check API health on mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      const data = await response.json();
      setApiKeyConfigured(data.api_key_configured);
    } catch (err) {
      console.error('Failed to check API health:', err);
    }
  };

  // Fetch live arbitrages
  const fetchLiveArbitrages = useCallback(async () => {
    setLoadingLive(true);
    setErrorLive(null);
    setPlayerPropsNote(null);

    try {
      const params = new URLSearchParams({
        sport: filters.sport,
        markets: filters.markets,
        regions: filters.regions,
        min_profit: filters.minProfit,
        include_live: filters.includeLive,
        include_player_props: filters.includePlayerProps || false
      });

      const response = await fetch(`http://localhost:8000/arbitrage/live?${params}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch arbitrages');
      }

      const data = await response.json();
      
      if (data.error) {
        setErrorLive(data.error);
        setLiveArbitrages([]);
        setPlayerPropsNote(null);
      } else {
        setLiveArbitrages(data.arbitrages || []);
        setApiRequestsRemaining(data.api_requests_remaining);
        
        // Show warning if player props were requested but not available
        if (data.player_props_note && filters.includePlayerProps) {
          setPlayerPropsNote(data.player_props_note);
        }
      }
    } catch (err) {
      setErrorLive(err.message || 'Failed to fetch live arbitrages');
      setLiveArbitrages([]);
      setPlayerPropsNote(null);
    } finally {
      setLoadingLive(false);
    }
  }, [filters]);

  // Auto-refresh effect
  useEffect(() => {
    if (filters.autoRefresh && apiKeyConfigured && viewMode === 'live') {
      const interval = setInterval(() => {
        fetchLiveArbitrages();
      }, 60000); // 60 seconds

      return () => clearInterval(interval);
    }
  }, [filters.autoRefresh, apiKeyConfigured, viewMode, fetchLiveArbitrages]);

  // Reset market type view when player props are disabled
  useEffect(() => {
    if (!filters.includePlayerProps && marketTypeView !== 'game') {
      setMarketTypeView('game');
    }
  }, [filters.includePlayerProps, marketTypeView]);

  // Manual game arbitrage calculation
  const calculateArbitrage = (odds1, odds2) => {
    const impliedProb = (1 / odds1) + (1 / odds2);
    const arbExists = impliedProb < 1;
    const profit = arbExists ? ((1 / impliedProb - 1) * 100).toFixed(2) : 0;
    return { arbExists, profit, impliedProb };
  };

  const findBestArbitrage = (game) => {
    let bestArb = { exists: false, profit: 0 };
    let bestCombination = null;

    for (let i = 0; i < game.sportsbooks.length; i++) {
      for (let j = 0; j < game.sportsbooks.length; j++) {
        const arb = calculateArbitrage(
          game.sportsbooks[i].odds1,
          game.sportsbooks[j].odds2
        );
        if (arb.arbExists && parseFloat(arb.profit) > parseFloat(bestArb.profit)) {
          bestArb = { exists: true, profit: arb.profit };
          bestCombination = {
            book1: game.sportsbooks[i].name,
            odds1: game.sportsbooks[i].odds1,
            team1: game.team1,
            book2: game.sportsbooks[j].name,
            odds2: game.sportsbooks[j].odds2,
            team2: game.team2
          };
        }
      }
    }

    return { bestArb, bestCombination };
  };

  const calculateStakes = (odds1, odds2, totalStake) => {
    const stake1 = (totalStake / (1 + (odds1 / odds2))).toFixed(2);
    const stake2 = (totalStake - stake1).toFixed(2);
    return { stake1, stake2 };
  };

  const addOddsToNewGame = () => {
    if (newOdds.sportsbook && newOdds.odds1 && newOdds.odds2) {
      setNewGame({
        ...newGame,
        sportsbooks: [...newGame.sportsbooks, {
          name: newOdds.sportsbook,
          odds1: parseFloat(newOdds.odds1),
          odds2: parseFloat(newOdds.odds2)
        }]
      });
      setNewOdds({ sportsbook: '', odds1: '', odds2: '' });
    }
  };

  const addGame = () => {
    if (newGame.sport && newGame.team1 && newGame.team2 && newGame.sportsbooks.length >= 2) {
      setManualGames([...manualGames, { ...newGame, id: Date.now() }]);
      setNewGame({ sport: '', team1: '', team2: '', date: '', sportsbooks: [] });
    }
  };

  const removeGame = (id) => {
    setManualGames(manualGames.filter(g => g.id !== id));
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleUploadSuccess = (data) => {
    // Set the arbitrages (even if empty, to show "no opportunities" message)
    setLiveArbitrages(data.arbitrages || []);
    
    // Switch to live view to show results
    setViewMode('live');
    
    // Clear any previous errors
    setErrorLive(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
            <TrendingUp className="text-green-400" size={36} />
            Sports Arbitrage Finder
          </h1>
          <p className="text-slate-400">Find guaranteed profit opportunities across sportsbooks</p>
        </div>

        {/* View Mode Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setViewMode('live')}
            className={`px-6 py-3 rounded-lg font-semibold transition ${
              viewMode === 'live'
                ? 'bg-green-600 text-white'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Live Odds (API)
          </button>
          <button
            onClick={() => setViewMode('manual')}
            className={`px-6 py-3 rounded-lg font-semibold transition ${
              viewMode === 'manual'
                ? 'bg-green-600 text-white'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Manual Entry
          </button>
          <button
            onClick={() => setViewMode('upload')}
            className={`px-6 py-3 rounded-lg font-semibold transition ${
              viewMode === 'upload'
                ? 'bg-green-600 text-white'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Upload Data
          </button>
        </div>

        {/* Live Odds View */}
        {viewMode === 'live' && (
          <>
            <FilterPanel
              filters={filters}
              onFilterChange={handleFilterChange}
              onRefresh={fetchLiveArbitrages}
              isRefreshing={loadingLive}
              apiKeyConfigured={apiKeyConfigured}
            />

            {playerPropsNote && (
              <div className="mt-4 mb-6 bg-blue-900/30 border border-blue-500/40 rounded-lg p-4 text-sm text-blue-200">
                {playerPropsNote}
              </div>
            )}

            {apiRequestsRemaining && (
              <div className="mt-4 mb-6 text-sm text-slate-400 text-center">
                API Requests Remaining: {apiRequestsRemaining}
              </div>
            )}

            <div className="mt-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold">
                  {liveArbitrages.length > 0 
                    ? `Found ${liveArbitrages.length} Arbitrage Opportunit${liveArbitrages.length === 1 ? 'y' : 'ies'}`
                    : 'Arbitrage Opportunities'
                  }
                </h2>
                
                <div className="flex items-center gap-3">
                  {/* Market Type Toggle */}
                  {filters.includePlayerProps && (
                    <div className="flex items-center gap-2 bg-slate-800 rounded-lg p-1 border border-slate-700">
                      <button
                        onClick={() => setMarketTypeView('game')}
                        className={`px-4 py-2 rounded text-sm font-semibold transition ${
                          marketTypeView === 'game' || marketTypeView === 'all'
                            ? 'bg-green-600 text-white'
                            : 'text-slate-300 hover:text-white'
                        }`}
                      >
                        Game Odds
                      </button>
                      <button
                        onClick={() => setMarketTypeView('player_props')}
                        className={`px-4 py-2 rounded text-sm font-semibold transition ${
                          marketTypeView === 'player_props' || marketTypeView === 'all'
                            ? 'bg-blue-600 text-white'
                            : 'text-slate-300 hover:text-white'
                        }`}
                      >
                        Player Props
                      </button>
                      <button
                        onClick={() => setMarketTypeView('all')}
                        className={`px-4 py-2 rounded text-sm font-semibold transition ${
                          marketTypeView === 'all'
                            ? 'bg-purple-600 text-white'
                            : 'text-slate-300 hover:text-white'
                        }`}
                      >
                        All
                      </button>
                    </div>
                  )}
                  
                  <ExportButton 
                    arbitrages={liveArbitrages} 
                    loading={loadingLive}
                  />
                </div>
              </div>
              
              {/* Filter and display arbitrages based on market type view */}
              {(() => {
                const gameArbitrages = liveArbitrages.filter(arb => 
                  !arb.market_type || arb.market_type === 'game'
                );
                const playerPropArbitrages = liveArbitrages.filter(arb => 
                  arb.market_type === 'player_prop'
                );
                
                if (marketTypeView === 'game' || (!filters.includePlayerProps && marketTypeView === 'game')) {
                  return (
                    <ArbitrageTable
                      arbitrages={gameArbitrages}
                      loading={loadingLive}
                      error={errorLive}
                    />
                  );
                } else if (marketTypeView === 'player_props') {
                  return (
                    <PlayerPropsTable
                      playerProps={playerPropArbitrages}
                      loading={loadingLive}
                      error={errorLive}
                    />
                  );
                } else {
                  // Show both
                  return (
                    <div className="space-y-8">
                      {gameArbitrages.length > 0 && (
                        <div>
                          <h3 className="text-xl font-bold mb-4 text-green-400">
                            Game Market Arbitrages ({gameArbitrages.length})
                          </h3>
                          <ArbitrageTable
                            arbitrages={gameArbitrages}
                            loading={false}
                            error={null}
                          />
                        </div>
                      )}
                      
                      {playerPropArbitrages.length > 0 && (
                        <div>
                          <h3 className="text-xl font-bold mb-4 text-blue-400">
                            Player Prop Arbitrages ({playerPropArbitrages.length})
                          </h3>
                          <PlayerPropsTable
                            playerProps={playerPropArbitrages}
                            loading={false}
                            error={null}
                          />
                        </div>
                      )}
                      
                      {gameArbitrages.length === 0 && playerPropArbitrages.length === 0 && (
                        <div className="text-center py-12 text-slate-400">
                          <AlertCircle size={48} className="mx-auto mb-4 opacity-50" />
                          <p className="text-lg">No arbitrage opportunities found</p>
                          <p className="text-sm mt-2">Try adjusting your filters or check back later</p>
                        </div>
                      )}
                    </div>
                  );
                }
              })()}
            </div>
          </>
        )}

        {/* Upload View */}
        {viewMode === 'upload' && (
          <div className="mt-6">
            <UploadOdds onUploadSuccess={handleUploadSuccess} />
          </div>
        )}

        {/* Manual Entry View */}
        {viewMode === 'manual' && (
          <>
            {/* Add New Game */}
            <div className="bg-slate-800 rounded-lg p-6 mb-6 border border-slate-700">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Plus size={20} />
                Add New Game
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                <input
                  type="text"
                  placeholder="Sport (e.g., NBA)"
                  value={newGame.sport}
                  onChange={(e) => setNewGame({...newGame, sport: e.target.value})}
                  className="bg-slate-700 rounded px-4 py-2 border border-slate-600 focus:border-green-400 focus:outline-none"
                />
                <input
                  type="text"
                  placeholder="Team 1"
                  value={newGame.team1}
                  onChange={(e) => setNewGame({...newGame, team1: e.target.value})}
                  className="bg-slate-700 rounded px-4 py-2 border border-slate-600 focus:border-green-400 focus:outline-none"
                />
                <input
                  type="text"
                  placeholder="Team 2"
                  value={newGame.team2}
                  onChange={(e) => setNewGame({...newGame, team2: e.target.value})}
                  className="bg-slate-700 rounded px-4 py-2 border border-slate-600 focus:border-green-400 focus:outline-none"
                />
                <input
                  type="date"
                  value={newGame.date}
                  onChange={(e) => setNewGame({...newGame, date: e.target.value})}
                  className="bg-slate-700 rounded px-4 py-2 border border-slate-600 focus:border-green-400 focus:outline-none"
                />
              </div>

              <div className="bg-slate-700 rounded p-4 mb-4">
                <h3 className="font-semibold mb-3">Add Sportsbook Odds</h3>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-3 mb-3">
                  <input
                    type="text"
                    placeholder="Sportsbook"
                    value={newOdds.sportsbook}
                    onChange={(e) => setNewOdds({...newOdds, sportsbook: e.target.value})}
                    className="bg-slate-600 rounded px-3 py-2 border border-slate-500 focus:border-green-400 focus:outline-none"
                  />
                  <input
                    type="number"
                    step="0.01"
                    placeholder="Team 1 Odds"
                    value={newOdds.odds1}
                    onChange={(e) => setNewOdds({...newOdds, odds1: e.target.value})}
                    className="bg-slate-600 rounded px-3 py-2 border border-slate-500 focus:border-green-400 focus:outline-none"
                  />
                  <input
                    type="number"
                    step="0.01"
                    placeholder="Team 2 Odds"
                    value={newOdds.odds2}
                    onChange={(e) => setNewOdds({...newOdds, odds2: e.target.value})}
                    className="bg-slate-600 rounded px-3 py-2 border border-slate-500 focus:border-green-400 focus:outline-none"
                  />
                  <button
                    onClick={addOddsToNewGame}
                    className="bg-green-600 hover:bg-green-700 rounded px-4 py-2 font-semibold transition"
                  >
                    Add Odds
                  </button>
                </div>
                {newGame.sportsbooks.length > 0 && (
                  <div className="text-sm">
                    <p className="text-slate-300 mb-2">Added odds:</p>
                    {newGame.sportsbooks.map((sb, idx) => (
                      <div key={idx} className="text-slate-400">
                        {sb.name}: {sb.odds1} / {sb.odds2}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <button
                onClick={addGame}
                disabled={!newGame.sport || !newGame.team1 || !newGame.team2 || newGame.sportsbooks.length < 2}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed rounded px-6 py-2 font-semibold transition w-full md:w-auto"
              >
                Add Game to List
              </button>
            </div>

            {/* Manual Games List */}
            <div className="space-y-6">
              {manualGames.map(game => {
                const { bestArb, bestCombination } = findBestArbitrage(game);
                const stakes = bestCombination ? calculateStakes(
                  bestCombination.odds1,
                  bestCombination.odds2,
                  1000
                ) : null;

                return (
                  <div key={game.id} className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
                    <div className="bg-slate-750 px-6 py-4 border-b border-slate-700 flex justify-between items-center">
                      <div>
                        <div className="flex items-center gap-3">
                          <span className="bg-blue-600 px-3 py-1 rounded text-sm font-semibold">{game.sport}</span>
                          <h3 className="text-xl font-bold">{game.team1} vs {game.team2}</h3>
                        </div>
                        <p className="text-slate-400 text-sm mt-1">{game.date}</p>
                      </div>
                      <button
                        onClick={() => removeGame(game.id)}
                        className="text-red-400 hover:text-red-300 transition"
                      >
                        <Trash2 size={20} />
                      </button>
                    </div>

                    {bestArb.exists ? (
                      <div className="bg-gradient-to-r from-green-900/40 to-emerald-900/40 border-l-4 border-green-400 p-6">
                        <div className="flex items-start gap-3 mb-4">
                          <AlertCircle className="text-green-400 mt-1" size={24} />
                          <div className="flex-1">
                            <h4 className="text-xl font-bold text-green-400 mb-2">
                              Arbitrage Opportunity Found! {bestArb.profit}% Profit
                            </h4>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                              <div className="bg-slate-800/50 rounded p-4">
                                <p className="text-slate-300 text-sm mb-1">Bet on {bestCombination.team1}</p>
                                <p className="text-2xl font-bold">{bestCombination.book1}</p>
                                <p className="text-green-400 text-xl">
                                  {decimalToAmerican(bestCombination.odds1)} <span className="text-sm text-slate-400">({bestCombination.odds1})</span>
                                </p>
                              </div>
                              <div className="bg-slate-800/50 rounded p-4">
                                <p className="text-slate-300 text-sm mb-1">Bet on {bestCombination.team2}</p>
                                <p className="text-2xl font-bold">{bestCombination.book2}</p>
                                <p className="text-green-400 text-xl">
                                  {decimalToAmerican(bestCombination.odds2)} <span className="text-sm text-slate-400">({bestCombination.odds2})</span>
                                </p>
                              </div>
                            </div>
                            {stakes && (
                              <div className="bg-slate-800/70 rounded p-4">
                                <p className="font-semibold mb-2">Recommended Stakes (for $1000 total):</p>
                                <div className="grid grid-cols-2 gap-4">
                                  <div>
                                    <p className="text-slate-400 text-sm">Stake on {bestCombination.team1}</p>
                                    <p className="text-xl font-bold text-green-400">${stakes.stake1}</p>
                                  </div>
                                  <div>
                                    <p className="text-slate-400 text-sm">Stake on {bestCombination.team2}</p>
                                    <p className="text-xl font-bold text-green-400">${stakes.stake2}</p>
                                  </div>
                                </div>
                                <p className="text-green-400 mt-3 font-semibold">
                                  Guaranteed Profit: ${(1000 * (bestArb.profit / 100)).toFixed(2)}
                                </p>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    ) : (
                      <div className="p-6 bg-slate-900/30">
                        <p className="text-slate-400 flex items-center gap-2">
                          <AlertCircle size={18} />
                          No arbitrage opportunity found for this game
                        </p>
                      </div>
                    )}

                <div className="p-6">
                  <h4 className="font-semibold mb-3 text-slate-300">All Odds:</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-slate-700">
                          <th className="text-left py-2 px-3 text-slate-400">Sportsbook</th>
                          <th className="text-center py-2 px-3 text-slate-400">{game.team1}</th>
                          <th className="text-center py-2 px-3 text-slate-400">{game.team2}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {game.sportsbooks.map((book, idx) => (
                          <tr key={idx} className="border-b border-slate-700/50">
                            <td className="py-2 px-3 font-semibold">{book.name}</td>
                            <td className="py-2 px-3 text-center">
                              <span className="font-bold text-green-400">{decimalToAmerican(book.odds1)}</span>
                              <span className="text-xs text-slate-500 ml-2">({book.odds1})</span>
                            </td>
                            <td className="py-2 px-3 text-center">
                              <span className="font-bold text-green-400">{decimalToAmerican(book.odds2)}</span>
                              <span className="text-xs text-slate-500 ml-2">({book.odds2})</span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
                  </div>
                );
              })}
            </div>

            {manualGames.length === 0 && (
              <div className="text-center py-12 text-slate-400">
                <Search size={48} className="mx-auto mb-4 opacity-50" />
                <p>No games added yet. Add a game above to start finding arbitrage opportunities.</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default SportsArbitrageApp;

