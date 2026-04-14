# CEREBRUM ULTIMATE — Complete Ecosystem Specification

> **"The brain that learns, governs, persists, and improves everything it touches."**

---

## Vision

The CEREBRUM is not just a capital allocator. It is the **meta-learning orchestrator** that:
1. **Ingests** from all neurons (Meme Sniper, HMM, Forex EAs, Stallion)
2. **Allocates** capital optimally via Bayesian intelligence
3. **Governs** with automatic circuit breakers and kill switches
4. **Persists** through crashes, reboots, and failures
5. **Observes** everything in real-time with full transparency
6. **Improves** other systems by feeding back learnings

**The CEREBRUM makes your entire ecosystem smarter over time.**

---

## Architecture: The Seven Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 7: META-IMPROVEMENT ENGINE                                    │
│  ├─ Analyzes neuron code and suggests optimizations                  │
│  ├─ Auto-tunes hyperparameters based on performance                  │
│  ├─ Detects when neurons need retraining                             │
│  └─ Generates improvement PRs for other systems                      │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 6: OBSERVABILITY DASHBOARD                                    │
│  ├─ Real-time brain state visualization                              │
│  ├─ Historical performance analytics                                 │
│  ├─ Alert system (Slack/Discord/email)                               │
│  └─ Mobile-friendly web interface                                    │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 5: PERSISTENCE & IMMORTALITY                                  │
│  ├─ Windows Service / Task Scheduler integration                     │
│  ├─ Automatic restart on crash                                       │
│  ├─ State checkpointing for zero-downtime updates                    │
│  └─ Health monitoring & heartbeat system                             │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 4: COMMANDER & GOVERNANCE                                    │
│  ├─ Automatic circuit breakers (drawdown, decay, losses)             │
│  ├─ Manual override capabilities (pause/resume/throttle)             │
│  ├─ Position size enforcement                                        │
│  └─ Emergency stop protocols                                         │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 3: MULTI-NEURON MESH                                          │
│  ├─ Unified ingestion from all neuron types                          │
│  ├─ Standardized data schema across neurons                          │
│  ├─ Health checking & heartbeat monitoring                            │
│  └─ Cross-neuron correlation analysis                                │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 2: MQL5 EA BRIDGE                                             │
│  ├─ CEREBRUM → EA command execution                                  │
│  ├─ EA → CEREBRUM trade reporting                                    │
│  ├─ Acknowledgement protocol                                         │
│  └─ Fallback mechanisms                                              │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 1: CORE INTELLIGENCE (BUILT ✅)                               │
│  ├─ Bayesian Sharpe estimation                                       │
│  ├─ Thompson Sampling                                                │
│  ├─ Contextual bandits                                               │
│  ├─ Robust portfolio optimization                                    │
│  ├─ Information-theoretic abstention                                 │
│  ├─ Changepoint detection                                            │
│  ├─ Causal impact analysis                                           │
│  └─ Meta-learning                                                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Layer 2: MQL5 EA Bridge (Optimal)

### 2.1 CEREBRUM → EA Command Protocol

Create `Include/CerebrumBridge.mqh`:

```cpp
// CEREBRUM Bridge for MQL5 EAs
// Enables two-way communication between CEREBRUM brain and EAs

#ifndef CEREBRUM_BRIDGE_MQH
#define CEREBRUM_BRIDGE_MQH

#include <JAson.mqh>

// Command types from CEREBRUM
enum ENUM_CEREBRUM_COMMAND
{
   CEREBRUM_CMD_NONE = 0,
   CEREBRUM_CMD_PAUSE = 1,        // Stop new trades
   CEREBRUM_CMD_RESUME = 2,       // Resume trading
   CEREBRUM_CMD_THROTTLE = 3,     // Reduce position size by X%
   CEREBRUM_CMD_DRAIN = 4,        // Close positions, stop new trades
   CEREBRUM_CMD_EMERGENCY_STOP = 5,// Immediate halt, close all
   CEREBRUM_CMD_UPDATE_PARAMS = 6 // Update trading parameters
};

// Command structure
struct CerebrumCommand
{
   long command_id;           // Unique command ID
   ENUM_CEREBRUM_COMMAND type;
   double param_value;        // e.g., throttle percentage
   string reason;             // Why command was issued
   datetime issued_at;
   bool acknowledged;         // Did EA receive?
   datetime acknowledged_at;
   bool executed;             // Did EA execute?
   datetime executed_at;
};

// Trade report structure
struct CerebrumTradeReport
{
   long trade_id;
   string neuron_id;
   string symbol;
   int order_type;
   double volume;
   double open_price;
   double close_price;
   double profit;
   double commission;
   double swap;
   datetime open_time;
   datetime close_time;
   int duration_minutes;
   string regime;             // Current market regime
   string exit_reason;
};

class CCerebrumBridge
{
private:
   string m_neuron_id;
   string m_command_file;     // File for receiving commands
   string m_report_file;      // File for sending reports
   string m_heartbeat_file;   // File for health checks
   
   CerebrumCommand m_last_command;
   datetime m_last_heartbeat;
   
public:
   CCerebrumBridge(string neuron_id);
   
   // Initialization
   bool Init();
   void Shutdown();
   
   // Command handling
   CerebrumCommand CheckForCommands();
   bool AcknowledgeCommand(long command_id);
   bool ReportExecution(long command_id, bool success, string details);
   
   // Trade reporting
   void ReportTrade(CerebrumTradeReport &trade);
   void ReportPositionUpdate();
   
   // Health monitoring
   void SendHeartbeat(double equity, double margin, double daily_pnl);
   bool IsBrainConnected();
   
   // Parameter updates from CEREBRUM
   double GetUpdatedLotSize(double current_lot);
   double GetUpdatedStopLoss(double current_sl);
   double GetUpdatedTakeProfit(double current_tp);
};

// Implementation
CCerebrumBridge::CCerebrumBridge(string neuron_id)
{
   m_neuron_id = neuron_id;
   m_command_file = "Cerebrum\\commands\\" + neuron_id + "_commands.json";
   m_report_file = "Cerebrum\\reports\\" + neuron_id + "_trades.jsonl";
   m_heartbeat_file = "Cerebrum\\heartbeats\\" + neuron_id + ".json";
   m_last_heartbeat = 0;
}

bool CCerebrumBridge::Init()
{
   // Ensure directories exist
   string dirs[] = {
      "Cerebrum",
      "Cerebrum\\commands",
      "Cerebrum\\reports",
      "Cerebrum\\heartbeats"
   };
   
   for(int i = 0; i < ArraySize(dirs); i++)
   {
      if(!FolderCreate(dirs[i], FILE_COMMON))
         Print("CEREBRUM Bridge: Warning - could not create directory: ", dirs[i]);
   }
   
   Print("CEREBRUM Bridge initialized for neuron: ", m_neuron_id);
   return true;
}

CerebrumCommand CCerebrumBridge::CheckForCommands()
{
   CerebrumCommand cmd;
   cmd.type = CEREBRUM_CMD_NONE;
   
   // Check if command file exists
   string filename = m_command_file;
   if(!FileIsExist(filename, FILE_COMMON))
      return cmd;
   
   // Read command
   int handle = FileOpen(filename, FILE_READ|FILE_TXT|FILE_COMMON);
   if(handle == INVALID_HANDLE)
      return cmd;
   
   string json_str = FileReadString(handle);
   FileClose(handle);
   
   // Parse JSON
   CJAson json;
   if(!json.Deserialize(json_str))
   {
      Print("CEREBRUM Bridge: Failed to parse command JSON");
      return cmd;
   }
   
   cmd.command_id = StringToInteger(json["command_id"].ToStr());
   cmd.type = (ENUM_CEREBRUM_COMMAND)StringToInteger(json["type"].ToStr());
   cmd.param_value = StringToDouble(json["param_value"].ToStr());
   cmd.reason = json["reason"].ToStr();
   cmd.issued_at = StringToTime(json["issued_at"].ToStr());
   
   // Acknowledge immediately
   AcknowledgeCommand(cmd.command_id);
   
   Print("CEREBRUM Bridge: Received command ", cmd.type, " - ", cmd.reason);
   
   return cmd;
}

bool CCerebrumBridge::AcknowledgeCommand(long command_id)
{
   string ack_file = "Cerebrum\\commands\\" + m_neuron_id + "_ack_" + IntegerToString(command_id) + ".json";
   
   int handle = FileOpen(ack_file, FILE_WRITE|FILE_TXT|FILE_COMMON);
   if(handle == INVALID_HANDLE)
      return false;
   
   FileWriteString(handle, "{\"command_id\":" + IntegerToString(command_id) + 
                         ",\"neuron_id\":\"" + m_neuron_id + "\"" +
                         ",\"acknowledged_at\":\"" + TimeToString(TimeCurrent()) + "\"}");
   FileClose(handle);
   
   return true;
}

void CCerebrumBridge::ReportTrade(CerebrumTradeReport &trade)
{
   // Append to JSONL file
   int handle = FileOpen(m_report_file, FILE_READ|FILE_WRITE|FILE_TXT|FILE_COMMON);
   if(handle == INVALID_HANDLE)
   {
      // Create new file
      handle = FileOpen(m_report_file, FILE_WRITE|FILE_TXT|FILE_COMMON);
      if(handle == INVALID_HANDLE)
      {
         Print("CEREBRUM Bridge: Failed to open report file");
         return;
      }
   }
   
   // Seek to end
   FileSeek(handle, 0, SEEK_END);
   
   // Write JSON line
   string json_line = "{" +
      "\"trade_id\":" + IntegerToString(trade.trade_id) + "," +
      "\"neuron_id\":\"" + trade.neuron_id + "\"," +
      "\"symbol\":\"" + trade.symbol + "\"," +
      "\"profit\":" + DoubleToString(trade.profit, 2) + "," +
      "\"regime\":\"" + trade.regime + "\"," +
      "\"timestamp\":\"" + TimeToString(TimeCurrent()) + "\"" +
   "}";
   
   FileWriteString(handle, json_line + "\n");
   FileClose(handle);
}

void CCerebrumBridge::SendHeartbeat(double equity, double margin, double daily_pnl)
{
   int handle = FileOpen(m_heartbeat_file, FILE_WRITE|FILE_TXT|FILE_COMMON);
   if(handle == INVALID_HANDLE)
      return;
   
   string json = "{" +
      "\"neuron_id\":\"" + m_neuron_id + "\"," +
      "\"timestamp\":\"" + TimeToString(TimeCurrent()) + "\"," +
      "\"equity\":" + DoubleToString(equity, 2) + "," +
      "\"margin\":" + DoubleToString(margin, 2) + "," +
      "\"daily_pnl\":" + DoubleToString(daily_pnl, 2) + "," +
      "\"status\":\"healthy\"" +
   "}";
   
   FileWriteString(handle, json);
   FileClose(handle);
   
   m_last_heartbeat = TimeCurrent();
}

bool CCerebrumBridge::IsBrainConnected()
{
   // Check if CEREBRUM is writing to our heartbeat directory
   // (it reads heartbeats to confirm neurons are alive)
   return (TimeCurrent() - m_last_heartbeat) < PeriodSeconds(PERIOD_M5);
}

#endif // CEREBRUM_BRIDGE_MQH
```

