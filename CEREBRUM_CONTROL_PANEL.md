# CEREBRUM Control Panel — Mission Control Interface

> **"The brain needs a cockpit."**

---

## Control Panel Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CEREBRUM CONTROL PANEL                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  HEADER: Brain Status + Global Controls                              │   │
│  │  [🧠 CEREBRUM v2.0] [Status: LIVE] [Uptime: 3d 4h] [🔴 STOP]        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   NEURON     │  │  ALLOCATION  │  │   CIRCUIT    │  │   COMMAND    │   │
│  │   MESH       │  │   DASHBOARD  │  │  BREAKERS    │  │   CENTER     │   │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤   │
│  │ • Ferrari EA │  │ Pie Chart    │  │ 🟢 Active    │  │ [PAUSE]      │   │
│  │   Sharpe:2.1 │  │ Current      │  │ • Daily DD   │  │ [RESUME]     │   │
│  │   Status: ✅ │  │ Allocation   │  │ • Sharpe Dec │  │ [THROTTLE]   │   │
│  │              │  │              │  │ • Con Loss   │  │ [EMERGENCY]  │   │
│  │ • Meme Snipe │  │ Cash: 15%    │  │              │  │              │   │
│  │   Score: 45  │  │ Ferrari: 35% │  │ 🔴 Triggered │  │ Target:      │   │
│  │   Status: ⏸️ │  │ Lambo: 25%   │  │ • Ferrari    │  │ [Dropdown ▼] │   │
│  │              │  │              │  │   PAUSED     │  │              │   │
│  │ [+] Add Neuron│  │ [Reallocate] │  │ [Reset]      │  │ [Execute]    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  LIVE FEED: Trades, Commands, Alerts                                 │   │
│  │  [2026-04-14 15:32:01] Ferrari: Trade closed +$45 (TP hit)          │   │
│  │  [2026-04-14 15:31:45] CEREBRUM: Allocated 35% to Ferrari           │   │
│  │  [2026-04-14 15:30:22] ⚠️ Meme Sniper: Score 45 (below threshold)   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────┐  ┌──────────────────────────────────────────┐   │
│  │   CONFIGURATION      │  │   OBSIDIAN INTEGRATION                   │   │
│  │   PANEL              │  │                                          │   │
│  ├──────────────────────┤  ├──────────────────────────────────────────┤   │
│  │ Min Confidence: [70] │  │ 📊 Daily Report: Generated               │   │
│  │ Max Drawdown:  [8%]  │  │ 🧠 Brain State: Logged                   │   │
│  │ Rebalance:     [60s] │  │ 💡 Suggestions: 3 pending                │   │
│  │                      │  │ 📈 Performance: Chart link               │   │
│  │ [Save] [Reset]       │  │                                          │   │
│  └──────────────────────┘  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Backend: FastAPI Control Server

Create `control_panel/api_server.py`:

