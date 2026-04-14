# The Observability Mandate

> **"If I can't see it in Obsidian, it didn't happen."**
> 
> — Visibility Rule

---

## Core Principle

You operate multiple AI systems across multiple sessions. **Obsidian is your shared memory.** If a system doesn't write to Obsidian, it might as well not exist — because you (and future AIs) will have no record of what it did, why it did it, or how it performed.

**This is not logging.** This is **narrative infrastructure.**

---

## The Three Outputs

Every system must write to **three places simultaneously**:

### 1. SQLite — Structured Data
For queries, analysis, machine learning.

```sql
-- Example: trades table
CREATE TABLE trades (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    token_symbol TEXT,
    token_address TEXT,
    entry_price REAL,
    exit_price REAL,
    position_size_sol REAL,
    pnl_sol REAL,
    pnl_pct REAL,
    exit_reason TEXT,  -- 'tp1', 'tp2', 'trailing_stop', 'whale_exit', 'time_stop'
    whale_consensus_score REAL,
    metadata JSON
);
```

**Rule:** Any metric you might want to plot in 6 months must be in SQLite.

---

### 2. Markdown (Obsidian) — Human Narrative
For understanding context, decisions, and stories.

**Daily Reports:**
```markdown
# Meme Sniper Report — 2026-04-14

## Summary
- Signals scanned: 156
- Trades executed: 0
- Paper portfolio: 3.000 SOL (unchanged)
- Best candidate: $UNCEON (score: 33.5/100)

## Why No Trades?
Score threshold is 60. Best candidate scored 33.5.
Missing: whale consensus (avg: 0.2/1.0), liquidity ($34k vs $5k min).

## Whale Activity
| Wallet | Nickname | Trades Today | Consensus Impact |
|--------|----------|--------------|------------------|
| G5nx... | LeBron | 0 | 0.00 |
| H1aJ... | AI16Z_Wizard | 0 | 0.00 |

## Notable Signals
1. $UNCEON — mc=$180k, liq=$34k, age=53min, score=33.5
   - Reason for low score: liquidity below $50k preference, whale consensus weak

## System Health
- Status: ✅ Healthy
- Cycles completed: 2880
- Errors: 0
- Warnings: Helius API latency 2.3s (acceptable)

## Tomorrow's Focus
- Continue whale wallet discovery (target: 12 wallets)
- Monitor for any token breaking 60-point threshold
```

**Individual Trade Reports:**
```markdown
# Trade: $GHOST — 2026-04-14 14:23 UTC

## Decision Context
- Entry signal: Whale consensus 0.8 (LeBron + AI16Z_Wizard both buying)
- Momentum score: 72/100
- Liquidity: $890k (excellent)
- Age: 12 minutes (early)

## Execution
- Entry: 0.00001234 SOL
- Position size: 0.6 SOL (20% of portfolio)
- Expected exit: TP1 @ +50%, TP2 @ +100%, trailing stop @ -20%

## Whale Consensus Breakdown
| Whale | Weight | Action | Confidence |
|-------|--------|--------|------------|
| LeBron | 0.4 | Buy | 0.95 |
| AI16Z_Wizard | 0.35 | Buy | 0.88 |
| AI_MegaWhale | 0.25 | Hold | 0.00 |

## Rationale
Strong early consensus from top 2 whales. High liquidity means low slippage.
Young token age suggests potential upside. Score 72 exceeds threshold 60.

## Exit Plan
1. TP1 (+50%): Sell 25% at 0.00001851
2. TP2 (+100%): Sell 25% at 0.00002468
3. Trailing stop: 20% below peak
4. Time stop: Close at 4h if no TP hit
```

---

### 3. Logs — Debug Detail
For troubleshooting when things break.