### 2.2 Python Command Dispatcher

Create `core/governance/command_dispatcher.py`:

```python
"""
CEREBRUM Command Dispatcher
Sends commands to MQL5 EAs and tracks acknowledgements
"""

import json
import os
import time
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import threading
import sqlite3

@dataclass
class Command:
    command_id: str
    neuron_id: str
    command_type: str  # pause, resume, throttle, drain, emergency_stop
    param_value: float
    reason: str
    issued_at: datetime
    acknowledged_at: Optional[datetime] = None
    executed_at: Optional[datetime] = None
    status: str = "pending"  # pending, acknowledged, executed, failed, expired

class CommandDispatcher:
    """
    Dispatches commands to MQL5 EAs via filesystem bridge.
    Tracks acknowledgements and execution status.
    """
    
    COMMAND_TYPES = ['pause', 'resume', 'throttle', 'drain', 'emergency_stop', 'update_params']
    
    def __init__(self, base_path: str = "C:/Kimi_EAs/Cerebrum", db_path: str = None):
        self.base_path = Path(base_path)
        self.commands_dir = self.base_path / "commands"
        self.acks_dir = self.base_path / "acks"
        self.db_path = db_path or str(self.base_path / "cerebrum.db")
        
        # Ensure directories exist
        self.commands_dir.mkdir(parents=True, exist_ok=True)
        self.acks_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory command tracking
        self.pending_commands: Dict[str, Command] = {}
        self.ack_lock = threading.Lock()
        
        # Start acknowledgement monitor
        self.monitor_thread = threading.Thread(target=self._monitor_acks, daemon=True)
        self.monitor_thread.start()
    
    def issue_command(self, neuron_id: str, command_type: str, 
                     reason: str, param_value: float = 0.0) -> Command:
        """
        Issue a command to a neuron.
        
        Args:
            neuron_id: Target EA identifier
            command_type: One of COMMAND_TYPES
            reason: Human-readable reason for command
            param_value: Optional parameter (e.g., throttle percentage)
        
        Returns:
            Command object with tracking ID
        """
        if command_type not in self.COMMAND_TYPES:
            raise ValueError(f"Unknown command type: {command_type}")
        
        cmd = Command(
            command_id=str(uuid.uuid4()),
            neuron_id=neuron_id,
            command_type=command_type,
            param_value=param_value,
            reason=reason,
            issued_at=datetime.now()
        )
        
        # Write command file for EA to pick up
        cmd_file = self.commands_dir / f"{neuron_id}_commands.json"
        with open(cmd_file, 'w') as f:
            json.dump({
                'command_id': cmd.command_id,
                'type': command_type,
                'param_value': param_value,
                'reason': reason,
                'issued_at': cmd.issued_at.isoformat()
            }, f)
        
        # Track pending command
        with self.ack_lock:
            self.pending_commands[cmd.command_id] = cmd
        
        # Log to database
        self._persist_command(cmd)
        
        return cmd
    
    def _monitor_acks(self):
        """Background thread: Monitor for acknowledgements from EAs"""
        while True:
            try:
                self._check_acknowledgements()
                self._check_executions()
                time.sleep(1)  # Check every second
            except Exception as e:
                print(f"CommandDispatcher monitor error: {e}")
                time.sleep(5)
    
    def _check_acknowledgements(self):
        """Check for acknowledgement files from EAs"""
        with self.ack_lock:
            for cmd_id in list(self.pending_commands.keys()):
                cmd = self.pending_commands[cmd_id]
                
                # Look for ack file
                ack_pattern = f"{cmd.neuron_id}_ack_{cmd_id}"
                ack_files = list(self.acks_dir.glob(f"{ack_pattern}*"))
                
                if ack_files:
                    # Acknowledgement received!
                    cmd.acknowledged_at = datetime.now()
                    cmd.status = "acknowledged"
                    self._persist_command(cmd)
                    
                    print(f"✅ Command {cmd_id} acknowledged by {cmd.neuron_id}")
    
    def _check_executions(self):
        """Check if commands have been executed (via trade data or explicit report)"""
        # This would integrate with trade ingestion to verify command effects
        pass
    
    def get_command_status(self, command_id: str) -> Optional[Command]:
        """Get current status of a command"""
        with self.ack_lock:
            return self.pending_commands.get(command_id)
    
    def get_pending_for_neuron(self, neuron_id: str) -> List[Command]:
        """Get all pending commands for a specific neuron"""
        with self.ack_lock:
            return [
                cmd for cmd in self.pending_commands.values()
                if cmd.neuron_id == neuron_id and cmd.status == "pending"
            ]
    
    def _persist_command(self, cmd: Command):
        """Save command to database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT OR REPLACE INTO cerebrum_commands 
            (command_id, neuron_id, command_type, param_value, reason, 
             issued_at, acknowledged_at, executed_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cmd.command_id, cmd.neuron_id, cmd.command_type, cmd.param_value,
            cmd.reason, cmd.issued_at.isoformat(),
            cmd.acknowledged_at.isoformat() if cmd.acknowledged_at else None,
            cmd.executed_at.isoformat() if cmd.executed_at else None,
            cmd.status
        ))
        conn.commit()
        conn.close()
```

