import uuid
import yaml
import aiosqlite
from datetime import datetime, timezone
from typing import List, Optional
from core.models import PaperTrade, TokenSignal, ExitAction, ExitReason, Status
from pathlib import Path

class PaperExecutor:
    def __init__(self, settings_path: str = "config/settings.yaml"):
        with open(settings_path, 'r') as f:
            self.settings = yaml.safe_load(f)
        self.db_path = self.settings['paths']['db']
        self.fees = self.settings['fees']
        self.slippage = self.settings['slippage']
        self.exit_cfg = self.settings['exit_strategy']

    def _slippage_pct(self, market_cap: float) -> float:
        base = self.slippage['base_pct']
        if market_cap < 100_000:
            return base + self.slippage['mc_under_100k']
        elif market_cap < 1_000_000:
            return base + self.slippage['mc_100k_to_1m']
        else:
            return base + self.slippage['mc_over_1m']

    def simulate_buy(self, token_mint: str, token_symbol: str, sol_amount: float, price_usd: float, market_cap: float) -> PaperTrade:
        slip = self._slippage_pct(market_cap)
        effective_price = price_usd * (1 + slip / 100)
        jup_fee_sol = sol_amount * self.fees['jupiter_fee_pct']
        tx_cost_sol = self.fees['sol_tx_cost_sol']
        total_fees_sol = jup_fee_sol + tx_cost_sol
        net_sol = sol_amount - total_fees_sol
        tokens = net_sol * self.settings['wallet']['sol_price_usd'] / max(effective_price, 1e-9)
        trade = PaperTrade(
            trade_id=str(uuid.uuid4())[:8],
            token_mint=token_mint,
            token_symbol=token_symbol,
            entry_time=datetime.now(timezone.utc),
            entry_price_usd=price_usd,
            sol_invested=sol_amount,
            tokens_received=tokens,
            tokens_remaining=tokens,
            slippage_pct=slip,
            fees_sol=total_fees_sol,
            fees_usd=total_fees_sol * self.settings['wallet']['sol_price_usd'],
            market_cap_at_entry=market_cap,
            peak_price_usd=price_usd
        )
        return trade

    async def record_buy(self, trade: PaperTrade):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO paper_trades (trade_id, token_mint, entry_time, entry_price_usd, sol_invested,
                tokens_received, tokens_remaining, slippage_pct, fees_sol, fees_usd, status,
                market_cap_at_entry, realized_pnl_sol, realized_pnl_pct, peak_price_usd)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                trade.trade_id, trade.token_mint, trade.entry_time.isoformat(), trade.entry_price_usd,
                trade.sol_invested, trade.tokens_received, trade.tokens_remaining, trade.slippage_pct,
                trade.fees_sol, trade.fees_usd, trade.status.value, trade.market_cap_at_entry,
                trade.realized_pnl_sol, trade.realized_pnl_pct, trade.peak_price_usd
            ))
            await db.commit()

    async def get_open_positions(self) -> List[PaperTrade]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            rows = await db.execute("SELECT * FROM paper_trades WHERE status IN (?,?)", (Status.OPEN.value, Status.PARTIAL_EXIT.value))
            rows = await rows.fetchall()
        trades = []
        for r in rows:
            trades.append(PaperTrade(**{k: r[k] for k in r.keys()}))
        return trades

    async def simulate_sell(self, trade_id: str, action: ExitAction) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            row = await (await db.execute("SELECT * FROM paper_trades WHERE trade_id=?", (trade_id,))).fetchone()
            if not row:
                return False
            trade = PaperTrade(**{k: row[k] for k in row.keys()})
            if trade.status == Status.CLOSED:
                return False
            sell_tokens = trade.tokens_remaining * action.percent
            if sell_tokens <= 1e-9:
                return False
            slip = self._slippage_pct(trade.market_cap_at_entry)
            effective_price = action.price_usd * (1 - slip / 100)
            usd_received = sell_tokens * effective_price
            sol_received = usd_received / self.settings['wallet']['sol_price_usd']
            tx_cost = self.fees['sol_tx_cost_sol']
            net_sol = sol_received - tx_cost
            entry_sol_for_tokens = trade.sol_invested * (sell_tokens / trade.tokens_received)
            pnl_sol = net_sol - entry_sol_for_tokens
            pnl_pct = pnl_sol / entry_sol_for_tokens if entry_sol_for_tokens > 0 else 0

            new_remaining = trade.tokens_remaining - sell_tokens
            new_status = Status.PARTIAL_EXIT if new_remaining > 1e-9 else Status.CLOSED

            tp1_hit = trade.tp1_hit or (action.reason == ExitReason.TP1)
            tp2_hit = trade.tp2_hit or (action.reason == ExitReason.TP2)

            await db.execute("""
                UPDATE paper_trades SET tokens_remaining=?, realized_pnl_sol=realized_pnl_sol+?,
                realized_pnl_pct=?, status=?, exit_time=?, exit_price_usd=?, exit_reason=?,
                tp1_hit=?, tp2_hit=? WHERE trade_id=?
            """, (new_remaining, pnl_sol, pnl_pct, new_status.value,
                  datetime.now(timezone.utc).isoformat(), action.price_usd, action.reason.value,
                  tp1_hit, tp2_hit, trade_id))
            await db.commit()
            return True

    async def get_cash_available(self) -> float:
        async with aiosqlite.connect(self.db_path) as db:
            row = await (await db.execute("SELECT SUM(realized_pnl_sol) FROM paper_trades")).fetchone()
            realized = row[0] or 0.0
            row2 = await (await db.execute("SELECT SUM(sol_invested * (tokens_remaining / tokens_received)) FROM paper_trades WHERE status IN (?,?)", (Status.OPEN.value, Status.PARTIAL_EXIT.value))).fetchone()
            invested = row2[0] or 0.0
        return self.settings['wallet']['initial_sol'] + realized - invested

    async def get_portfolio_value(self) -> float:
        cash = await self.get_cash_available()
        positions = await self.get_open_positions()
        total = cash
        for t in positions:
            total += t.sol_invested * (t.tokens_remaining / t.tokens_received)
        return total

    async def update_peak_price(self, trade_id: str, price: float):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE paper_trades SET peak_price_usd = MAX(COALESCE(peak_price_usd,0), ?) WHERE trade_id=?", (price, trade_id))
            await db.commit()

    def check_exits(self, trade: PaperTrade, metrics: TokenSignal) -> List[ExitAction]:
        exits = []
        if trade.status == Status.CLOSED:
            return exits
        current_price = metrics.price_usd
        entry_price = trade.entry_price_usd
        if entry_price <= 0:
            return exits
        peak = trade.peak_price_usd or entry_price
        peak_profit_pct = (peak - entry_price) / entry_price if entry_price > 0 else 0
        profit_pct = (current_price - entry_price) / entry_price

        if not trade.tp1_hit and profit_pct >= self.exit_cfg['tp1_profit_pct']:
            exits.append(ExitAction(percent=self.exit_cfg['tp1_sell_pct'], reason=ExitReason.TP1, price_usd=current_price))

        if not trade.tp2_hit and profit_pct >= self.exit_cfg['tp2_profit_pct']:
            exits.append(ExitAction(percent=self.exit_cfg['tp2_sell_pct'], reason=ExitReason.TP2, price_usd=current_price))

        if peak_profit_pct >= self.exit_cfg['trailing_start_profit_pct']:
            trailing_price = peak * (1 - self.exit_cfg['trailing_drop_pct'])
            hard_stop = entry_price * (1 - self.exit_cfg['hard_stop_loss_pct'])
            trailing_price = max(trailing_price, hard_stop)
            if current_price <= trailing_price:
                remaining_pct = trade.tokens_remaining / trade.tokens_received
                exits.append(ExitAction(percent=remaining_pct, reason=ExitReason.TRAILING_STOP, price_usd=current_price))
        elif profit_pct <= -self.exit_cfg['hard_stop_loss_pct']:
            remaining_pct = trade.tokens_remaining / trade.tokens_received
            exits.append(ExitAction(percent=remaining_pct, reason=ExitReason.HARD_STOP, price_usd=current_price))

        age_min = (datetime.now(timezone.utc) - trade.entry_time).total_seconds() / 60.0
        if age_min >= self.exit_cfg['time_stop_minutes'] and profit_pct > 0:
            remaining_pct = trade.tokens_remaining / trade.tokens_received
            exits.append(ExitAction(percent=remaining_pct, reason=ExitReason.TIME_STOP, price_usd=current_price))

        return exits