```json
{"timestamp": "2026-04-14T07:45:32Z", "level": "INFO", "component": "signal_collector", "message": "DexScreener scan complete", "signals_found": 28, "filters_applied": ["min_liquidity_usd", "min_age_minutes"], "signals_passed": 3}
{"timestamp": "2026-04-14T07:45:33Z", "level": "DEBUG", "component": "whale_tracker", "message": "Querying Helius for whale activity", "wallets_checked": 8, "active_whales": 0, "consensus_score": 0.0}
{"timestamp": "2026-04-14T07:45:34Z", "level": "INFO", "component": "scoring_engine", "message": "Token scored", "token": "UNCEON", "score": 33.5, "threshold": 60, "passed": false, "reason": "below_threshold"}
```

**Log levels:**
- `DEBUG` — Detailed flow (for development)
- `INFO` — Normal operations (for monitoring)
- `WARN` — Anomalies that didn't break things (for attention)
- `ERROR` — Failures that need fixing (for immediate action)
- `CRITICAL` — System is down (for alerts)

---

## Obsidian Folder Structure

```
Obsidian Vault/
├── 00_INBOX/                    # Raw, unprocessed inputs
│   └── (temp files, don't commit)
│
├── 01_MANDATES/                 # Core principles (these files!)
│   ├── COMPOUNDING_INTELLIGENCE_MANDATE.md
│   ├── NEURON_DOCTRINE.md
│   ├── AI_HANDOVER_STANDARD.md
│   └── OBSERVABILITY_MANDATE.md  ← you are here
│
├── 02_SYSTEMS/                  # System documentation
│   ├── MEME_SNIPER/
│   │   ├── ARCHITECTURE.md
│   │   ├── SETUP.md
│   │   └── DECISIONS/           # ADRs
│   │       └── 001_why_whale_consensus.md
│   │
│   ├── HMM_REGIME_DETECTOR/
│   ├── FOREX_GARAGE/
│   └── PROJECT_STALLION/
│
├── 03_DAILY/                    # Auto-generated daily reports
│   ├── 2026-04-14.md
│   ├── 2026-04-13.md
│   └── ...
│
├── 04_TRADES/                   # Individual trade narratives
│   ├── 2026-04-14_GHOST_entry.md
│   ├── 2026-04-14_GHOST_exit.md
│   └── ...
│
├── 05_ANALYSIS/                 # Periodic analysis
│   ├── whale_performance_review.md
│   ├── strategy_backtest_results.md
│   └── system_health_trends.md
│
├── 06_DECISIONS/                # Architecture Decision Records
│   ├── ADR-001-use-sqlite-over-postgres.md
│   ├── ADR-002-why-60-point-threshold.md
│   └── ADR-003-auto-whale-discovery-design.md
│
├── 07_HANDOVER/                 # AI handover states
│   ├── CURRENT.md               # Link to latest HANDOVER.md
│   └── archive/
│
└── 99_ARCHIVE/                  # Old, completed, deprecated
    └── (move old files here)
```

---

## The Daily Report Ritual

Every system must generate a daily report at **00:00 UTC** (or local midnight).

**Required sections:**
1. **Summary** — Numbers at a glance
2. **What Happened** — Narrative of the day
3. **Why It Happened** — Analysis, not just facts
4. **System Health** — Status, errors, warnings
5. **Tomorrow's Focus** — What to watch for

**Automation:**
```python
def generate_daily_report():
    yesterday = datetime.now() - timedelta(days=1)
    trades = query_sqlite_for_date(yesterday)
    signals = query_signals_for_date(yesterday)
    health = get_system_health()
    
    markdown = render_template(trades, signals, health)
    write_to_obsidian(f"03_DAILY/{yesterday.strftime('%Y-%m-%d')}.md", markdown)
```

---

## Architecture Decision Records (ADRs)

**Every significant decision gets an ADR in `06_DECISIONS/`.**

