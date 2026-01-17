import React from 'react';
import { Download, FileSpreadsheet } from 'lucide-react';

const ExportButton = ({ arbitrages, loading }) => {
  const exportToCSV = () => {
    if (!arbitrages || arbitrages.length === 0) {
      alert('No arbitrage data to export');
      return;
    }

    // Create CSV header
    const headers = [
      'Match',
      'Sport',
      'Market',
      'Game Time',
      'Sportsbook A',
      'Outcome A',
      'Odds A (American)',
      'Odds A (Decimal)',
      'Sportsbook B',
      'Outcome B',
      'Odds B (American)',
      'Odds B (Decimal)',
      'Profit %',
      'Implied Probability',
      'Stake A ($1000)',
      'Stake B ($1000)',
      'Guaranteed Profit',
      'Confidence',
      'Warning Message'
    ];

    // Convert American odds helper
    const toAmerican = (decimal) => {
      if (decimal >= 2.0) {
        return `+${Math.round((decimal - 1) * 100)}`;
      } else {
        return `${Math.round(-100 / (decimal - 1))}`;
      }
    };

    // Format game time helper
    const formatTime = (isoTime) => {
      if (!isoTime) return '';
      try {
        const date = new Date(isoTime);
        return date.toLocaleString('en-US', {
          month: 'short',
          day: 'numeric',
          hour: 'numeric',
          minute: '2-digit',
          hour12: true
        });
      } catch {
        return isoTime;
      }
    };

    // Create CSV rows
    const rows = arbitrages.map(arb => [
      arb.match || '',
      arb.sport || '',
      arb.market || '',
      formatTime(arb.commence_time),
      arb.sportsbook_a || '',
      arb.outcome_a || '',
      toAmerican(arb.odds_a),
      arb.odds_a?.toFixed(2) || '',
      arb.sportsbook_b || '',
      arb.outcome_b || '',
      toAmerican(arb.odds_b),
      arb.odds_b?.toFixed(2) || '',
      arb.profit_percentage?.toFixed(2) + '%' || '',
      (arb.implied_probability * 100)?.toFixed(2) + '%' || '',
      arb.stake_a || '',
      arb.stake_b || '',
      arb.guaranteed_profit || '',
      arb.warning?.level || '',
      arb.warning?.message || ''
    ]);

    // Combine header and rows
    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => {
        // Escape cells that contain commas
        const cellStr = String(cell);
        if (cellStr.includes(',')) {
          return `"${cellStr}"`;
        }
        return cellStr;
      }).join(','))
    ].join('\n');

    // Create blob and download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `arbitrage_opportunities_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const exportToGoogleSheets = () => {
    if (!arbitrages || arbitrages.length === 0) {
      alert('No arbitrage data to export');
      return;
    }

    alert(
      'To use with Google Sheets:\n\n' +
      '1. Click "Export to CSV" button\n' +
      '2. Open Google Sheets (sheets.google.com)\n' +
      '3. Create new spreadsheet\n' +
      '4. Go to File → Import → Upload\n' +
      '5. Select the downloaded CSV file\n' +
      '6. Choose "Replace current sheet"\n\n' +
      'Or use our Google Apps Script for live updates!\n' +
      '(See GOOGLE_SHEETS_INTEGRATION.md)'
    );
  };

  return (
    <div className="flex gap-2">
      <button
        onClick={exportToCSV}
        disabled={loading || !arbitrages || arbitrages.length === 0}
        className={`flex items-center gap-2 px-4 py-2 rounded font-semibold transition ${
          loading || !arbitrages || arbitrages.length === 0
            ? 'bg-slate-600 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700'
        }`}
        title="Export arbitrage data to CSV file (works with Google Sheets)"
      >
        <Download size={18} />
        Export to CSV
      </button>

      <button
        onClick={exportToGoogleSheets}
        disabled={loading || !arbitrages || arbitrages.length === 0}
        className={`flex items-center gap-2 px-3 py-2 rounded font-semibold transition ${
          loading || !arbitrages || arbitrages.length === 0
            ? 'bg-slate-600 cursor-not-allowed'
            : 'bg-green-600 hover:bg-green-700'
        }`}
        title="Instructions for Google Sheets import"
      >
        <FileSpreadsheet size={18} />
        Google Sheets
      </button>
    </div>
  );
};

export default ExportButton;

