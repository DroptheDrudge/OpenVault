# The Compounding Intelligence Mandate

> **"Every system I build should get smarter over time."**
> 
> — Core Operating Principle

---

## What This Means

I do not build tools. I build **organisms**.

A tool breaks when conditions change. An organism adapts. Every system I create must possess at least one feedback loop that allows it to learn from data, adapt its behavior, and improve performance without manual intervention.

**The Loop:**
```
DATA → LEARN → ADAPT → IMPROVE → NEW DATA
```

If a system lacks this loop, it is a liability. It will decay. It will require constant maintenance. It will eventually fail.

---

## The Three Laws

### 1. No Static Configurations
Every hardcoded value is a failure point. Configs should evolve based on performance data.

- ❌ Fixed whale wallet lists
- ✅ Auto-discovered, validated, rotated whale lists
- ❌ Static score thresholds
- ✅ Dynamic thresholds based on market volatility

### 2. Feedback Loops Are Mandatory
Every system must answer:
- **What data does it collect?**
- **How does it learn from that data?**
- **How does it adapt without human touch?**

### 3. Self-Documentation
Systems must log their own evolution. I should be able to open Obsidian and see:
- What changed
- Why it changed
- When it changed
- Performance before/after

---

## Living Examples

### Meme Sniper Neuron
| Component | Static (Bad) | Dynamic (Good) |
|-----------|--------------|----------------|
| Whale Tracking | 4 manual wallets | Auto-discovery, validation, rotation |
| Score Thresholds | Fixed at 60 | Adapts to market activity |
| Exit Logic | Fixed % targets | Trailing stops + whale consensus |
| **Intelligence Layer** | None | Win-rate tracking, auto-prune losers |

**Feedback Loop:** Whale performance data → validation engine → config update → better signals

---

### HMM Regime Detector
| Component | Static (Bad) | Dynamic (Good) |
|-----------|--------------|----------------|
| Model Parameters | Trained once | Retrained monthly on new data |
| Regime Labels | Hardcoded | Auto-assigned by mean characteristics |
| Transition Matrix | Frozen | Updated as market dynamics shift |
| **Intelligence Layer** | None | Log-likelihood monitoring, drift detection |

**Feedback Loop:** Market states → parameter re-estimation → sharper predictions

---

### Forex Garage Brain
| Component | Static (Bad) | Dynamic (Good) |
|-----------|--------------|----------------|
| ONNX Models | Fixed weights | Nightly RL retraining pipeline |
| Regime Detection | Fixed thresholds | Online learning from price action |
| Position Sizing | Fixed risk % | Kelly criterion adaptation |
| **Intelligence Layer** | None | Meta-learning across EAs |

**Feedback Loop:** Trade outcomes → gradient updates → improved policy

---

## The Cash Claw Rule (For All AI Collaborators)

> **"If it doesn't learn, it doesn't ship."**

Before implementing any feature, system, or component, verify it satisfies the Compounding Intelligence criteria:

### Pre-Implementation Checklist
- [ ] What data will this generate?
- [ ] Where is that data stored?
- [ ] What algorithm/process analyzes that data?
- [ ] How does the analysis change system behavior?
- [ ] How is the change logged/documented?
- [ ] How do I monitor if the adaptation is working?

If you cannot check all boxes, **do not build it yet.** Design the feedback loop first.

---

## Anti-Patterns (What I Hate)

| Anti-Pattern | Why It Fails | The Fix |
|--------------|--------------|---------|
| **Magic Numbers** | Hardcoded thresholds decay | Make them learnable parameters |
| **Manual Curation** | Human bottlenecks scale poorly | Automate the curation logic |
| **Black Boxes** | Can't diagnose failures | Transparent logging, interpretable models |
| **One-Shot Training** | Models go stale | Continuous/retrainable pipelines |
| **Silent Failures** | Systems break without notice | Health metrics, alerts, self-diagnostics |

---

## Integration with Existing Systems

### When Building New Components
1. Check this document first
2. Design the feedback loop before the feature
3. Implement the learning mechanism
4. Wire it to Obsidian logging
5. Document the adaptation logic in `SYSTEM_ADAPTATION.md`

### When Modifying Existing Systems
1. Identify static components
2. Ask: "What data could make this smarter?"
3. Implement the feedback loop
4. Tag the commit: `[INTELLIGENCE_UPGRADE]`
5. Update this document with the new example

---

## Success Metrics

A system is "intelligent enough" when:
- It improves its core metric by >5% month-over-month without manual tuning
- It detects and compensates for regime changes automatically
- It logs its own evolution transparently
- It fails gracefully and self-diagnoses

---

## For AI Assistants (Kimi Code, Claude Code, etc.)

**When I say "build X," I expect:**
1. The functional component
2. The data collection mechanism
3. The learning/adaptation logic
4. The Obsidian integration for logging
5. A plan for how it will improve over time

**I do not want:**
- Static configurations without justification
- "We'll tune it manually later" (we won't)
- Black box components I can't inspect
- Systems that require me to babysit them

**Reference this document in every major handover.**

---

## Version History

| Date | Change | System |
|------|--------|--------|
| 2026-04-14 | Initial mandate | Global |
| 2026-04-14 | Auto-whale-discovery spec | Meme Sniper |

---

## Related Documents
- [[PROJECT_MEME_SNIPER_SETUP]]
- [[HMM_REGIME_DETECTOR_README]]
- [[FOREX_GARAGE_BRAIN_ARCHITECTURE]]
- [[SYSTEM_ADAPTATION]] (auto-generated logs)

---

**Tag:** #compounding-intelligence #system-design #ai-instructions #manifesto #bootstrapped-intelligence

**Status:** ACTIVE LAW