```python
"""
CEREBRUM Control Panel API Server
Provides REST API and WebSocket for real-time control
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import sqlite3
import json
import asyncio
from pathlib import Path
import threading

# Import CEREBRUM components
import sys
sys.path.insert(0, "C:/Kimi_EAs")
from core.governance.command_dispatcher import CommandDispatcher
from core.mesh.unified_ingestion import UnifiedIngestionHub

app = FastAPI(title="CEREBRUM Control Panel", version="2.0")

# Global state
DB_PATH = "C:/Kimi_EAs/Cerebrum/cerebrum.db"
dispatcher = CommandDispatcher("C:/Kimi_EAs/Cerebrum", DB_PATH)
hub = UnifiedIngestionHub(DB_PATH)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# Pydantic models
class CommandRequest(BaseModel):
    neuron_id: str
    command_type: str  # pause, resume, throttle, drain, emergency_stop
    param_value: Optional[float] = 0.0
    reason: str

class ConfigUpdate(BaseModel):
    min_confidence: Optional[float] = None
    max_drawdown: Optional[float] = None
    rebalance_interval: Optional[int] = None

# API Endpoints

@app.get("/api/status")
async def get_status():
    """Get current CEREBRUM status"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Self-awareness state
    cursor = conn.execute("""
        SELECT * FROM self_awareness_state
        ORDER BY timestamp DESC LIMIT 1
    """)
    awareness = dict(cursor.fetchone()) if cursor else None
    
    # Active neurons
    cursor = conn.execute("""
        SELECT neuron_id, neuron_type, status, equity, daily_pnl
        FROM neuron_heartbeats
        WHERE timestamp > datetime('now', '-5 minutes')
        ORDER BY timestamp DESC
    """)
    neurons = [dict(row) for row in cursor.fetchall()]
    
    # Latest allocation
    cursor = conn.execute("""
        SELECT * FROM allocation_decisions
        ORDER BY timestamp DESC LIMIT 1
    """)
    allocation = dict(cursor.fetchone()) if cursor else None
    
    # Circuit breakers triggered today
    cursor = conn.execute("""
        SELECT COUNT(*) as count FROM cerebrum_commands
        WHERE reason LIKE 'CIRCUIT BREAKER%'
        AND issued_at >= date('now')
    """)
    circuits_triggered = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "awareness": awareness,
        "neurons": neurons,
        "allocation": allocation,
        "circuits_triggered_today": circuits_triggered,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/neurons")
async def get_neurons():
    """Get all neurons with detailed stats"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    cursor = conn.execute("""
        SELECT 
            n.neuron_id,
            n.neuron_type,
            n.status,
            n.equity,
            n.daily_pnl,
            COUNT(t.trade_id) as total_trades,
            AVG(t.pnl) as avg_pnl,
            SUM(CASE WHEN t.pnl > 0 THEN 1 ELSE 0 END) as winning_trades
        FROM neuron_heartbeats n
        LEFT JOIN neuron_trades t ON n.neuron_id = t.neuron_id
        WHERE n.timestamp > datetime('now', '-1 hour')
        GROUP BY n.neuron_id
        ORDER BY n.timestamp DESC
    """)
    
    neurons = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"neurons": neurons}

@app.get("/api/allocations")
async def get_allocations(limit: int = 10):
    """Get recent allocation decisions"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    cursor = conn.execute("""
        SELECT * FROM allocation_decisions
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    allocations = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"allocations": allocations}

@app.get("/api/circuit-breakers")
async def get_circuit_breakers():
    """Get circuit breaker history"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    cursor = conn.execute("""
        SELECT * FROM cerebrum_commands
        WHERE reason LIKE 'CIRCUIT BREAKER%'
        ORDER BY issued_at DESC
        LIMIT 20
    """)
    
    circuits = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"circuit_breakers": circuits}

@app.get("/api/commands/pending")
async def get_pending_commands():
    """Get pending commands awaiting acknowledgement"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    cursor = conn.execute("""
        SELECT * FROM cerebrum_commands
        WHERE status = 'pending'
        ORDER BY issued_at DESC
    """)
    
    commands = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"pending_commands": commands}

@app.post("/api/commands/send")
async def send_command(cmd: CommandRequest):
    """Send a command to a neuron"""
    try:
        command = dispatcher.issue_command(
            neuron_id=cmd.neuron_id,
            command_type=cmd.command_type,
            reason=cmd.reason,
            param_value=cmd.param_value
        )
        
        # Broadcast to all connected clients
        await manager.broadcast({
            "type": "command_sent",
            "data": {
                "command_id": command.command_id,
                "neuron_id": cmd.neuron_id,
                "command_type": cmd.command_type,
                "reason": cmd.reason,
                "timestamp": datetime.now().isoformat()
            }
        })
        
        return {"success": True, "command_id": command.command_id}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/config")
async def update_config(config: ConfigUpdate):
    """Update CEREBRUM configuration"""
    # Write to config file
    config_path = Path("C:/Kimi_EAs/cerebrum_config.json")
    
    current_config = {}
    if config_path.exists():
        with open(config_path) as f:
            current_config = json.load(f)
    
    if config.min_confidence is not None:
        current_config["min_confidence"] = config.min_confidence
    if config.max_drawdown is not None:
        current_config["max_drawdown"] = config.max_drawdown
    if config.rebalance_interval is not None:
        current_config["rebalance_interval"] = config.rebalance_interval
    
    with open(config_path, 'w') as f:
        json.dump(current_config, f, indent=2)
    
    await manager.broadcast({
        "type": "config_updated",
        "data": current_config
    })
    
    return {"success": True, "config": current_config}

@app.post("/api/emergency-stop")
async def emergency_stop():
    """Emergency stop all neurons"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT DISTINCT neuron_id FROM neuron_heartbeats
        WHERE timestamp > datetime('now', '-1 hour')
    """)
    
    neurons = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    commands_sent = []
    for neuron_id in neurons:
        cmd = dispatcher.issue_command(
            neuron_id=neuron_id,
            command_type="emergency_stop",
            reason="EMERGENCY: Manual stop all neurons from control panel"
        )
        commands_sent.append(cmd.command_id)
    
    await manager.broadcast({
        "type": "emergency_stop",
        "data": {
            "neurons_affected": len(neurons),
            "command_ids": commands_sent,
            "timestamp": datetime.now().isoformat()
        }
    })
    
    return {
        "success": True,
        "neurons_affected": len(neurons),
        "command_ids": commands_sent
    }

# WebSocket for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send heartbeat every 2 seconds
            status = await get_status()
            await websocket.send_json({
                "type": "status_update",
                "data": status
            })
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the main dashboard HTML"""
    with open("static/index.html") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

---

## Frontend: Interactive Dashboard

Create `control_panel/static/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 CEREBRUM Control Panel</title>
    <link rel="stylesheet" href="/static/style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-left">
            <span class="logo">🧠</span>
            <div class="title">
                <h1>CEREBRUM Control Panel</h1>
                <span class="subtitle">Meta-Cognitive Capital Allocator v2.0</span>
            </div>
        </div>
        <div class="header-center">
            <div class="status-indicator" id="brain-status">
                <span class="status-dot status-live"></span>
                <span>LIVE</span>
            </div>
            <div class="uptime" id="uptime">Uptime: --</div>
        </div>
        <div class="header-right">
            <button class="btn btn-danger" onclick="emergencyStop()">
                🔴 EMERGENCY STOP ALL
            </button>
        </div>
    </header>

    <!-- Main Grid -->
    <div class="main-grid">
        
        <!-- Neuron Mesh Panel -->
        <div class="panel">
            <div class="panel-header">
                <h2>🕸️ Neuron Mesh</h2>
                <span class="badge" id="neuron-count">0</span>
            </div>
            <div class="panel-content" id="neuron-list">
                <!-- Populated by JS -->
                <div class="loading">Loading neurons...</div>
            </div>
            <button class="btn btn-secondary" onclick="refreshNeurons()">🔄 Refresh</button>
        </div>

        <!-- Allocation Dashboard -->
        <div class="panel panel-wide">
            <div class="panel-header">
                <h2>📊 Capital Allocation</h2>
                <div class="confidence-display">
                    Confidence: <span id="confidence-value">--</span>%
                </div>
            </div>
            <div class="panel-content">
                <div class="allocation-chart-container">
                    <canvas id="allocationChart"></canvas>
                </div>
                <div class="allocation-info" id="allocation-info">
                    <div class="allocation-item">
                        <span class="allocation-label">Cash Reserve</span>
                        <span class="allocation-value" id="cash-pct">--</span>
                    </div>
                </div>
            </div>
            <div class="panel-actions">
                <button class="btn btn-primary" onclick="forceReallocate()">
                    🔄 Force Reallocation
                </button>
                <span id="last-allocation-time">Last: --</span>
            </div>
        </div>

        <!-- Circuit Breakers Panel -->
        <div class="panel">
            <div class="panel-header">
                <h2>🛡️ Circuit Breakers</h2>
                <span class="badge badge-warning" id="circuit-count">0</span>
            </div>
            <div class="panel-content" id="circuit-list">
                <div class="circuit-rule">
                    <span class="rule-name">Daily Drawdown > 5%</span>
                    <span class="rule-action">PAUSE</span>
                </div>
                <div class="circuit-rule">
                    <span class="rule-name">Sharpe Decay 7d</span>
                    <span class="rule-action">THROTTLE 50%</span>
                </div>
                <div class="circuit-rule">
                    <span class="rule-name">Consecutive Losses > 5</span>
                    <span class="rule-action">PAUSE</span>
                </div>
                <div class="circuit-rule circuit-danger">
                    <span class="rule-name">Max Drawdown > 8%</span>
                    <span class="rule-action">EMERGENCY STOP</span>
                </div>
            </div>
            <div class="panel-content" id="triggered-circuits">
                <h4>Triggered Today</h4>
                <div id="triggered-list">None</div>
            </div>
        </div>

        <!-- Command Center -->
        <div class="panel">
            <div class="panel-header">
                <h2>🎮 Command Center</h2>
            </div>
            <div class="panel-content">
                <div class="form-group">
                    <label>Target Neuron</label>
                    <select id="target-neuron">
                        <option value="">Select neuron...</option>
                    </select>
                </div>
                
                <div class="command-buttons">
                    <button class="btn btn-warning" onclick="sendCommand('pause')">
                        ⏸️ PAUSE
                    </button>
                    <button class="btn btn-success" onclick="sendCommand('resume')">
                        ▶️ RESUME
                    </button>
                    <button class="btn btn-warning" onclick="showThrottleDialog()">
                        ⚠️ THROTTLE
                    </button>
                    <button class="btn btn-secondary" onclick="sendCommand('drain')">
                        🚰 DRAIN
                    </button>
                </div>
                
                <div class="form-group">
                    <label>Reason (optional)</label>
                    <input type="text" id="command-reason" 
                           placeholder="Manual intervention...">
                </div>
            </div>
            <div class="panel-content" id="pending-commands">
                <h4>Pending Commands</h4>
                <div id="pending-list">None</div>
            </div>
        </div>

        <!-- Configuration Panel -->
        <div class="panel">
            <div class="panel-header">
                <h2>⚙️ Configuration</h2>
            </div>
            <div class="panel-content">
                <div class="form-group">
                    <label>Min Confidence (%)</label>
                    <input type="number" id="config-confidence" 
                           min="0" max="100" value="70">
                </div>
                
                <div class="form-group">
                    <label>Max Drawdown (%)</label>
                    <input type="number" id="config-drawdown" 
                           min="1" max="50" value="8">
                </div>
                
                <div class="form-group">
                    <label>Rebalance Interval (seconds)</label>
                    <input type="number" id="config-rebalance" 
                           min="10" max="3600" value="60">
                </div>
            </div>
            <div class="panel-actions">
                <button class="btn btn-primary" onclick="saveConfig()">💾 Save</button>
                <button class="btn btn-secondary" onclick="resetConfig()">↩️ Reset</button>
            </div>
        </div>

        <!-- Obsidian Integration -->
        <div class="panel">
            <div class="panel-header">
                <h2>📓 Obsidian</h2>
            </div>
            <div class="panel-content">
                <div class="obsidian-item">
                    <span>📊 Daily Report</span>
                    <span class="status-ok">✓ Generated</span>
                </div>
                <div class="obsidian-item">
                    <span>🧠 Brain State</span>
                    <span class="status-ok">✓ Logged</span>
                </div>
                <div class="obsidian-item">
                    <span>💡 Suggestions</span>
                    <span id="suggestion-count">0 pending</span>
                </div>
                <div class="obsidian-item">
                    <span>📈 Performance</span>
                    <a href="#" target="_blank">View Chart →</a>
                </div>
            </div>
            <button class="btn btn-secondary" onclick="openObsidian()">
                📂 Open Vault
            </button>
        </div>

    </div>

    <!-- Live Feed -->
    <div class="live-feed">
        <div class="feed-header">
            <h3>📡 Live Feed</h3>
            <button class="btn btn-small" onclick="clearFeed()">Clear</button>
        </div>
        <div class="feed-content" id="live-feed">
            <!-- Real-time events -->
        </div>
    </div>

    <!-- Throttle Modal -->
    <div class="modal" id="throttle-modal">
        <div class="modal-content">
            <h3>⚠️ Throttle Position Size</h3>
            <p>Reduce position size to what percentage?</p>
            <input type="range" id="throttle-slider" min="10" max="100" value="50">
            <div class="slider-value"><span id="throttle-value">50</span>%</div>
            
            <div class="modal-actions">
                <button class="btn btn-primary" onclick="sendThrottle()">Apply</button>
                <button class="btn btn-secondary" onclick="closeThrottleModal()">Cancel</button>
            </div>
        </div>
    </div>

    <script src="/static/app.js"></script>
