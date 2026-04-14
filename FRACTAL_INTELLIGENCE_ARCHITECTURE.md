# Fractal Intelligence Architecture

> **"Every neuron contains a brain. Every brain is composed of neurons. Intelligence is recursive."**
>
> — Meta-Architectural Principle

---

## The Core Insight

Traditional systems are **hierarchical**: Brain commands, neurons obey.

Your systems are **fractal**: Every neuron has local intelligence. The global brain emerges from their interaction. The brain improves neurons. Neurons improve the brain. **Intelligence flows in all directions.**

```
┌─────────────────────────────────────────┐
│      GLOBAL BRAIN (Performance Oracle)  │
│  ┌─────────────────────────────────┐    │
│  │  Neuron 1: Meme Sniper          │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │  Local Brain:           │    │    │
│  │  │  - Self-tuning scores   │    │    │
│  │  │  - Local pattern rec    │    │    │
│  │  │  - Auto-prune wallets   │    │    │
│  │  └─────────────────────────┘    │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │  Neuron 2: Ferrari EA           │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │  Local Brain:           │    │    │
│  │  │  - Online regime adapt  │    │    │
│  │  │  - Position sizing ML   │    │    │
│  │  │  - Entry timing opt     │    │    │
│  │  └─────────────────────────┘    │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │  META-BRAIN: Self-Architecture  │    │
│  │  (Improves the Oracle itself)   │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

---

## Layer 0: The Recursive Stack

### Level 3: Global Brain (Performance Oracle)
- **Scope:** Cross-neuron intelligence
- **Learns:** Which neurons win in which regimes
- **Adapts:** Capital allocation, neuron birth/death decisions
- **Meta-function:** Improves its own architecture (Level 3→Level 3)

### Level 2: Local Brains (Inside Each Neuron)
- **Scope:** Single-neuron optimization
- **Learns:** Parameter tuning, local patterns, self-health
- **Adapts:** Internal algorithms without global coordination
- **Meta-function:** Reports insights upward, suggests global improvements

### Level 1: Micro-Intelligence (Sub-components)
- **Scope:** Function-level adaptation
- **Example:** Self-tuning thresholds, dynamic slippage models
- **Learns:** Local data distributions, latency patterns

### Level 0: Raw Execution
- **Scope:** Stateless, pure execution
- **Example:** Math operations, I/O, logging

---

## The Three Recursion Patterns

### Pattern 1: Bottom-Up Insight Flow
```
Micro-Intelligence detects pattern
    ↓
Local Brain validates and generalizes
    ↓
Global Brain integrates across neurons
    ↓
Architecture evolves to capture new dimension
```

**Example:**
1. Meme Sniper's micro-layer detects "whale buys cluster at 2-4am UTC"
2. Local Brain validates: 73% of winning signals occur in this window
3. Global Brain notices: Other neurons also perform better 2-4am (lower volatility?)
4. Architecture evolves: Add `market_session` dimension to all neurons

---

### Pattern 2: Top-Down Adaptation Flow
```
Global Brain detects regime shift
    ↓
Local Brains receive new allocation/parameters
    ↓
Micro-layers adjust execution tactics
    ↓
Performance feeds back up
```

**Example:**
1. Global Brain detects: High-vol regime starting (HMM confidence 0.89)
2. Meme Sniper Local Brain receives: Increase allocation +20%, lower score threshold
3. Micro-layer adjusts: Tighter stops, faster exits
4. Results feed back: P&L improves, validates adaptation

---

### Pattern 3: Self-Referential Evolution
```
Global Brain evaluates its own performance
    ↓
Detects its allocator is too slow to adapt
    ↓
Proposes architectural change: Add momentum to Kelly weights
    ↓
Implements, tests, validates
    ↓
New allocator performance feeds back
```

**The brain improves its own wiring.**

---

## Local Brain Specification (Inside Every Neuron)

Every neuron you build must contain a `local_brain/` module:

```
neuron/
├── local_brain/
│   ├── __init__.py
│   ├── self_tuner.py          # Parameter optimization
│   ├── pattern_detector.py    # Local anomaly/pattern detection
│   ├── health_monitor.py      # Self-diagnostics
│   └── meta_reporter.py       # Insights to Global Brain
├── core/                      # Main execution logic
├── data/                      # Local SQLite
└── obsidian/                  # Local reports
```

### 1. Self-Tuner
Optimizes neuron-specific parameters without global coordination:

```python
class LocalSelfTuner:
    """Each neuron tunes its own knobs."""
    
    def __init__(self, neuron_id, param_space):
        self.neuron_id = neuron_id
        self.params = param_space  # e.g., score_threshold, stop_pct
        
    def online_update(self, recent_trades):
        """Bayesian update of parameters based on last N trades."""
        for param in self.params:
            # Test: current vs +5% vs -5%
            candidates = [
                self.params[param],
                self.params[param] * 1.05,
                self.params[param] * 0.95
            ]
            best = self.evaluate_candidates(candidates, recent_trades)
            self.params[param] = best
            
        self.log_tuning_decision()
