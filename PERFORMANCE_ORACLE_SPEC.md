# Performance Oracle — Master Specification

> **"The brain that learns from every neuron, discovers what's missing, and allocates capital where the edge is strongest."**

---

## Vision

The Performance Oracle is a **meta-learning capital allocation and strategy intelligence system**. It sits above all trading neurons, ingests their outputs, learns cross-strategy patterns, identifies gaps in the ecosystem, and dynamically reallocates resources.

**It does not trade directly. It makes every other system smarter.**

---

## Systems in the Ecosystem (Data Sources)

| Neuron ID | Asset Class | Strategy Type | Data Output |
|-----------|-------------|---------------|-------------|
| `meme_sniper` | Solana meme coins | Momentum + whale consensus | P&L, scores, whale hits, signals |
| `ferrari_ea` | Forex | Statistical arbitrage + ONNX regime | Sharpe, win rate, z-scores, regimes |
| `lamborghini_ea` | Forex | Trend following | Sharpe, trend capture rate, drawdowns |
| `porsche_ea` | Forex | SMC + session optimization | Win rate by session, drawdown |
| `bugatti_ea` | Forex | Macro/carry | Carry returns, interest rate correlation |
| `mclaren_ea` | Forex | Sentiment/COT contrarian | COT positioning, contrarian timing |
| `stallion_ea` | US Equities | Momentum + mean reversion + pair trades | Prop firm equity, daily P&L, regime fit |
| `hmm_detector` | All markets | Regime classification | Regime labels, transition probabilities |
| `prediction_bot` | Multi-asset | ML price predictions | Directional accuracy, calibration |
| `crypto_bot` | Multi-crypto | (To be discovered by Oracle) | Performance metrics |

**Rule:** Any system that produces structured performance data can register itself with the Oracle.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    PERFORMANCE ORACLE                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  LAYER 1: INGESTION HUB (Sensory Neuron)                     │
│  ├─ SQLite connectors for each registered neuron            │
│  ├─ File watchers for MQL5/Markdown logs                    │
│  ├─ REST endpoints for push-based data                      │
│  └─ Unified data lake (SQLite + Parquet cache)              │
│                                                              │
│  LAYER 2: INTELLIGENCE ENGINE (Processing Neuron)            │
│  ├─ Regime-Skill Mapper                                     │
│  ├─ Cross-Strategy Correlation Detector                     │
│  ├─ Gap Discovery Engine                                    │
│  ├─ Bayesian Skill Estimator                                │
│  └─ Kelly Capital Allocator                                 │
│                                                              │
│  LAYER 3: ACTION DISPATCHER (Motor Neuron)                  │
│  ├─ Config writer (enables/pauses EAs)                      │
│  ├─ Position sizing publisher                               │
│  ├─ Alert generator                                         │
│  └─ Neuron birth requester (flags missing strategies)       │
│                                                              │
│  LAYER 4: NARRATIVE ENGINE (Glial Neuron)                   │
│  ├─ Daily allocation report                                 │
│  ├─ Strategy gap report                                     │
│  ├─ Neuron scorecard                                        │
│  └─ Cross-strategy insight log                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Ingestion Hub

### Unified Schema

Every neuron must write to SQLite with at least these tables:

```sql
-- Neuron registry (self-registration)
CREATE TABLE oracle_registry (
    neuron_id TEXT PRIMARY KEY,
    asset_class TEXT,
    strategy_type TEXT,
    status TEXT,  -- active | paused | dead
    first_seen TEXT,
    last_heartbeat TEXT
);

-- Performance metrics (daily snapshots)
CREATE TABLE oracle_performance (
    id INTEGER PRIMARY KEY,
    neuron_id TEXT,
    date TEXT,
    metric_name TEXT,  -- sharpe, win_rate, max_dd, profit_factor, expectancy
    metric_value REAL,
    sample_size INTEGER,
    regime TEXT  -- trend_up, range, high_vol, etc. (optional)
);

-- Trade-level data (for deep analysis)
CREATE TABLE oracle_trades (
    id INTEGER PRIMARY KEY,
    neuron_id TEXT,
    timestamp TEXT,
    symbol TEXT,
    direction TEXT,  -- long | short | neutral
    entry_price REAL,
    exit_price REAL,
    pnl_pct REAL,
    pnl_abs REAL,
    regime TEXT,
    holding_time_hours REAL,
    exit_reason TEXT
);

-- Market context at time of trade/signal
CREATE TABLE oracle_context (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    regime TEXT,
    regime_confidence REAL,
    vix_proxy REAL,
    btc_dominance REAL,
    sol_meme_index REAL  -- custom composite indices
);
```

### Ingestion Modes