</body>
</html>
```

---

## CSS Styling

Create `control_panel/static/style.css`:

```css
:root {
    --bg-dark: #0a0a0a;
    --bg-panel: #1a1a1a;
    --bg-hover: #2a2a2a;
    --text-primary: #00ff00;
    --text-secondary: #888;
    --accent-danger: #ff3333;
    --accent-warning: #ffaa00;
    --accent-success: #00ff00;
    --accent-info: #00aaff;
    --border: #333;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', monospace;
    background: var(--bg-dark);
    color: var(--text-primary);
    min-height: 100vh;
}

/* Header */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 30px;
    background: var(--bg-panel);
    border-bottom: 2px solid var(--text-primary);
}

.header-left {
    display: flex;
    align-items: center;
    gap: 15px;
}

.logo {
    font-size: 2.5em;
}

.title h1 {
    font-size: 1.5em;
    margin-bottom: 2px;
}

.subtitle {
    font-size: 0.8em;
    color: var(--text-secondary);
}

.header-center {
    text-align: center;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: bold;
}

.status-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

.status-live {
    background: var(--accent-success);
    box-shadow: 0 0 10px var(--accent-success);
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.uptime {
    font-size: 0.85em;
    color: var(--text-secondary);
    margin-top: 4px;
}

/* Main Grid */
.main-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    padding: 20px;
}

