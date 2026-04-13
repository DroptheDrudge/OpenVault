import yaml
from typing import Optional
from core.models import TokenSignal, WhaleConsensus

class MomentumScorer:
    def __init__(self, settings_path: str = "config/settings.yaml"):
        with open(settings_path, 'r') as f:
            self.settings = yaml.safe_load(f)
        self.weights = self.settings['scoring']['weights']
        self.entry = self.settings['entry_criteria']

    def meets_entry_criteria(self, pair: TokenSignal) -> bool:
        return (
            self.entry['min_age_minutes'] <= pair.age_minutes <= self.entry['max_age_minutes']
            and pair.liquidity_usd >= self.entry['min_liquidity_usd']
            and self.entry['min_market_cap_usd'] <= pair.market_cap <= self.entry['max_market_cap_usd']
        )

    def calculate_composite_score(self, pair: TokenSignal, whale: WhaleConsensus) -> float:
        vol_24h_avg = pair.volume_24h / 24.0 if pair.volume_24h > 0 else 1.0
        vol_accel = min(pair.volume_1h / max(vol_24h_avg, 1e-9), 10.0)
        vol_score = min(vol_accel / 10.0 * 100, 100)

        price_vel = max(min(pair.price_change_1h, 100.0), -100.0)
        price_score = (price_vel + 100) / 2.0

        whale_count_score = min(whale.unique_buyers * 25, 100)
        whale_pressure_score = min(whale.buy_pressure_sol / 10.0 * 100, 100)
        holder_score = min((pair.holder_count or 0) / 500.0 * 100, 100)

        bs = max(min(pair.buy_sell_ratio, 5.0), 0.2)
        bs_score = ((bs - 0.2) / (5.0 - 0.2)) * 100

        composite = (
            vol_score * self.weights['volume_acceleration'] +
            price_score * self.weights['price_velocity'] +
            whale_count_score * self.weights['whale_count'] +
            whale_pressure_score * self.weights['whale_buy_pressure'] +
            holder_score * self.weights['holder_growth'] +
            bs_score * self.weights['buy_sell_ratio']
        )
        return round(max(0.0, min(100.0, composite)), 2)
