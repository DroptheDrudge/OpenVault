import numpy as np
import pandas as pd
from typing import Tuple, Optional
from hmmlearn import hmm
import joblib
import json


class HMMRegimeTrainer:
    """
    Train a Gaussian HMM for market regime detection.
    Designed for integration with MQL5 EAs via parameter export.
    """
    
    def __init__(self, n_regimes: int = 3, random_state: int = 42):
        self.n_regimes = n_regimes
        self.random_state = random_state
        self.model = None
        self.feature_names = None
        
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer regime features from OHLCV data.
        
        Expected columns: open, high, low, close, volume
        """
        df = df.copy()
        
        # Returns
        df['returns'] = df['close'].pct_change()
        
        # Volatility (rolling std of returns)
        df['volatility'] = df['returns'].rolling(window=20).std()
        
        # ATR-like range
        df['range'] = (df['high'] - df['low']) / df['close']
        
        # Volume anomaly
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        
        # Trend strength (price vs MA)
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['trend_strength'] = (df['close'] - df['ma20']) / df['ma20']
        
        # Select features for HMM
        features = ['returns', 'volatility', 'range', 'volume_ratio', 'trend_strength']
        df = df.dropna()
        
        self.feature_names = features
        return df[features]
    
    def fit(self, X: np.ndarray) -> 'HMMRegimeTrainer':
        """Fit the HMM model."""
        self.model = hmm.GaussianHMM(
            n_components=self.n_regimes,
            covariance_type="diag",  # Simpler, more robust, easier to export
            n_iter=100,
            random_state=self.random_state,
            init_params="ste",  # Initialize start prob, transmat, means
            params="ste"
        )
        
        # Set better initialization to avoid convergence issues
        self.model.means_ = np.zeros((self.n_regimes, X.shape[1]))
        
        self.model.fit(X)
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict hidden states."""
        return self.model.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict state probabilities."""
        return self.model.predict_proba(X)
    
    def get_regime_labels(self, X: np.ndarray) -> dict:
        """
        Automatically label regimes based on their mean characteristics.
        Returns a mapping: state_index -> regime_name
        """
        means = self.model.means_
        labels = {}
        
        # Use returns and volatility to label
        returns_idx = self.feature_names.index('returns') if 'returns' in self.feature_names else 0
        vol_idx = self.feature_names.index('volatility') if 'volatility' in self.feature_names else 1
        
        for i in range(self.n_regimes):
            ret = means[i, returns_idx]
            vol = means[i, vol_idx]
            
            if vol > np.percentile(means[:, vol_idx], 66):
                labels[i] = "high_vol"
            elif ret > np.percentile(means[:, returns_idx], 60):
                labels[i] = "trend_up"
            elif ret < np.percentile(means[:, returns_idx], 40):
                labels[i] = "trend_down"
            else:
                labels[i] = "range"
                
        return labels
    
    def export_to_json(self, filepath: str):
        """Export model parameters to JSON for MQL5 consumption."""
        labels = self.get_regime_labels(self.model.means_)
        
        export = {
            "n_regimes": self.n_regimes,
            "n_features": len(self.feature_names),
            "feature_names": self.feature_names,
            "start_prob": self.model.startprob_.tolist(),
            "transmat": self.model.transmat_.tolist(),
            "means": self.model.means_.tolist(),
            "covars": self.model.covars_.tolist(),
            "regime_labels": labels
        }
        
        with open(filepath, 'w') as f:
            json.dump(export, f, indent=2)
            
    def save(self, filepath: str):
        """Save full model with joblib."""
        joblib.dump({
            'model': self.model,
            'feature_names': self.feature_names,
            'n_regimes': self.n_regimes
        }, filepath)
    
    @classmethod
    def load(cls, filepath: str) -> 'HMMRegimeTrainer':
        """Load full model."""
        data = joblib.load(filepath)
        trainer = cls(n_regimes=data['n_regimes'])
        trainer.model = data['model']
        trainer.feature_names = data['feature_names']
        return trainer
    
    def summary(self) -> dict:
        """Human-readable model summary."""
        labels = self.get_regime_labels(self.model.means_)
        
        summary = {
            "n_regimes": self.n_regimes,
            "features": self.feature_names,
            "log_likelihood": self.model.score(self.model.means_),
            "regimes": {}
        }
        
        for i in range(self.n_regimes):
            summary["regimes"][labels[i]] = {
                "mean": {k: round(v, 6) for k, v in zip(self.feature_names, self.model.means_[i])},
                "variance": {k: round(v, 6) for k, v in zip(self.feature_names, self.model.covars_[i])},
                "persistence": round(self.model.transmat_[i, i], 4)
            }
            
        return summary