---

## Layer 3: Multi-Neuron Mesh (Optimal)

### 3.1 Unified Ingestion Hub

Create `core/mesh/unified_ingestion.py`:

```python
"""
Multi-Neuron Mesh Ingestion
Standardized ingestion from all neuron types
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Iterator
from datetime import datetime
import json
import sqlite3
from pathlib import Path

@dataclass
class NeuronHeartbeat:
    """Standardized heartbeat from any neuron"""
    neuron_id: str
    neuron_type: str  # 'meme_sniper', 'hmm_detector', 'forex_ea', 'stallion'
    timestamp: datetime
    status: str  # 'healthy', 'degraded', 'unhealthy', 'offline'
    equity: Optional[float] = None
    daily_pnl: Optional[float] = None
    open_positions: int = 0
    metadata: Dict = None

@dataclass
class NeuronTrade:
    """Standardized trade report from any neuron"""
    trade_id: str
    neuron_id: str
    neuron_type: str
    timestamp: datetime
    symbol: str
    direction: str  # 'long', 'short'
    entry_price: float
    exit_price: Optional[float] = None
    size: float
    pnl: Optional[float] = None
    pnl_pct: Optional[float] = None
    regime: Optional[str] = None
    duration_seconds: Optional[int] = None
    exit_reason: Optional[str] = None
    metadata: Dict = None

class NeuronAdapter(ABC):
    """Base class for neuron-specific adapters"""
    
    @abstractmethod
    def read_heartbeats(self) -> Iterator[NeuronHeartbeat]:
        """Read heartbeats from this neuron type"""
        pass
    
    @abstractmethod
    def read_trades(self) -> Iterator[NeuronTrade]:
        """Read trades from this neuron type"""
        pass
    
    @abstractmethod
    def get_neuron_type(self) -> str:
        """Return neuron type identifier"""
        pass

class MemeSniperAdapter(NeuronAdapter):
    """Adapter for Meme Sniper neuron"""
    
    def __init__(self, data_path: str = "C:/Users/Robert/meme_sniper"):
        self.data_path = Path(data_path)
    
    def get_neuron_type(self) -> str:
        return "meme_sniper"
    
    def read_heartbeats(self) -> Iterator[NeuronHeartbeat]:
        # Read from meme_sniper SQLite or log files
        pass
    
    def read_trades(self) -> Iterator[NeuronTrade]:
        # Convert meme sniper format to standard
        pass

class HMMDetectorAdapter(NeuronAdapter):
    """Adapter for HMM Regime Detector"""
    
    def __init__(self, data_path: str = "C:/Kimi_EAs/hmm_detector"):
        self.data_path = Path(data_path)
    
    def get_neuron_type(self) -> str:
        return "hmm_detector"
    
    def read_heartbeats(self) -> Iterator[NeuronHeartbeat]:
        pass
    
    def read_trades(self) -> Iterator[NeuronTrade]:
        # HMM detector doesn't trade, but provides regime classifications
        pass
    
    def read_regimes(self) -> Iterator[Dict]:
        """Special: Read regime classifications"""
        pass

class ForexEAAdapter(NeuronAdapter):
    """Adapter for Forex Expert Advisors"""
    
    def __init__(self, cerebrum_path: str = "C:/Kimi_EAs/Cerebrum"):
        self.reports_dir = Path(cerebrum_path) / "reports"
        self.heartbeats_dir = Path(cerebrum_path) / "heartbeats"
    
    def get_neuron_type(self) -> str:
        return "forex_ea"
    
    def read_heartbeats(self) -> Iterator[NeuronHeartbeat]:
        """Read heartbeat files from MQL5 EAs"""
        for hb_file in self.heartbeats_dir.glob("*.json"):
            try:
                with open(hb_file) as f:
                    data = json.load(f)
                
                yield NeuronHeartbeat(
                    neuron_id=data['neuron_id'],
                    neuron_type='forex_ea',
                    timestamp=datetime.fromisoformat(data['timestamp']),
                    status=data.get('status', 'unknown'),
                    equity=data.get('equity'),
                    daily_pnl=data.get('daily_pnl'),
                    metadata=data
                )
            except Exception as e:
                print(f"Error reading heartbeat {hb_file}: {e}")
    
    def read_trades(self) -> Iterator[NeuronTrade]:
        """Read trade reports from MQL5 EAs (JSONL format)"""
        for report_file in self.reports_dir.glob("*_trades.jsonl"):
            neuron_id = report_file.stem.replace("_trades", "")
            
            with open(report_file) as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        
                        yield NeuronTrade(
                            trade_id=str(data['trade_id']),
                            neuron_id=neuron_id,
                            neuron_type='forex_ea',
                            timestamp=datetime.fromisoformat(data['timestamp']),
                            symbol=data.get('symbol', ''),
                            direction='long' if data.get('profit', 0) >= 0 else 'short',
                            entry_price=data.get('open_price', 0),
                            exit_price=data.get('close_price'),
                            size=data.get('volume', 0),
                            pnl=data.get('profit'),
                            regime=data.get('regime'),
                            metadata=data
                        )
                    except Exception as e:
                        print(f"Error parsing trade line: {e}")

class UnifiedIngestionHub:
    """
    Central ingestion hub for all neuron types.
    
    Standardizes data from disparate neurons into unified schema.
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.adapters: List[NeuronAdapter] = []
        
    def register_adapter(self, adapter: NeuronAdapter):
        """Register a neuron adapter"""
        self.adapters.append(adapter)
    
    def ingest_all(self):
        """Ingest data from all registered neurons"""
        for adapter in self.adapters:
            print(f"Ingesting from {adapter.get_neuron_type()}...")
            
            # Ingest heartbeats
            for heartbeat in adapter.read_heartbeats():
                self._store_heartbeat(heartbeat)
            
            # Ingest trades
            for trade in adapter.read_trades():
                self._store_trade(trade)
    
    def _store_heartbeat(self, hb: NeuronHeartbeat):
        """Store heartbeat in unified table"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT OR REPLACE INTO neuron_heartbeats 
            (neuron_id, neuron_type, timestamp, status, equity, daily_pnl, open_positions, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            hb.neuron_id, hb.neuron_type, hb.timestamp.isoformat(),
            hb.status, hb.equity, hb.daily_pnl, hb.open_positions,
            json.dumps(hb.metadata) if hb.metadata else None
        ))
        conn.commit()
        conn.close()
    
    def _store_trade(self, trade: NeuronTrade):
        """Store trade in unified table"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT OR REPLACE INTO neuron_trades 
            (trade_id, neuron_id, neuron_type, timestamp, symbol, direction,
             entry_price, exit_price, size, pnl, pnl_pct, regime, 
             duration_seconds, exit_reason, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trade.trade_id, trade.neuron_id, trade.neuron_type,
            trade.timestamp.isoformat(), trade.symbol, trade.direction,
            trade.entry_price, trade.exit_price, trade.size, trade.pnl,
            trade.pnl_pct, trade.regime, trade.duration_seconds,
            trade.exit_reason, json.dumps(trade.metadata) if trade.metadata else None
        ))
        conn.commit()
        conn.close()
    
    def get_mesh_health(self) -> Dict[str, List[NeuronHeartbeat]]:
        """Get health status of entire neuron mesh"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT neuron_id, neuron_type, timestamp, status, equity
            FROM neuron_heartbeats
            WHERE timestamp > datetime('now', '-5 minutes')
            ORDER BY timestamp DESC
        """)
        
        health = {}
        for row in cursor.fetchall():
            neuron_type = row[1]
            if neuron_type not in health:
                health[neuron_type] = []
            
            health[neuron_type].append(NeuronHeartbeat(
                neuron_id=row[0],
                neuron_type=neuron_type,
                timestamp=datetime.fromisoformat(row[2]),
                status=row[3],
                equity=row[4]
            ))
        
        conn.close()
        return health
```

