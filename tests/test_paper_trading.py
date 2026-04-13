import pytest
from datetime import datetime, timezone
from core.models import TokenSignal, WhaleConsensus, PaperTrade, Status, ExitReason
from core.paper_executor import PaperExecutor
from core.risk_manager import RiskManager
from core.momentum_scorer import MomentumScorer
from core.whale_tracker import WhaleTracker
from core.models import WhaleSignal

def test_slippage_calculation():
    pe = PaperExecutor()
    assert pe._slippage_pct(50_000) == pytest.approx(0.5 + 5.0)
    assert pe._slippage_pct(500_000) == pytest.approx(0.5 + 3.0)
    assert pe._slippage_pct(5_000_000) == pytest.approx(0.5 + 1.5)

def test_position_sizing_limits():
    rm = RiskManager()
    size = rm.calculate_position_size(100, 10.0, 50_000)
    assert size <= 10.0 * 0.20
    size2 = rm.calculate_position_size(100, 10.0, 50_000)
    assert size2 == pytest.approx(10.0 * 0.15 * 0.5, abs=1e-6)
    assert rm.can_open_position(4) is True
    assert rm.can_open_position(5) is False

def test_trailing_stop_logic():
    pe = PaperExecutor()
    trade = PaperTrade(
        trade_id="T1", token_mint="M1", token_symbol="SYM",
        entry_time=datetime.now(timezone.utc), entry_price_usd=1.0,
        sol_invested=1.0, tokens_received=100.0, tokens_remaining=100.0,
        slippage_pct=1.0, fees_sol=0.01, fees_usd=1.0,
        market_cap_at_entry=50_000, status=Status.OPEN,
        peak_price_usd=3.0
    )
    metrics = TokenSignal(
        token_mint="M1", symbol="SYM", pair_address="P1", dex_id="dex",
        pair_created_at=datetime.now(timezone.utc), age_minutes=10,
        price_usd=2.0, market_cap=50_000, liquidity_usd=10_000,
        volume_1h=1000, volume_24h=5000, price_change_1h=50,
        txns_1h_buys=10, txns_1h_sells=5, buy_sell_ratio=2.0
    )
    exits = pe.check_exits(trade, metrics)
    reasons = [e.reason for e in exits]
    assert ExitReason.TRAILING_STOP in reasons

    trade2 = PaperTrade(
        trade_id="T2", token_mint="M2", token_symbol="SYM2",
        entry_time=datetime.now(timezone.utc), entry_price_usd=1.0,
        sol_invested=1.0, tokens_received=100.0, tokens_remaining=100.0,
        slippage_pct=1.0, fees_sol=0.01, fees_usd=1.0,
        market_cap_at_entry=50_000, status=Status.OPEN,
        peak_price_usd=1.0
    )
    metrics2 = TokenSignal(
        token_mint="M2", symbol="SYM2", pair_address="P2", dex_id="dex",
        pair_created_at=datetime.now(timezone.utc), age_minutes=10,
        price_usd=0.85, market_cap=50_000, liquidity_usd=10_000,
        volume_1h=1000, volume_24h=5000, price_change_1h=-20,
        txns_1h_buys=5, txns_1h_sells=10, buy_sell_ratio=0.5
    )
    exits2 = pe.check_exits(trade2, metrics2)
    assert any(e.reason == ExitReason.HARD_STOP for e in exits2)

def test_whale_consensus_scoring():
    wt = WhaleTracker()
    signals = []
    for i in range(3):
        signals.append(WhaleSignal(
            wallet=f"W{i}", wallet_nickname=f"W{i}", token_mint="M1",
            timestamp=datetime.now(timezone.utc), signal_type="BUY",
            amount_sol=2.0, amount_token=100.0, price_usd=0.01
        ))
    consensus = wt.calculate_whale_consensus("M1", signals)
    assert consensus.consensus_score > 0
    assert consensus.unique_buyers == 3

def test_composite_score_range():
    ms = MomentumScorer()
    pair = TokenSignal(
        token_mint="M1", symbol="SYM", pair_address="P1", dex_id="dex",
        pair_created_at=datetime.now(timezone.utc), age_minutes=10,
        price_usd=1.0, market_cap=50_000, liquidity_usd=10_000,
        volume_1h=10000, volume_24h=2400, price_change_1h=50,
        txns_1h_buys=100, txns_1h_sells=10, buy_sell_ratio=10.0,
        holder_count=600
    )
    whale = WhaleConsensus(
        token_mint="M1", total_whale_buys=5, total_whale_sells=0,
        unique_buyers=4, buy_pressure_sol=20.0, consensus_score=100.0
    )
    score = ms.calculate_composite_score(pair, whale)
    assert 0 <= score <= 100
