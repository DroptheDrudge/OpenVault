# Meme Sniper Bot 🎯

A production-ready Solana meme coin sniper bot with paper trading capabilities. Detects early-stage opportunities using on-chain signals, whale tracking, and momentum scoring — all without risking real capital.

## Features

- **Paper Trading Wallet**: Starts with 3.0 SOL, simulates realistic slippage, Jupiter fees, and Solana transaction costs.
- **Signal Layer**: Integrates DexScreener, Pump.fun, and Helius for real-time pair discovery.
- **Whale Radar**: Tracks configured whale wallets, calculates consensus scores, and detects accumulation vs distribution.
- **Momentum Scorer**: Composite 0-100 score based on volume, price velocity, whale activity, holder growth, and buy/sell ratio.
- **Exit Strategy**: TP1 (+50%), TP2 (+100%), trailing stop, time stop, and whale-exit rules.
- **Obsidian Integration**: Auto-generates daily markdown reports and individual trade logs.
- **Async Architecture**: Main loop polls every 30 seconds, fully non-blocking.

## Project Structure

```
/meme_sniper/
├── config/
│   ├── settings.yaml       # All tunable parameters
│   └── wallets.yaml        # Whale wallet list
├── core/
│   ├── __init__.py
│   ├── database.py         # SQLite schema & init
│   ├── models.py           # Pydantic data models
│   ├── signal_collector.py # DexScreener / Pump.fun / Helius
│   ├── whale_tracker.py    # Whale monitoring & consensus
│   ├── momentum_scorer.py  # Scoring & entry logic
│   ├── paper_executor.py   # Paper trade simulation
│   ├── risk_manager.py     # Position sizing & limits
│   └── obsidian_logger.py  # Markdown report generation
├── data/                   # SQLite DB + cached data
├── logs/                   # Runtime logs
├── obsidian/               # Generated markdown reports
├── tests/
│   └── test_paper_trading.py
├── main.py                 # Async entry point
├── requirements.txt
└── README.md
```

## Setup

### 1. Install Python 3.10+

```bash
python --version  # ensure 3.10 or higher
```

### 2. Install Dependencies

```bash
cd meme_sniper
pip install -r requirements.txt
```

### 3. Configure Helius API Key

Get a free API key at [https://helius.xyz](https://helius.xyz). Then edit `config/settings.yaml`:

```yaml
apis:
  helius_api_key: "YOUR_ACTUAL_API_KEY_HERE"
```

### 4. Configure Whale Wallets

Edit `config/wallets.yaml` with the addresses you want to track:

```yaml
wallets:
  - address: "5Q5..."
    nickname: "Whale_A"
```

### 5. Run the Bot

```bash
python main.py
```

The bot will:
- Initialize the SQLite database at `data/meme_sniper.db`
- Start scanning for new Solana pairs
- Log trades to the database and Obsidian markdown files
- Print portfolio snapshots every 30 seconds

## Configuration Highlights

All settings live in `config/settings.yaml`:

| Section | Key Details |
|---------|-------------|
| `wallet` | Initial SOL, max position % (20%), max concurrent positions (5) |
| `slippage` | Base 0.5% + market-cap tiers up to +5% |
| `scoring` | Weights for volume, price, whales, holders, buy/sell ratio |
| `entry_criteria` | Token age 5–120 min, liquidity >$5K, market cap $10K–$1M |
| `exit_strategy` | TP1 (+50%), TP2 (+100%), trailing stop, 4h time stop, whale exit |

## Running Tests

```bash
pytest tests/test_paper_trading.py -v
```

Tests cover:
- Slippage calculation by market cap
- Position sizing limits (max 20%, max 5 positions)
- Trailing stop and hard stop logic
- Whale consensus scoring
- Composite score range (0–100)

## Obsidian Output

- **Daily reports**: `obsidian/daily/YYYY-MM-DD.md`
- **Trade logs**: `obsidian/trades/TRADE_ID.md`

Each trade log includes entry context, exit events, P&L, and whale signals.

## Notes

- Helius free tier has rate limits. If you hit limits, the bot gracefully skips whale scanning for that iteration.
- The bot uses **polling** for Helius (not a persistent webhook server) to keep deployment simple.
- All API integrations use free tiers: DexScreener, Pump.fun, and Helius.

## License

MIT — use at your own risk. This is a paper-trading educational tool.
