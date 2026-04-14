# CEREBRUM Integration Guide — Connect All Neurons

> **"The brain learns from every trade, every signal, every heartbeat."**

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CEREBRUM BRAIN                               │
│  ├─ Ingests from all neurons via Unified Mesh                        │
│  ├─ Allocates capital via Thompson Sampling                          │
│  ├─ Commands neurons via MQL5 Bridge                                 │
│  └─ Logs everything to Obsidian                                      │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                                │ JSONL + Heartbeats
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
   ┌────▼────┐            ┌────▼────┐           ┌──────▼─────┐
   │  Forex  │            │  Meme   │           │    HMM     │
   │  EAs    │            │ Sniper  │           │  Detector  │
   │ (9x)    │            │         │           │            │
   └────┬────┘            └────┬────┘           └──────┬─────┘
        │                       │                       │
        │ MQL5 Bridge           │ SQLite/API            │ JSONL
        │                       │                       │
   ┌────▼───────────────────────▼───────────────────────▼─────┐
   │              C:\Kimi_EAs\Cerebrum\                        │
   │  ├─ reports\    (trade JSONL from all neurons)           │
   │  ├─ heartbeats\ (health status from all neurons)         │
   │  ├─ commands\   (commands TO neurons)                    │
   │  └─ cerebrum.db (unified data store)                     │
   └──────────────────────────────────────────────────────────┘
```

---

## Step 1: Standardize Data Format

### JSONL Trade Format (All Neurons Must Use This)

Create `C:\Kimi_EAs\Cerebrum\schemas\trade_schema.json`:

```json
{
  "trade_id": "unique_trade_identifier",
  "neuron_id": "ferrari_ea_v2",
  "neuron_type": "forex_ea",
  "timestamp": "2026-04-14T15:30:00Z",
  "symbol": "EURUSD",
  "direction": "long",
  "entry_price": 1.0850,
  "exit_price": 1.0860,
  "size": 0.1,
  "pnl": 10.00,
  "pnl_pct": 0.0092,
  "commission": 0.50,
  "spread_paid": 0.0001,
  "duration_seconds": 3600,
  "exit_reason": "tp_hit",
  "regime": "trend_up",
  "metadata": {
    "slippage": 0.0,
    "max_adverse_excursion": -5.0,
    "max_favorable_excursion": 15.0
  }
}
```

### Heartbeat Format

```json
{
  "neuron_id": "ferrari_ea_v2",
  "neuron_type": "forex_ea",
  "timestamp": "2026-04-14T15:30:00Z",
  "status": "healthy",
  "equity": 10500.00,
  "balance": 10450.00,
  "daily_pnl": 150.00,
  "daily_pnl_pct": 0.0145,
  "open_positions": 2,
  "open_exposure": 0.02,
  "margin_used": 500.00,
  "free_margin": 99500.00,
  "uptime_seconds": 86400
}
```

---

## Step 2: Connect Forex EAs (MQL5 Bridge)

### Add to Each EA's `OnInit()`

```cpp
#include <CerebrumBridge.mqh>

CCerebrumBridge* g_cerebrum = NULL;
input string InpNeuronID = "ferrari_ea_v2";  // Unique ID for this EA