.panel {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
}

.panel-wide {
    grid-column: span 2;
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    background: var(--bg-hover);
    border-bottom: 1px solid var(--border);
}

.panel-header h2 {
    font-size: 1.1em;
}

.panel-content {
    padding: 15px;
}

.panel-actions {
    display: flex;
    gap: 10px;
    padding: 15px;
    border-top: 1px solid var(--border);
}

/* Badges */
.badge {
    background: var(--text-primary);
    color: var(--bg-dark);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.85em;
    font-weight: bold;
}

.badge-warning {
    background: var(--accent-warning);
}

/* Buttons */
.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.2s;
}

.btn:hover {
    transform: translateY(-1px);
}

.btn-primary {
    background: var(--text-primary);
    color: var(--bg-dark);
}

.btn-secondary {
    background: var(--bg-hover);
    color: var(--text-primary);
    border: 1px solid var(--text-primary);
}

.btn-danger {
    background: var(--accent-danger);
    color: white;
}

.btn-warning {
    background: var(--accent-warning);
    color: var(--bg-dark);
}

.btn-success {
    background: var(--accent-success);
    color: var(--bg-dark);
}

.btn-small {
    padding: 5px 10px;
    font-size: 0.85em;
}

/* Neuron List */
.neuron-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    margin-bottom: 8px;
    background: var(--bg-hover);
    border-radius: 4px;
    border-left: 3px solid var(--text-primary);
}

