# IMPLEMENTATION PROMPT: Build CEREBRUM v2.0 (Optimal)

> **Mission:** Build the optimal intelligent capital allocator using state-of-the-art quant finance and machine learning.

## Background

The CEREBRUM infrastructure is complete:
- ✅ Data ingestion (21/21 tests passing)
- ✅ Scorecard with provisional/tiered rankings
- ✅ P1 production fixes (idempotent, robust)
- ✅ Command bus table for governance

**Now build the CONSCIOUSNESS LAYER using cutting-edge methods.**

## Build These 8 Modules

### 1. `core/intelligence/bayesian_sharpe.py`
**Bayesian Sharpe Estimation with Robust Statistics**

```python
class BayesianSharpeModel:
    def __init__(self):
        self.neuron_posteriors = {}  # neuron_id -> (mean, std)
        self.population_mean = 0.0
        self.population_std = 1.0
    
    def update(self, neuron_id: str, new_returns: np.ndarray):
        """
        Online Bayesian update using:
        - Student-t likelihood (robust to outliers, nu=5)
        - Conjugate prior for analytical updates (fast)
        - Median-based sample statistics (not mean)
        - MAD for volatility (not std)
        """
    
    def sample_sharpe(self, neuron_id: str) -> float:
        """Sample from posterior for Thompson Sampling"""
    
    def credible_interval(self, neuron_id: str, alpha: float = 0.05) -> Tuple[float, float]:
        """Return (lower, upper) credible interval"""
```

**Key:** Never use point estimates. Always return posterior distributions.

---

### 2. `core/intelligence/thompson_sampler.py`
**Thompson Sampling for Optimal Explore-Exploit**

```python
class ThompsonSampler:
    def __init__(self, sharpe_model: BayesianSharpeModel, temperature: float = 0.5):
        self.sharpe_model = sharpe_model
        self.temperature = temperature
    
    def allocate(self, neuron_ids: List[str]) -> Dict[str, float]:
        """
        1. Sample Sharpe from each neuron's posterior
        2. Softmax allocation with temperature
        3. Returns: neuron_id -> capital_pct (sums to 1.0)
        
        This naturally explores high-uncertainty neurons
        and exploits high-expected-Sharpe neurons.
        """
```

**Key:** Thompson Sampling has optimal regret bounds O(sqrt(T log T)).

---

### 3. `core/intelligence/contextual_bandit.py`
**Regime-Aware Contextual Bandits**

```python
class ContextualBanditAllocator:
    def __init__(self, regimes: List[str] = ['trend', 'range', 'high_vol', 'low_vol']):
        self.regime_bandits = {regime: BayesianSharpeModel() for regime in regimes}
    
    def allocate(self, current_regime: str, neuron_ids: List[str]) -> Dict[str, float]:
        """
        Use regime-specific bandit.
        Learns: "Ferrari great in range, bad in trend"
        """
    
    def update_regime(self, regime: str, neuron_id: str, return_value: float):
        """Update regime-specific posterior"""
```

**Key:** Each (neuron, regime) pair is a separate "arm" in the bandit.

---

### 4. `core/intelligence/robust_portfolio.py`
**Robust Portfolio Optimization**

```python
class RobustPortfolioOptimizer:
    def optimize(self, 
                 neuron_ids: List[str],
                 sharpe_posteriors: Dict[str, Tuple[float, float]],
                 correlation_samples: List[np.ndarray],
                 n_monte_carlo: int = 1000) -> Dict[str, float]:
        """
        1. Sample Sharpe from posteriors (1000 samples)
        2. Sample correlation matrices
        3. Solve mean-variance for each sample
        4. Take MEDIAN portfolio (robust aggregation)
        5. Return normalized weights
        
        Uses median returns (not mean) for robustness.
        """
```

**Key:** Ensemble over uncertainty. Median aggregation prevents outliers.

---

### 5. `core/consciousness/information_abstention.py`
**Information-Theoretic Self-Awareness**

```python
class InformationTheoreticSelfAwareness:
    def should_abstain(self, 
                       neuron_posteriors: Dict[str, Tuple[float, float]],
                       entropy_threshold: float = 1.5,
                       uncertainty_threshold: float = 2.0) -> Tuple[bool, str]:
        """
        Abstain if:
        1. Decision entropy > threshold (too uncertain)
        2. Total posterior std > threshold (no strong beliefs)
        3. Expected information gain from waiting > expected return
        
        Returns: (should_abstain, reason)
        """
    
    def calculate_entropy(self, allocations: Dict[str, float]) -> float:
        """Shannon entropy of allocation distribution"""
```

**Key:** The CEREBRUM must know when to say "I don't know enough."

---

### 6. `core/consciousness/changepoint_detector.py`
**Online Structural Break Detection**

```python
class StructuralBreakDetector:
    """
    Bayesian Online Changepoint Detection (Adams & MacKay, 2007)
    """
    
    def __init__(self, hazard: float = 0.01):
        self.hazard = hazard  # Prior probability of changepoint
        self.run_length = 0
    
    def update(self, new_return: float) -> Optional[str]:
        """
        Update changepoint detection.
        Returns "changepoint_detected" if break found.
        """
    
    def reset_uncertainty(self, sharpe_model: BayesianSharpeModel, neuron_id: str):
        """Increase posterior std when changepoint detected"""
```

