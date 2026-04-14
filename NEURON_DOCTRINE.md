# The Neuron Doctrine

> **"Every new system is a neuron. It must be able to connect to the brain, but it must also function standalone."**
> 
> — Architecture Mandate

---

## Core Principle

Your infrastructure is a **brain**. Individual systems are **neurons**. The brain coordinates, but neurons have agency. If the brain goes offline, neurons continue firing. If a neuron fails, the brain reroutes around it.

**This is not microservices.** This is not monolith. This is **intelligent agency with federation.**

---

## The Four Rules of Neuron Design

### 1. Modular by Default
A neuron must boot and operate **without hard dependencies** on other neurons.

**✅ Good:**
- Meme Sniper runs paper trading even if Obsidian bridge is down
- HMM Detector generates MQL5 files even if MT5 isn't installed
- Forex Garage EA makes local decisions if Brain Stem is offline

**❌ Bad:**
- System crashes because Redis is unreachable
- Bot won't start because it can't reach a config server
- EA refuses to trade without live brain connection

**Implementation:**
- Local SQLite for state (not remote DB)
- YAML configs (not centralized config service)
- Graceful degradation with clear fallback logic

---

### 2. Standardized Interfaces
Every neuron speaks the same language.

| Component | Standard | Example |
|-----------|----------|---------|
| **Configuration** | YAML files | `config/settings.yaml` |
| **Structured Data** | SQLite | `data/trades.db` |
| **Human Narrative** | Markdown | `obsidian/daily/2026-04-14.md` |
| **Inter-neuron Comms** | ZeroMQ or HTTP | `tcp://localhost:5555` |
| **Logs** | Structured JSON | `logs/bot_run.log` |
| **Health Status** | JSON endpoint | `GET /health` returns `{"status": "ok", "last_trade": "..."}` |

**Why:** Any AI (Kimi, Claude, Codex) can pick up any neuron and understand it in <5 minutes.

---

### 3. Self-Identification
Every neuron must answer: *"Who am I, what am I doing, and am I healthy?"*

**Required in every system:**
```python
SYSTEM_ID = {
    "name": "meme_sniper",
    "version": "1.2.0",
    "purpose": "Solana meme coin paper trading with whale consensus",
    "health": {
        "status": "healthy",
        "last_heartbeat": "2026-04-14T07:45:00Z",
        "active_positions": 3,
        "whales_tracked": 12
    }
}
```

**CLI command:** Every neuron must support `python main.py --status` and return the above.

---

### 4. Graceful Degradation
When dependencies fail, the neuron must **degrade, not die**.

| Failure | Degradation Strategy |
|---------|---------------------|
| Helius API down | Continue with DexScreener signals only, whale score = 0 |
| SQLite locked | Write to temp JSON, retry in 60s |
| Obsidian bridge offline | Queue markdown writes, flush on reconnect |
| ZeroMQ brain offline | Switch to local-only mode, log decisions locally |
| Network timeout | Exponential backoff, max 5 retries, then skip cycle |

**Rule:** The 30-second loop must never break. Ever.

---

## Neuron Taxonomy

### Type A: Sensory Neurons (Data Ingestion)
- **Purpose:** Collect raw data from external sources
- **Examples:**
  - DexScreener scraper
  - Helius whale tracker
  - MT5 tick collector
- **Output:** Structured data to SQLite

### Type B: Processing Neurons (Analysis)
- **Purpose:** Transform data into signals/decisions
- **Examples:**
  - Momentum scorer
  - HMM regime classifier
  - ONNX inference engine
- **Output:** Scores, regimes, predictions

### Type C: Motor Neurons (Action)
- **Purpose:** Execute decisions in the real world
- **Examples:**
  - Paper trading engine
  - MQL5 order executor
  - Alert dispatcher
- **Output:** Trades, alerts, reports

### Type D: Glial Neurons (Support)
- **Purpose:** Support other neurons (logging, health, coordination)
- **Examples:**
  - Obsidian bridge
  - Health monitor
  - Brain Stem coordinator
- **Output:** Documentation, status, routing

---

## Connection Patterns

### Pattern 1: Direct Synapse (Tight Coupling)
```
Meme Sniper → ZeroMQ → Brain Stem
```
Use when: Real-time coordination is critical
Risk: Dependency failure
Mitigation: Local queue + retry

