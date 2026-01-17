# 🔌 API Usage Examples

Complete guide to using the Sports Arbitrage API.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Health Check

Check if the API is running and if the API key is configured.

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-09T12:34:56.789Z",
  "api_key_configured": true
}
```

---

### 2. Get Available Sports

List all sports available from The Odds API.

```bash
curl http://localhost:8000/sports
```

**Response:**
```json
{
  "sports": [
    {
      "key": "americanfootball_nfl",
      "group": "American Football",
      "title": "NFL",
      "description": "US Football"
    },
    {
      "key": "basketball_nba",
      "group": "Basketball",
      "title": "NBA",
      "description": "US Basketball"
    }
  ]
}
```

---

### 3. Find Live Arbitrage Opportunities

Fetch live odds and calculate arbitrage opportunities.

#### Basic Usage

```bash
curl "http://localhost:8000/arbitrage/live?sport=upcoming&markets=h2h&regions=us&min_profit=0"
```

#### NFL Specific

```bash
curl "http://localhost:8000/arbitrage/live?sport=americanfootball_nfl&markets=h2h&regions=us&min_profit=1.0"
```

#### NBA with Spreads

```bash
curl "http://localhost:8000/arbitrage/live?sport=basketball_nba&markets=h2h,spreads&regions=us&min_profit=0.5"
```

#### Soccer with All Markets

```bash
curl "http://localhost:8000/arbitrage/live?sport=soccer_epl&markets=h2h,spreads,totals&regions=uk,eu&min_profit=0"
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sport` | string | No | Sport key (default: "upcoming") |
| `regions` | string | No | Comma-separated regions (default: "us") |
| `markets` | string | No | Comma-separated markets (default: "h2h") |
| `min_profit` | float | No | Minimum profit % (default: 0.0) |

#### Sport Keys

- `upcoming` - All upcoming games
- `americanfootball_nfl` - NFL
- `basketball_nba` - NBA
- `baseball_mlb` - MLB
- `icehockey_nhl` - NHL
- `soccer_epl` - English Premier League
- `soccer_uefa_champs_league` - UEFA Champions League

#### Market Types

- `h2h` - Head-to-head (moneyline)
- `spreads` - Point spreads
- `totals` - Over/Under

#### Regions

- `us` - United States
- `uk` - United Kingdom
- `eu` - Europe
- `au` - Australia

**Response:**
```json
{
  "count": 2,
  "arbitrages": [
    {
      "match": "Eagles vs Giants",
      "sport": "NFL",
      "market": "h2h",
      "sportsbook_a": "DraftKings",
      "odds_a": 2.10,
      "outcome_a": "Eagles",
      "sportsbook_b": "FanDuel",
      "odds_b": 2.05,
      "outcome_b": "Giants",
      "profit_percentage": 3.7,
      "stake_a": 493.97,
      "stake_b": 506.03,
      "guaranteed_profit": 37.00,
      "timestamp": "2025-10-09T12:34:56.789Z"
    }
  ],
  "api_requests_remaining": "495"
}
```

---

### 4. Upload Manual Odds Data

Upload a JSON or CSV file with custom odds data.

#### JSON Upload

```bash
curl -X POST \
  http://localhost:8000/upload \
  -F "file=@data/sample_odds.json"
```

#### CSV Upload

```bash
curl -X POST \
  http://localhost:8000/upload \
  -F "file=@my_odds.csv"
```

#### JSON Format

```json
{
  "games": [
    {
      "match": "Team A vs Team B",
      "sport": "NBA",
      "date": "2025-10-15",
      "bookmakers": [
        {
          "name": "DraftKings",
          "home": 2.10,
          "away": 1.80
        },
        {
          "name": "FanDuel",
          "home": 1.95,
          "away": 1.95
        }
      ]
    }
  ]
}
```

#### Three-Way Format (Soccer)

```json
{
  "games": [
    {
      "match": "Manchester United vs Liverpool",
      "sport": "Soccer",
      "date": "2025-10-20",
      "bookmakers": [
        {
          "name": "Bet365",
          "home": 2.75,
          "draw": 3.40,
          "away": 2.60
        }
      ]
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "count": 1,
  "arbitrages": [
    {
      "match": "Team A vs Team B",
      "sport": "NBA",
      "market": "h2h",
      "sportsbook_a": "DraftKings",
      "odds_a": 2.10,
      "outcome_a": "Home/Team A",
      "sportsbook_b": "FanDuel",
      "odds_b": 1.95,
      "outcome_b": "Away/Team B",
      "profit_percentage": 2.1,
      "stake_a": 481.93,
      "stake_b": 518.07,
      "guaranteed_profit": 21.00
    }
  ]
}
```

---

### 5. Convert Odds

Convert odds between different formats.

#### American to Decimal

```bash
curl -X POST "http://localhost:8000/convert-odds" \
  -H "Content-Type: application/json" \
  -d '{
    "odds_value": -110,
    "from_format": "american",
    "to_format": "decimal"
  }'
```

**Response:**
```json
{
  "original": -110,
  "format": "american",
  "decimal": 1.909
}
```

#### Fractional to Decimal

```bash
curl -X POST "http://localhost:8000/convert-odds" \
  -H "Content-Type: application/json" \
  -d '{
    "odds_value": "5/2",
    "from_format": "fractional",
    "to_format": "decimal"
  }'
