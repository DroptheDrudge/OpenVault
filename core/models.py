from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    OPEN = "OPEN"
    PARTIAL_EXIT = "PARTIAL_EXIT"
    CLOSED = "CLOSED"

class ExitReason(str, Enum):
    TP1 = "TP1"
    TP2 = "TP2"
    TRAILING_STOP = "TRAILING_STOP"
    TIME_STOP = "TIME_STOP"
    WHALE_EXIT = "WHALE_EXIT"
    HARD_STOP = "HARD_STOP"
    UNKNOWN = "UNKNOWN"

class TokenSignal(BaseModel):
    token_mint: str
    symbol: str
    pair_address: str
    dex_id: str
    pair_created_at: datetime
    age_minutes: float
    price_usd: float
    market_cap: float
    liquidity_usd: float
    volume_1h: float
    volume_24h: float
    price_change_1h: float
    txns_1h_buys: int
    txns_1h_sells: int
    buy_sell_ratio: float
    momentum_score: Optional[float] = None
    composite_score: Optional[float] = None
    holder_count: Optional[int] = None

class PaperTrade(BaseModel):
    trade_id: str
    token_mint: str
    token_symbol: str
    entry_time: datetime
    exit_time: Optional[datetime] = None
    entry_price_usd: float
    exit_price_usd: Optional[float] = None
    sol_invested: float
    tokens_received: float
    tokens_remaining: float
    slippage_pct: float
    fees_sol: float
    fees_usd: float
    status: Status = Status.OPEN
    tp1_hit: bool = False
    tp2_hit: bool = False
    trailing_stop_price: Optional[float] = None
    market_cap_at_entry: float
    whale_signals_at_entry: Optional[str] = None
    realized_pnl_sol: float = 0.0
    realized_pnl_pct: float = 0.0
    exit_reason: Optional[str] = None
    peak_price_usd: Optional[float] = None

class WhaleSignal(BaseModel):
    wallet: str
    wallet_nickname: Optional[str] = None
    token_mint: str
    timestamp: datetime
    signal_type: str
    amount_sol: float
    amount_token: float
    price_usd: float
    token_age_at_signal: Optional[float] = None
    market_cap_at_signal: Optional[float] = None

class WhaleConsensus(BaseModel):
    token_mint: str
    total_whale_buys: int = 0
    total_whale_sells: int = 0
    unique_buyers: int = 0
    buy_pressure_sol: float = 0.0
    consensus_score: float = 0.0

class ExitAction(BaseModel):
    percent: float
    reason: ExitReason
    price_usd: float