.neuron-item.paused {
    border-left-color: var(--accent-warning);
    opacity: 0.7;
}

.neuron-item.offline {
    border-left-color: var(--accent-danger);
}

.neuron-info h4 {
    margin-bottom: 4px;
}

.neuron-stats {
    display: flex;
    gap: 15px;
    font-size: 0.85em;
    color: var(--text-secondary);
}

.neuron-status {
    font-size: 1.5em;
}

/* Allocation Chart */
.allocation-chart-container {
    height: 200px;
    margin-bottom: 15px;
}

.allocation-item {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
}

/* Circuit Rules */
.circuit-rule {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    margin-bottom: 8px;
    background: var(--bg-hover);
    border-radius: 4px;
}

.circuit-danger {
    border: 1px solid var(--accent-danger);
}

.rule-action {
    font-weight: bold;
    color: var(--accent-warning);
}

/* Forms */
.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-size: 0.9em;
    color: var(--text-secondary);
}

.form-group input,
.form-group select {
    width: 100%;
    padding: 10px;
    background: var(--bg-dark);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text-primary);
    font-size: 1em;
}

.command-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 15px;
}

/* Live Feed */
.live-feed {
    margin: 0 20px 20px;
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
}

.feed-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    background: var(--bg-hover);
    border-bottom: 1px solid var(--border);
}

