import aiohttp
import yaml
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from core.models import TokenSignal

class SignalCollector:
    def __init__(self, settings_path: str = "config/settings.yaml"):
        with open(settings_path, 'r') as f:
            self.settings = yaml.safe_load(f)
        self.dex_url = self.settings['apis']['dexscreener_url']
        self.pump_url = self.settings['apis']['pump_fun_url']
        self.helius_key = self.settings['apis']['helius_api_key']
        self.helius_api = self.settings['apis']['helius_api_url']

    async def fetch_dexscreener_pairs(self) -> List[TokenSignal]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.dex_url) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
        pairs = data.get('pairs', [])
        signals = []
        now = datetime.now(timezone.utc)
        for p in pairs:
            if p.get('chainId') != 'solana':
                continue
            created = p.get('pairCreatedAt')
            if not created:
                continue
            created_dt = datetime.fromtimestamp(created / 1000, tz=timezone.utc)
            age_min = (now - created_dt).total_seconds() / 60.0
            if age_min < 0 or age_min > 180:
                continue
            vol = p.get('volume', {})
            txns = p.get('txns', {}).get('h1', {})
            liquidity = p.get('liquidity', {}).get('usd', 0) or 0
            market_cap = p.get('marketCap', 0) or p.get('fdv', 0) or 0
            price = p.get('priceUsd', 0) or 0
            price_change = p.get('priceChange', {}).get('h1', 0) or 0
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            ratio = buys / max(sells, 1)
            signals.append(TokenSignal(
                token_mint=p.get('baseToken', {}).get('address', ''),
                symbol=p.get('baseToken', {}).get('symbol', 'UNKNOWN'),
                pair_address=p.get('pairAddress', ''),
                dex_id=p.get('dexId', ''),
                pair_created_at=created_dt,
                age_minutes=age_min,
                price_usd=float(price),
                market_cap=float(market_cap),
                liquidity_usd=float(liquidity),
                volume_1h=float(vol.get('h1', 0) or 0),
                volume_24h=float(vol.get('h24', 0) or 0),
                price_change_1h=float(price_change),
                txns_1h_buys=int(buys),
                txns_1h_sells=int(sells),
                buy_sell_ratio=float(ratio),
                holder_count=None
            ))
        return signals

    async def fetch_pump_fun_coins(self) -> List[TokenSignal]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.pump_url, headers={'Accept': 'application/json'}) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
        signals = []
        now = datetime.now(timezone.utc)
        for coin in data:
            created = coin.get('created_timestamp')
            if not created:
                continue
            created_dt = datetime.fromtimestamp(created / 1000, tz=timezone.utc)
            age_min = (now - created_dt).total_seconds() / 60.0
            market_cap = coin.get('market_cap', 0) or 0
            price = coin.get('price', 0) or 0
            signals.append(TokenSignal(
                token_mint=coin.get('mint', ''),
                symbol=coin.get('symbol', 'UNKNOWN'),
                pair_address=coin.get('bonding_curve', ''),
                dex_id='pump.fun',
                pair_created_at=created_dt,
                age_minutes=age_min,
                price_usd=float(price),
                market_cap=float(market_cap),
                liquidity_usd=float(market_cap),
                volume_1h=0.0,
                volume_24h=0.0,
                price_change_1h=0.0,
                txns_1h_buys=0,
                txns_1h_sells=0,
                buy_sell_ratio=1.0,
                holder_count=coin.get('holder_count', None)
            ))
        return signals

    async def get_token_metrics(self, token_mint: str) -> Optional[TokenSignal]:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{token_mint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
        pairs = data.get('pairs', [])
        if not pairs:
            return None
        p = pairs[0]
        vol = p.get('volume', {})
        txns = p.get('txns', {}).get('h1', {})
        created = p.get('pairCreatedAt')
        created_dt = datetime.now(timezone.utc)
        if created:
            created_dt = datetime.fromtimestamp(created / 1000, tz=timezone.utc)
        age_min = (datetime.now(timezone.utc) - created_dt).total_seconds() / 60.0
        return TokenSignal(
            token_mint=p.get('baseToken', {}).get('address', token_mint),
            symbol=p.get('baseToken', {}).get('symbol', 'UNKNOWN'),
            pair_address=p.get('pairAddress', ''),
            dex_id=p.get('dexId', ''),
            pair_created_at=created_dt,
            age_minutes=age_min,
            price_usd=float(p.get('priceUsd', 0) or 0),
            market_cap=float(p.get('marketCap', 0) or p.get('fdv', 0) or 0),
            liquidity_usd=float(p.get('liquidity', {}).get('usd', 0) or 0),
            volume_1h=float(vol.get('h1', 0) or 0),
            volume_24h=float(vol.get('h24', 0) or 0),
            price_change_1h=float(p.get('priceChange', {}).get('h1', 0) or 0),
            txns_1h_buys=int(txns.get('buys', 0)),
            txns_1h_sells=int(txns.get('sells', 0)),
            buy_sell_ratio=float(txns.get('buys', 0) / max(txns.get('sells', 1), 1)),
            holder_count=None
        )

    async def fetch_helius_whale_txs(self, wallet: str, limit: int = 10) -> List[Dict[str, Any]]:
        if self.helius_key == "YOUR_HELIUS_API_KEY_HERE":
            return []
        url = f"{self.helius_api}/addresses/{wallet}/transactions?api-key={self.helius_key}&limit={limit}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return []
                return await resp.json()