```

**Example:** Meme Sniper's Local Brain notices score threshold 60 misses early pumps. Tests 55, 50. Finds 52 captures +15% more profit. Auto-adjusts. Reports to Global: *"Lower threshold improved early capture"*

---

### 2. Pattern Detector
Finds local patterns invisible to Global Brain:

```python
class LocalPatternDetector:
    """Detects neuron-specific anomalies."""
    
    def detect(self, data_stream):
        patterns = []
        
        # Pattern: API latency spikes before market moves
        if self.detect_latency_pattern(data_stream):
            patterns.append({
                'type': 'leading_indicator',
                'description': 'Helius latency spikes 30s before price volatility',
                'confidence': 0.73,
                'action': 'Use latency as early warning signal'
            })
        
        # Pattern: Specific wallet only wins on weekdays
        if self.detect_temporal_bias(data_stream):
            patterns.append({
                'type': 'temporal_bias',
                'description': 'Whale_XYZ has 0% win rate weekends, 65% weekdays',
                'confidence': 0.89,
                'action': 'Downweight Whale_XYZ Friday 5pm - Sunday 5pm'
            })
        
        return patterns
```

**Key:** Patterns too granular for Global Brain to detect, but actionable locally.

---

### 3. Health Monitor
Self-diagnostics that prevent neuron death:

```python
class LocalHealthMonitor:
    """Neuron checks its own vital signs."""
    
    def check(self):
        vitals = {
            'cycle_time': self.measure_cycle_time(),
            'error_rate': self.calculate_error_rate(),
            'data_freshness': self.check_data_age(),
            'memory_usage': self.get_memory_usage(),
            'api_quota': self.check_api_limits()
        }
        
        # Self-healing actions
        if vitals['error_rate'] > 0.05:
            self.enter_degraded_mode()
            self.schedule_restart()
            
        if vitals['api_quota'] < 100:
            self.reduce_poll_frequency()
            
        return vitals
```

---

### 4. Meta-Reporter
Reports insights upward to Global Brain:

```python
class MetaReporter:
    """Neuron tells Global Brain what it learned."""
    
    def generate_insight_report(self):
        return {
            'neuron_id': self.neuron_id,
            'timestamp': now(),
            'local_discoveries': [
                {
                    'type': 'parameter_optimization',
                    'finding': 'score_threshold 52 beats 60 by +15% P&L',
                    'confidence': 0.81,
                    'sample_size': 47
                },
                {
                    'type': 'environmental_change',
                    'finding': 'DexScreener API latency increased 300% since April 1',
                    'confidence': 0.99,
                    'recommendation': 'Add timeout handling, consider fallback to Pump.fun'
                }
            ],
            'suggested_global_changes': [
                'Consider session-based allocation (neurons perform differently 2-4am)',
                'Global timeout policy should increase from 5s to 15s'
            ]
        }
```

---

## Global Brain: The Meta-Architecture Engine

The Global Brain has a special module: `meta_architecture/` that improves the Oracle itself.

### Components:

#### 1. Architecture Smell Detector
```python
class ArchitectureSmellDetector:
    """Detects when Oracle's own design is insufficient."""
    
    SMELLS = {
        'SCHEMA_INSUFFICIENT': 'Gap detected but no column to store root cause',
        'ALLOCATOR_LAG': 'Kelly weights change >20% daily (too volatile)',
        'BLIND_SPOT': 'All neurons underperform in condition X but X not tracked',
        'CORRELATION_BLINDNESS': 'High correlation detected but no penalty applied',
        'TEMPORAL_MYOPA': 'Oracle only looks back 30 days, missing cyclical patterns'
    }
    
    def detect(self):
        smells = []
        
        # Check: Are we detecting gaps we can't categorize?
        uncategorized_gaps = self.find_gaps_without_classification()
        if len(uncategorized_gaps) > 3:
            smells.append({
                'type': 'SCHEMA_INSUFFICIENT',
                'severity': 'HIGH',
                'evidence': uncategorized_gaps,
                'proposed_fix': 'Add gap_taxonomy table with sub-categories'
            })
        
        # Check: Is allocator too jittery?
        allocation_variance = self.calculate_allocation_variance(days=7)
        if allocation_variance > 0.20:
            smells.append({
                'type': 'ALLOCATOR_LAG',
                'severity': 'MEDIUM',
                'evidence': f'Variance: {allocation_variance}',
                'proposed_fix': 'Add smoothing factor or Bayesian prior'
            })
        
        return smells