.feed-content {
    height: 200px;
    overflow-y: auto;
    padding: 15px;
    font-family: monospace;
    font-size: 0.9em;
}

.feed-item {
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    animation: fadeIn 0.3s;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateX(-10px); }
    to { opacity: 1; transform: translateX(0); }
}

.feed-item.warning {
    color: var(--accent-warning);
}

.feed-item.danger {
    color: var(--accent-danger);
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal.active {
    display: flex;
}

.modal-content {
    background: var(--bg-panel);
    padding: 30px;
    border-radius: 8px;
    border: 1px solid var(--text-primary);
    min-width: 300px;
}

.modal-content h3 {
    margin-bottom: 15px;
}

.slider-value {
    text-align: center;
    font-size: 1.5em;
    margin: 15px 0;
}

.modal-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

/* Responsive */
@media (max-width: 1400px) {
    .main-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .main-grid {
        grid-template-columns: 1fr;
    }
    
    .panel-wide {
        grid-column: span 1;
    }
    
    .header {
        flex-direction: column;
        gap: 15px;
        text-align: center;
    }
}

/* Loading */
.loading {
    text-align: center;
    padding: 30px;
    color: var(--text-secondary);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-dark);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
}
```

---

## JavaScript Frontend Logic

Create `control_panel/static/app.js`:

```javascript
// CEREBRUM Control Panel Frontend

const API_BASE = '';
let ws = null;
let neurons = [];
let allocationChart = null;

// Initialize
async function init() {
    console.log('🧠 CEREBRUM Control Panel initializing...');
    
    // Initialize chart
    initAllocationChart();
    
    // Load initial data
    await loadNeurons();
    await updateStatus();
    
    // Connect WebSocket
    connectWebSocket();
    
    // Setup throttle slider
    document.getElementById('throttle-slider').addEventListener('input', (e) => {
        document.getElementById('throttle-value').textContent = e.target.value;
    });
    
    // Periodic refresh (every 5 seconds)
    setInterval(updateStatus, 5000);
}

// WebSocket connection
function connectWebSocket() {
    ws = new WebSocket(`ws://${window.location.host}/ws`);
    
    ws.onopen = () => {
        console.log('🔌 WebSocket connected');
        addFeedItem('Connected to CEREBRUM brain', 'info');
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };
    
    ws.onclose = () => {
        console.log('🔌 WebSocket disconnected, reconnecting...');
        addFeedItem('Connection lost, reconnecting...', 'warning');
        setTimeout(connectWebSocket, 3000);
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
}

function handleWebSocketMessage(data) {
    if (data.type === 'status_update') {
        updateDashboard(data.data);
    } else if (data.type === 'command_sent') {
        addFeedItem(`Command sent: ${data.data.command_type} → ${data.data.neuron_id}`, 'info');
    } else if (data.type === 'emergency_stop') {
        addFeedItem(`🚨 EMERGENCY STOP: ${data.data.neurons_affected} neurons halted`, 'danger');
    }
}

// Load neurons
async function loadNeurons() {
    try {
        const response = await fetch('/api/neurons');
        const data = await response.json();
        neurons = data.neurons;
        
        renderNeuronList(neurons);
        updateNeuronSelect(neurons);
    } catch (error) {
        console.error('Failed to load neurons:', error);
    }
}

// Update status
async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Failed to update status:', error);
    }
}

