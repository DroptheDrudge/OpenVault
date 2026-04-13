import yaml
from core.models import TokenSignal

class RiskManager:
    def __init__(self, settings_path: str = "config/settings.yaml"):
        with open(settings_path, 'r') as f:
            self.settings = yaml.safe_load(f)
        self.wallet = self.settings['wallet']
        self.sizing = self.settings['position_sizing']

    def can_open_position(self, current_open_count: int) -> bool:
        return current_open_count < self.wallet['max_concurrent_positions']

    def calculate_position_size(self, score: float, available_sol: float, market_cap: float) -> float:
        min_pct = self.sizing['base_min_pct']
        max_pct = self.sizing['base_max_pct']
        score_factor = (score - 60) / 40.0
        base_pct = min_pct + (max_pct - min_pct) * max(0.0, min(1.0, score_factor))
        if market_cap < 100_000:
            mult = self.sizing['mc_under_100k_multiplier']
        elif market_cap < 1_000_000:
            mult = self.sizing['mc_100k_to_1m_multiplier']
        else:
            mult = 1.0
        size = available_sol * base_pct * mult
        max_size = available_sol * self.wallet['max_position_pct']
        return round(min(size, max_size), 6)