```

---

#### 2. Self-Modification Proposer
```python
class SelfModificationProposer:
    """Proposes changes to Oracle's own code/schema."""
    
    def propose_schema_evolution(self, smell):
        if smell['type'] == 'SCHEMA_INSUFFICIENT':
            return {
                'proposal_id': 'ARCH-001',
                'type': 'schema_migration',
                'motivation': smell['evidence'],
                'sql_changes': [
                    'ALTER TABLE oracle_context ADD COLUMN session TEXT;',
                    'ALTER TABLE oracle_context ADD COLUMN day_of_week INTEGER;',
                    'CREATE INDEX idx_session_regime ON oracle_context(session, regime);'
                ],
                'code_changes': [
                    'core/regime_mapper.py: Add session dimension to skill calculation',
                    'core/ingestion/hmm_detector.py: Extract session from timestamp'
                ],
                'expected_benefit': 'Enable session-aware allocation, estimated +0.15 Sharpe',
                'risk': 'Migration requires downtime, backup required',
                'rollback_plan': 'Restore from pre-migration backup'
            }
    
    def propose_algorithm_evolution(self, smell):
        if smell['type'] == 'ALLOCATOR_LAG':
            return {
                'proposal_id': 'ALG-001',
                'type': 'algorithm_update',
                'motivation': smell['evidence'],
                'current_code': 'allocation = raw_kelly / sum(raw_kelly)',
                'proposed_code': '''
                    # Add exponential smoothing
                    smoothed_kelly = 0.7 * raw_kelly + 0.3 * yesterday_allocation
                    allocation = smoothed_kelly / sum(smoothed_kelly)
                ''',
                'expected_benefit': 'Reduce allocation churn by ~60%',
                'test_strategy': 'Backtest on 90 days historical, compare turnover'
            }
```

---

#### 3. Self-Performance Evaluator
```python
class SelfPerformanceEvaluator:
    """Oracle evaluates its own allocation decisions."""
    
    def evaluate_allocator(self):
        """Did neurons with high allocation actually perform well?"""
        predictions = self.get_historical_allocations()
        outcomes = self.get_actual_performance()
        
        calibration_error = self.calculate_calibration(predictions, outcomes)
        
        if calibration_error > 0.15:
            return {
                'issue': 'ALLOCATOR_MISCALIBRATION',
                'finding': f'Calibration error: {calibration_error}',
                'diagnosis': 'Oracle overconfident in recent winners',
                'proposed_fix': 'Increase Bayesian prior strength, reduce recency bias'
            }
    
    def evaluate_gap_detector(self):
        """Did detected gaps lead to profitable neurons?"""
        historical_gaps = self.get_gap_history()
        filled_gaps = [g for g in historical_gaps if g['filled']]
        
        success_rate = len([g for g in filled_gaps if g['neuron_sharpe'] > 1.0]) / len(filled_gaps)
        
        if success_rate < 0.5:
            return {
                'issue': 'GAP_DETECTOR_PRECISION',
                'finding': f'Only {success_rate:.0%} of filled gaps produced good neurons',
                'diagnosis': 'Gap detector too permissive',
                'proposed_fix': 'Increase threshold for gap severity'
            }
```

---

## The Recursive Improvement Cycle

```
WEEK 1-2: Foundation
├── Global Brain ingests data from neurons with Local Brains
├── Local Brains self-tune parameters
└── Everything works, but static

WEEK 3-4: First Recursion
├── Meme Sniper Local Brain discovers: "2-4am UTC = best signals"
├── Reports to Global Brain
├── Global Brain notices: Other neurons also perform better 2-4am
├── Architecture Smell Detector: "Missing session dimension"
└── Self-Modification Proposer: "Add session to schema"

