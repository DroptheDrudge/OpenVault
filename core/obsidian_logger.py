import os
from datetime import datetime, timezone, date
from pathlib import Path
from typing import Dict, Any
import yaml
from core.models import PaperTrade, TokenSignal, ExitAction

class ObsidianLogger:
    def __init__(self, settings_path: str = "config/settings.yaml"):
        with open(settings_path, 'r') as f:
            self.settings = yaml.safe_load(f)
        self.daily_dir = Path(self.settings['paths']['obsidian_daily'])
        self.trades_dir = Path(self.settings['paths']['obsidian_trades'])
        self.ensure_dirs()

    def ensure_dirs(self):
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.trades_dir.mkdir(parents=True, exist_ok=True)

    def log_entry(self, trade: PaperTrade, pair: TokenSignal):
        path = self.trades_dir / f"{trade.trade_id}.md"
        content = f"""# Trade Entry: {trade.token_symbol}

| Field | Value |
|-------|-------|
| Trade ID | {trade.trade_id} |
| Token | {trade.token_mint} |
| Symbol | {trade.token_symbol} |
| Entry Time | {trade.entry_time.isoformat()} |
| Entry Price | ${trade.entry_price_usd:.8f} |
| Market Cap | ${pair.market_cap:,.0f} |
| SOL Invested | {trade.sol_invested:.4f} SOL |
| Tokens Received | {trade.tokens_received:.4f} |
| Slippage | {trade.slippage_pct:.2f}% |
| Fees (SOL) | {trade.fees_sol:.6f} |
| Status | {trade.status.value} |

## Context
- Pair: {pair.pair_address}
- DEX: {pair.dex_id}
- Age: {pair.age_minutes:.1f} minutes
- Liquidity: ${pair.liquidity_usd:,.0f}
- Buy/Sell Ratio: {pair.buy_sell_ratio:.2f}
"""
        path.write_text(content, encoding='utf-8')

    def log_exit(self, trade: PaperTrade, action: ExitAction):
        path = self.trades_dir / f"{trade.trade_id}.md"
        existing = path.read_text(encoding='utf-8') if path.exists() else ""
        exit_block = f"""

## Exit: {action.reason.value}
- Time: {datetime.now(timezone.utc).isoformat()}
- Price: ${action.price_usd:.8f}
- Percent Sold: {action.percent*100:.1f}%
- Realized PnL SOL: {trade.realized_pnl_sol:.6f}
- Realized PnL %: {trade.realized_pnl_pct*100:.2f}%
- Status: {trade.status.value}
"""
        path.write_text(existing + exit_block, encoding='utf-8')

    def generate_daily_report(self, performance: Dict[str, Any]):
        today = date.today().isoformat()
        path = self.daily_dir / f"{today}.md"
        content = f"""# Daily Report: {today}

## Performance Snapshot
| Metric | Value |
|--------|-------|
| Starting SOL | {performance.get('starting_sol', 0):.4f} |
| Ending SOL | {performance.get('ending_sol', 0):.4f} |
| Total PnL SOL | {performance.get('total_pnl_sol', 0):.4f} |
| Total PnL % | {performance.get('total_pnl_pct', 0)*100:.2f}% |
| Trades | {performance.get('trades_count', 0)} |
| Wins | {performance.get('win_count', 0)} |
| Losses | {performance.get('loss_count', 0)} |
| Win Rate | {performance.get('win_rate', 0)*100:.2f}% |
| Avg Win % | {performance.get('avg_win_pct', 0)*100:.2f}% |
| Avg Loss % | {performance.get('avg_loss_pct', 0)*100:.2f}% |
| Profit Factor | {performance.get('profit_factor', 0):.2f} |
| Max Drawdown % | {performance.get('max_drawdown_pct', 0)*100:.2f}% |
"""
        path.write_text(content, encoding='utf-8')
