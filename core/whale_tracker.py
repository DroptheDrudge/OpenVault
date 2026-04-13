import yaml
from typing import List, Dict, Optional
from datetime import datetime, timezone
from collections import defaultdict
from core.models import WhaleSignal, WhaleConsensus
from core.signal_collector import SignalCollector

class WhaleTracker:
    def __init__(self, wallets_path: str = "config/wallets.yaml", settings_path: str = "config/settings.yaml"):
        with open(wallets_path, 'r') as f:
            data = yaml.safe_load(f)
        self.wallets = {w['address']: w.get('nickname', w['address'][:6]) for w in data.get('wallets', [])}
        with open(settings_path, 'r') as f:
            self.settings = yaml.safe_load(f)
        self.collector = SignalCollector(settings_path)

    async def fetch_whale_signals(self, token_mint: str) -> List[WhaleSignal]:
        signals = []
        for address, nickname in self.wallets.items():
            txs = await self.collector.fetch_helius_whale_txs(address, limit=20)
            for tx in txs:
                timestamp = tx.get('timestamp')
                if not timestamp:
                    continue
                tx_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                token_transfers = tx.get('tokenTransfers', [])
                for tt in token_transfers:
                    if tt.get('mint') != token_mint:
                        continue
                    from_addr = tt.get('fromUserAccount', '')
                    to_addr = tt.get('toUserAccount', '')
                    amount = float(tt.get('tokenAmount', 0))
                    sol_amount = 0.0
                    for nt in tx.get('nativeTransfers', []):
                        if nt.get('toUserAccount') == address or nt.get('fromUserAccount') == address:
                            sol_amount += float(nt.get('lamports', 0)) / 1e9
                    if to_addr == address:
                        signal_type = 'BUY'
                    elif from_addr == address:
                        signal_type = 'SELL'
                    else:
                        continue
                    price = sol_amount / max(amount, 1e-9)
                    signals.append(WhaleSignal(
                        wallet=address,
                        wallet_nickname=nickname,
                        token_mint=token_mint,
                        timestamp=tx_dt,
                        signal_type=signal_type,
                        amount_sol=sol_amount,
                        amount_token=amount,
                        price_usd=price
                    ))
        return signals

    def calculate_whale_consensus(self, token_mint: str, signals: List[WhaleSignal]) -> WhaleConsensus:
        buys = [s for s in signals if s.signal_type == 'BUY']
        sells = [s for s in signals if s.signal_type == 'SELL']
        unique_buyers = len({s.wallet for s in buys})
        buy_pressure = sum(s.amount_sol for s in buys)
        total = len(buys) + len(sells)
        consensus = 0.0
        if total > 0:
            consensus = (len(buys) / total) * 100
        if unique_buyers >= 2:
            consensus = min(100, consensus + unique_buyers * 10)
        return WhaleConsensus(
            token_mint=token_mint,
            total_whale_buys=len(buys),
            total_whale_sells=len(sells),
            unique_buyers=unique_buyers,
            buy_pressure_sol=buy_pressure,
            consensus_score=consensus
        )

    def detect_pattern(self, signals: List[WhaleSignal]) -> str:
        if not signals:
            return "NEUTRAL"
        buys = [s for s in signals if s.signal_type == 'BUY']
        sells = [s for s in signals if s.signal_type == 'SELL']
        buy_vol = sum(s.amount_sol for s in buys)
        sell_vol = sum(s.amount_sol for s in sells)
        if buy_vol > sell_vol * 2:
            return "ACCUMULATION"
        elif sell_vol > buy_vol * 2:
            return "DISTRIBUTION"
        return "MIXED"