int OnInit()
{
    // Initialize CEREBRUM bridge
    g_cerebrum = new CCerebrumBridge(InpNeuronID);
    if(!g_cerebrum.Init())
    {
        Print("Failed to initialize CEREBRUM bridge");
        return INIT_FAILED;
    }
    
    Print("✅ CEREBRUM connected:", InpNeuronID);
    return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
    if(g_cerebrum != NULL)
    {
        g_cerebrum.Shutdown();
        delete g_cerebrum;
    }
}
```

### Add to `OnTick()` — Command Checking

```cpp
void OnTick()
{
    // Check for commands from CEREBRUM every 5 seconds
    static datetime last_command_check = 0;
    if(TimeCurrent() - last_command_check >= 5)
    {
        last_command_check = TimeCurrent();
        
        CerebrumCommand cmd = g_cerebrum.CheckForCommands();
        
        switch(cmd.type)
        {
            case CEREBRUM_CMD_PAUSE:
                Print("🛑 CEREBRUM: PAUSE command received");
                g_trading_enabled = false;
                g_cerebrum.ReportExecution(cmd.command_id, true, "Trading paused");
                break;
                
            case CEREBRUM_CMD_RESUME:
                Print("▶️ CEREBRUM: RESUME command received");
                g_trading_enabled = true;
                g_cerebrum.ReportExecution(cmd.command_id, true, "Trading resumed");
                break;
                
            case CEREBRUM_CMD_THROTTLE:
                Print("⚠️ CEREBRUM: THROTTLE to ", cmd.param_value * 100, "%");
                g_lot_size_multiplier = cmd.param_value;
                g_cerebrum.ReportExecution(cmd.command_id, true, 
                    StringFormat("Position size throttled to %.0f%%", cmd.param_value * 100));
                break;
                
            case CEREBRUM_CMD_EMERGENCY_STOP:
                Print("🚨 CEREBRUM: EMERGENCY STOP!");
                CloseAllPositions();
                g_trading_enabled = false;
                g_cerebrum.ReportExecution(cmd.command_id, true, "All positions closed, trading halted");
                break;
        }
    }
    
    // Only trade if enabled
    if(!g_trading_enabled) return;
    
    // Your existing trading logic here...
}
```

### Add Heartbeat in `OnTick()`

```cpp
void OnTick()
{
    // ... command checking ...
    
    // Send heartbeat every 30 seconds
    static datetime last_heartbeat = 0;
    if(TimeCurrent() - last_heartbeat >= 30)
    {
        last_heartbeat = TimeCurrent();
        
        double equity = AccountInfoDouble(ACCOUNT_EQUITY);
        double margin = AccountInfoDouble(ACCOUNT_MARGIN);
        
        // Calculate daily PnL
        static double start_of_day_equity = 0;
        if(start_of_day_equity == 0) start_of_day_equity = equity;
        double daily_pnl = equity - start_of_day_equity;
        
        g_cerebrum.SendHeartbeat(equity, margin, daily_pnl);
    }
    
    // ... trading logic ...
}
```

### Report Trades in `OnTrade()` or Position Close

```cpp
void OnTradeTransaction(const MqlTradeTransaction& trans,
                       const MqlTradeRequest& request,
                       const MqlTradeResult& result)
{
    // Check if position was closed
    if(trans.type == TRADE_TRANSACTION_DEAL_ADD)
    {
        CerebrumTradeReport report;
        report.trade_id = trans.deal;
        report.neuron_id = InpNeuronID;
        report.symbol = trans.symbol;
        report.profit = result.profit;
        report.open_price = request.price;
        report.close_price = result.price;
        report.volume = result.volume;
        
        // Get regime from HMM detector (if available)
        report.regime = GetCurrentRegime();  // Your function
        
        g_cerebrum.ReportTrade(report);
        
        Print("📊 Trade reported to CEREBRUM:", report.trade_id, "PnL:", report.profit);
    }
}
```

---

## Step 3: Connect Meme Sniper

### Modify `meme_sniper/bot.py`

```python
import json
import requests
from datetime import datetime
from pathlib import Path

class CerebrumReporter:
    """Reports Meme Sniper activity to CEREBRUM"""
    
    def __init__(self, cerebrum_path: str = "C:/Kimi_EAs/Cerebrum"):
        self.reports_dir = Path(cerebrum_path) / "reports"
        self.heartbeats_dir = Path(cerebrum_path) / "heartbeats"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.heartbeats_dir.mkdir(parents=True, exist_ok=True)
    
    def report_scan(self, token: str, score: float, whale_consensus: list):
        """Report a token scan (not a trade, just monitoring)"""
        # Meme Sniper doesn't report scans to CEREBRUM
        # Only reports actual trades
        pass
    
    def report_paper_trade(self, trade_data: dict):
        """Report a paper trade to CEREBRUM"""
        trade_record = {
            "trade_id": f"meme_{trade_data['token']}_{int(datetime.now().timestamp())}",
            "neuron_id": "meme_sniper",
            "neuron_type": "meme_sniper",
            "timestamp": datetime.now().isoformat(),
            "symbol": trade_data['token'],
            "direction": "long",  # Meme sniper only goes long
            "entry_price": trade_data['entry_price'],
            "exit_price": trade_data.get('exit_price'),
            "size": trade_data['size_sol'],
            "pnl": trade_data.get('pnl_sol'),
            "pnl_pct": trade_data.get('pnl_pct'),
            "regime": trade_data.get('whale_consensus', 'unknown'),
            "exit_reason": trade_data.get('exit_reason', 'open'),
            "metadata": {
                "score": trade_data.get('score'),
                "whale_wallets": trade_data.get('whale_wallets', []),
                "chain": "solana"
            }
        }
        
        # Append to JSONL
        report_file = self.reports_dir / "meme_sniper_trades.jsonl"
        with open(report_file, 'a') as f:
            f.write(json.dumps(trade_record) + '\n')
    
    def send_heartbeat(self, wallet_balance: float, daily_pnl: float, 
                      pending_trades: int, status: str = "healthy"):
        """Send health status to CEREBRUM"""
        heartbeat = {
            "neuron_id": "meme_sniper",
            "neuron_type": "meme_sniper",
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "equity": wallet_balance,
            "daily_pnl": daily_pnl,
            "open_positions": pending_trades,
            "metadata": {
                "chain": "solana",
                "wallet": "paper_trading"
            }
        }
        
        heartbeat_file = self.heartbeats_dir / "meme_sniper.json"
        with open(heartbeat_file, 'w') as f:
            json.dump(heartbeat, f)

