# AI Handover Standard

> **"Any AI must be able to pick up where another left off in under 5 minutes."**
> 
> — Collaboration Protocol

---

## The Problem

You work with multiple AI systems: **Kimi Code**, **Claude Code**, **Codex**, and others. Each has different strengths. Each has different context windows. Each has different memory.

**The danger:** An AI builds something, you switch to another AI, and the new AI has no idea what exists, why it exists, or how to modify it safely.

**The solution:** Standardized handover protocol. GitHub is the source of truth. The repo speaks when the AI can't.

---

## The Three-Layer Handover

### Layer 1: The Repo (Source of Truth)
Everything lives in Git. Always. No exceptions.

**Required at repo root:**
```
repo/
├── HANDOVER.md           # ← Current state, blockers, next steps
├── SYSTEM_STATUS.md      # ← What's running, what's broken
├── README.md             # ← What this system does
├── COMPOUNDING_INTELLIGENCE_MANDATE.md
├── NEURON_DOCTRINE.md
└── .ai-context/          # ← AI-specific notes
    ├── kimi-code-notes.md
    ├── claude-notes.md
    └── codex-notes.md
```

**Rule:** If it's not committed, it doesn't exist.

---

### Layer 2: HANDOVER.md (Current State)

This file is **the first thing any AI reads** when entering a project.

**Template:**
```markdown
# System Handover

**Last Updated:** 2026-04-14 07:45 UTC  
**Updated By:** Claude Code  
**Status:** ACTIVE_DEVELOPMENT

## What's Running Right Now
| System | Status | Last Activity | Notes |
|--------|--------|---------------|-------|
| Meme Sniper | 🟢 Running | 2 min ago | 8 whales tracked, no trades yet |
| HMM Detector | 🔴 Not Started | N/A | Awaiting MQL5 integration test |
| Forex Brain | 🟡 Degraded | 1h ago | ZMQ connection flaky |

## Current Blockers
1. **Meme Sniper:** Need more whale wallets — only 8/15 slots filled
2. **HMM Detector:** Need to test MQL5 export on live MT5
3. **Forex Brain:** DLL compilation failing on Windows

## Next Priority
1. Fix Forex Brain ZMQ (blocking Project Stallion)
2. Add auto-whale-discovery to Meme Sniper
3. Validate HMM regime predictions vs ONNX model

## Recent Changes (Last 7 Days)
| Date | Change | By | Reason |
|------|--------|-----|--------|
| 2026-04-14 | Added 4 new whale wallets | Kimi Code | Boost consensus scores |
| 2026-04-13 | Fixed trailing stop bug | Claude Code | Prevent duplicate exits |
| 2026-04-12 | Deployed Meme Sniper v1.0 | Kimi Code | Paper trading live |

## Active Branches
- `master` — Stable, what's deployed
- `feature/auto-whale-discovery` — Kimi Code working here
- `bugfix/zmq-reconnect` — Needs attention

## Context for Next AI
If you're picking this up:
1. Check SYSTEM_STATUS.md for detailed health
2. The Meme Sniper logs to `meme_sniper/logs/bot_run.log`
3. Whale config is in `meme_sniper/config/wallets.yaml`
4. I was about to test the HMM MQL5 export — that's your next task

## Questions?
Ask Bob: "What was the last thing [Previous AI] was working on?"
```

**Update this file:**
- After every significant change
- Before switching to a different AI
- When status changes (running → broken, etc.)

---

### Layer 3: Commit Messages (The Timeline)

**Every commit must answer:** What, Why, and Context.

**❌ Bad:**
```
fix bug
update config
wip
```

**✅ Good:**
```
[MEME_SNIPER] Fix trailing stop deduplication bug

Trailing stops were firing multiple times because the 
`trailing_stop_hit` flag wasn't being persisted to SQLite.

Added column to trades table, updated PaperTrade model,
verified with test_trailing_stop_deduplication.py

Closes: Duplicate exit bug reported in HANDOVER.md 2026-04-13
AI: Claude Code
```

**Required tags:**
- `[MEME_SNIPER]` — Which system
- `[INTELLIGENCE_UPGRADE]` — Added learning capability
- `[NEURON_BIRTH]` — New system created
- `[HOTFIX]` — Urgent fix, review carefully
- `[WIP]` — Work in progress, may be broken

---

## The 5-Minute Onboarding Checklist

**For any AI entering a project:**

1. **Read HANDOVER.md** — Understand current state
2. **Read SYSTEM_STATUS.md** — Detailed health info
3. **Check git log --oneline -20** — Recent context
4. **List files changed in last commit** — What was just touched
5. **Ask Bob: "What should I focus on?"** — Human intent

**Time limit:** 5 minutes. After that, you're building, not reading.

---

## AI-Specific Context Files

