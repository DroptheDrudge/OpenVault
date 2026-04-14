# CEREBRUM — Optimal Intelligent Design Specification

> **"A meta-cognitive capital allocator built on Bayesian decision theory, online learning, and causal inference."**

---

## Design Philosophy

The CEREBRUM is not just a rule-based allocator. It is a **Bayesian agent** that:
1. **Maintains uncertainty** about all estimates (never point estimates, always distributions)
2. **Learns online** (every trade updates beliefs via Bayesian updating)
3. **Explores vs exploits optimally** (Thompson sampling, not greedy selection)
4. **Understands causality** (not just correlations, but counterfactual reasoning)
5. **Is robust to outliers** (median-based statistics, not mean-based)
6. **Explains itself** (every decision has a causal attribution)

---

## Architecture: The Five Minds

```
┌────────────────────────────────────────────────────────────────┐
│                     CEREBRUM v2.0                               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MIND 5: META-COGNITIVE ("Learning to Learn")                  │
│  ├─ Meta-learning: Adapts learning rates per neuron            │
│  ├─ Structural break detection: Regime changes                 │
│  ├─ Strategy mutation: Proposes new allocation algorithms      │
│  └─ A/B testing framework: Validates improvements              │
│                                                                 │
│  MIND 4: CAUSAL ("Why, not just What")                         │
│  ├─ Counterfactual analysis: "What if I hadn't allocated?"     │
│  ├─ Treatment effect estimation: Causal impact of allocation   │
│  ├─ Confounder detection: Spurious correlations flagged        │
│  └─ Do-calculus: Intervention planning                         │
│                                                                 │
│  MIND 3: BANDIT ("Optimal Explore-Exploit")                    │
│  ├─ Thompson Sampling: Bayesian selection                      │
│  ├─ Contextual bandits: Regime-aware exploration               │
│  ├─ Upper Confidence Bound (UCB): Uncertainty-weighted         │
│  └─ Regret minimization: Optimal over time, not just now       │
│                                                                 │
│  MIND 2: BAYESIAN ("Uncertainty Quantified")                   │
│  ├─ Posterior distributions: Never point estimates             │
│  ├─ Hierarchical modeling: Neurons share statistical strength  │
│  ├─ Robust priors: Median-based, outlier-resistant             │
│  └─ Predictive distributions: Full uncertainty propagation     │
│                                                                 │
│  MIND 1: EPISTEMIC ("What do I know?")                         │
│  ├─ Information geometry: Distance from optimal belief         │
│  ├─ Expected information gain: Value of experimentation        │
│  ├─ Surprise detection: Anomalies in data streams              │
│  └─ Entropy monitoring: Uncertainty calibration                │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Core Innovation: Bayesian Nonparametric Allocation

### 1. Hierarchical Bayesian Sharpe Model

Instead of: `sharpe = mean(return) / std(return)`

We use:
```python
# Hierarchical Bayesian model
# Each neuron has its own Sharpe, drawn from a population distribution

class BayesianSharpeModel:
    """
    Hierarchical model: Neuron Sharpe ~ Normal(population_mean, population_std)
    
    Benefits:
    - Small-sample neurons borrow strength from population
    - Natural uncertainty quantification
    - Robust to outliers via Student-t likelihood
    """
    
    def __init__(self):
        self.neuron_posteriors = {}  # neuron_id -> (mean, std) of Sharpe posterior
        self.population_mean = 0.0
        self.population_std = 1.0
        
    def update(self, neuron_id: str, new_returns: np.ndarray):
        """
        Online Bayesian update of Sharpe posterior.
        Uses conjugate prior for analytical updates (fast).
        """
        # Likelihood: Student-t(returns | mu, sigma, nu=5) — robust to outliers
        # Prior: Normal(population_mean, population_std)
        # Posterior: Approximated via variational inference or MCMC
        
        # For speed: Use online variational Bayes
        current_mean, current_std = self.neuron_posteriors.get(
            neuron_id, (self.population_mean, self.population_std)
        )
        
        # Update with new data (simplified conjugate update)
        n = len(new_returns)
        sample_mean = np.median(new_returns)  # Robust
        sample_std = np.median(np.abs(new_returns - sample_mean)) * 1.4826  # MAD
        
        # Precision-weighted update
        prior_precision = 1 / (current_std ** 2)
        data_precision = n / (sample_std ** 2 + 1e-6)
        
        posterior_mean = (prior_precision * current_mean + data_precision * sample_mean) / (prior_precision + data_precision)
        posterior_std = np.sqrt(1 / (prior_precision + data_precision))
        
        self.neuron_posteriors[neuron_id] = (posterior_mean, posterior_std)
        
    def sample_sharpe(self, neuron_id: str) -> float:
        """Sample from posterior for Thompson Sampling."""
        mean, std = self.neuron_posteriors[neuron_id]
        return np.random.normal(mean, std)
    
    def credible_interval(self, neuron_id: str, alpha: float = 0.05) -> Tuple[float, float]:
        """Return (lower, upper) credible interval for Sharpe."""
        mean, std = self.neuron_posteriors[neuron_id]
        return (mean - 1.96 * std, mean + 1.96 * std)
