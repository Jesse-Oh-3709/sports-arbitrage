/**
 * Convert decimal odds to American odds format
 * @param {number} decimalOdds - Decimal odds (e.g., 1.91, 2.50)
 * @returns {string} - American odds with + or - prefix (e.g., "-110", "+150")
 */
export function decimalToAmerican(decimalOdds) {
  if (!decimalOdds || decimalOdds < 1) return 'N/A';
  
  let americanOdds;
  
  if (decimalOdds >= 2.0) {
    // Favorite: decimal >= 2.0 → positive American odds
    americanOdds = Math.round((decimalOdds - 1) * 100);
    return `+${americanOdds}`;
  } else {
    // Underdog: decimal < 2.0 → negative American odds
    americanOdds = Math.round(-100 / (decimalOdds - 1));
    return `${americanOdds}`;
  }
}

/**
 * Format odds for display with both formats
 * @param {number} decimalOdds - Decimal odds
 * @returns {object} - Object with both formats
 */
export function formatOdds(decimalOdds) {
  return {
    american: decimalToAmerican(decimalOdds),
    decimal: decimalOdds.toFixed(2)
  };
}

/**
 * Format game commence time to user-friendly format
 * @param {string} isoTime - ISO format time string (e.g., "2025-10-12T13:30:00Z")
 * @returns {string} - Formatted date/time string
 */
export function formatGameTime(isoTime) {
  if (!isoTime) return '';
  
  try {
    const gameDate = new Date(isoTime);
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const isToday = gameDate.toDateString() === now.toDateString();
    const isTomorrow = gameDate.toDateString() === tomorrow.toDateString();
    
    // Format time
    const timeOptions = { hour: 'numeric', minute: '2-digit', hour12: true };
    const timeString = gameDate.toLocaleTimeString('en-US', timeOptions);
    
    if (isToday) {
      return `Today ${timeString}`;
    } else if (isTomorrow) {
      return `Tomorrow ${timeString}`;
    } else {
      // Format as "Oct 12, 2:30 PM" or "Sun 2:30 PM" if within a week
      const daysUntil = Math.floor((gameDate - now) / (1000 * 60 * 60 * 24));
      
      if (daysUntil <= 7) {
        const dayName = gameDate.toLocaleDateString('en-US', { weekday: 'short' });
        return `${dayName} ${timeString}`;
      } else {
        const dateString = gameDate.toLocaleDateString('en-US', { 
          month: 'short', 
          day: 'numeric' 
        });
        return `${dateString} ${timeString}`;
      }
    }
  } catch (error) {
    return isoTime;
  }
}

