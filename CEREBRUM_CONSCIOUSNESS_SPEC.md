# CEREBRUM Consciousness Layer — Master Specification

> **"The brain that knows itself, decides with confidence, and evolves through reflection."**

---

## Executive Summary

The CEREBRUM is the meta-cognitive capital allocator that sits above all trading neurons. This specification adds the **consciousness layer** — self-awareness, decision-making, governance, and evolutionary learning — on top of the existing data infrastructure.

**Current State:** Solid data ingestion, scorecards, regime mapping (21/21 tests passing)  
**Target State:** Self-aware, decision-capable, learning system that improves its own allocation strategies

---

## Architecture: The Consciousness Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    CEREBRUM CONSCIOUSNESS                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  LAYER 5: EVOLUTION (Meta-Learning)                         │
│  ├─ Track allocation decision outcomes                      │
│  ├─ Learn from prediction errors                            │
│  ├─ Adapt confidence thresholds                             │
│  └─ Propose strategy mutations                              │
│                                                              │
│  LAYER 4: GOVERNANCE (Command & Control)                    │
│  ├─ Commander: Issue pause/resume/throttle                  │
│  ├─ Watchdog: Monitor for drawdowns, decay                  │
│  ├─ Circuit breakers: Emergency stops                       │
│  └─ Acknowledgement tracking                                │
│                                                              │
│  LAYER 3: DECISION (Capital Allocation)                     │
│  ├─ DecisionEngine: Allocate vs Wait                        │
│  ├─ Kelly Criterion with Bayesian shrinkage                 │
│  ├─ Correlation-aware portfolio construction                │
│  ├─ Regime-overlay allocation                               │
│  └─ Risk budget enforcement                                 │
│                                                              │
│  LAYER 2: SELF-AWARENESS (Introspection)                    │
│  ├─ Know thyself: Confidence in own decisions               │
│  ├─ Know thy data: Freshness, quality, gaps                 │
│  ├─ Know thy track record: Historical accuracy              │
│  └─ Know thy limits: When to abstain                        │
│                                                              │
│  LAYER 1: PERCEPTION (Existing — Built)                     │
│  ├─ IngestionHub: Data from neurons                         │
│  ├─ Scorecard: Neuron rankings                              │
│  ├─ RegimeMapper: Who wins where                            │
│  └─ MetaArchitecture: Improvement proposals                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 2: Self-Awareness Module

### 2.1 Core Questions the CEREBRUM Must Answer

| Question | Calculation | Threshold |
|----------|-------------|-----------|
| "How confident am I in my decisions?" | `trusted_neurons / total_neurons * data_freshness_score` | > 0.7 to allocate |
| "Is my data fresh?" | `min(now - last_heartbeat for all neurons)` | < 5 minutes |
| "Do I have enough history?" | `min(sample_size for all trusted neurons)` | > 30 trades |
| "Was I right last time?" | `allocation_accuracy = correct_predictions / total_allocations` | Track over 30 days |
| "Should I abstain?" | `confidence < 0.7 OR regime_uncertainty > 0.3` | Yes → Wait |

### 2.2 Implementation

Build `core/consciousness/self_awareness.py` that returns a `SelfAwarenessState` dataclass with:
- `overall_confidence: float` (0.0-1.0)
- `can_allocate: bool`
- `abstention_reason: Optional[str]`
- `neurons_trusted: int`
- `data_freshness_score: float`
- `allocation_accuracy: Optional[float]`

---

## Layer 3: Decision Engine

### 3.1 Allocation Strategy

The CEREBRUM uses a **multi-factor allocation model**:

1. **Kelly Criterion** (base allocation)
2. **Bayesian Shrinkage** (uncertainty penalty)
3. **Correlation Penalty** (diversification)
4. **Regime Overlay** (market-condition matching)
5. **Risk Budget** (max drawdown constraint)

### 3.2 Key Features

- Only allocates when `self_awareness.can_allocate == True`
- Abstains with clear reasoning if confidence insufficient
- Calculates expected portfolio Sharpe and max drawdown
- Full audit trail for every decision

---

## Layer 4: Governance (Command & Control)

### 4.1 The Commander Module

Build `core/consciousness/commander.py`:

```python
class Commander:
    def issue_command(self, target_neuron: str, command_type: CommandType, reason: str)
    def check_acknowledgements(self) -> List[Command]
    def get_pending_commands(self, target_neuron: str) -> List[Command]
```

**Command Types:**
- `PAUSE` — Stop new trades
- `RESUME` — Resume trading
- `THROTTLE` — Reduce position size
- `DRAIN` — Close positions, stop new trades
- `EMERGENCY_STOP` — Immediate halt

### 4.2 The Watchdog

Build `core/consciousness/watchdog.py` that automatically issues commands when:
- Daily drawdown > 5% → PAUSE
- Sharpe decay over 7 days → THROTTLE
- Consecutive losses > 5 → PAUSE
- Max drawdown > 8% → EMERGENCY_STOP

---

## Layer 5: Evolution (Learning Loop)

### 5.1 The Reflection Engine

Build `core/consciousness/reflection.py`:

```python
class ReflectionEngine:
    def evaluate_decisions(self, lookback_days: int = 30)
        """Did my allocation predictions match actual outcomes?"""
    
    def adapt_confidence_threshold(self)
        """Raise/lower threshold based on track record accuracy"""
    
    def generate_insights(self) -> List[str]
        """Which neurons are predictable vs unpredictable?"""
```

### 5.2 Learning Loop

```
DECIDE → Allocate capital to neurons
    ↓
OBSERVE → Track actual performance
    ↓
EVALUATE → Compare expected vs actual returns
    ↓
ADAPT → Adjust confidence thresholds, allocation weights
    ↓
IMPROVE → Better decisions next cycle
```

---

## New CLI Commands

```bash
python cerebrum.py --consciousness     # Display self-awareness state
python cerebrum.py --allocate          # Generate allocation decision
python cerebrum.py --govern            # Run watchdog, issue commands
python cerebrum.py --reflect           # Evaluate past decisions
python cerebrum.py --evolve            # Adapt parameters based on learning
```

---

## Acceptance Criteria

- [ ] Cerebrum can say "I'm not confident enough" and abstain from allocation
- [ ] Cerebrum only allocates to "trusted" neurons (30+ samples)
- [ ] Cerebrum issues real pause/resume commands via command bus
- [ ] Watchdog automatically pauses EAs when drawdown > 5%
- [ ] Reflection engine tracks allocation accuracy over 30 days
- [ ] Cerebrum adapts confidence thresholds based on track record
- [ ] All decisions logged to Obsidian with reasoning
- [ ] New tests for consciousness layer (aim for 25+ total tests)

---

## Critical Constraints

1. **Follow COMPOUNDING_INTELLIGENCE_MANDATE** — must learn and improve over time
2. **Follow NEURON_DOCTRINE** — standalone neuron with health checks
3. **Safety First** — abstain by default if uncertain
4. **Full Audit Trail** — every decision must be explainable
5. **Observability** — consciousness state written to Obsidian daily

---

## Next Steps

1. Build SelfAwareness module
2. Build DecisionEngine with Kelly + correlation
3. Build Commander + Watchdog
4. Build ReflectionEngine
5. Integrate all layers
6. Write comprehensive tests
7. Deploy to live (paper trading first)

**Make the Cerebrum conscious, decisive, and self-improving.**