// Render neuron list
function renderNeuronList(neurons) {
    const container = document.getElementById('neuron-list');
    document.getElementById('neuron-count').textContent = neurons.length;
    
    if (neurons.length === 0) {
        container.innerHTML = '<div class="loading">No neurons connected</div>';
        return;
    }
    
    container.innerHTML = neurons.map(n => `
        <div class="neuron-item ${n.status === 'paused' ? 'paused' : ''} ${n.status === 'offline' ? 'offline' : ''}">
            <div class="neuron-info">
                <h4>${n.neuron_id}</h4>
                <div class="neuron-stats">
                    <span>${n.neuron_type}</span>
                    ${n.total_trades ? `<span>Trades: ${n.total_trades}</span>` : ''}
                    ${n.avg_pnl ? `<span>Avg PnL: $${n.avg_pnl.toFixed(2)}</span>` : ''}
                </div>
            </div>
            <div class="neuron-status">
                ${n.status === 'healthy' ? '✅' : n.status === 'paused' ? '⏸️' : '🔴'}
            </div>
        </div>
    `).join('');
}

// Update neuron dropdown
function updateNeuronSelect(neurons) {
    const select = document.getElementById('target-neuron');
    select.innerHTML = `
        <option value="">Select neuron...</option>
        ${neurons.map(n => `<option value="${n.neuron_id}">${n.neuron_id}</option>`).join('')}
    `;
}

// Update dashboard with data
function updateDashboard(data) {
    // Update confidence
    if (data.awareness) {
        const confidence = (data.awareness.overall_confidence * 100).toFixed(1);
        document.getElementById('confidence-value').textContent = confidence;
        
        // Update status indicator
        const statusDot = document.querySelector('.status-dot');
        if (data.awareness.can_allocate) {
            statusDot.className = 'status-dot status-live';
            document.getElementById('brain-status').innerHTML = `
                <span class="status-dot status-live"></span>
                <span>ALLOCATING</span>
            `;
        } else {
            statusDot.className = 'status-dot';
            statusDot.style.background = '#ffaa00';
            document.getElementById('brain-status').innerHTML = `
                <span class="status-dot" style="background:#ffaa00"></span>
                <span>ABSTAINING</span>
            `;
        }
    }
    
    // Update circuit breaker count
    document.getElementById('circuit-count').textContent = data.circuits_triggered_today;
    
    // Update allocation chart
    if (data.allocation && data.allocation.allocations) {
        updateAllocationChart(data.allocation.allocations);
        document.getElementById('last-allocation-time').textContent = 
            'Last: ' + new Date(data.allocation.timestamp).toLocaleTimeString();
    }
}

// Initialize Chart.js
function initAllocationChart() {
    const ctx = document.getElementById('allocationChart').getContext('2d');
    allocationChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    '#00ff00', '#00cc00', '#009900', '#006600',
                    '#00aaff', '#0088cc', '#006699',
                    '#ffaa00', '#cc8800'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#00ff00' }
                }
            }
        }
    });
}

function updateAllocationChart(allocations) {
    const labels = Object.keys(allocations);
    const data = Object.values(allocations).map(v => (v * 100).toFixed(1));
    
    allocationChart.data.labels = labels;
    allocationChart.data.datasets[0].data = data;
    allocationChart.update();
    
    // Update text display
    const info = document.getElementById('allocation-info');
    info.innerHTML = `
        <div class="allocation-item">
            <span class="allocation-label">Cash Reserve</span>
            <span class="allocation-value">${(100 - data.reduce((a,b) => parseFloat(a)+parseFloat(b), 0)).toFixed(1)}%</span>
        </div>
        ${labels.map((l, i) => `
            <div class="allocation-item">
                <span class="allocation-label">${l}</span>
                <span class="allocation-value">${data[i]}%</span>
            </div>
        `).join('')}
    `;
}