### Pattern 2: Chemical Synapse (Loose Coupling)
```
Meme Sniper → SQLite → Obsidian Bridge → Brain Stem
```
Use when: Durability > latency
Benefit: Complete decoupling, audit trail

### Pattern 3: Reflex Arc (Local Only)
```
MQL5 EA → Local ONNX → Immediate decision
```
Use when: Speed is everything
Note: Logs to brain post-hoc, doesn't wait for permission

---

## Health Monitoring

Every neuron must expose:

```bash
$ python main.py --health
{
  "neuron_id": "meme_sniper",
  "status": "healthy",  // healthy | degraded | critical | dead
  "uptime_seconds": 86400,
  "cycles_completed": 2880,
  "cycles_failed": 0,
  "last_output": "2026-04-14T07:45:00Z",
  "dependencies": {
    "helius_api": "ok",
    "dexscreener": "ok",
    "sqlite": "ok",
    "obsidian_bridge": "degraded (retrying)"
  }
}
```

**The Brain Stem polls this every 60 seconds.** If a neuron is `critical` for 5 minutes, it gets restarted. If `dead`, an alert fires.

---

## Testing a Neuron

Before any neuron ships, verify:

- [ ] Boots without internet connection (uses cached config)
- [ ] Runs for 100 cycles without crashing
- [ ] Survives all dependency failures (tested via mocks)
- [ ] `--health` returns valid JSON
- [ ] `--status` explains current activity
- [ ] Logs are structured and parseable
- [ ] Can be restarted mid-cycle and resume correctly
- [ ] Memory usage is stable (no leaks over 24h)

---

## Examples of Neuron Architecture

### Meme Sniper (Current)
```
Sensory:    DexScreener API, Helius API
Processing: Signal scorer, whale consensus calculator
Motor:      Paper trading engine, SQLite writer
Glial:      Obsidian bridge, health reporter

Interfaces:
- Config:   config/settings.yaml
- Data:     data/meme_sniper.db
- Narrative: obsidian/daily/*.md, obsidian/trades/*.md
- Health:   HTTP endpoint on :8080/health
```

### HMM Regime Detector (Planned)
```
Sensory:    OHLCV from MT5 or CSV
Processing: HMM fit/predict
Motor:      MQL5 file export, signal emitter
Glial:      Model versioning, performance tracker

Interfaces:
- Config:   config/hmm_config.yaml
- Data:     data/regime_history.db
- Narrative: obsidian/regimes/*.md
- Health:   CLI --health flag
```

---

## Anti-Patterns

| Anti-Pattern | The Sin | The Fix |
|--------------|---------|---------|
| **Distributed Monolith** | Neurons can't function alone | Design for standalone first, connect second |
| **Spaghetti Synapses** | Random HTTP calls between neurons | Standardize on ZeroMQ or SQLite as interface |
| **Silent Neuron** | No health check, no status | Mandatory --health and --status commands |
| **Hardcoded Brain** | Brain address burned into code | Configurable, with local fallback |
| **Memory Leak Neuron** | RAM grows unbounded | Profile 24h run, fix leaks before ship |

---

## For AI Assistants

**When Bob says "build a new neuron":**

1. **Read this doctrine first**
2. **Classify the neuron:** Sensory | Processing | Motor | Glial
3. **Define interfaces:** How will other neurons interact with this?
4. **Design degradation:** What happens when dependencies fail?
5. **Implement health checks:** --health and --status flags
6. **Test standalone:** Disconnect everything, does it still boot?
7. **Document in Obsidian:** Create SYSTEM.md in appropriate folder

**If it can't run alone, it's not a neuron. It's a tumor.**

---

## Related Documents
- [[COMPOUNDING_INTELLIGENCE_MANDATE]] — How neurons learn
- [[AI_HANDOVER_STANDARD]] — How neurons transition between AIs
- [[OBSERVABILITY_MANDATE]] — How neurons report their state

**Status:** ACTIVE LAW  
**Enforced by:** All AI collaborators  
**Violations:** Rewrite until compliant

---

*A brain is only as smart as its neurons are robust.* 🧠⚡