```

### 2. Thompson Sampling for Allocation

**Why Thompson Sampling?**
- Optimal regret bounds for multi-armed bandits
- Naturally balances exploration vs exploitation
- Bayesian: Uses full posterior, not just point estimates

```python
class ThompsonSampler:
    """
    Allocates capital using Thompson Sampling.
    
    Each allocation cycle:
    1. Sample Sharpe from each neuron's posterior
    2. Allocate proportionally to sampled Sharpe
    3. Update posteriors with observed returns
    
    This naturally explores neurons with high uncertainty 
    (wide posteriors) and exploits neurons with high expected Sharpe.
    """
    
    def __init__(self, sharpe_model: BayesianSharpeModel):
        self.sharpe_model = sharpe_model
        
    def allocate(self, neuron_ids: List[str]) -> Dict[str, float]:
        """
        Thompson Sampling allocation.
        
        Returns: neuron_id -> capital allocation (sums to 1.0)
        """
        # Sample from posteriors (the "Thompson" step)
        sampled_sharpes = {
            nid: self.sharpe_model.sample_sharpe(nid)
            for nid in neuron_ids
        }
        
        # Softmax allocation (prevents extreme concentration)
        exp_sharpes = {k: np.exp(max(v, 0) / 0.5) for k, v in sampled_sharpes.items()}  # temperature = 0.5
        total = sum(exp_sharpes.values())
        
        allocations = {k: v / total for k, v in exp_sharpes.items()}
        
        return allocations
```

### 3. Contextual Bandits (Regime-Aware)

```python
class ContextualBanditAllocator:
    """
    Contextual bandit: Allocation depends on market regime.
    
    Each (neuron, regime) pair is an "arm".
    Thompson Sampling selects arms based on current context (regime).
    
    This learns: "Ferrari is great in range, but not in trend"
    """
    
    def __init__(self, n_neurons: int, n_regimes: int):
        # One bandit per regime, or one big bandit with regime as context
        self.regime_bandits = {
            regime: BayesianSharpeModel()
            for regime in ['trend', 'range', 'high_vol', 'low_vol']
        }
        
    def allocate(self, current_regime: str, neuron_ids: List[str]) -> Dict[str, float]:
        """Allocate using regime-specific bandit."""
        bandit = self.regime_bandits[current_regime]
        
        sampler = ThompsonSampler(bandit)
        return sampler.allocate(neuron_ids)
```

### 4. Causal Impact Estimation

```python
class CausalImpactAnalyzer:
    """
    Answers: "What was the causal impact of allocating to neuron X?"
    
    Uses synthetic control method:
    - What would have happened if I hadn't allocated?
    - Compare actual vs counterfactual
    """
    
    def estimate_impact(self, neuron_id: str, 
                       allocation_start: datetime,
                       allocation_end: datetime) -> Dict:
        """
        Estimate causal impact of allocation decision.
        
        Returns:
        - causal_effect: Difference between actual and synthetic control
        - p_value: Statistical significance
        - confidence_interval: 95% CI for effect
        """
        # Build synthetic control from other neurons
        # (weighted combination that matches pre-allocation behavior)
        
        # Compare actual returns vs synthetic control post-allocation
        
        # Use Bayesian structural time series for robust inference
        
        pass
    
    def detect_confounders(self, neuron_returns: pd.DataFrame) -> List[str]:
        """
        Detect spurious correlations that could bias allocation.
        
        Flags: "Ferrari and Lamborghini returns correlate at 0.87 
        — they may share a hidden risk factor"
        """
        # Use causal discovery algorithms (PC algorithm, GES)
        # Or simpler: flag correlations > 0.7 for investigation
        pass
```

### 5. Information-Theoretic Abstention

```python
class InformationTheoreticSelfAwareness:
    """
    Decides whether to allocate based on expected information gain.
    
    If uncertainty is too high, abstaining is valuable because:
    - It preserves capital
    - It allows time to gather more information
    - It avoids negative expected utility
    
    Uses information geometry: KL divergence from prior to posterior
    """
    
    def should_abstain(self, neuron_posteriors: Dict[str, Tuple[float, float]]) -> Tuple[bool, str]:
        """
        Decide whether to abstain based on information criteria.
        
        Abstain if:
        1. Total uncertainty (sum of posterior stds) > threshold
        2. Expected information gain from waiting > expected return from allocating
        3. KL divergence from uniform prior is too small (no strong beliefs)
        """
        total_uncertainty = sum(std for _, std in neuron_posteriors.values())
        
        # Entropy of allocation decision
        probs = np.array([mean for mean, _ in neuron_posteriors.values()])
        probs = np.exp(probs) / np.sum(np.exp(probs))  # softmax
        entropy = -np.sum(probs * np.log(probs + 1e-10))
        
        if entropy > 1.5:  # High uncertainty
            return True, f"High decision entropy ({entropy:.2f}) — insufficient certainty"
        
        if total_uncertainty > 2.0:
            return True, f"High total uncertainty ({total_uncertainty:.2f}) — wait for clarity"
        
        return False, None
