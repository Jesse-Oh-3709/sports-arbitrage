# ⏰ The Odds API Time Range

## Summary

The Odds API provides odds for games **typically 7-14 days** into the future, depending on the sport and season.

---

## 📊 Current Coverage (Oct 10, 2025)

### NFL (americanfootball_nfl)
- **Games Available**: 29 games
- **Time Range**: 2-11 days ahead
- **Earliest Game**: Oct 12 (2 days)
- **Latest Game**: Oct 21 (11 days)
- **Typical Range**: ~10-14 days

---

## 🎯 General Time Limits

### Typical Coverage by Sport:

**Major US Sports (NFL, NBA, MLB, NHL):**
- **7-14 days** ahead
- Updated as games get closer
- More sportsbooks list odds closer to game time

**Soccer/Football:**
- **7-10 days** for regular leagues
- **2-4 weeks** for major tournaments
- Depends on league and competition

**Other Sports:**
- Varies by sport popularity
- Major events: 2-4 weeks
- Regular season: 7-10 days

---

## 📅 How It Works

### Dynamic Updates:
The Odds API continuously updates its window:

**Example Timeline:**
```
Today (Oct 10):
  Shows games: Oct 12 - Oct 21 (2-11 days)

Tomorrow (Oct 11):
  Shows games: Oct 13 - Oct 22 (2-11 days)

Next Week (Oct 17):
  Shows games: Oct 19 - Oct 28 (2-11 days)
```

**The window "rolls forward"** each day.

---

## 🔄 When Odds Appear

### NFL Example:
```
Tuesday:    Next Sunday's games appear (5-6 days ahead)
Wednesday:  Some Monday games may appear
Thursday:   Weekend games fully populated
Friday:     All Sunday games have odds
Saturday:   Sunday games well-covered
Sunday:     Following week starts appearing
```

### General Pattern:
- **Opening lines**: 7-10 days before game
- **Most books**: 3-5 days before
- **All books**: 1-2 days before
- **Best arb opportunities**: 12-48 hours before

---

## ⚠️ Limitations

### What You WON'T See:

**❌ Games too far in future:**
- NFL Week 15 odds won't show in Week 1
- Championship games months away
- Next season games

**❌ Off-season sports:**
- NBA in summer (no games)
- MLB in winter (no games)
- NFL in spring/summer (no games)

**✅ What You WILL See:**
- Current week games
- Next week games
- Sometimes 2 weeks ahead
- Depends on sport and season

---

## 📈 Coverage Improves Over Time

### 11 Days Out:
```
Games: 5-10 available
Sportsbooks per game: 2-5
Odds quality: Opening lines, may move
```

### 3 Days Out:
```
Games: 20-30 available
Sportsbooks per game: 10-15
Odds quality: Well-established
```

### 24 Hours Out:
```
Games: All weekend games listed
Sportsbooks per game: 15-25
Odds quality: Best for arbitrage
```

### Game Time:
```
Games: Locked (can't bet)
Sportsbooks: Remove from API
Live betting: Different API/markets
```

---

## 🎯 Best Time to Find Arbitrage

### Early (7-10 days out):
- ✅ Opening line inefficiencies
- ❌ Fewer sportsbooks
- ❌ Lines may move significantly

### Mid (3-5 days out):
- ✅ More sportsbooks active
- ✅ Lines more stable
- ✅ Good arbitrage opportunities

### Late (12-48 hours out):
- ✅ Maximum sportsbooks
- ✅ Most arbitrage opportunities
- ✅ Best for execution
- ⚠️ Odds change quickly

### Very Late (< 2 hours):
- ⚠️ High execution risk
- ⚠️ Odds very volatile
- ⚠️ May lock before you finish betting

---

## 🔍 Sport-Specific Ranges

### NFL:
- **10-14 days** - Full week ahead
- Thursday games: Listed previous Sunday
- Sunday games: Listed Tuesday/Wednesday
- Monday games: Listed mid-week

### NBA (In Season):
- **5-7 days** - Week ahead
- Back-to-backs: May be shorter
- Weekend games: Wednesday/Thursday

### MLB (In Season):
- **3-5 days** - Shorter window
- Pitching matchups matter
- Day games: Listed night before

### Soccer (EPL, La Liga):
- **7-10 days** - Weekend matches
- Midweek games: 5-7 days
- Cup matches: Varies

---

## 💡 Practical Implications

### For Your Dashboard:

**Daily Use:**
```
Morning: Check for new games appearing
Afternoon: Monitor line movements
Evening: Execute arbitrages for tomorrow
```

**Weekly Pattern:**
```
Monday: New games for next weekend appear
Wednesday: More sportsbooks list odds
Friday: Maximum coverage for weekend
Sunday: Next week's games start appearing
```

### Arbitrage Strategy:
```
1. Monitor 7-10 days out: Spot early opportunities
2. Target 2-3 days out: Best risk/reward
3. Execute 12-48h out: Maximum book coverage
4. Avoid < 2h out: Too risky, odds lock
```

---

## 🔢 API Request Planning

With your **500 requests/month** free tier:

### Smart Usage:
```
Check daily: ~2 requests/day = 60/month
Check twice daily: ~4 requests/day = 120/month
Auto-refresh hourly: 24*30 = 720/month ❌ TOO MANY
```

### Recommendation:
- Check **2-3 times per day**
- Focus on **2-3 days before games**
- **Disable auto-refresh** or set to manual
- Use **upload feature** for testing (no API cost)

---

## 📊 What You're Seeing Now

Based on the current data (Oct 10):

```
✅ Available: Games through Oct 21 (11 days)
✅ Total: 29 NFL games
✅ Coverage: Full week + partial next week
✅ Update: Rolling window moves forward daily
```

**In your dashboard:**
- Games showing: This weekend (Oct 12-13) + next weekend (Oct 19-21)
- Not showing: Games beyond Oct 21
- Updates: Each day, new games appear at the far end

---

## 🚀 Recommendations

### For Arbitrage Hunting:

**Best Times to Check:**
1. **Wednesday morning** - New weekend games appear
2. **Friday afternoon** - Maximum book coverage
3. **Saturday evening** - Late line movements

**Best Windows:**
- **Thursday-Saturday** for Sunday NFL games
- **Monday-Wednesday** for next weekend planning
- **2-3 days out** for most sports

---

## ⚠️ API Limits

### Free Tier:
- **500 requests/month**
- Each call with `regions=us,us2` counts as **2 requests**
- Plan accordingly!

### Your Current Usage:
- **API requests remaining**: 454 / 500
- **Used so far**: 46 requests
- **Pace**: Good for the month

---

## ✅ Bottom Line

**Time Range**: **7-14 days** into the future (varies by sport)

**NFL Current**: **11 days** of games available

**Best Practice**: Check **2-3 times per day**, focus on games **2-3 days out**

**Your Dashboard**: Already configured to show this rolling window automatically! 🎯

---

**The time range is perfect for finding and executing arbitrage opportunities before game time!**
