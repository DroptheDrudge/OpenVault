import unittest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.hmm_trainer import HMMRegimeTrainer
from core.mql5_exporter import MQL5Exporter
import json


class TestHMMRegimeTrainer(unittest.TestCase):
    
    def setUp(self):
        np.random.seed(42)
        n = 500
        self.df = pd.DataFrame({
            'open': 100 + np.cumsum(np.random.normal(0, 0.01, n)),
            'high': 101 + np.cumsum(np.random.normal(0, 0.01, n)),
            'low': 99 + np.cumsum(np.random.normal(0, 0.01, n)),
            'close': 100 + np.cumsum(np.random.normal(0, 0.01, n)),
            'volume': np.random.lognormal(10, 1, n)
        })
        self.trainer = HMMRegimeTrainer(n_regimes=3, random_state=42)
        self.X = self.trainer.engineer_features(self.df)
    
    def test_feature_engineering(self):
        """Test that features are generated correctly."""
        self.assertEqual(len(self.X), len(self.df) - 20)  # Rolling windows drop NaN
        self.assertIn('returns', self.X.columns)
        self.assertIn('volatility', self.X.columns)
        self.assertIn('trend_strength', self.X.columns)
    
    def test_model_fit(self):
        """Test HMM fitting."""
        self.trainer.fit(self.X.values)
        self.assertIsNotNone(self.trainer.model)
        self.assertEqual(self.trainer.model.n_components, 3)
        self.assertEqual(self.trainer.model.means_.shape[1], self.X.shape[1])
    
    def test_predict_range(self):
        """Test predictions are in valid range."""
        self.trainer.fit(self.X.values)
        regimes = self.trainer.predict(self.X.values)
        self.assertTrue(np.all(regimes >= 0))
        self.assertTrue(np.all(regimes < 3))
    
    def test_predict_proba_shape(self):
        """Test probability matrix shape."""
        self.trainer.fit(self.X.values)
        probs = self.trainer.predict_proba(self.X.values)
        self.assertEqual(probs.shape, (len(self.X), 3))
        # Rows should sum to 1
        np.testing.assert_array_almost_equal(probs.sum(axis=1), np.ones(len(self.X)))
    
    def test_persistence_high(self):
        """Test that diagonal of transition matrix is dominant."""
        self.trainer.fit(self.X.values)
        transmat = self.trainer.model.transmat_
        for i in range(3):
            self.assertGreaterEqual(transmat[i, i], 0.0)
            self.assertLessEqual(transmat[i, i], 1.0)
    
    def test_export_roundtrip(self):
        """Test JSON export creates valid output."""
        self.trainer.fit(self.X.values)
        json_path = Path(__file__).parent.parent / "data" / "test_hmm_model.json"
        json_path.parent.mkdir(exist_ok=True)
        self.trainer.export_to_json(json_path)
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(data['n_regimes'], 3)
        self.assertEqual(len(data['start_prob']), 3)
        self.assertEqual(len(data['transmat']), 3)
        self.assertEqual(len(data['transmat'][0]), 3)
        self.assertIn('regime_labels', data)


class TestMQL5Exporter(unittest.TestCase):
    
    def test_mqh_generation(self):
        """Test MQL5 header generation."""
        json_path = Path(__file__).parent.parent / "data" / "test_hmm_model.json"
        mqh_path = Path(__file__).parent.parent / "data" / "TestHMM.mqh"
        
        # Ensure test JSON exists
        if not json_path.exists():
            trainer = HMMRegimeTrainer(n_regimes=3, random_state=42)
            df = pd.DataFrame({
                'open': np.ones(100),
                'high': np.ones(100) * 1.01,
                'low': np.ones(100) * 0.99,
                'close': np.ones(100),
                'volume': np.ones(100) * 1000
            })
            X = trainer.engineer_features(df)
            trainer.fit(X.values)
            trainer.export_to_json(json_path)
        
        exporter = MQL5Exporter(json_path)
        exporter.generate_mqh(mqh_path, class_name="CTestHMM")
        
        with open(mqh_path, 'r') as f:
            content = f.read()
        
        self.assertIn("class CTestHMM", content)
        self.assertIn("HMM_N_REGIMES", content)
        self.assertIn("GaussianLogPDF", content)
        self.assertIn("Update(double observation[])", content)
        self.assertIn("GetRegimeProb(int regime)", content)


if __name__ == '__main__':
    unittest.main()