| Neuron | Ingestion Method | Frequency |
|--------|-----------------|-----------|
| Meme Sniper | SQLite read | Every 30s |
| MQL5 EAs | File watcher on `Experts/*.log` + JSON export | Every 1h |
| HMM Detector | SQLite read | Every bar close |
| Prediction Bot | REST API push | On prediction |
| Crypto Bot | SQLite read | Every 5 min |

---

## Layer 2: Intelligence Engine

### Module 2A: Regime-Skill Mapper
**Question:** *Which neuron performs best in which market regime?*

**Algorithm:**
```python
def map_regime_skills(neuron_id, lookback_days=30):
    regimes = get_unique_regimes(lookback_days)
    skills = {}
    for regime in regimes:
        trades = filter_trades(neuron_id, regime=regime, days=lookback_days)
        skills[regime] = {
            'sharpe': calculate_sharpe(trades),
            'win_rate': calculate_win_rate(trades),
            'expectancy': calculate_expectancy(trades),
            'sample_size': len(trades),
            'confidence': bayesian_confidence(len(trades))
        }
    return skills
```

**Output:** Regime-skill heatmap updated daily.

---

### Module 2B: Cross-Strategy Correlation Detector
**Question:** *Are my neurons secretly betting on the same thing?*

**Algorithm:**
```python
def detect_correlations():
    neurons = get_active_neurons()
    for i, j in combinations(neurons, 2):
        pnl_series_i = get_daily_pnl(i)
        pnl_series_j = get_daily_pnl(j)
        corr = pearson_correlation(pnl_series_i, pnl_series_j)
        if abs(corr) > 0.7:
            flag_redundancy(i, j, corr)
        elif abs(corr) > 0.4:
            flag_complementarity(i, j, corr)
```

**Why it matters:** If Ferrari and Stallion are 85% correlated, you're not diversified — you're doubling down. The Oracle should pause one or reduce capital.

---

### Module 2C: Gap Discovery Engine
**Question:** *What strategies or markets am I NOT covering that I should be?*

**Gap categories:**

| Gap Type | Detection Logic | Example Output |
|----------|----------------|----------------|
| **Regime Gap** | High-confidence regime with no winning neuron | "High-vol regime: no neuron has Sharpe >1.0" |
| **Asset Gap** | Asset class with active opportunities but no neuron | "Crypto altcoins: prediction_bot accuracy 34%, need specialist" |
| **Time Gap** | Specific hours/days where all neurons underperform | "Asian session: all forex EAs Sharpe <0.5" |
| **Correlation Gap** | All active neurons are highly correlated | "Portfolio correlation = 0.82, need contrarian neuron" |
| **Decay Gap** | Neuron performance declining over 30 days | "Porsche EA Sharpe dropped from 1.8 to 0.6" |

**Gap Report Example:**
```markdown
# Oracle Gap Report — 2026-04-14

## 🔴 Critical Gaps
1. **High-Volatility Regime Coverage Gap**
   - Current state: Only Meme Sniper performs here (Sharpe 2.34)
   - All forex EAs struggle in high-vol (Sharpe <0.8)
   - Recommendation: Build volatility-targeting forex neuron OR pause forex during high-vol

2. **Asian Session Underperformance**
   - Lamborghini: Sharpe 0.12 in Asian session
   - Ferrari: Sharpe 0.34 in Asian session
   - Porsche: Slightly better at 0.89
   - Recommendation: Consider session-specific position sizing OR build Asia-specialist neuron

## 🟡 Warnings
3. **Correlation Creep**
   - Ferrari and Stallion daily P&L correlation: 0.71
   - They may be exposed to the same risk factor (US equity momentum)
   - Recommendation: Investigate overlap, diversify macro factor exposure

## 🟢 Opportunities
4. **Meme Sniper Momentum**
   - Whale consensus hit rate improving: 34% → 52% over 14 days
   - Consider increasing allocation cap from 20% to 30%
```

---

### Module 2D: Bayesian Skill Estimator
**Question:** *How good is each neuron, really, accounting for uncertainty?*

**Algorithm:**
```python
def bayesian_skill_estimate(neuron_id, regime=None):
    prior = get_historical_performance(neuron_id, regime)
    likelihood = get_recent_performance(neuron_id, regime, days=30)
    
    # Beta distribution for win rate
    alpha = prior['wins'] + likelihood['wins'] + 1
    beta = prior['losses'] + likelihood['losses'] + 1
    win_rate_distribution = Beta(alpha, beta)
    
    # For Sharpe: use Student's t posterior
    sharpe_distribution = students_t_posterior(likelihood['returns'])
    
    return {
        'win_rate_mean': win_rate_distribution.mean(),
        'win_rate_5th_percentile': win_rate_distribution.ppf(0.05),
        'sharpe_mean': sharpe_distribution.mean(),
        'sharpe_5th_percentile': sharpe_distribution.ppf(0.05)
    }
```