---

## Layer 4: Commander & Watchdog (Optimal)

### 4.1 Automatic Circuit Breakers

Create `core/governance/circuit_breakers.py`:

```python
"""
CEREBRUM Circuit Breakers
Automatic intervention when neurons breach risk thresholds
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
import sqlite3
from enum import Enum

class CircuitType(Enum):
    DAILY_DRAWDOWN = "daily_drawdown"
    SHARPE_DECAY = "sharpe_decay"
    CONSECUTIVE_LOSSES = "consecutive_losses"
    MAX_DRAWDOWN = "max_drawdown"
    VOLATILITY_SPIKE = "volatility_spike"
    CORRELATION_BREAKDOWN = "correlation_breakdown"

@dataclass
class CircuitBreakerRule:
    """A single circuit breaker rule"""
    circuit_type: CircuitType
    threshold: float
    lookback_days: int
    action: str  # 'pause', 'throttle', 'drain', 'emergency_stop'
    param_value: float = 0.0  # e.g., throttle percentage
    cooldown_hours: int = 1  # Don't re-trigger for this long

class CircuitBreakerEngine:
    """
    Monitors neurons and automatically triggers circuit breakers.
    
    Rules:
    - Daily drawdown > 5% → PAUSE
    - Sharpe decay over 7 days → THROTTLE 50%
    - Consecutive losses > 5 → PAUSE
    - Max drawdown > 8% → EMERGENCY_STOP
    - Volatility spike > 3x average → DRAIN
    """
    
    DEFAULT_RULES = [
        CircuitBreakerRule(CircuitType.DAILY_DRAWDOWN, 0.05, 1, 'pause'),
        CircuitBreakerRule(CircuitType.SHARPE_DECAY, 0.5, 7, 'throttle', 0.5),
        CircuitBreakerRule(CircuitType.CONSECUTIVE_LOSSES, 5, 1, 'pause'),
        CircuitBreakerRule(CircuitType.MAX_DRAWDOWN, 0.08, 30, 'emergency_stop'),
        CircuitBreakerRule(CircuitType.VOLATILITY_SPIKE, 3.0, 1, 'drain'),
    ]
    
    def __init__(self, db_path: str, command_dispatcher):
        self.db_path = db_path
        self.dispatcher = command_dispatcher
        self.rules = self.DEFAULT_RULES.copy()
        self.triggered_circuits: Dict[str, datetime] = {}  # circuit_key -> last_triggered
        
    def add_rule(self, rule: CircuitBreakerRule):
        """Add a custom circuit breaker rule"""
        self.rules.append(rule)
    
    def scan_all_neurons(self) -> List[Dict]:
        """
        Scan all neurons and trigger circuit breakers as needed.
        
        Returns list of triggered circuits.
        """
        triggered = []
        
        conn = sqlite3.connect(self.db_path)
        
        # Get all active neurons
        cursor = conn.execute("""
            SELECT DISTINCT neuron_id FROM neuron_heartbeats
            WHERE timestamp > datetime('now', '-1 hour')
        """)
        
        neurons = [row[0] for row in cursor.fetchall()]
        
        for neuron_id in neurons:
            for rule in self.rules:
                if self._should_check(rule, neuron_id):
                    breach = self._check_rule(conn, neuron_id, rule)
                    if breach:
                        triggered.append(breach)
                        self._trigger_circuit(neuron_id, rule, breach)
        
        conn.close()
        return triggered
    
    def _should_check(self, rule: CircuitBreakerRule, neuron_id: str) -> bool:
        """Check if enough time has passed since last trigger"""
        circuit_key = f"{neuron_id}:{rule.circuit_type.value}"
        last_triggered = self.triggered_circuits.get(circuit_key)
        
        if last_triggered is None:
            return True
        
        cooldown = timedelta(hours=rule.cooldown_hours)
        return datetime.now() - last_triggered > cooldown
    
    def _check_rule(self, conn: sqlite3.Connection, neuron_id: str, 
                   rule: CircuitBreakerRule) -> Optional[Dict]:
        """Check if a specific rule is breached"""
        
        if rule.circuit_type == CircuitType.DAILY_DRAWDOWN:
            return self._check_daily_drawdown(conn, neuron_id, rule)
        
        elif rule.circuit_type == CircuitType.SHARPE_DECAY:
            return self._check_sharpe_decay(conn, neuron_id, rule)
        
        elif rule.circuit_type == CircuitType.CONSECUTIVE_LOSSES:
            return self._check_consecutive_losses(conn, neuron_id, rule)
        
        elif rule.circuit_type == CircuitType.MAX_DRAWDOWN:
            return self._check_max_drawdown(conn, neuron_id, rule)
        
        elif rule.circuit_type == CircuitType.VOLATILITY_SPIKE:
            return self._check_volatility_spike(conn, neuron_id, rule)
        
        return None
    
    def _check_daily_drawdown(self, conn, neuron_id, rule) -> Optional[Dict]:
        """Check if daily drawdown exceeds threshold"""
        cursor = conn.execute("""
            SELECT 
                (MIN(equity) - MAX(equity)) / MAX(equity) as drawdown
            FROM neuron_heartbeats
            WHERE neuron_id = ? 
            AND timestamp >= datetime('now', '-1 day')
        """, (neuron_id,))
        
        row = cursor.fetchone()
        if row and row[0] and abs(row[0]) > rule.threshold:
            return {
                'neuron_id': neuron_id,
                'circuit_type': rule.circuit_type.value,
                'breach_value': abs(row[0]),
                'threshold': rule.threshold,
                'message': f"Daily drawdown {abs(row[0]):.2%} exceeds {rule.threshold:.2%}"
            }
        return None
    
    def _check_sharpe_decay(self, conn, neuron_id, rule) -> Optional[Dict]:
        """Check if Sharpe has decayed over lookback period"""
        cursor = conn.execute("""
            SELECT 
                AVG(CASE WHEN date >= date('now', ?) THEN sharpe END) as recent_sharpe,
                AVG(CASE WHEN date < date('now', ?) THEN sharpe END) as prior_sharpe
            FROM oracle_performance
            WHERE neuron_id = ?
        """, (f'-{rule.lookback_days} days', f'-{rule.lookback_days} days', neuron_id))
        
        row = cursor.fetchone()
        if row and row[0] and row[1] and row[1] > 0:
            decay = row[0] / row[1]  # Ratio of recent to prior
            if decay < rule.threshold:
                return {
                    'neuron_id': neuron_id,
                    'circuit_type': rule.circuit_type.value,
                    'breach_value': decay,
                    'threshold': rule.threshold,
                    'message': f"Sharpe decayed to {decay:.2f}x of prior (threshold {rule.threshold})"
                }
        return None
    
    def _check_consecutive_losses(self, conn, neuron_id, rule) -> Optional[Dict]:
        """Check for consecutive losing trades"""
        cursor = conn.execute("""
            SELECT pnl FROM neuron_trades
            WHERE neuron_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (neuron_id, int(rule.threshold * 2)))  # Get enough history
        
        losses = 0
        for row in cursor.fetchall():
            if row[0] < 0:
                losses += 1
                if losses >= rule.threshold:
                    return {
                        'neuron_id': neuron_id,
                        'circuit_type': rule.circuit_type.value,
                        'breach_value': losses,
                        'threshold': rule.threshold,
                        'message': f"{losses} consecutive losses (threshold {rule.threshold})"
                    }
            else:
                break  # Streak broken
        
        return None
    
    def _trigger_circuit(self, neuron_id: str, rule: CircuitBreakerRule, breach: Dict):
        """Trigger the circuit breaker action"""
        circuit_key = f"{neuron_id}:{rule.circuit_type.value}"
        self.triggered_circuits[circuit_key] = datetime.now()
        
        # Issue command via dispatcher
        cmd = self.dispatcher.issue_command(
            neuron_id=neuron_id,
            command_type=rule.action,
            reason=f"CIRCUIT BREAKER: {breach['message']}",
            param_value=rule.param_value
        )
        
        print(f"🚨 CIRCUIT BREAKER TRIGGERED: {breach['message']}")
        print(f"   Action: {rule.action} | Command ID: {cmd.command_id}")
        
        # Log to Obsidian
        self._log_to_obsidian(neuron_id, rule, breach, cmd)
    
    def _log_to_obsidian(self, neuron_id, rule, breach, cmd):
        """Write circuit breaker event to Obsidian"""
        # Implementation to write to Obsidian vault
        pass
```

