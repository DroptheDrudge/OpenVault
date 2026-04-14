# Token Optimization Strategy

> **"Use high-level models for architecture and meta-analysis. Use low-level models for implementation. Never waste reasoning tokens on what a cheaper model can do."**
> 
> — Resource Efficiency Mandate

---

## The Problem

AI models are not equal. Some are deep thinkers (expensive, slow, great at architecture). Some are fast executors (cheap, quick, great at writing code). **Using a reasoning model to write boilerplate is like using a Formula 1 car to deliver groceries.**

You want the **best systems** at the **lowest token cost.** This document defines how to allocate model intelligence efficiently.

---

## The Model Hierarchy

### Tier 1: Architects (High-Level Reasoning)
**Models:** o1, o3-mini-high, Kimi K2.5 thinking, Claude 3.5 Sonnet/Opus
**Cost:** $$$-$$$$ per 1M tokens
**Latency:** Slow (10-60s per response)
**Strengths:**
- System architecture design
- Complex tradeoff analysis
- Debugging obscure failures
- Meta-analysis of strategies
- Reviewing and critiquing designs

**Use for:**
- Designing new neuron architectures
- Deciding between technologies (e.g., HMM vs LSTM vs Transformer)
- Analyzing why a system is failing
- Writing specification documents and ADRs
- Code review of critical components

**Never use for:**
- Writing simple CRUD endpoints
- Generating repetitive MQL5 boilerplate
- Formatting YAML configs
- Basic refactoring

---

### Tier 2: Builders (Implementation Specialists)
**Models:** Claude 3.5 Haiku, GPT-4o-mini, Kimi K2.5 standard, Gemini 1.5 Flash
**Cost:** $-$$ per 1M tokens
**Latency:** Fast (2-10s per response)
**Strengths:**
- Writing clean, working code
- Following detailed specifications
- Implementing well-defined features
- Generating tests and documentation
- Refactoring and formatting

**Use for:**
- Implementing features from a spec
- Writing unit tests
- Generating MQL5 include files
- Creating YAML configs
- Producing Obsidian report templates
- Handling routine git operations

**Never use for:**
- Designing the overall system from scratch
- Solving novel algorithmic problems
- Debugging complex distributed failures

---

### Tier 3: Clerks (Routine Operations)
**Models:** Local LLMs, scripted automation, non-AI tools
**Cost:** $ or free
**Latency:** Instant
**Strengths:**
- Formatting
- Search and replace
- File operations
- Linting
- Running tests

**Use for:**
- `black`, `isort`, `flake8`
- `git commit`, `git push`
- File search and grep
- Basic template rendering

---

## The Workflow: How to Allocate Intelligence

### Phase 1: Architecture (Architect Model)
**Duration:** 1-3 messages  
**Model:** Tier 1 (Reasoning)

**Prompt structure:**
```
I want to build [SYSTEM]. Here are my constraints:
- [Constraint 1]
- [Constraint 2]

Read [MANDATE_FILES] first.

Your job: Design the architecture, identify key components, 
recommend technologies, and flag risks. Do NOT write code yet.

Deliver:
1. Component diagram (text-based)
2. Technology choices with justification
3. 3 biggest risks and mitigations
4. Decision tree for any ambiguous choices
```

**Goal:** Lock in the design. This is the expensive part, but it's small.

---

### Phase 2: Specification (Architect Model)
**Duration:** 1-2 messages  
**Model:** Tier 1 (Reasoning)

**Prompt structure:**
```
Based on the architecture above, write a detailed spec for [COMPONENT].

Include:
1. Interfaces (functions, classes, APIs)
2. Data structures
3. Error handling strategy
4. Testing strategy
5. Obsidian logging requirements
6. Fallback/degradation behavior

Do NOT write full code. Write pseudocode and interfaces only.
```

**Goal:** Hand the spec to a builder model with zero ambiguity.

---

### Phase 3: Implementation (Builder Model)
**Duration:** 5-20 messages  
**Model:** Tier 2 (Fast/Cheap)

**Prompt structure:**
```
Implement the following spec. Read the architecture and spec first.

[SPEC pasted here]

Rules:
- Follow NEURON_DOCTRINE.md (standalone, health checks, etc.)
- Follow OBSERVABILITY_MANDATE.md (SQLite + Markdown + Logs)
- Follow COMPOUNDING_INTELLIGENCE_MANDATE.md (feedback loops)
- Write tests for every public function
- Use --status and --health CLI flags
- Commit to git after each major file

Write the code now.
```

