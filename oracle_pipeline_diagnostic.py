#!/usr/bin/env python3
"""
Oracle Pipeline Diagnostic
Checks if MQL5 EA JSONL files exist and if data is flowing into Oracle DB.
Run this on your Windows machine where MT5 + Oracle are installed.
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

# ── CONFIG ── Adjust these paths to your setup ──
MT5_TERMINAL_PATH = Path(r"C:/Users/Robert/AppData/Roaming/MetaQuotes/Terminal")
ORACLE_DB_PATH = Path(r"C:/Kimi_EAs/oracle/data/oracle.db")
EA_NAMES = ["ferrari", "stallion", "lamborghini", "porsche", "bugatti", "mclaren"]

# ── HELPERS ──
def find_jsonl_files():
    """Discover all EA JSONL report files in MT5 Terminal tree."""
    found = []
    if not MT5_TERMINAL_PATH.exists():
        print(f"❌ MT5 Terminal path not found: {MT5_TERMINAL_PATH}")
        return found
    
    for ea in EA_NAMES:
        pattern = f"*_{ea}.jsonl"
        matches = list(MT5_TERMINAL_PATH.rglob(pattern))
        if matches:
            for m in matches:
                size = m.stat().st_size
                found.append({"ea": ea, "path": str(m), "size_bytes": size})
        else:
            found.append({"ea": ea, "path": None, "size_bytes": 0})
    return found

def tail_jsonl(filepath, n=3):
    """Read last N lines from JSONL file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [json.loads(line.strip()) for line in lines[-n:] if line.strip()]
    except Exception as e:
        return [{"error": str(e)}]

def check_oracle_db():
    """Check Oracle DB for ingested EA data."""
    if not ORACLE_DB_PATH.exists():
        print(f"❌ Oracle DB not found: {ORACLE_DB_PATH}")
        return None
    
    conn = sqlite3.connect(str(ORACLE_DB_PATH))
    cursor = conn.cursor()
    
    results = {}
    
    # Registry
    cursor.execute("SELECT neuron_id, last_heartbeat FROM oracle_registry;")
    results["registry"] = cursor.fetchall()
    
    # Performance rows per neuron
    cursor.execute("""
        SELECT neuron_id, COUNT(*), MAX(date) 
        FROM oracle_performance 
        GROUP BY neuron_id;
    """)
    results["performance"] = cursor.fetchall()
    
    # Trade rows per neuron
    cursor.execute("""
        SELECT neuron_id, COUNT(*), MAX(timestamp) 
        FROM oracle_trades 
        GROUP BY neuron_id;
    """)
    results["trades"] = cursor.fetchall()
    
    conn.close()
    return results

# ── MAIN ──
def main():
    print("=" * 60)
    print("🔍 ORACLE PIPELINE DIAGNOSTIC")
    print("=" * 60)
    
    # 1. Check JSONL files
    print("\n📁 MQL5 EA JSONL Files:")
    files = find_jsonl_files()
    for f in files:
        if f["path"]:
            print(f"  ✅ {f['ea']}: {f['path']} ({f['size_bytes']} bytes)")
            if f["size_bytes"] > 0:
                print(f"     └─ Last 3 entries:")
                for entry in tail_jsonl(f["path"], 3):
                    action = entry.get("action", "unknown")
                    ts = entry.get("timestamp", "?")
                    print(f"        • [{action}] @ {ts}")
        else:
            print(f"  ❌ {f['ea']}: NO JSONL FILE FOUND")
    
    # 2. Check Oracle DB
    print("\n🧠 Oracle Database:")
    db = check_oracle_db()
    if db:
        print(f"  DB: {ORACLE_DB_PATH}")
        print(f"\n  Registered Neurons:")
        for row in db["registry"]:
            print(f"    • {row[0]} — last heartbeat: {row[1]}")
        
        print(f"\n  Performance Rows:")
        if db["performance"]:
            for row in db["performance"]:
                print(f"    • {row[0]}: {row[1]} rows (latest: {row[2]})")
        else:
            print("    ⚠️  No performance data ingested yet")
        
        print(f"\n  Trade Rows:")
        if db["trades"]:
            for row in db["trades"]:
                print(f"    • {row[0]}: {row[1]} rows (latest: {row[2]})")
        else:
            print("    ⚠️  No trade data ingested yet")
    
    # 3. Summary
    print("\n" + "=" * 60)
    jsonl_ok = sum(1 for f in files if f["path"] and f["size_bytes"] > 0)
    total_eas = len(EA_NAMES)
    
    if jsonl_ok == 0:
        print("🔴 BLOCKED: No EA JSONL files with data found.")
        print("   → Add Oracle_Reporter.mqh to your EAs and trigger a trade/heartbeat.")
    elif db and not db["performance"] and not db["trades"]:
        print("🟡 PARTIAL: EAs are writing JSONL, but Oracle hasn't ingested yet.")
        print("   → Run: python oracle.py --ingest")
    else:
        print(f"🟢 HEALTHY: {jsonl_ok}/{total_eas} EAs reporting, Oracle has data.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