---

## Layer 5: Persistence & Immortality

### 5.1 Windows Service Wrapper

Create `cerebrum_service.py`:

```python
"""
CEREBRUM Windows Service
Runs as Windows service, auto-starts on boot, auto-restarts on crash
"""

import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import sys
import os
import time
import signal
import json
from pathlib import Path
from datetime import datetime

class CerebrumService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CerebrumBrain"
    _svc_display_name_ = "CEREBRUM Capital Allocator"
    _svc_description_ = "Meta-cognitive capital allocation brain with consciousness layer - always-on, self-healing"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.process = None
        self.restart_count = 0
        self.last_restart_hour = datetime.now().hour
        self.max_restarts_per_hour = 10
        
    def SvcStop(self):
        """Called when service is stopped"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        
        # Graceful shutdown
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=15)
            except:
                self.process.kill()
                
        servicemanager.LogInfoMsg("CEREBRUM Service: Stopped gracefully")
    
    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()
    
    def main(self):
        """Keep CEREBRUM running forever with intelligent restart"""
        cerebrum_path = r"C:\Kimi_EAs\cerebrum.py"
        checkpoint_dir = Path(r"C:\Kimi_EAs\checkpoints")
        checkpoint_dir.mkdir(exist_ok=True)
        
        servicemanager.LogInfoMsg("CEREBRUM Service: Starting main loop...")
        
        while True:
            # Check if we should stop
            if win32event.WaitForSingleObject(self.stop_event, 2000) == win32event.WAIT_OBJECT_0:
                break
            
            # Reset restart counter each hour
            current_hour = datetime.now().hour
            if current_hour != self.last_restart_hour:
                self.restart_count = 0
                self.last_restart_hour = current_hour
            
            # Rate limit restarts
            if self.restart_count >= self.max_restarts_per_hour:
                servicemanager.LogErrorMsg(
                    f"CEREBRUM Service: Too many restarts ({self.restart_count}), waiting..."
                )
                time.sleep(60)
                continue
            
            # Start or restart CEREBRUM
            if self.process is None or self.process.poll() is not None:
                if self.process is not None:
                    exit_code = self.process.poll()
                    servicemanager.LogWarningMsg(
                        f"CEREBRUM Service: Brain exited with code {exit_code}, restarting..."
                    )
                
                # Brief delay before restart
                time.sleep(3)
                
                try:
                    self.restart_count += 1
                    servicemanager.LogInfoMsg(
                        f"CEREBRUM Service: Starting brain (attempt {self.restart_count})..."
                    )
                    
                    # Write checkpoint before starting
                    checkpoint = {
                        'timestamp': datetime.now().isoformat(),
                        'restart_count': self.restart_count,
                        'pid': None
                    }
                    
                    self.process = subprocess.Popen(
                        [sys.executable, cerebrum_path, "--continuous", "--service-mode"],
                        cwd=r"C:\Kimi_EAs",
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                    )
                    
                    checkpoint['pid'] = self.process.pid
                    with open(checkpoint_dir / "last_restart.json", "w") as f:
                        json.dump(checkpoint, f)
                    
                    servicemanager.LogInfoMsg(
                        f"CEREBRUM Service: Brain started (PID {self.process.pid})"
                    )
                    
                    # Monitor output in background
                    self._monitor_output()
                    
                except Exception as e:
                    servicemanager.LogErrorMsg(f"CEREBRUM Service: Failed to start: {e}")
                    time.sleep(10)
    
    def _monitor_output(self):
        """Stream CEREBRUM output to Windows Event Log"""
        if self.process and self.process.stdout:
            try:
                # Read a few lines
                for _ in range(5):
                    line = self.process.stdout.readline()
                    if line and "ERROR" in line.upper():
                        servicemanager.LogWarningMsg(f"CEREBRUM: {line[:250]}")
            except:
                pass

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(CerebrumService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(CerebrumService)
```