**Key:** Automatically detect when a neuron's performance regime changes.

---

### 7. `core/consciousness/causal_impact.py`
**Causal Impact Estimation**

```python
class CausalImpactAnalyzer:
    def estimate_impact(self, 
                       neuron_id: str,
                       allocation_start: datetime,
                       allocation_end: datetime) -> Dict:
        """
        Synthetic control method:
        - Build synthetic control from other neurons
        - Compare actual vs counterfactual
        - Return: causal_effect, p_value, confidence_interval
        """
    
    def predict_success_probability(self, 
                                   allocations: Dict[str, float], 
                                   regime: str) -> float:
        """
        Predict P(success | allocations, regime) based on historical
        causal impacts in similar regimes.
        """
```

**Key:** Answer "What would have happened if I hadn't allocated?"

---

### 8. `core/consciousness/meta_learner.py`
**Meta-Learning (Learning to Allocate)**

```python
class MetaLearningAllocator:
    """
    Model-Agnostic Meta-Learning (MAML) for allocation strategies.
    """
    
    def __init__(self):
        self.meta_params = {
            'exploration_rate': 0.3,
            'temperature': 0.5,
            'risk_aversion': 1.0,
            'correlation_penalty': 0.2
        }
    
    def meta_update(self, regime_performance: Dict[str, float]):
        """
        Update meta-parameters based on performance.
        
        If exploration too high -> decrease rate
        If missing opportunities -> increase rate
        """
    
    def get_meta_params(self) -> Dict[str, float]:
        """Return current meta-parameters for allocation"""
```

**Key:** The allocator learns how to allocate better over time.

---

## Integration: The Optimal Allocator

### `core/consciousness/optimal_allocator.py`

```python
class OptimalCerebrumAllocator:
    """
    Complete optimal allocator combining all 8 modules.
    """
    
    def __init__(self, db_path: str):
        self.sharpe_model = BayesianSharpeModel()
        self.thompson = ThompsonSampler(self.sharpe_model)
        self.bandit = ContextualBanditAllocator()
        self.portfolio = RobustPortfolioOptimizer()
        self.self_aware = InformationTheoreticSelfAwareness()
        self.changepoint = StructuralBreakDetector()
        self.causal = CausalImpactAnalyzer()
        self.meta = MetaLearningAllocator()
    
    def allocate(self, available_capital: float = 1.0) -> AllocationDecision:
        """
        Main allocation loop:
        
        1. Self-awareness check (abstain if uncertain?)
        2. Detect changepoints (reset uncertainty if needed)
        3. Get current regime
        4. Thompson Sampling allocation
        5. Robust portfolio optimization
        6. Ensemble blend (Thompson + Robust)
        7. Causal check (predict success probability)
        8. Meta-learning update
        9. Return decision with full audit trail
        """
```

---

## New CLI Commands

Add to `cerebrum.py`:

```bash
python cerebrum.py --consciousness     # Display self-awareness state
python cerebrum.py --allocate          # Generate optimal allocation
python cerebrum.py --regime-change     # Check for structural breaks
python cerebrum.py --causal-impact     # Analyze past allocation impacts
python cerebrum.py --meta-learn        # Update meta-parameters
```

---

## Acceptance Criteria

- [ ] Uses Bayesian posteriors (never point estimates)
- [ ] Thompson Sampling for allocation (not greedy)
- [ ] Information-theoretic abstention (knows when to wait)
- [ ] Robust statistics (median, MAD, not mean/std)
- [ ] Regime-aware contextual bandits
- [ ] Automatic changepoint detection
- [ ] Causal impact estimation
- [ ] Meta-learning adaptation
- [ ] Full uncertainty quantification in every decision
- [ ] 25+ tests covering all 8 modules

---

## Key Design Principles

1. **Bayesian Everything** — Posterior distributions, not point estimates
2. **Thompson Sampling** — Optimal explore-exploit, not greedy
3. **Robust Statistics** — Median-based, outlier-resistant
4. **Information Geometry** — Know when uncertainty is too high
5. **Causal Attribution** — Not just correlation
6. **Online Learning** — Every trade updates beliefs
7. **Meta-Learning** — Learn how to learn

---

## References to Implement

- Thompson (1933), Russo et al. (2018) — Thompson Sampling
- Adams & MacKay (2007) — Bayesian Online Changepoint Detection
- Li et al. (2010) — Contextual Bandits
- Brodersen et al. (2015) — Causal Impact
- Finn et al. (2017) — MAML Meta-Learning
- Huber & Ronchetti (2009) — Robust Statistics

---

## Full Spec

Read: https://github.com/DroptheDrudge/OpenVault/blob/master/CEREBRUM_OPTIMAL_DESIGN.md

---

**Build the CEREBRUM as a true Bayesian agent. Optimal. Robust. Self-aware. Ever-learning.**