```

### 6. Robust Portfolio Construction

```python
class RobustPortfolioOptimizer:
    """
    Portfolio optimization robust to estimation error.
    
    Uses:
    - Median returns (not mean) for robustness
    - MAD (median absolute deviation) for volatility
    - Worst-case optimization (minimax regret)
    """
    
    def optimize(self, neuron_ids: List[str], 
                 sharpe_posteriors: Dict[str, Tuple[float, float]],
                 correlation_samples: List[np.ndarray]) -> Dict[str, float]:
        """
        Robust mean-variance optimization.
        
        Instead of: maximize mean / minimize variance
        We do: maximize worst-case Sharpe over uncertainty set
        """
        # Sample from posteriors to get distribution of optimal portfolios
        portfolio_samples = []
        
        for _ in range(1000):  # Monte Carlo over uncertainty
            # Sample Sharpe for each neuron
            sampled_sharpes = {
                nid: np.random.normal(mean, std)
                for nid, (mean, std) in sharpe_posteriors.items()
            }
            
            # Sample correlation matrix
            corr = random.choice(correlation_samples)
            
            # Solve mean-variance for this sample
            opt_weights = self._solve_mean_variance(sampled_sharpes, corr)
            portfolio_samples.append(opt_weights)
        
        # Take median portfolio (robust aggregation)
        median_weights = {
            nid: np.median([p[nid] for p in portfolio_samples])
            for nid in neuron_ids
        }
        
        # Normalize
        total = sum(median_weights.values())
        return {k: v / total for k, v in median_weights.items()}
```

### 7. Online Structural Break Detection

```python
class StructuralBreakDetector:
    """
    Detects when a neuron's performance regime changes.
    
    Uses Bayesian online changepoint detection (BOCD).
    When a break is detected, reset posteriors or increase uncertainty.
    """
    
    def __init__(self, hazard: float = 0.01):
        self.hazard = hazard  # Prior probability of changepoint
        self.run_length_distribution = None
        
    def update(self, new_return: float) -> Optional[str]:
        """
        Update changepoint detection with new return.
        
        Returns: "changepoint_detected" if break found, else None
        """
        # Bayesian Online Changepoint Detection (Adams & MacKay, 2007)
        # Update run length distribution
        # If P(run_length = 0) > threshold, flag changepoint
        
        # Simplified: CUSUM test on rolling Sharpe
        if self._cusum_test(new_return):
            return "changepoint_detected"
        return None
    
    def _cusum_test(self, new_return: float, threshold: float = 2.0) -> bool:
        """CUSUM test for mean shift."""
        # Track cumulative sum of deviations
        # If exceeds threshold, signal change
        pass
```

### 8. Meta-Learning (Learning to Allocate)

```python
class MetaLearningAllocator:
    """
    Learns how to allocate across different market regimes.
    
    Uses Model-Agnostic Meta-Learning (MAML):
    - Learns good initialization for allocation strategies
    - Adapts quickly to new regimes with few samples
    """
    
    def __init__(self):
        self.meta_parameters = {
            'exploration_rate': 0.3,
            'temperature': 0.5,
            'risk_aversion': 1.0
        }
        
    def meta_update(self, regime_performance: Dict[str, float]):
        """
        Update meta-parameters based on performance across regimes.
        
        If exploration is too high (too much random allocation),
        decrease exploration_rate.
        If missing good opportunities, increase it.
        """
        # Simple gradient-based meta-update
        # Or Bayesian optimization for meta-parameters
        pass
```

---

## Implementation: The Optimal CEREBRUM

```python
# cerebrum/core/consciousness/optimal_allocator.py