Create `.ai-context/` in each major repo for notes that help specific AIs.

### .ai-context/kimi-code-notes.md
```markdown
# Notes for Kimi Code

## Your Strengths Here
- Multi-file master prompts
- End-to-end system building
- Python/MQL5 hybrid projects

## Known Issues You've Fixed
- 2026-04-12: Fixed WinError 206 by shortening paths
- 2026-04-13: Resolved PyTorch 2.6 compatibility

## Bob's Preferences with You
- Likes master prompts that build complete systems
- Prefers you ask clarifying questions upfront
- Wants all 5 EAs eventually, but one at a time

## Current Threads You're Owning
1. Auto-whale-discovery module (in progress)
2. HMM MQL5 integration test (pending)
```

### .ai-context/claude-notes.md
```markdown
# Notes for Claude Code

## Your Strengths Here
- Architecture and debugging
- MQL5/MT5 integration
- Troubleshooting complex issues

## Known Issues You've Fixed
- 2026-04-10: Resolved MT5 EA initialization errors
- 2026-04-11: Fixed ONNX Runtime integration

## Bob's Preferences with You
- Likes systematic debugging
- Values concise, actionable responses
- Hates disclaimers about trading risk

## Current Threads You're Owning
1. Forex Brain ZMQ stability (in progress)
2. HMM regime detector validation (pending)
```

---

## Cross-AI Collaboration Patterns

### Pattern 1: The Relay Race
**Kimi Code builds** → **Claude Code debugs** → **Bob tests** → **Kimi Code ships**

**How:**
1. Kimi creates feature branch, pushes, updates HANDOVER.md
2. Claude pulls, debugs, commits fixes with `[HOTFIX]` tag
3. Bob tests, reports results in HANDOVER.md
4. Kimi merges, tags release

### Pattern 2: Parallel Work
**Kimi works on System A** while **Claude works on System B**

**How:**
- Different branches
- Different HANDOVER sections (System A vs System B)
- Daily sync in HANDOVER.md "Cross-System Impact" section

### Pattern 3: The Swap
**Kimi is blocked** → **Claude takes over** → **Kimi resumes later**

**How:**
1. Kimi writes detailed HANDOVER.md entry: "Paused here, next step is X"
2. Claude reads HANDOVER.md, asks Bob for clarification
3. Claude completes task, updates HANDOVER.md with findings
4. Kimi returns, reads HANDOVER.md, resumes

---

## The Handover Ritual

**When switching AIs, Bob will say:**
> "I'm handing this off from [Previous AI] to [New AI]. Read HANDOVER.md first, then confirm you understand the current state."

**The new AI must respond:**
1. Summary of current state (prove comprehension)
2. Clarifying questions (if any)
3. Confirmation of next priority

**Example:**
> "I've read HANDOVER.md. Current state: Meme Sniper running with 8 whales, no trades yet because scores <60. Blocker: need more whales. Next priority: implement auto-whale-discovery. I see Kimi Code started this on branch `feature/auto-whale-discovery`. I'll continue there. Confirm?"

**Then Bob says:** "Confirmed, go."

**Now you're aligned.**

---

## Anti-Patterns

| Anti-Pattern | The Sin | The Fix |
|--------------|---------|---------|
| **Context Loss** | New AI has no idea what exists | Mandatory HANDOVER.md read |
| **Overwriting** | New AI destroys previous work | Check git diff before any edit |
| **Ghost Changes** | Code exists but isn't committed | Commit or it doesn't exist |
| **Vague Handover** | "Just keep working on it" | Specific priority, specific blocker |
| **AI Amnesia** | AI forgets its own previous work | .ai-context/ notes |

---

## Emergency Protocol

**If an AI completely loses context and can't recover:**

1. **Stop.** Don't write new code.
2. **Read:** HANDOVER.md, README.md, git log
3. **Run:** `python main.py --status` (see what's actually running)
4. **Ask Bob:** "I need clarification on current state"
5. **Document:** Update HANDOVER.md with what you found

**Never guess.** A wrong assumption wastes more tokens than a clarifying question.

---

## Tools That Help

- `git diff HEAD~5` — See recent changes
- `find . -name "*.md" -mtime -7` — Find recently updated docs
- `grep -r "TODO" --include="*.py" .` — Find open tasks
- `python main.py --status` — Check system health

---

## Related Documents
- [[COMPOUNDING_INTELLIGENCE_MANDATE]] — How systems learn
- [[NEURON_DOCTRINE]] — How systems are structured
- [[OBSERVABILITY_MANDATE]] — How systems report state

**Status:** ACTIVE LAW  
**Enforced by:** Bob + All AI collaborators  
**Violation:** Confusion, rework, wasted tokens

---

*An AI handover should be like a relay race: seamless, fast, no dropped batons.* 🏃⚡