WEEK 5: Evolution
├── Schema migration executed
├── All neurons now report session context
├── Allocator updated: session-aware weights
└── Performance improves: +0.12 portfolio Sharpe

WEEK 6-8: Second Recursion
├── Global Brain evaluates: "Allocator less jittery now?"
├── Self-Performance Evaluator: "Still 25% daily variance"
├── Architecture Smell: "ALLOCATOR_LAG persists"
├── Algorithm Evolution: "Add smoothing"
└── Allocator improves: Churn down 40%

WEEK 9+: Continuous
├── Neurons improve locally
├── Global Brain improves cross-neuron intelligence
├── Meta-Architecture improves Global Brain itself
└── System becomes smarter in three dimensions simultaneously
```

---

## Implementation: The Recursive Stack

### For Every New Neuron (Local Brain Template)

```python
# Template: local_brain/core.py
class LocalBrain:
    """Every neuron has one."""
    
    def __init__(self, neuron_id):
        self.tuner = SelfTuner(neuron_id)
        self.patterns = PatternDetector()
        self.health = HealthMonitor()
        self.reporter = MetaReporter(neuron_id)
        
    def cycle(self, data):
        # 1. Self-tune
        self.tuner.online_update(data['recent_trades'])
        
        # 2. Detect local patterns
        patterns = self.patterns.detect(data['stream'])
        
        # 3. Health check
        vitals = self.health.check()
        
        # 4. Report up
        if patterns or vitals['status'] != 'healthy':
            self.reporter.send_to_global_brain(patterns, vitals)
        
        return {
            'params': self.tuner.params,
            'health': vitals,
            'patterns': patterns
        }
```

### For Global Brain (Meta-Architecture)

```python
# oracle/core/meta_architecture.py
class MetaArchitectureEngine:
    """The brain that improves the brain."""
    
    def __init__(self):
        self.smell_detector = ArchitectureSmellDetector()
        self.proposer = SelfModificationProposer()
        self.evaluator = SelfPerformanceEvaluator()
        
    def meta_cycle(self):
        # 1. Detect smells in own architecture
        smells = self.smell_detector.detect()
        
        # 2. Evaluate own performance
        perf_issues = self.evaluator.evaluate()
        
        # 3. Generate proposals
        all_issues = smells + perf_issues
        proposals = [self.proposer.propose_fix(i) for i in all_issues]
        
        # 4. Write to Obsidian for Bob/AI review
        self.write_proposals_to_obsidian(proposals)
        
        return proposals
```

---

## The Fractal Mandate

Add this to your constitution:

```
Every system must:
1. EXECUTE (Level 0) — Do its job
2. ADAPT (Level 1) — Tune internal parameters  
3. LEARN (Level 2) — Discover local patterns
4. COMMUNICATE (Level 3) — Share insights with Global Brain
5. EVOLVE (Global) — Contribute to architectural improvements

No neuron is too small for a Local Brain.
No Global Brain is too big for self-modification.
```

---

## Why This Changes Everything

| Traditional | Fractal Intelligence |
|-------------|---------------------|
| Static systems | Self-evolving ecosystem |
| Top-down commands | Bidirectional insight flow |
| Manual optimization | Continuous self-tuning |
| Fixed architecture | Schema evolves with data |
| Brittle failures | Graceful degradation + adaptation |
| You maintain everything | Systems maintain themselves |

**You are not building tools. You are bootstrapping a synthetic organism that gets smarter faster than the market changes.**

---

## Next Step

Give Kimi Code this addition:

```
## ADDITION TO PERFORMANCE ORACLE SPEC

### Local Brain Module

Every neuron must have a `local_brain/` directory with:
1. Self-tuner (Bayesian parameter optimization)
2. Pattern detector (local anomalies)
3. Health monitor (self-diagnostics)
4. Meta-reporter (insights to Global Brain)

### Meta-Architecture Module

Global Brain must have `core/meta_architecture/`:
1. ArchitectureSmellDetector — finds limitations in Oracle's own design
2. SelfModificationProposer — suggests schema/code improvements
3. SelfPerformanceEvaluator — checks if Oracle's allocations were correct

### The Recursive Rule

Implement the cycle: Neurons improve locally → report up → Global Brain integrates → detects architectural gaps → proposes self-modification → evolves schema → neurons benefit from new capabilities → repeat.

This is the compounding of compounding.
```

**Ready to make this canon?** 🧠⚡🔄