**Template:**
```markdown
# ADR-003: Auto-Whale-Discovery Design

## Status
Accepted

## Context
Only 4 whale wallets manually added. Need 12 for good consensus scores.
Manual research is slow and doesn't scale.

## Decision
Build auto-discovery that:
1. Scans tokens with 3x+ pumps
2. Identifies early buyers (first 30 min)
3. Validates profitability (30-day history)
4. Auto-adds to config if >40% win rate

## Consequences
- Positive: Scales to 15 wallets without manual work
- Positive: Adapts to market (finds new whales as they emerge)
- Risk: May add low-quality whales during data gaps
- Mitigation: 14-day inactivity auto-removal

## Alternatives Considered
1. **Manual curation only** — Rejected: doesn't scale
2. **Paid whale alert services** — Rejected: costs money, not customizable
3. **Copy-trade aggregators** — Rejected: laggy, everyone sees same signals

## Related
- [[COMPOUNDING_INTELLIGENCE_MANDATE]]
- [[MEME_SNIPER_ARCHITECTURE]]
```

**When to write an ADR:**
- Choosing a technology (SQLite vs Postgres, ZeroMQ vs HTTP)
- Changing a core algorithm (scoring, exits, detection)
- Adding/removing a major feature
- Any decision that future-you might question

---

## The System Health Dashboard

Every system must maintain a `SYSTEM_STATUS.md` at repo root.

```markdown
# System Status — Meme Sniper

**Last Updated:** 2026-04-14 07:45 UTC  
**Status:** 🟢 Healthy

## Vitals
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Uptime | 24h 12m | >24h | ✅ |
| Cycles | 2880 | >2000 | ✅ |
| Error Rate | 0% | <1% | ✅ |
| Avg Cycle Time | 28s | <35s | ✅ |
| Disk Usage | 45MB | <1GB | ✅ |
| Memory Usage | 128MB | <512MB | ✅ |

## Subsystems
| Subsystem | Status | Last Activity | Notes |
|-----------|--------|---------------|-------|
| Signal Collector | ✅ OK | 2 min ago | 28 signals/min avg |
| Whale Tracker | ⚠️ Degraded | 5 min ago | Helius latency 2.3s |
| Scoring Engine | ✅ OK | 2 min ago | — |
| Paper Trading | ✅ OK | N/A | No trades today |
| SQLite | ✅ OK | 2 min ago | 156 trades logged |
| Obsidian Bridge | ✅ OK | 2 min ago | — |

## Alerts (Last 24h)
- 2026-04-14 03:12: WARN — Helius API latency >2s (resolved)
- 2026-04-14 05:45: INFO — Daily report generated

## Open Issues
1. Need more whale wallets (8/15)
2. Consider lowering score threshold in low-activity periods

## Next Maintenance
- None scheduled
```

**Update frequency:** Every 15 minutes (or on status change)

---

## Anti-Patterns

| Anti-Pattern | The Sin | The Fix |
|--------------|---------|---------|
| **Silent Running** | System works but logs nothing | Mandatory daily reports |
| **Log Spew** | Too much noise, signal lost | Structured logging with levels |
| **Missing Context** | "Error: failed" with no details | Always log: what, why, stack trace |
| **Orphaned Data** | SQLite has data, no markdown narrative | Every DB write has MD equivalent |
| **Ancient History** | Can't find what happened 3 weeks ago | Date-stamped files, archive old ones |

---

## For AI Assistants

**When building a system, ask:**
1. What data should be in SQLite for later analysis?
2. What narrative should be in Markdown for human understanding?
3. What detail should be in Logs for debugging?
4. Where does the daily report go?
5. How do I handle errors visibly?

**When modifying a system:**
1. Will this change the data schema? (Update SQLite)
2. Will this change the user experience? (Update Markdown templates)
3. Will this change the debugging experience? (Update Log messages)

**Rule of thumb:** If you spend more than 10 minutes debugging something, that debugging info should have been in Obsidian from the start.

---

## Related Documents
- [[COMPOUNDING_INTELLIGENCE_MANDATE]] — How systems learn
- [[NEURON_DOCTRINE]] — How systems are structured  
- [[AI_HANDOVER_STANDARD]] — How systems transition between AIs

**Status:** ACTIVE LAW  
**Enforced by:** All AI collaborators  
**Violation:** Blind spots, mystery bugs, wasted investigation time

---

*What gets measured gets managed. What gets narrated gets understood.* 📊📝
