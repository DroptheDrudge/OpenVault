import asyncio
import yaml
import aiosqlite
from datetime import datetime, timezone, date
from pathlib import Path
from core.database import init_db
from core.signal_collector import SignalCollector
from core.whale_tracker import WhaleTracker
from core.momentum_scorer import MomentumScorer
from core.paper_executor import PaperExecutor
from core.risk_manager import RiskManager
from core.obsidian_logger import ObsidianLogger
from core.models import PaperTrade, Status

async def calculate_daily_performance(executor: PaperExecutor, settings: dict) -> dict:
    today = date.today().isoformat()
    async with aiosqlite.connect(settings['paths']['db']) as db:
        row = await (await db.execute("""
            SELECT SUM(realized_pnl_sol), COUNT(*), SUM(CASE WHEN realized_pnl_sol>0 THEN 1 ELSE 0 END),
            SUM(CASE WHEN realized_pnl_sol<0 THEN 1 ELSE 0 END),
            AVG(CASE WHEN realized_pnl_sol>0 THEN realized_pnl_pct END),
            AVG(CASE WHEN realized_pnl_sol<0 THEN realized_pnl_pct END)
            FROM paper_trades WHERE date(entry_time)=?
        """, (today,))).fetchone()
    total_pnl = row[0] or 0.0
    trades = row[1] or 0
    wins = row[2] or 0
    losses = row[3] or 0
    avg_win = row[4] or 0.0
    avg_loss = row[5] or 0.0
    win_rate = wins / trades if trades > 0 else 0.0
    profit_factor = (wins * avg_win) / max(losses * abs(avg_loss), 1e-9)
    starting = settings['wallet']['initial_sol']
    ending = starting + total_pnl
    return {
        'starting_sol': starting,
        'ending_sol': ending,
        'total_pnl_sol': total_pnl,
        'total_pnl_pct': total_pnl / starting if starting > 0 else 0,
        'trades_count': trades,
        'win_count': wins,
        'loss_count': losses,
        'win_rate': win_rate,
        'avg_win_pct': avg_win,
        'avg_loss_pct': avg_loss,
        'profit_factor': profit_factor,
        'max_drawdown_pct': 0.0
    }

async def main_loop():
    await init_db()
    with open('config/settings.yaml', 'r') as f:
        settings = yaml.safe_load(f)
    collector = SignalCollector()
    whale_tracker = WhaleTracker()
    scorer = MomentumScorer()
    executor = PaperExecutor()
    risk = RiskManager()
    logger = ObsidianLogger()
    last_report_date = None

    print("🚀 Meme Sniper Bot starting...")
    print("=" * 50)
    
    while True:
        try:
            now = datetime.now(timezone.utc)
            open_positions = await executor.get_open_positions()
            
            print(f"\n⏰ {now.strftime('%H:%M:%S')} | Portfolio: {await executor.get_portfolio_value():.3f} SOL | Open: {len(open_positions)}")

            # 1. Check exits
            for pos in open_positions:
                metrics = await collector.get_token_metrics(pos.token_mint)
                if not metrics:
                    continue
                await executor.update_peak_price(pos.trade_id, metrics.price_usd)
                
                async with aiosqlite.connect(settings['paths']['db']) as db:
                    db.row_factory = aiosqlite.Row
                    fresh = await (await db.execute("SELECT * FROM paper_trades WHERE trade_id=?", (pos.trade_id,))).fetchone()
                if not fresh:
                    continue
                fresh_pos = PaperTrade(**{k: fresh[k] for k in fresh.keys()})
                exits = executor.check_exits(fresh_pos, metrics)
                for exit_action in exits:
                    success = await executor.simulate_sell(fresh_pos.trade_id, exit_action)
                    if success:
                        async with aiosqlite.connect(settings['paths']['db']) as db:
                            db.row_factory = aiosqlite.Row
                            r = await (await db.execute("SELECT * FROM paper_trades WHERE trade_id=?", (fresh_pos.trade_id,))).fetchone()
                            updated_trade = PaperTrade(**{k: r[k] for k in r.keys()})
                        logger.log_exit(updated_trade, exit_action)
                        print(f"  📤 EXIT {updated_trade.token_symbol}: {exit_action.reason.value} at ${metrics.price_usd:.6f}")

            # 2. New entries
            open_positions = await executor.get_open_positions()
            if risk.can_open_position(len(open_positions)):
                dex_signals = await collector.fetch_dexscreener_pairs()
                pump_signals = await collector.fetch_pump_fun_coins()
                seen = set()
                all_signals = []
                for s in dex_signals + pump_signals:
                    if s.token_mint in seen:
                        continue
                    seen.add(s.token_mint)
                    all_signals.append(s)

                for pair in all_signals:
                    if not scorer.meets_entry_criteria(pair):
                        continue
                    whale_signals = await whale_tracker.fetch_whale_signals(pair.token_mint)
                    consensus = whale_tracker.calculate_whale_consensus(pair.token_mint, whale_signals)
                    score = scorer.calculate_composite_score(pair, consensus)
                    if score >= settings['scoring']['min_score']:
                        available_sol = await executor.get_cash_available()
                        size = risk.calculate_position_size(score, available_sol, pair.market_cap)
                        if size > 0.001:
                            trade = executor.simulate_buy(pair.token_mint, pair.symbol, size, pair.price_usd, pair.market_cap)
                            await executor.record_buy(trade)
                            logger.log_entry(trade, pair)
                            print(f"  🎯 ENTRY {trade.token_symbol}: {trade.sol_invested:.4f} SOL @ ${pair.price_usd:.6f} (score {score})")

            # 4. Daily report at midnight
            today = date.today()
            if last_report_date != today and now.hour == 0 and now.minute < 1:
                perf = await calculate_daily_performance(executor, settings)
                logger.generate_daily_report(perf)
                last_report_date = today
                print(f"  📄 Daily report generated for {today}")

        except Exception as e:
            print(f"❌ Error: {e}")
        
        await asyncio.sleep(settings['loop']['interval_seconds'])

if __name__ == "__main__":
    asyncio.run(main_loop())
