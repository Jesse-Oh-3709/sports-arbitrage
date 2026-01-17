# ✅ Sportsbooks Update - Offshore & Specialty Books Removed

## What Changed

Your arbitrage detector now uses **only regulated US sportsbooks** - offshore and specialty books have been excluded.

---

## 🚫 REMOVED (7 Books)

### Offshore Books (4):
- ❌ **BetOnline.ag** - Offshore
- ❌ **Bovada** - Offshore
- ❌ **BetUS** - Offshore
- ❌ **MyBookie.ag** - Offshore

### Specialty/Social Books (3):
- ❌ **LowVig.ag** - Reduced vig specialty
- ❌ **Fliff** - Social/sweepstakes betting
- ❌ **BetAnything** - Smaller operator

---

## ✅ NOW USING (7 Books)

### Major National Books (3):
1. **DraftKings** ⭐
2. **FanDuel** ⭐
3. **ESPN BET** ⭐

### Regional US Books (4):
4. **BetRivers**
5. **Hard Rock Bet**
6. **betPARX**
7. **Bally Bet**

---

## 📊 Before vs After

| Metric | Before | After |
|--------|--------|-------|
| **Total Books** | 14 | **7** ✅ |
| **Offshore Books** | 4 | **0** ✅ |
| **Specialty Books** | 3 | **0** ✅ |
| **Regulated US Books** | 7 | **7** ✅ |

---

## 🎯 Why This Change?

### ✅ Benefits of Regulated Books Only:

**1. Legal Clarity**
- All 7 books are state-licensed in the US
- Operating under state gaming regulations
- Clear legal recourse if issues arise

**2. Better Account Longevity**
- Regulated books less likely to close accounts suddenly
- More transparent terms of service
- Better customer support

**3. Easier Deposits/Withdrawals**
- Direct bank transfers (no crypto required)
- Faster withdrawal processing
- FDIC protection in some cases

**4. Tax Reporting**
- Automatic W-2G forms for wins > $600
- Easier to stay compliant with IRS
- No offshore reporting complications

**5. Safer Funds**
- State-mandated segregated accounts
- Gaming commission oversight
- Better fraud protection

---

## 🏆 Book Details

### **DraftKings** (National)
- **States**: 25+ states
- **Reputation**: Industry leader
- **Limits**: High initially, may reduce for arb bettors
- **Best For**: Major markets (NFL, NBA, MLB)

### **FanDuel** (National)
- **States**: 25+ states
- **Reputation**: Most popular US book
- **Limits**: High volume, competitive lines
- **Best For**: All major sports

### **ESPN BET** (National - New)
- **States**: 17+ states (expanding)
- **Reputation**: Backed by PENN Entertainment
- **Limits**: Still learning, softer lines
- **Best For**: Finding +EV opportunities (newer)

### **BetRivers** (Regional)
- **States**: 15+ states
- **Reputation**: Rush Street Gaming (solid)
- **Limits**: Moderate, more tolerant
- **Best For**: Regional markets, props

### **Hard Rock Bet** (Regional)
- **States**: Florida, New Jersey, online
- **Reputation**: Hard Rock brand
- **Limits**: Competitive in their markets
- **Best For**: State-specific lines

### **betPARX** (Regional)
- **States**: Pennsylvania, New Jersey, Michigan, Ohio
- **Reputation**: Greenwood Gaming
- **Limits**: Good for regional bettors
- **Best For**: PA/NJ markets

### **Bally Bet** (Regional)
- **States**: Select states
- **Reputation**: Bally's Corporation
- **Limits**: Smaller player, more flexible
- **Best For**: Less efficient markets

---

## 📈 Impact on Arbitrage

### What You'll Notice:

**Fewer Total Opportunities**
- Was: ~14 books = more combinations
- Now: 7 books = fewer combinations
- **BUT: All opportunities are with regulated books**

**Higher Quality Opportunities**
- Only legitimate, regulated sportsbooks
- Easier to execute bets quickly
- Less risk of account issues

**More Sustainable**
- Better long-term relationships with books
- Less likely to get banned immediately
- Can build betting history

---

## 💡 Pro Tips

### **Best Combinations for Arbitrage:**

**1. Major vs Regional**
```
DraftKings (national) vs betPARX (regional)
→ Different customer bases = different lines
```

**2. Established vs New**
```
FanDuel (mature) vs ESPN BET (new)
→ ESPN still learning, softer lines
```

**3. Different States**
```
Hard Rock (FL-focused) vs BetRivers (multi-state)
→ Regional pricing differences
```

---

## 🔍 Testing the Changes

### Check Active Books:
```bash
curl "http://localhost:8000/arbitrage/live?sport=americanfootball_nfl&regions=us,us2&markets=h2h&min_profit=0"
```

You'll now only see these 7 regulated books!

---

## 🚀 What's Next

The system will now:
- ✅ Only fetch odds from these 7 books
- ✅ Only show arbitrage between regulated operators
- ✅ Filter out offshore/specialty books automatically
- ✅ Work with both API and manual/upload modes

---

## 📝 Technical Changes

### File Modified: `backend/app.py`

```python
# Added exclusion list
EXCLUDED_SPORTSBOOKS = {
    # Offshore books
    'BetOnline.ag',
    'Bovada',
    'BetUS',
    'MyBookie.ag',
    # Specialty/social books
    'LowVig.ag',
    'Fliff',
    'BetAnything'
}

# Applied filtering in API endpoint
if bookmaker["title"] in EXCLUDED_SPORTSBOOKS:
    continue
```

---

## ✅ Summary

**You now have a cleaner, safer arbitrage system:**
- ✅ **7 regulated US sportsbooks only**
- ✅ **No offshore operations**
- ✅ **No specialty/social books**
- ✅ **All state-licensed operators**

**Trade-off:**
- Fewer total books = fewer opportunities
- BUT: Higher quality, lower risk opportunities

---

## 🎯 Current Active Books (Refresh to See)

Visit: **http://localhost:3000**

Click "Refresh Odds" and you'll now only see arbitrage opportunities between:
1. DraftKings
2. FanDuel
3. ESPN BET
4. BetRivers
5. Hard Rock Bet
6. betPARX
7. Bally Bet

**All regulated. All legitimate. All safe.** ✅

---

**Backend restarted with new filtering - changes are live!** 🎉