**Why Bayesian:** Small sample sizes are common. A neuron with 8/10 wins is promising but uncertain. Bayesian methods don't overrate it.

---

### Module 2E: Kelly Capital Allocator
**Question:** *How much capital should each neuron get?*

**Algorithm:**
```python
def kelly_allocation(neuron_skills, max_per_neuron=0.40, min_allocation=0.0):
    """
    neuron_skills: dict of {neuron_id: {'win_rate': w, 'avg_win': aw, 'avg_loss': al}}
    """
    raw_kelly = {}
    for neuron_id, skill in neuron_skills.items():
        w = skill['win_rate']
        b = skill['avg_win'] / skill['avg_loss'] if skill['avg_loss'] != 0 else 10
        kelly = (w * b - (1 - w)) / b
        raw_kelly[neuron_id] = max(0, kelly)  # No negative allocations
    
    # Normalize
    total = sum(raw_kelly.values())
    if total == 0:
        return {n: 0.0 for n in neuron_skills}
    
    allocations = {n: v / total for n, v in raw_kelly.items()}
    
    # Apply constraints
    for n in allocations:
        allocations[n] = min(allocations[n], max_per_neuron)
    
    # Renormalize after capping
    total = sum(allocations.values())
    allocations = {n: v / total for n, v in allocations.items()}
    
    return allocations
```

**Modifications:**
- **Regime overlay:** Multiply allocation by `P(regime → neuron wins)`
- **Correlation penalty:** If two neurons have correlation >0.6, reduce both by 20%
- **Prop firm safety:** Neurons with daily drawdown >3% get hard cap at 15%

---

## Layer 3: Action Dispatcher

### Config Writer
Automatically updates neuron configs based on Oracle decisions:

```yaml
# oracle_allocation.yaml (auto-generated)
generated_at: "2026-04-14T08:00:00Z"
regime: "range"
allocations:
  meme_sniper:
    capital_pct: 0.20
    status: "active"
    position_size_multiplier: 1.0
  
  ferrari_ea:
    capital_pct: 0.35
    status: "active"
    max_positions: 4
  
  lamborghini_ea:
    capital_pct: 0.05
    status: "active"
    # Suppressed in range regime
  
  bugatti_ea:
    capital_pct: 0.00
    status: "paused"
    reason: "30-day Sharpe below 0.50 in all regimes"
    resume_condition: "Sharpe > 0.70 for 14 days in any regime"
```

Each neuron reads this file on startup and adjusts behavior.

### Alert Generator
- Telegram/Discord webhook for critical gaps
- Daily summary to Obsidian
- Emergency alert if portfolio correlation >0.85

### Neuron Birth Requester
When a gap is detected that no existing neuron can fill:
```markdown
# Neuron Birth Request — 2026-04-14

## Gap Identified
**Missing:** High-volatility forex specialist
**Evidence:** All forex EAs Sharpe <0.8 in high-vol regime
**Opportunity:** HMM detects high-vol regime 18% of the time
**Expected Value:** If a specialist could achieve Sharpe 1.2, annual contribution = +8.4%

## Proposed Neuron Spec
**Name:** `volatility_ea`
**Asset Class:** Forex majors
**Strategy:** Volatility breakout + straddle-like position scaling
**Required Data:** ATR(14), Bollinger Band width, VIX proxy
**Estimated Build Time:** 3-5 sessions
**Priority:** MEDIUM

## Parent Systems
- Feeds from HMM Detector (regime = high_vol)
- Reports to Performance Oracle
- Uses Forex Garage Brain for execution
```

This gets written to `07_HANDOVER/neuron_birth_requests/` for Bob and AIs to pick up.

---

## Layer 4: Narrative Engine

### Daily Oracle Report Sections
1. **Executive Summary** — allocations, top performer, biggest concern
2. **Neuron Scorecard** — updated leaderboard
3. **Regime-Skill Heatmap** — which neurons win where
4. **Gap Discovery** — what's missing
5. **Cross-Strategy Insights** — correlations, redundancies, hidden risks
6. **Tomorrow's Outlook** — expected regime, recommended allocation

### Cross-Strategy Insight Log
```markdown
# Cross-Strategy Insight — 2026-04-14

## Finding: Meme Sniper and Lamborghini share a hidden macro factor
**Correlation:** 0.43 daily P&L
**Hypothesis:** Both are exposed to "risk-on" sentiment.
- Meme Sniper pumps when crypto risk appetite is high
- Lamborghini (trend forex) captures USD/JPY momentum, which is also risk-sentiment driven
**Implication:** On risk-off days (VIX spikes), both underperform simultaneously.
**Recommendation:** Increase McLaren allocation during risk-off (it's designed as contrarian)
```

