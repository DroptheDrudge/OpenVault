# Oracle MQL5 Integration — Quick Start

## Files

| File | Purpose |
|------|---------|
| `oracle_mql5_reporter.mqh` | Drop-in MQL5 header for all Forex Garage EAs |
| `oracle_pipeline_diagnostic.py` | Windows diagnostic script to verify data flow |

## Step 1: Add Reporter to EAs

Copy `oracle_mql5_reporter.mqh` to:
```
MetaEditor/MQL5/Include/Oracle_Reporter.mqh
```

Add to each EA's `.mq5` file:

```mql5
#include <Oracle_Reporter.mqh>

int OnInit()
{
   OracleReporterInit("ferrari_ea");  // Use exact neuron_id from oracle/config/oracle.yaml
   return(INIT_SUCCEEDED);
}

void OnTrade()
{
   // ... your trade logic ...
   OracleReportTrade(
      _Symbol,
      PositionGetDouble(POSITION_PRICE_OPEN),
      PositionGetDouble(POSITION_PRICE_CURRENT),
      PositionGetDouble(POSITION_VOLUME),
      OrderProfit(),
      CurrentRegime(),  // your regime detection function
      "tp_hit"
   );
}

void OnTick()
{
   // Heartbeat once per hour
   static datetime last_heartbeat = 0;
   if(TimeCurrent() - last_heartbeat >= 3600)
   {
      OracleReportHeartbeat(CurrentRegime());
      last_heartbeat = TimeCurrent();
   }
}
```

## Step 2: Verify Data Flow

Run the diagnostic script:
```powershell
cd C:\Kimi_EAs
python oracle_pipeline_diagnostic.py
```

## Step 3: Ingest to Oracle

```powershell
cd C:\Kimi_EAs\oracle
python oracle.py --ingest
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No JSONL files found | EAs need `Oracle_Reporter.mqh` included and compiled |
| JSONL exists but 0 bytes | No trades/heartbeats fired yet — wait or force heartbeat |
| Oracle ingest shows 0 rows | Check `config/oracle.yaml` paths match your Terminal folders |
| File locked during ingest | Normal — Oracle skips locked files and retries next cycle |