# Add to your main bot loop
class MemeSniperBot:
    def __init__(self):
        self.cerebrum = CerebrumReporter()
        # ... existing init ...
    
    async def main_loop(self):
        while True:
            # ... existing scan logic ...
            
            # Send heartbeat every 30 seconds
            self.cerebrum.send_heartbeat(
                wallet_balance=self.wallet.balance,
                daily_pnl=self.daily_pnl,
                pending_trades=len(self.pending_trades)
            )
            
            # When executing paper trade
            if signal_score >= 60:
                trade = await self.execute_paper_trade(token, signal)
                self.cerebrum.report_paper_trade(trade)
            
            await asyncio.sleep(30)
```

---

## Step 4: Connect HMM Regime Detector

### Modify `hmm_detector/regime_publisher.py`

```python
import json
from datetime import datetime
from pathlib import Path

class RegimePublisher:
    """Publishes regime classifications to CEREBRUM"""
    
    def __init__(self, cerebrum_path: str = "C:/Kimi_EAs/Cerebrum"):
        self.context_dir = Path(cerebrum_path) / "context"
        self.heartbeats_dir = Path(cerebrum_path) / "heartbeats"
        self.context_dir.mkdir(parents=True, exist_ok=True)
        self.heartbeats_dir.mkdir(parents=True, exist_ok=True)
    
    def publish_regime(self, symbol: str, regime: str, confidence: float,
                      features: dict):
        """Publish current regime classification"""
        context = {
            "neuron_id": f"hmm_{symbol}",
            "neuron_type": "hmm_detector",
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol,
            "regime": regime,
            "confidence": confidence,
            "features": features
        }
        
        # Write to context file
        context_file = self.context_dir / f"{symbol}_regime.json"
        with open(context_file, 'w') as f:
            json.dump(context, f)
    
    def send_heartbeat(self, symbols_monitored: list):
        """Send health status"""
        heartbeat = {
            "neuron_id": "hmm_detector",
            "neuron_type": "hmm_detector",
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "metadata": {
                "symbols_monitored": symbols_monitored,
                "model_type": "gaussian_hmm"
            }
        }
        
        heartbeat_file = self.heartbeats_dir / "hmm_detector.json"
        with open(heartbeat_file, 'w') as f:
            json.dump(heartbeat, f)

# Usage in HMM detector
publisher = RegimePublisher()

# Every bar close
publisher.publish_regime(
    symbol="EURUSD",
    regime=current_regime,  # 'trend_up', 'range', etc.
    confidence=regime_prob,
    features={
        "returns": current_return,
        "volatility": current_vol,
        "trend_strength": adx_value
    }
)
```

---

## Step 5: CEREBRUM Configuration

### Create `cerebrum_config.yaml`

```yaml
# CEREBRUM Integration Configuration

cerebrum:
  db_path: "C:/Kimi_EAs/Cerebrum/cerebrum.db"
  obsidian_path: "C:/Users/Robert/Documents/Obsidian Vault"
  