**Goal:** Bulk of the code gets written cheaply and quickly.

---

### Phase 4: Review (Architect Model)
**Duration:** 1 message  
**Model:** Tier 1 (Reasoning)

**Prompt structure:**
```
Review this implementation against the original spec.
[CODE pasted or linked]

Check for:
1. Security issues
2. Performance bottlenecks
3. Deviation from spec
4. Missing edge cases
5. Anti-patterns from our mandates

Be harsh. Flag anything that would fail in production.
```

**Goal:** Catch expensive mistakes before they ship.

---

### Phase 5: Refinement (Builder Model)
**Duration:** 2-5 messages  
**Model:** Tier 2 (Fast/Cheap)

**Prompt structure:**
```
Fix these issues identified in review:
[REVIEW_FEEDBACK listed]
```

**Goal:** Address review feedback cheaply.

---

### Phase 6: Final Validation (Clerk / Script)
**Duration:** Automated  
**Model:** Tier 3 (Scripts)

**Actions:**
- Run tests: `pytest`
- Run linters: `black`, `flake8`
- Check types: `mypy`
- Verify health checks: `python main.py --health`
- Verify status: `python main.py --status`
- Push to GitHub

---

## Example: Building the Auto-Whale-Discovery Module

### Total Token Cost Estimate

| Phase | Model Tier | Messages | Est. Cost | Est. Time |
|-------|-----------|----------|-----------|-----------|
| Architecture | Tier 1 | 2 | $0.50 | 5 min |
| Specification | Tier 1 | 2 | $0.30 | 3 min |
| Implementation | Tier 2 | 12 | $0.20 | 10 min |
| Review | Tier 1 | 1 | $0.20 | 2 min |
| Refinement | Tier 2 | 3 | $0.05 | 3 min |
| Validation | Tier 3 | Auto | $0.00 | 1 min |
| **Total** | — | **20** | **$1.25** | **24 min** |

**If you used Tier 1 for everything:** ~$3.50 and 40 minutes  
**If you used Tier 2 for architecture:** Risk of poor design, more rework  

**The mixed approach is optimal.**

---

## The "Punt Down" Rule

If a task can be done by a lower tier, **it must be punted down.**

| Task | Wrong Tier | Right Tier | Savings |
|------|-----------|------------|---------|
| "Write a for loop in Python" | Tier 1 | Tier 2 | 10x |
| "Refactor this variable name" | Tier 1 | Tier 3 | 100x |
| "Design the scoring algorithm" | Tier 2 | Tier 1 | Better outcome |
| "Debug this segfault" | Tier 2 | Tier 1 | Faster resolution |
| "Generate test fixtures" | Tier 1 | Tier 2 | 10x |
| "Review this for thread safety" | Tier 2 | Tier 1 | Prevents bugs |

---

## Prompt Compression for Tier 1

Reasoning models are expensive. **Compress your prompts:**

### ✅ Good (concise, dense):
```
Meme Sniper needs auto-whale-discovery.

Constraints:
- Helius API only
- Max 15 wallets
- Must validate win rate >40%
- Must log to Obsidian

Read mandates from OpenVault first.

Design the architecture. Focus on:
1. How to discover whales from pumping tokens
2. How to validate profitability
3. How to rotate stale wallets
4. Integration with existing 30s loop

No code. Architecture only.
```

### ❌ Bad (verbose, scattered):
```
Hey I was thinking about building this thing where we find wallets and track them and it's really important because the bot isn't finding enough signals and I read somewhere that lookonchain is good but also maybe we can use helius and what do you think about DexScreener and also can you write some code for me...
```

**Rule:** Every sentence in a Tier 1 prompt should carry architectural weight.

---

## Context Window Management

### For Tier 1 (limited context, expensive tokens)
- **Summarize, don't paste.** Link to specs instead of embedding full code.
- **Use bullet points.** Dense information = fewer tokens.
- **One decision per message.** Don't ask it to design AND implement.
- **Reference, don't repeat.** "See HMM spec" instead of restating.

### For Tier 2 (larger context, cheaper tokens)
- **Paste the spec inline.** They follow instructions well with full context.
- **Multi-file edits are fine.** They're good at bulk implementation.
- **Iterative refinement works.** Let them make mistakes and fix them.

---

## The Decision Matrix

Use this to choose the right model for any task:

```
Is the task novel or ambiguous?
├── YES → Tier 1 (Architect)
│   └── Examples: System design, debugging unknowns, tradeoff analysis
│
└── NO → Is it well-specified implementation?
    ├── YES → Tier 2 (Builder)
    │   └── Examples: Write code from spec, tests, configs
    │
    └── NO → Is it mechanical/repetitive?
        ├── YES → Tier 3 (Clerk/Script)
        │   └── Examples: Formatting, linting, git ops
        │
        └── NO → Ask Bob for clarification
```

---

## Special Cases

### When to Override and Use Tier 1 for Implementation
- Security-critical code (wallet signing, encryption)
- Performance-critical code (real-time inference loops)
- Novel algorithms (custom HMM inference, proprietary scoring)
- Complex concurrent code (threading, async coordination)

### When to Override and Use Tier 2 for Architecture
- Minor architectural tweaks (adding one field to an API)
- Well-trodden patterns (CRUD API, simple webhook handler)
- Refactoring existing architecture (no novel decisions)

---

## Tool Recommendations by Tier

### Tier 1 Platforms
- **Kimi Code** (K2.5) — Best for multi-file master prompts
- **Claude Code** (Opus/Sonnet) — Best for debugging and architecture
- **OpenAI Codex** (o1/o3-mini-high) — Best for reasoning-heavy tasks
- **OpenClaw sessions** (kimi-coding/k2p5) — Good for long-context specs

### Tier 2 Platforms
- **Kimi Code** (standard mode) — Fast implementation
- **Claude Code** (Haiku/Sonnet non-thinking) — Quick coding
- **GitHub Copilot** — Inline completion, simple generation
- **Gemini 1.5 Flash** — Bulk code generation

### Tier 3 Platforms
- **Local scripts** — `sed`, `awk`, `python` one-liners
- **Pre-commit hooks** — `black`, `isort`, `flake8`
- **IDE refactoring** — VSCode rename, extract method, etc.
- **Git CLI** — `git commit`, `git rebase`, `git diff`

---

## Tracking Efficiency

**Create a simple log in your repo:**

```markdown
# Token Efficiency Log

| Date | Project | Phase | Model | Messages | Est. Cost | Outcome |
|------|---------|-------|-------|----------|-----------|---------|
| 2026-04-14 | Meme Sniper Whale Discovery | Arch | Claude Opus | 2 | $0.50 | ✅ Clean design |
| 2026-04-14 | Meme Sniper Whale Discovery | Impl | Kimi K2.5 | 12 | $0.20 | ✅ Working code |
| 2026-04-14 | HMM Detector | Review | Claude Opus | 1 | $0.20 | ✅ Caught race condition |
```

**Review monthly:** Are you overusing Tier 1? Are you underusing Tier 2?

---

## Anti-Patterns

| Anti-Pattern | The Sin | The Fix |
|--------------|---------|---------|
| **Architect Does Everything** | $5 per feature, slow progress | Punt implementation to Tier 2 |
| **Builder Designs Everything** | Poor architecture, lots of rework | Use Tier 1 for 2-3 messages upfront |
| **Premature Optimization** | Spending 10 minutes saving $0.05 | Optimize the big phases first |
| **Monolithic Prompts** | Asking one model to do everything | Split into architect → builder phases |
| **No Review Gate** | Shipping without Tier 1 review | Always have a review phase |

---

## For AI Assistants

**If you're an architect model (Tier 1):**
- Focus on design, not implementation
- Be concise — every word costs
- Flag ambiguous requirements for clarification
- Write specs that a Tier 2 model can execute flawlessly

**If you're a builder model (Tier 2):**
- Follow specs exactly
- Ask for clarification on ambiguity
- Write tests, docs, and health checks
- Commit frequently

**If you're an OpenClaw instance:**
- Route architecture tasks to reasoning mode
- Route bulk implementation to standard mode
- Use scripts for formatting and validation

---

## Related Documents
- [[COMPOUNDING_INTELLIGENCE_MANDATE]] — What systems must do
- [[NEURON_DOCTRINE]] — How systems must be structured
- [[AI_HANDOVER_STANDARD]] — How AIs must collaborate
- [[OBSERVABILITY_MANDATE]] — How systems must report

**Status:** ACTIVE LAW  
**Enforced by:** Bob + All AI collaborators  
**Violation:** Wasted tokens, slow progress, suboptimal systems

---

*Smart resource allocation is itself a form of intelligence.* 🧠⚡💰