---

## The Compounding Loop

```
Day 1: Oracle ingests data, generates first allocation
    ↓
Day 7: Oracle detects Ferrari outperforms in range regimes
    ↓
Day 14: Oracle increases Ferrari allocation in range, decreases Lamborghini
    ↓
Day 30: Oracle detects all forex EAs underperform in Asian session
    ↓
Day 45: Oracle requests "Asia-Specialist Neuron" birth
    ↓
Day 60: Asia-Specialist neuron is built, registered, starts producing data
    ↓
Day 90: Oracle evaluates Asia-Specialist, integrates into allocation
    ↓
Year 1: Portfolio of 8-12 specialized neurons, dynamically allocated
```

**The Oracle never stops learning. The ecosystem never stops growing.**

---

## Interfaces & Standards

### CLI Commands
```bash
python oracle.py --status     # Show current allocation + health
python oracle.py --report     # Generate today's Obsidian report
python oracle.py --gaps       # Show all detected gaps
python oracle.py --simulate   # Run allocation on historical data
python oracle.py --health     # JSON health output
```

### REST API
```
POST /register      # New neuron registers itself
GET  /allocation    # Current capital allocation
GET  /scorecard     # JSON neuron scorecard
GET  /gaps          # Detected strategy gaps
POST /ingest        # Push data from external neuron
```

### File Outputs
- `data/oracle.db` — Unified data lake
- `obsidian/oracle/daily/YYYY-MM-DD.md` — Daily reports
- `obsidian/oracle/gaps/` — Gap discovery reports
- `obsidian/oracle/scorecard.md` — Live scorecard
- `config/oracle_allocation.yaml` — Active allocations

---

## Testing Strategy

1. **Backtest Mode:** Run Oracle on 90 days of synthetic/historical data. Verify allocations shift based on performance.
2. **Simulation Mode:** Run live but output allocations only (no config writes). Compare to static equal-weight benchmark.
3. **Gradual Deployment:** Start with 2-3 neurons. Add one per week. Monitor for stability.
4. **Chaos Tests:** Drop a neuron's data feed. Verify Oracle degrades gracefully.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | The Fix |
|--------------|--------------|---------|
| **Overfitting to Recent Data** | Chases last week's winner | Bayesian smoothing + minimum sample sizes |
| **Binary On/Off** | Pausing neurons too aggressively | Soft allocations (0% to 40%) instead of hard kills |
| **Ignoring Correlations** | Thinks 10 neurons = 10x diversification | Correlation penalty in allocator |
| **Silent Gaps** | Missing opportunities go unnoticed | Automated gap reports + priority scoring |
| **Manual Overrides** | Bob tweaks allocations based on gut | Override logged as ADR, reverted if not justified |

---

## Implementation Roadmap

### Phase 1: Ingestion + Unified Schema (Session 1)
- Build ingestion connectors for Meme Sniper + HMM Detector
- Define unified schema
- Start collecting data

### Phase 2: Regime-Skill Mapper + Scorecard (Session 2)
- Calculate performance by regime
- Generate first scorecard
- Write to Obsidian

### Phase 3: Kelly Allocator + Config Writer (Session 3)
- Implement Kelly logic
- Generate `oracle_allocation.yaml`
- Backtest on synthetic data

### Phase 4: Gap Discovery + Correlation Detector (Session 4)
- Cross-strategy correlation analysis
- Gap detection rules
- Birth request generation

### Phase 5: Full Integration (Session 5)
- Connect all neurons
- Live simulation mode
- Iterate on edge cases

---

## For AI Assistants

**When building the Performance Oracle:**
1. It is a **processing neuron** that reads from sensory neurons and writes to motor neurons
2. It must be **standalone** — can simulate allocations even if no other neurons are online
3. It must **self-document** — every allocation decision has a rationale in Obsidian
4. It must **fail gracefully** — if a data feed drops, use last known values with uncertainty penalties
5. It must **get smarter** — every day of new data improves the Bayesian estimates

**This is the brain of brains. Build it like one.**

---

## Related Documents
- [[COMPOUNDING_INTELLIGENCE_MANDATE]]
- [[NEURON_DOCTRINE]]
- [[AI_HANDOVER_STANDARD]]
- [[OBSERVABILITY_MANDATE]]
- [[TOKEN_OPTIMIZATION_STRATEGY]]

**Status:** SPEC_COMPLETE — Ready for Implementation  
**Priority:** HIGHEST  
**Impact:** Multiplicative on all existing neurons

---

*The Oracle doesn't predict the future. It learns which part of your brain should be awake right now.* 🧠⚡💰