# Neuron Registry
neurons:
  # Forex EAs
  - id: "ferrari_ea_v2"
    type: "forex_ea"
    symbol: "EURUSD"
    enabled: true
    min_trades_for_trust: 30
    
  - id: "lamborghini_ea_v2"
    type: "forex_ea"
    symbol: "GBPUSD"
    enabled: true
    min_trades_for_trust: 30
    
  # Add all 9 EAs here...
  
  # Meme Sniper
  - id: "meme_sniper"
    type: "meme_sniper"
    chain: "solana"
    enabled: true
    min_trades_for_trust: 20
    
  # HMM Detectors
  - id: "hmm_EURUSD"
    type: "hmm_detector"
    symbol: "EURUSD"
    enabled: true
    
  - id: "hmm_GBPUSD"
    type: "hmm_detector"
    symbol: "GBPUSD"
    enabled: true

# Circuit Breaker Rules
circuit_breakers:
  daily_drawdown:
    threshold: 0.05  # 5%
    action: "pause"
    
  sharpe_decay:
    threshold: 0.5
    lookback_days: 7
    action: "throttle"
    param_value: 0.5
    
  consecutive_losses:
    threshold: 5
    action: "pause"
    
  max_drawdown:
    threshold: 0.08  # 8%
    action: "emergency_stop"

# Allocation Settings
allocation:
  min_confidence: 0.7
  max_per_neuron: 0.40
  min_per_neuron: 0.05
  cash_buffer: 0.10  # Always keep 10% cash
  
# Meta-Learning
meta_learning:
  adaptation_rate: 0.1
  review_interval_hours: 24
```

---

## Step 6: Quick Integration Test

### Create `test_integration.py`

```python
"""Test CEREBRUM integration with all neurons"""

import json
import time
from pathlib import Path
from datetime import datetime

def test_ea_bridge():
    """Test MQL5 EA bridge"""
    print("Testing Forex EA Bridge...")
    
    # Simulate EA heartbeat
    heartbeat = {
        "neuron_id": "ferrari_ea_v2",
        "timestamp": datetime.now().isoformat(),
        "equity": 10500.0,
        "daily_pnl": 150.0,
        "status": "healthy"
    }
    
    hb_file = Path("C:/Kimi_EAs/Cerebrum/heartbeats/ferrari_ea_v2.json")
    hb_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(hb_file, 'w') as f:
        json.dump(heartbeat, f)
    
    print(f"  ✅ EA heartbeat written to {hb_file}")
    
    # Simulate command file
    cmd_file = Path("C:/Kimi_EAs/Cerebrum/commands/ferrari_ea_v2_commands.json")
    command = {
        "command_id": "test_001",
        "type": "throttle",
        "param_value": 0.5,
        "reason": "Test command",
        "issued_at": datetime.now().isoformat()
    }
    
    with open(cmd_file, 'w') as f:
        json.dump(command, f)
    
    print(f"  ✅ Command written to {cmd_file}")
    print("  EA should pick up this command within 5 seconds!")

def test_meme_sniper():
    """Test Meme Sniper integration"""
    print("\nTesting Meme Sniper Integration...")
    
    trade = {
        "trade_id": "meme_TEST_12345",
        "neuron_id": "meme_sniper",
        "neuron_type": "meme_sniper",
        "timestamp": datetime.now().isoformat(),
        "symbol": "TEST_TOKEN",
        "direction": "long",
        "entry_price": 0.001,
        "size": 0.5,
        "pnl": 0.1,
        "regime": "whale_consensus_high"
    }
    
    report_file = Path("C:/Kimi_EAs/Cerebrum/reports/meme_sniper_trades.jsonl")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'a') as f:
        f.write(json.dumps(trade) + '\n')
    
    print(f"  ✅ Meme trade written to {report_file}")

def test_hmm_detector():
    """Test HMM integration"""
    print("\nTesting HMM Detector Integration...")
    
    regime = {
        "neuron_id": "hmm_EURUSD",
        "neuron_type": "hmm_detector",
        "timestamp": datetime.now().isoformat(),
        "symbol": "EURUSD",
        "regime": "trend_up",
        "confidence": 0.85
    }
    
    regime_file = Path("C:/Kimi_EAs/Cerebrum/context/EURUSD_regime.json")
    regime_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(regime_file, 'w') as f:
        json.dump(regime, f)
    
    print(f"  ✅ Regime written to {regime_file}")

