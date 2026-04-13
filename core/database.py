import aiosqlite
from pathlib import Path

DB_PATH = Path("data/meme_sniper.db")

async def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS tokens (
                mint TEXT PRIMARY KEY,
                symbol TEXT,
                name TEXT,
                created_at TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY,
                token_mint TEXT,
                timestamp TIMESTAMP,
                price_usd REAL,
                volume_1h REAL,
                market_cap REAL,
                holder_count INTEGER
            );
            CREATE TABLE IF NOT EXISTS paper_trades (
                trade_id TEXT PRIMARY KEY,
                token_mint TEXT,
                entry_time TIMESTAMP,
                exit_time TIMESTAMP,
                entry_price_usd REAL,
                exit_price_usd REAL,
                sol_invested REAL,
                tokens_received REAL,
                tokens_remaining REAL,
                realized_pnl_sol REAL DEFAULT 0.0,
                realized_pnl_pct REAL DEFAULT 0.0,
                status TEXT,
                exit_reason TEXT,
                slippage_pct REAL,
                fees_sol REAL,
                fees_usd REAL,
                tp1_hit BOOLEAN DEFAULT 0,
                tp2_hit BOOLEAN DEFAULT 0,
                trailing_stop_price REAL,
                peak_price_usd REAL,
                market_cap_at_entry REAL,
                whale_signals_at_entry TEXT
            );
            CREATE TABLE IF NOT EXISTS whale_transactions (
                id INTEGER PRIMARY KEY,
                wallet TEXT,
                token_mint TEXT,
                timestamp TIMESTAMP,
                tx_type TEXT,
                amount_sol REAL,
                amount_token REAL,
                price_usd REAL,
                signature TEXT UNIQUE
            );
            CREATE TABLE IF NOT EXISTS daily_performance (
                date DATE PRIMARY KEY,
                starting_sol REAL,
                ending_sol REAL,
                total_pnl_sol REAL,
                total_pnl_pct REAL,
                trades_count INTEGER,
                win_count INTEGER,
                loss_count INTEGER,
                win_rate REAL,
                avg_win_pct REAL,
                avg_loss_pct REAL,
                profit_factor REAL,
                max_drawdown_pct REAL
            );
        """)
        await db.commit()