// Send command
async function sendCommand(commandType) {
    const neuronId = document.getElementById('target-neuron').value;
    const reason = document.getElementById('command-reason').value || 'Manual command from control panel';
    
    if (!neuronId) {
        alert('Please select a target neuron');
        return;
    }
    
    try {
        const response = await fetch('/api/commands/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                neuron_id: neuronId,
                command_type: commandType,
                reason: reason
            })
        });
        
        const result = await response.json();
        if (result.success) {
            addFeedItem(`✅ Command sent: ${commandType} → ${neuronId}`, 'success');
        } else {
            addFeedItem(`❌ Command failed: ${result.error}`, 'danger');
        }
    } catch (error) {
        addFeedItem(`❌ Network error: ${error.message}`, 'danger');
    }
}

// Throttle dialog
function showThrottleDialog() {
    document.getElementById('throttle-modal').classList.add('active');
}

function closeThrottleModal() {
    document.getElementById('throttle-modal').classList.remove('active');
}

async function sendThrottle() {
    const neuronId = document.getElementById('target-neuron').value;
    const value = document.getElementById('throttle-slider').value / 100;
    
    if (!neuronId) {
        alert('Please select a target neuron');
        return;
    }
    
    try {
        const response = await fetch('/api/commands/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                neuron_id: neuronId,
                command_type: 'throttle',
                param_value: value,
                reason: `Throttle to ${(value*100).toFixed(0)}% from control panel`
            })
        });
        
        const result = await response.json();
        if (result.success) {
            addFeedItem(`✅ Throttled ${neuronId} to ${(value*100).toFixed(0)}%`, 'success');
            closeThrottleModal();
        }
    } catch (error) {
        addFeedItem(`❌ Error: ${error.message}`, 'danger');
    }
}

// Emergency stop
async function emergencyStop() {
    if (!confirm('🚨 EMERGENCY STOP ALL NEURONS?\n\nThis will halt ALL trading immediately!')) {
        return;
    }
    
    try {
        const response = await fetch('/api/emergency-stop', { method: 'POST' });
        const result = await response.json();
        
        if (result.success) {
            addFeedItem(`🚨 EMERGENCY STOP executed: ${result.neurons_affected} neurons halted`, 'danger');
        }
    } catch (error) {
        addFeedItem(`❌ Emergency stop failed: ${error.message}`, 'danger');
    }
}

// Configuration
async function saveConfig() {
    const config = {
        min_confidence: parseFloat(document.getElementById('config-confidence').value) / 100,
        max_drawdown: parseFloat(document.getElementById('config-drawdown').value) / 100,
        rebalance_interval: parseInt(document.getElementById('config-rebalance').value)
    };
    
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });
        
        const result = await response.json();
        if (result.success) {
            addFeedItem('✅ Configuration saved', 'success');
        }
    } catch (error) {
        addFeedItem(`❌ Failed to save config: ${error.message}`, 'danger');
    }
}

function resetConfig() {
    document.getElementById('config-confidence').value = 70;
    document.getElementById('config-drawdown').value = 8;
    document.getElementById('config-rebalance').value = 60;
    addFeedItem('Configuration reset to defaults', 'info');
}

// Feed
function addFeedItem(message, type = 'info') {
    const feed = document.getElementById('live-feed');
    const time = new Date().toLocaleTimeString();
    
    const item = document.createElement('div');
    item.className = `feed-item ${type}`;
    item.innerHTML = `[${time}] ${message}`;
    
    feed.insertBefore(item, feed.firstChild);
    
    // Keep only last 50 items
    while (feed.children.length > 50) {
        feed.removeChild(feed.lastChild);
    }
}

function clearFeed() {
    document.getElementById('live-feed').innerHTML = '';
}

// Utility
function refreshNeurons() {
    loadNeurons();
    addFeedItem('Neuron list refreshed', 'info');
}

function forceReallocate() {
    addFeedItem('Force reallocation requested...', 'info');
    // This would trigger immediate allocation
}

function openObsidian() {
    window.open('file:///C:/Users/Robert/Documents/Obsidian%20Vault', '_blank');
}

// Start
init();
```

---

## Installation

```powershell
# Install dependencies
pip install fastapi uvicorn websockets

# Start control panel
python control_panel/api_server.py

# Open in browser
start http://localhost:8080
```

---

**Your mission control is ready!** 🎛️🧠