def verify_cerebrum_ingestion():
    """Verify CEREBRUM can ingest all data"""
    print("\nVerifying CEREBRUM Ingestion...")
    
    # Import and test
    import sys
    sys.path.insert(0, "C:/Kimi_EAs")
    
    from core.mesh.unified_ingestion import UnifiedIngestionHub, ForexEAAdapter
    
    hub = UnifiedIngestionHub("C:/Kimi_EAs/Cerebrum/cerebrum.db")
    hub.register_adapter(ForexEAAdapter())
    
    print("  Running ingestion...")
    hub.ingest_all()
    
    health = hub.get_mesh_health()
    print(f"  ✅ Found {len(health)} neuron types")
    
    for neuron_type, neurons in health.items():
        print(f"    - {neuron_type}: {len(neurons)} neurons")

if __name__ == "__main__":
    print("="*60)
    print("CEREBRUM INTEGRATION TEST")
    print("="*60)
    
    test_ea_bridge()
    test_meme_sniper()
    test_hmm_detector()
    
    time.sleep(1)  # Give filesystem time
    
    verify_cerebrum_ingestion()
    
    print("\n" + "="*60)
    print("✅ INTEGRATION TEST COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Attach EA to chart in MT5")
    print("2. Run: python cerebrum_ultimate.py")
    print("3. Watch dashboard: http://localhost:5000")
```

---

## Step 7: Deployment Checklist

```powershell
# 1. Ensure all directories exist
mkdir "C:\Kimi_EAs\Cerebrum\reports" -Force
mkdir "C:\Kimi_EAs\Cerebrum\heartbeats" -Force
mkdir "C:\Kimi_EAs\Cerebrum\commands" -Force
mkdir "C:\Kimi_EAs\Cerebrum\context" -Force

# 2. Copy CerebrumBridge.mqh to MT5
Copy-Item "C:\Kimi_EAs\Cerebrum\mql5\CerebrumBridge.mqh" "C:\Users\$env:USERNAME\AppData\Roaming\MetaQuotes\Terminal\MQL5\Include\"

# 3. Update all EAs with bridge code
# (Compile each EA with new bridge code)

# 4. Start CEREBRUM
python C:\Kimi_EAs\cerebrum_ultimate.py

# 5. Attach EAs to charts
# (EAs will auto-connect to CEREBRUM)

# 6. Verify connections
python C:\Kimi_EAs\test_integration.py

# 7. Start dashboard
python C:\Kimi_EAs\dashboard\app.py
```

---

## Expected Behavior After Integration

### CEREBRUM Sees:
```
🧠 CEREBRUM ULTIMATE initialized!
  ✅ Core Intelligence
  ✅ Command Dispatcher
  ✅ Circuit Breakers
  ✅ Multi-Neuron Mesh
  ✅ Meta-Improvement Engine

▶️  Starting main loop...
  Ingesting from forex_ea...
    - Found 9 neurons
    - Ferrari: 4 trades, 3.625 Sharpe (provisional)
  Ingesting from meme_sniper...
    - No trades yet (score threshold filtering)
  Ingesting from hmm_detector...
    - EURUSD: trend_up (85% confidence)
    - GBPUSD: range (72% confidence)

📊 Allocated: {'ferrari_ea_v2': 0.35, 'lamborghini_ea_v2': 0.25, ...}
  (Only trusted neurons with 30+ trades)

⏸️  Abstained: Overall confidence 0.62 < threshold 0.70
  (Not enough trusted neurons yet)
```

### When Ferrari EA Bleeds:
```
🚨 CIRCUIT BREAKER TRIGGERED: Daily drawdown 5.2% exceeds 5.0%
   Action: pause | Command ID: cb_001
   
[EA Console]
🛑 CEREBRUM: PAUSE command received
   Acknowledged: cb_001
   Trading paused
```

### After 30 Trades:
```
📊 Allocated: {'ferrari_ea_v2': 0.40, 'lamborghini_ea_v2': 0.35}
   Expected Sharpe: 2.1
   Max Drawdown Est: 4.5%
   
💡 Meta-Improvement: Generated 3 suggestions
   - Ferrari: Reduce position size in high_vol regime
   - Meme Sniper: Lower threshold from 60 to 50
   Written to Obsidian
```

---

**The CEREBRUM is now the brain. All neurons feed it data. It governs them all.** 🧠⚡🌐
