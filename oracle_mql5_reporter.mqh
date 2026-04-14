//+------------------------------------------------------------------+
//| Oracle_Reporter.mqh — Drop-in header for all Forex Garage EAs    |
//| Writes JSONL logs that Performance Oracle ingests live             |
//+------------------------------------------------------------------+
#ifndef ORACLE_REPORTER_MQH
#define ORACLE_REPORTER_MQH

#include <StdLibH>
#include <String>

//--- Config
string ORACLE_REPORT_DIR = "EA_Reports/";
int    ORACLE_REPORT_HANDLE = INVALID_HANDLE;
string ORACLE_EA_NAME = "";

//+------------------------------------------------------------------+
//| Initialize reporter with EA name                                 |
//+------------------------------------------------------------------+
void OracleReporterInit(string ea_name)
{
   ORACLE_EA_NAME = ea_name;
   string filepath = ORACLE_REPORT_DIR + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + "_" + ORACLE_EA_NAME + ".jsonl";
   
   // Ensure directory exists
   long search = FileFindFirst(ORACLE_REPORT_DIR + "*", filepath);
   if(search == INVALID_HANDLE)
      FolderCreate(ORACLE_REPORT_DIR);
   else
      FileFindClose(search);
}

//+------------------------------------------------------------------+
//| Report trade event to Oracle                                     |
//+------------------------------------------------------------------+
void OracleReportTrade(string symbol, double entry, double exit_price, double lots, double pnl, string regime, string exit_reason)
{
   string filepath = ORACLE_REPORT_DIR + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + "_" + ORACLE_EA_NAME + ".jsonl";
   int handle = FileOpen(filepath, FILE_WRITE|FILE_READ|FILE_TXT|FILE_SHARE_WRITE|FILE_COMMON);
   
   if(handle == INVALID_HANDLE) return;
   
   FileSeek(handle, 0, SEEK_END);
   
   double pnl_pct = (entry != 0) ? ((exit_price - entry) / entry) * 100.0 : 0.0;
   if(StringFind(_Symbol, "JPY") != -1) pnl_pct = pnl_pct * 100.0; // JPY pairs adjustment if needed
   
   string timestamp = TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS);
   StringReplace(timestamp, ".", "-");
   
   string json = StringFormat(
      "{\"timestamp\":\"%s\",\"ea\":\"%s\",\"action\":\"trade_closed\",\"symbol\":\"%s\",\"entry\":%.5f,\"exit\":%.5f,\"lots\":%.2f,\"pnl\":%.2f,\"pnl_pct\":%.4f,\"regime\":\"%s\",\"exit_reason\":\"%s\",\"balance\":%.2f,\"equity\":%.2f,\"open_positions\":%d}\n",
      timestamp, ORACLE_EA_NAME, symbol, entry, exit_price, lots, pnl, pnl_pct, regime, exit_reason,
      AccountInfoDouble(ACCOUNT_BALANCE), AccountInfoDouble(ACCOUNT_EQUITY), PositionsTotal()
   );
   
   FileWriteString(handle, json);
   FileClose(handle);
}

//+------------------------------------------------------------------+
//| Report heartbeat / daily metrics to Oracle                       |
//+------------------------------------------------------------------+
void OracleReportHeartbeat(string regime)
{
   string filepath = ORACLE_REPORT_DIR + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + "_" + ORACLE_EA_NAME + ".jsonl";
   int handle = FileOpen(filepath, FILE_WRITE|FILE_READ|FILE_TXT|FILE_SHARE_WRITE|FILE_COMMON);
   
   if(handle == INVALID_HANDLE) return;
   
   FileSeek(handle, 0, SEEK_END);
   
   string timestamp = TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS);
   StringReplace(timestamp, ".", "-");
   
   string json = StringFormat(
      "{\"timestamp\":\"%s\",\"ea\":\"%s\",\"action\":\"heartbeat\",\"regime\":\"%s\",\"balance\":%.2f,\"equity\":%.2f,\"open_positions\":%d}\n",
      timestamp, ORACLE_EA_NAME, regime,
      AccountInfoDouble(ACCOUNT_BALANCE), AccountInfoDouble(ACCOUNT_EQUITY), PositionsTotal()
   );
   
   FileWriteString(handle, json);
   FileClose(handle);
}

//+------------------------------------------------------------------+
//| Report signal / analysis event (analysis-only EAs like Stallion) |
//+------------------------------------------------------------------+
void OracleReportSignal(string symbol, string direction, string regime, double confidence, string reason)
{
   string filepath = ORACLE_REPORT_DIR + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + "_" + ORACLE_EA_NAME + ".jsonl";
   int handle = FileOpen(filepath, FILE_WRITE|FILE_READ|FILE_TXT|FILE_SHARE_WRITE|FILE_COMMON);
   
   if(handle == INVALID_HANDLE) return;
   
   FileSeek(handle, 0, SEEK_END);
   
   string timestamp = TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS);
   StringReplace(timestamp, ".", "-");
   
   string json = StringFormat(
      "{\"timestamp\":\"%s\",\"ea\":\"%s\",\"action\":\"signal\",\"symbol\":\"%s\",\"direction\":\"%s\",\"regime\":\"%s\",\"confidence\":%.4f,\"reason\":\"%s\",\"balance\":%.2f,\"equity\":%.2f}\n",
      timestamp, ORACLE_EA_NAME, symbol, direction, regime, confidence, reason,
      AccountInfoDouble(ACCOUNT_BALANCE), AccountInfoDouble(ACCOUNT_EQUITY)
   );
   
   FileWriteString(handle, json);
   FileClose(handle);
}

#endif