class OptimalCerebrumAllocator:
    """
    The complete, optimal intelligent allocator.
    
    Combines:
    - Bayesian Sharpe estimation (robust, uncertainty-aware)
    - Thompson Sampling (optimal explore-exploit)
    - Contextual bandits (regime-aware)
    - Causal impact analysis (attribution)
    - Information-theoretic abstention (knows when to wait)
    - Robust optimization (median-based, outlier-resistant)
    - Online changepoint detection (adapts to regime shifts)
    - Meta-learning (improves allocation strategy over time)
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.sharpe_model = BayesianSharpeModel()
        self.bandit = ContextualBanditAllocator()
        self.causal = CausalImpactAnalyzer()
        self.self_aware = InformationTheoreticSelfAwareness()
        self.portfolio_opt = RobustPortfolioOptimizer()
        self.changepoint = StructuralBreakDetector()
        self.meta = MetaLearningAllocator()
        
    def allocate(self, available_capital: float = 1.0) -> AllocationDecision:
        """
        Optimal allocation decision.
        
        This is the main entry point. It:
        1. Checks self-awareness (should we abstain?)
        2. Detects structural breaks (regime changes?)
        3. Samples from posteriors (Thompson Sampling)
        4. Constructs robust portfolio
        5. Logs decision with full uncertainty quantification
        """
        # 1. Self-awareness check
        should_abstain, reason = self.self_aware.should_abstain(
            self.sharpe_model.neuron_posteriors
        )
        
        if should_abstain:
            return self._create_abstain_decision(reason)
        
        # 2. Get trusted neurons
        trusted_neurons = self._get_trusted_neurons()
        
        if len(trusted_neurons) == 0:
            return self._create_abstain_decision("No trusted neurons")
        
        # 3. Check for changepoints
        for neuron in trusted_neurons:
            if self.changepoint.update(neuron['last_return']) == "changepoint_detected":
                self.sharpe_model.reset_uncertainty(neuron['id'])  # Increase uncertainty
        
        # 4. Get current regime
        current_regime = self._get_current_regime()
        
        # 5. Thompson Sampling allocation
        thompson_alloc = self.bandit.allocate(current_regime, [n['id'] for n in trusted_neurons])
        
        # 6. Robust portfolio optimization
        correlation_samples = self._sample_correlation_posterior(trusted_neurons)
        final_alloc = self.portfolio_opt.optimize(
            [n['id'] for n in trusted_neurons],
            self.sharpe_model.neuron_posteriors,
            correlation_samples
        )
        
        # 7. Blend Thompson + Robust (ensemble)
        blended = self._ensemble_allocate(thompson_alloc, final_alloc, weight=0.5)
        
        # 8. Causal check: "Has this allocation worked before in this regime?"
        causal_score = self.causal.predict_success_probability(blended, current_regime)
        
        if causal_score < 0.3:
            return self._create_abstain_decision(
                f"Causal model predicts low success probability ({causal_score:.1%})"
            )
        
        # 9. Meta-learning update
        self.meta.meta_update({current_regime: causal_score})
        
        # 10. Build decision with full audit trail
        return AllocationDecision(
            allocations=blended,
            reasoning=self._generate_reasoning(blended, causal_score),
            uncertainty_quantification=self._quantify_uncertainty(blended),
            expected_regret=self._estimate_regret(blended),
            causal_score=causal_score
        )
```

---

## Key Innovations Summary

| Feature | Traditional | Optimal CEREBRUM |
|---------|-------------|------------------|
| Sharpe estimation | Point estimate | Posterior distribution |
| Allocation | Greedy (max Sharpe) | Thompson Sampling (optimal) |
| Uncertainty | Ignored | Fully quantified |
| Outliers | Sensitive | Robust (median-based) |
| Regime | Static weights | Contextual bandits |
| Causality | Correlation only | Causal impact estimation |
| Abstention | Fixed threshold | Information-theoretic |
| Learning | Batch | Online Bayesian |
| Changepoints | Manual | Automatic detection |
| Meta-learning | None | Strategy adaptation |

---

## Acceptance Criteria (Optimal)

- [ ] Uses full Bayesian posteriors, never point estimates
- [ ] Thompson Sampling for optimal explore-exploit
- [ ] Abstains when expected information gain > expected return
- [ ] Robust to outliers (median-based statistics)
- [ ] Detects structural breaks automatically
- [ ] Causal attribution for every allocation
- [ ] Meta-learns optimal exploration rate
- [ ] Quantifies full uncertainty in every decision
- [ ] Ensemble of multiple allocation strategies
- [ ] Regret bounds: O(sqrt(T log T)) for T allocation cycles

---

## References

1. **Thompson Sampling:** Thompson (1933), Russo et al. (2018)
2. **Contextual Bandits:** Li et al. (2010), Chu et al. (2011)
3. **Bayesian Online Changepoint Detection:** Adams & MacKay (2007)
4. **Causal Impact:** Brodersen et al. (2015)
5. **Robust Statistics:** Huber & Ronchetti (2009)
6. **Meta-Learning:** Finn et al. (2017) - MAML
7. **Information Geometry:** Amari (2016)

---

**Build the CEREBRUM as a true Bayesian agent. Optimal. Robust. Self-aware. Ever-learning.**