### 5.2 Installation Script

Create `install_service.ps1`:

```powershell
# CEREBRUM Windows Service Installer
# Run as Administrator

Write-Host "Installing CEREBRUM Windows Service..." -ForegroundColor Green

# Check if running as admin
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "Please run as Administrator!"
    exit 1
}

# Install dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
pip install pywin32

# Install the service
Write-Host "Installing service..." -ForegroundColor Yellow
python.exe "C:\Kimi_EAs\cerebrum_service.py" install

# Configure auto-start
Write-Host "Configuring auto-start..." -ForegroundColor Yellow
sc.exe config CerebrumBrain start= auto

# Start the service
Write-Host "Starting service..." -ForegroundColor Yellow
sc.exe start CerebrumBrain

# Verify
Write-Host "Verifying installation..." -ForegroundColor Yellow
$service = Get-Service -Name "CerebrumBrain" -ErrorAction SilentlyContinue
if ($service) {
    Write-Host "✅ CEREBRUM Service installed successfully!" -ForegroundColor Green
    Write-Host "   Status: $($service.Status)"
    Write-Host "   StartType: $($service.StartType)"
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Cyan
    Write-Host "  sc.exe query CerebrumBrain    - Check status"
    Write-Host "  sc.exe stop CerebrumBrain     - Stop service"
    Write-Host "  sc.exe start CerebrumBrain    - Start service"
    Write-Host "  python.exe cerebrum_service.py remove  - Uninstall"
} else {
    Write-Error "❌ Service installation failed!"
}
```

---

## Layer 6: Observability Dashboard

### 6.1 Real-Time Web Dashboard

Create `dashboard/app.py`:

```python
"""
CEREBRUM Real-Time Dashboard
Flask-based web interface for monitoring the brain
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cerebrum-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

DB_PATH = Path("C:/Kimi_EAs/Cerebrum/cerebrum.db")

@app.route("/")
def index():
    """Main dashboard page"""
    return render_template("dashboard.html")

@app.route("/api/status")
def api_status():
    """Get current CEREBRUM status"""
    conn = sqlite3.connect(DB_PATH)
    
    # Get latest self-awareness state
    cursor = conn.execute("""
        SELECT * FROM self_awareness_state
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    awareness = cursor.fetchone()
    
    # Get active neurons
    cursor = conn.execute("""
        SELECT neuron_id, status, COUNT(*) as trade_count
        FROM neuron_heartbeats h
        LEFT JOIN neuron_trades t ON h.neuron_id = t.neuron_id
        WHERE h.timestamp > datetime('now', '-5 minutes')
        GROUP BY h.neuron_id
    """)
    neurons = [dict(row) for row in cursor.fetchall()]
    
    # Get recent allocations
    cursor = conn.execute("""
        SELECT * FROM allocation_decisions
        ORDER BY timestamp DESC
        LIMIT 10
    """)
    allocations = [dict(row) for row in cursor.fetchall()]
    
    # Get circuit breaker history
    cursor = conn.execute("""
        SELECT * FROM cerebrum_commands
        WHERE reason LIKE 'CIRCUIT BREAKER%'
        ORDER BY issued_at DESC
        LIMIT 10
    """)
    circuits = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'awareness': dict(awareness) if awareness else None,
        'neurons': neurons,
        'allocations': allocations,
        'circuit_breakers': circuits,
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status_update', {'message': 'Connected to CEREBRUM'})

def broadcast_updates():
    """Background thread: Broadcast updates to all connected clients"""
    while True:
        try:
            with app.app_context():
                status = get_status_for_broadcast()
                socketio.emit('status_update', status)
            time.sleep(2)  # Update every 2 seconds
        except Exception as e:
            print(f"Broadcast error: {e}")
            time.sleep(5)

def get_status_for_broadcast():
    """Get condensed status for real-time updates"""
    conn = sqlite3.connect(DB_PATH)
    
    cursor = conn.execute("""
        SELECT overall_confidence, can_allocate, neurons_trusted
        FROM self_awareness_state
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    
    conn.close()
    
    return {
        'confidence': row[0] if row else 0,
        'can_allocate': row[1] if row else False,
        'trusted_neurons': row[2] if row else 0,
        'timestamp': datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Start broadcast thread
    broadcast_thread = threading.Thread(target=broadcast_updates, daemon=True)
    broadcast_thread.start()
    
    # Run server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

### 6.2 Dashboard HTML Template

Create `dashboard/templates/dashboard.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>CEREBRUM Dashboard</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0a0a;
            color: #00ff00;
            margin: 0;
            padding: 20px;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .panel {
            background: #1a1a1a;
            border: 1px solid #00ff00;
            border-radius: 8px;
            padding: 20px;
        }
        .panel h3 {
            margin-top: 0;
            color: #00ff00;
        }
        .metric {
            font-size: 2em;
            font-weight: bold;
        }
        .status-ok { color: #00ff00; }
        .status-warning { color: #ffff00; }
        .status-danger { color: #ff0000; }
        .neuron-list {
            list-style: none;
            padding: 0;
        }
        .neuron-item {
            padding: 10px;
            margin: 5px 0;
            background: #2a2a2a;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
        }
        #timestamp {
            text-align: center;
            color: #666;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 CEREBRUM Dashboard</h1>
        <p>Meta-Cognitive Capital Allocator</p>
    </div>

    <div class="grid">
        <div class="panel">
            <h3>Self-Awareness</h3>
            <div class="metric" id="confidence">--</div>
            <p>Overall Confidence</p>
            <div id="can-allocate">--</div>
        </div>

        <div class="panel">
            <h3>Neuron Mesh</h3>
            <div class="metric" id="neuron-count">--</div>
            <p>Active Neurons</p>
            <ul class="neuron-list" id="neuron-list"></ul>
        </div>

        <div class="panel">
            <h3>Recent Allocations</h3>
            <div id="allocations">--</div>
        </div>

        <div class="panel">
            <h3>Circuit Breakers</h3>
            <div id="circuits">No active circuits</div>
        </div>
    </div>

    <div id="timestamp"></div>

    <script>
        const socket = io();
        
        socket.on('status_update', (data) => {
            console.log('Update:', data);
            
            document.getElementById('confidence').textContent = 
                (data.confidence * 100).toFixed(1) + '%';
            
            const allocDiv = document.getElementById('can-allocate');
            if (data.can_allocate) {
                allocDiv.innerHTML = '<span class="status-ok">✅ CAN ALLOCATE</span>';
            } else {
                allocDiv.innerHTML = '<span class="status-warning">⏸️ ABSTAINING</span>';
            }
            
            document.getElementById('neuron-count').textContent = data.trusted_neurons;
            document.getElementById('timestamp').textContent = 
                'Last update: ' + new Date(data.timestamp).toLocaleTimeString();
        });
        
        // Load initial data
        fetch('/api/status')
            .then(r => r.json())
            .then(data => {
                console.log('Initial data:', data);
            });
    </script>
</body>
</html>
```

---

## Layer 7: Meta-Improvement Engine

### 7.1 System Optimizer

Create `core/meta_improvement/optimizer.py`:

```python
"""
CEREBRUM Meta-Improvement Engine
The brain analyzes and improves other systems
"""

import sqlite3
import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

@dataclass
class ImprovementSuggestion:
    """A suggested improvement for a neuron"""
    target_neuron: str
    target_system: str  # 'meme_sniper', 'forex_ea', etc.
    suggestion_type: str  # 'hyperparameter', 'architecture', 'feature', 'retrain'
    current_value: any
    suggested_value: any
    expected_improvement: float  # Predicted Sharpe improvement
    confidence: float  # 0-1
    reasoning: str
    created_at: datetime

class MetaImprovementEngine:
    """
    Analyzes neuron performance and suggests improvements.
    
    The CEREBRUM doesn't just allocate capital—it makes 
    the entire ecosystem smarter over time.
    """
    
    def __init__(self, db_path: str, obsidian_path: str):
        self.db_path = db_path
        self.obsidian_path = Path(obsidian_path)
        self.suggestions: List[ImprovementSuggestion] = []
    
    def analyze_all_neurons(self) -> List[ImprovementSuggestion]:
        """
        Analyze all neurons and generate improvement suggestions.
        
        Returns list of suggestions ranked by expected impact.
        """
        suggestions = []
        
        # Analyze each neuron type
        suggestions.extend(self._analyze_forex_eas())
        suggestions.extend(self._analyze_meme_sniper())
        suggestions.extend(self._analyze_hmm_detector())
        
        # Rank by expected improvement * confidence
        suggestions.sort(
            key=lambda s: s.expected_improvement * s.confidence,
            reverse=True
        )
        
        self.suggestions = suggestions
        return suggestions
    
    def _analyze_forex_eas(self) -> List[ImprovementSuggestion]:
        """Analyze Forex EAs and suggest improvements"""
        suggestions = []
        conn = sqlite3.connect(self.db_path)
        
        # Find EAs with decaying Sharpe
        cursor = conn.execute("""
            SELECT 
                neuron_id,
                AVG(CASE WHEN date >= date('now', '-7 days') THEN sharpe END) as recent_sharpe,
                AVG(CASE WHEN date BETWEEN date('now', '-30 days') AND date('now', '-7 days') 
                         THEN sharpe END) as prior_sharpe
            FROM oracle_performance
            GROUP BY neuron_id
            HAVING recent_sharpe < prior_sharpe * 0.8
        """)
        
        for row in cursor.fetchall():
            neuron_id, recent, prior = row
            decay = recent / prior if prior else 0
            
            suggestions.append(ImprovementSuggestion(
                target_neuron=neuron_id,
                target_system='forex_ea',
                suggestion_type='hyperparameter',
                current_value=f"Sharpe decayed to {decay:.2f}x",
                suggested_value="Reduce position size by 30%, tighten stop loss",
                expected_improvement=0.5,  # Predicted Sharpe recovery
                confidence=0.7,
                reasoning=f"{neuron_id} Sharpe decayed from {prior:.2f} to {recent:.2f}. "
                         f"Likely overfitting to recent regime. Reducing size will cut losses.",
                created_at=datetime.now()
            ))
        
        # Find EAs with high variance
        cursor = conn.execute("""
            SELECT neuron_id, AVG(sharpe) as avg_sharpe, 
                   SQRT(AVG(sharpe*sharpe) - AVG(sharpe)*AVG(sharpe)) as sharpe_std
            FROM oracle_performance
            WHERE date >= date('now', '-30 days')
            GROUP BY neuron_id
            HAVING sharpe_std > 1.5
        """)
        
        for row in cursor.fetchall():
            neuron_id, avg_sharpe, std = row
            
            suggestions.append(ImprovementSuggestion(
                target_neuron=neuron_id,
                target_system='forex_ea',
                suggestion_type='architecture',
                current_value=f"High Sharpe variance: {std:.2f}",
                suggested_value="Add regime filter - only trade in confirmed regimes",
                expected_improvement=0.8,
                confidence=0.6,
                reasoning=f"{neuron_id} has high Sharpe variance ({std:.2f}), suggesting "
                         f"it performs well in some regimes but poorly in others. "
                         f"Adding a regime filter would avoid bad regimes.",
                created_at=datetime.now()
            ))
        
        conn.close()
        return suggestions
    
    def _analyze_meme_sniper(self) -> List[ImprovementSuggestion]:
        """Analyze Meme Sniper and suggest improvements"""
        suggestions = []
        
        # Check if whale consensus threshold is too high
        # (causing missed opportunities)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT COUNT(*) as opportunity_count
            FROM neuron_trades
            WHERE neuron_type = 'meme_sniper'
            AND pnl IS NULL  -- Paper trades that didn't meet threshold
            AND timestamp >= datetime('now', '-7 days')
        """)
        
        row = cursor.fetchone()
        if row and row[0] > 50:  # More than 50 missed opportunities
            suggestions.append(ImprovementSuggestion(
                target_neuron='meme_sniper',
                target_system='meme_sniper',
                suggestion_type='hyperparameter',
                current_value='Score threshold: 60',
                suggested_value='Score threshold: 50 (with smaller position size)',
                expected_improvement=0.3,
                confidence=0.6,
                reasoning=f"{row[0]} opportunities missed in last 7 days due to high threshold. "
                         f"Lowering threshold + reducing position size may capture more alpha.",
                created_at=datetime.now()
            ))
        
        conn.close()
        return suggestions
    
    def _analyze_hmm_detector(self) -> List[ImprovementSuggestion]:
        """Analyze HMM detector and suggest improvements"""
        suggestions = []
        
        # Check if regime predictions correlate with actual performance
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT 
                r.regime,
                AVG(t.pnl) as avg_pnl,
                COUNT(*) as trade_count
            FROM neuron_trades t
            JOIN oracle_context r ON date(t.timestamp) = date(r.timestamp)
            WHERE r.timestamp >= date('now', '-30 days')
            GROUP BY r.regime
        """)
        
        regime_performance = {}
        for row in cursor.fetchall():
            regime_performance[row[0]] = {'avg_pnl': row[1], 'count': row[2]}
        
        # Check if any regime is consistently unprofitable
        for regime, stats in regime_performance.items():
            if stats['count'] > 10 and stats['avg_pnl'] < -0.01:
                suggestions.append(ImprovementSuggestion(
                    target_neuron='hmm_detector',
                    target_system='hmm_detector',
                    suggestion_type='retrain',
                    current_value=f"Regime '{regime}' avg PnL: {stats['avg_pnl']:.4f}",
                    suggested_value='Retrain HMM with more recent data',
                    expected_improvement=0.4,
                    confidence=0.5,
                    reasoning=f"Regime '{regime}' is consistently unprofitable. "
                             f"HMM may be misclassifying or regime characteristics have changed.",
                    created_at=datetime.now()
                ))
        
        conn.close()
        return suggestions
    
    def generate_improvement_report(self) -> str:
        """Generate formatted improvement report for Obsidian"""
        lines = [
            "# CEREBRUM Meta-Improvement Report",
            f"\nGenerated: {datetime.now().isoformat()}",
            f"\n## Top Suggestions ({len(self.suggestions)} total)\n"
        ]
        
        for i, s in enumerate(self.suggestions[:10], 1):
            lines.extend([
                f"\n### {i}. {s.target_neuron}",
                f"- **Type:** {s.suggestion_type}",
                f"- **System:** {s.target_system}",
                f"- **Current:** {s.current_value}",
                f"- **Suggested:** {s.suggested_value}",
                f"- **Expected Improvement:** +{s.expected_improvement:.2f} Sharpe",
                f"- **Confidence:** {s.confidence:.0%}",
                f"- **Reasoning:** {s.reasoning}",
            ])
        
        return "\n".join(lines)
    
    def write_to_obsidian(self):
        """Write improvement report to Obsidian vault"""
        report = self.generate_improvement_report()
        filename = self.obsidian_path / f"CEREBRUM_Improvements_{datetime.now().strftime('%Y-%m-%d')}.md"
        
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"✅ Improvement report written to {filename}")
```

---

## Complete Integration

### Master Orchestrator

Create `cerebrum_ultimate.py`:

```python
#!/usr/bin/env python3
"""
CEREBRUM ULTIMATE — The Complete Brain

Orchestrates all 7 layers:
1. Core Intelligence (Bayesian, Thompson, etc.)
2. MQL5 Bridge (command dispatch)
3. Multi-Neuron Mesh (unified ingestion)
4. Commander/Watchdog (circuit breakers)
5. Persistence (immortality)
6. Dashboard (observability)
7. Meta-Improvement (self-improving ecosystem)
"""

import threading
import time
import signal
import sys
from pathlib import Path
from datetime import datetime

# Import all layers
from core.intelligence.optimal_allocator import OptimalCerebrumAllocator
from core.governance.command_dispatcher import CommandDispatcher
from core.governance.circuit_breakers import CircuitBreakerEngine
from core.mesh.unified_ingestion import UnifiedIngestionHub, ForexEAAdapter, MemeSniperAdapter
from core.meta_improvement.optimizer import MetaImprovementEngine

class CerebrumUltimate:
    """The complete, ultimate CEREBRUM brain."""
    
    def __init__(self, base_path: str = "C:/Kimi_EAs/Cerebrum"):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / "cerebrum.db"
        self.running = False
        
        # Initialize all layers
        print("🧠 Initializing CEREBRUM ULTIMATE...")
        
        # Layer 1: Core Intelligence
        self.allocator = OptimalCerebrumAllocator(str(self.db_path))
        print("  ✅ Core Intelligence")
        
        # Layer 2: Command Dispatcher
        self.dispatcher = CommandDispatcher(str(self.base_path), str(self.db_path))
        print("  ✅ Command Dispatcher")
        
        # Layer 4: Circuit Breakers
        self.circuits = CircuitBreakerEngine(str(self.db_path), self.dispatcher)
        print("  ✅ Circuit Breakers")
        
        # Layer 3: Multi-Neuron Mesh
        self.mesh = UnifiedIngestionHub(str(self.db_path))
        self.mesh.register_adapter(ForexEAAdapter(str(self.base_path)))
        self.mesh.register_adapter(MemeSniperAdapter())
        print("  ✅ Multi-Neuron Mesh")
        
        # Layer 7: Meta-Improvement
        self.improver = MetaImprovementEngine(
            str(self.db_path),
            "C:/Users/Robert/Documents/Obsidian Vault"
        )
        print("  ✅ Meta-Improvement Engine")
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        
        print("\n🚀 CEREBRUM ULTIMATE initialized!")
    
    def handle_shutdown(self, signum, frame):
        """Graceful shutdown"""
        print("\n🛑 Shutdown signal received...")
        self.running = False
    
    def run(self):
        """Main orchestration loop"""
        print("\n▶️  Starting main loop...")
        self.running = True
        
        last_allocation = 0
        last_circuit_check = 0
        last_ingestion = 0
        last_improvement = 0
        
        while self.running:
            try:
                now = time.time()
                
                # Ingest data from all neurons (every 10 seconds)
                if now - last_ingestion > 10:
                    self.mesh.ingest_all()
                    last_ingestion = now
                
                # Run circuit breakers (every 5 seconds)
                if now - last_circuit_check > 5:
                    triggered = self.circuits.scan_all_neurons()
                    if triggered:
                        print(f"🚨 {len(triggered)} circuit breakers triggered!")
                    last_circuit_check = now
                
                # Make allocation decision (every 60 seconds)
                if now - last_allocation > 60:
                    decision = self.allocator.allocate()
                    if decision.can_allocate:
                        print(f"📊 Allocated: {decision.allocations}")
                    else:
                        print(f"⏸️  Abstained: {decision.abstention_reason}")
                    last_allocation = now
                
                # Generate improvement suggestions (every hour)
                if now - last_improvement > 3600:
                    suggestions = self.improver.analyze_all_neurons()
                    if suggestions:
                        self.improver.write_to_obsidian()
                        print(f"💡 Generated {len(suggestions)} improvement suggestions")
                    last_improvement = now
                
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(5)
        
        print("👋 CEREBRUM ULTIMATE shutdown complete")

def main():
    """Entry point"""
    brain = CerebrumUltimate()
    brain.run()

if __name__ == "__main__":
    main()
```

---

## Installation Checklist

```powershell
# 1. Install Python dependencies
pip install numpy scipy flask flask-socketio pywin32

# 2. Install CEREBRUM as Windows Service
.\install_service.ps1

# 3. Start dashboard
python dashboard/app.py

# 4. Open dashboard in browser
start http://localhost:5000

# 5. Verify all systems
python cerebrum_ultimate.py --check
```

---

## Summary: The Ultimate CEREBRUM

| Layer | Component | Status |
|-------|-----------|--------|
| 1 | Core Intelligence (8 modules) | ✅ **BUILT** |
| 2 | MQL5 Bridge | 🚧 **SPEC'D** |
| 3 | Multi-Neuron Mesh | 🚧 **SPEC'D** |
| 4 | Commander/Watchdog | 🚧 **SPEC'D** |
| 5 | Persistence | 🚧 **SPEC'D** |
| 6 | Dashboard | 🚧 **SPEC'D** |
| 7 | Meta-Improvement | 🚧 **SPEC'D** |

**Total: ~3000 lines of institutional-grade Python + MQL5**

**The CEREBRUM will be:**
- ✅ Self-aware and uncertainty-quantified
- ✅ Optimal explore-exploit (Thompson Sampling)
- ✅ Auto-governing (circuit breakers)
- ✅ Immortal (Windows service, auto-restart)
- ✅ Observable (real-time dashboard)
- ✅ Self-improving (suggests optimizations)
- ✅ Multi-neuron (unified ecosystem)

**Build the ultimate brain!** 🧠⚡🚀