```

**Response:**
```json
{
  "original": "5/2",
  "format": "fractional",
  "decimal": 3.5
}
```

---

## Python Examples

### Using requests library

```python
import requests

# Get live arbitrage opportunities
response = requests.get(
    "http://localhost:8000/arbitrage/live",
    params={
        "sport": "basketball_nba",
        "markets": "h2h",
        "regions": "us",
        "min_profit": 1.0
    }
)

data = response.json()
print(f"Found {data['count']} arbitrage opportunities")

for arb in data['arbitrages']:
    print(f"{arb['match']}: {arb['profit_percentage']}% profit")
    print(f"  Bet ${arb['stake_a']} on {arb['outcome_a']} @ {arb['odds_a']} ({arb['sportsbook_a']})")
    print(f"  Bet ${arb['stake_b']} on {arb['outcome_b']} @ {arb['odds_b']} ({arb['sportsbook_b']})")
    print(f"  Guaranteed profit: ${arb['guaranteed_profit']}")
    print()
```

### Upload file

```python
import requests

with open('data/sample_odds.json', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        "http://localhost:8000/upload",
        files=files
    )

data = response.json()
print(f"Found {data['count']} arbitrage opportunities")
```

---

## JavaScript/Node.js Examples

### Using fetch

```javascript
// Get live arbitrage opportunities
async function getArbitrages() {
  const params = new URLSearchParams({
    sport: 'basketball_nba',
    markets: 'h2h',
    regions: 'us',
    min_profit: '1.0'
  });

  const response = await fetch(
    `http://localhost:8000/arbitrage/live?${params}`
  );
  
  const data = await response.json();
  
  console.log(`Found ${data.count} arbitrage opportunities`);
  
  data.arbitrages.forEach(arb => {
    console.log(`${arb.match}: ${arb.profit_percentage}% profit`);
    console.log(`  Bet $${arb.stake_a} on ${arb.outcome_a} @ ${arb.odds_a} (${arb.sportsbook_a})`);
    console.log(`  Bet $${arb.stake_b} on ${arb.outcome_b} @ ${arb.odds_b} (${arb.sportsbook_b})`);
    console.log(`  Guaranteed profit: $${arb.guaranteed_profit}`);
  });
}

getArbitrages();
```

### Upload file

```javascript
async function uploadOdds(filePath) {
  const formData = new FormData();
  formData.append('file', fs.createReadStream(filePath));
  
  const response = await fetch('http://localhost:8000/upload', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  console.log(`Found ${data.count} arbitrage opportunities`);
}
```

---

## React Example (Frontend Integration)

```jsx
import { useState, useEffect } from 'react';

function ArbitrageDashboard() {
  const [arbitrages, setArbitrages] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchArbitrages = async () => {
    setLoading(true);
    
    const params = new URLSearchParams({
      sport: 'basketball_nba',
      markets: 'h2h',
      regions: 'us',
      min_profit: '1.0'
    });

    try {
      const response = await fetch(
        `http://localhost:8000/arbitrage/live?${params}`
      );
      const data = await response.json();
      setArbitrages(data.arbitrages);
    } catch (error) {
      console.error('Error fetching arbitrages:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArbitrages();
    
    // Auto-refresh every 60 seconds
    const interval = setInterval(fetchArbitrages, 60000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Found {arbitrages.length} Arbitrage Opportunities</h1>
      {arbitrages.map((arb, index) => (
        <div key={index}>
          <h2>{arb.match}</h2>
          <p>Profit: {arb.profit_percentage}%</p>
          <p>Guaranteed: ${arb.guaranteed_profit}</p>
        </div>
      ))}
    </div>
  );
}
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message here"
}
```

### Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found
- `500` - Internal Server Error

### Example Error Handling (Python)

```python
try:
    response = requests.get("http://localhost:8000/arbitrage/live")
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.ConnectionError:
    print("Could not connect to API")
except Exception as e:
    print(f"Error: {e}")
```

---

## Rate Limiting

The Odds API has the following limits:

- **Free Tier**: 500 requests/month
- **Each request** costs 1-10 requests depending on markets
- Check remaining requests in response header: `x-requests-remaining`

### Best Practices

1. Cache results when possible
2. Use auto-refresh sparingly (60+ seconds)
3. Filter by specific sports/markets to reduce API calls
4. Consider upgrading for production use

---

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Try all endpoints directly in the browser
- See request/response schemas
- Test with different parameters
- View detailed API specifications

---

## WebSocket Support (Future Enhancement)

For real-time updates without polling:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('New arbitrage:', data);
};
```

*Note: WebSocket support is not yet implemented but planned for future releases.*

---

## Questions?

- Check the [README.md](README.md) for more details
- Visit http://localhost:8000/docs for interactive API testing
- Review [QUICKSTART.md](QUICKSTART.md) for setup help

