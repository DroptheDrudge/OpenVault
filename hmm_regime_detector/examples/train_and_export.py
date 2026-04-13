#!/usr/bin/env python3
"""
Example: Train HMM regime detector and export to MQL5
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.hmm_trainer import HMMRegimeTrainer
from core.mql5_exporter import MQL5Exporter


def generate_sample_data(n_bars: int = 1000) -> pd.DataFrame:
    """
    Generate sample OHLCV data for demonstration.
    In production, load your actual price data.
    """
    np.random.seed(42)
    
    # Create regime-switching returns
    regimes = np.zeros(n_bars, dtype=int)
    returns = np.zeros(n_bars)
    
    # Start in regime 0 (trending up)
    current_regime = 0
    for i in range(n_bars):
        if np.random.random() < 0.02:  # 2% chance of regime switch
            current_regime = np.random.choice([0, 1, 2])
        regimes[i] = current_regime
        
        if current_regime == 0:  # Trend up
            returns[i] = np.random.normal(0.001, 0.01)
        elif current_regime == 1:  # Range
            returns[i] = np.random.normal(0, 0.005)
        else:  # High vol
            returns[i] = np.random.normal(-0.0005, 0.025)
    
    # Build OHLCV from returns
    close = 100 * np.exp(np.cumsum(returns))
    high = close * (1 + np.abs(np.random.normal(0, 0.005, n_bars)))
    low = close * (1 - np.abs(np.random.normal(0, 0.005, n_bars)))
    open_p = close * (1 + np.random.normal(0, 0.002, n_bars))
    volume = np.random.lognormal(10, 1, n_bars)
    
    df = pd.DataFrame({
        'open': open_p,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })
    
    return df


def main():
    print("=" * 60)
    print("HMM Regime Detector - Training & Export")
    print("=" * 60)
    
    # Paths
    data_dir = Path(__file__).parent.parent / "data"
    mql5_dir = Path(__file__).parent.parent / "mql5"
    data_dir.mkdir(exist_ok=True)
    mql5_dir.mkdir(exist_ok=True)
    
    # Load or generate data
    print("\n[1] Loading price data...")
    df = generate_sample_data(n_bars=2000)
    print(f"    Loaded {len(df)} bars")
    
    # Initialize trainer
    print("\n[2] Initializing HMM trainer (3 regimes)...")
    trainer = HMMRegimeTrainer(n_regimes=3, random_state=42)
    
    # Engineer features
    print("\n[3] Engineering features...")
    X = trainer.engineer_features(df)
    print(f"    Features: {trainer.feature_names}")
    print(f"    Samples: {len(X)}")
    
    # Train
    print("\n[4] Training HMM...")
    trainer.fit(X.values)
    print("    Training complete!")
    
    # Predict regimes
    print("\n[5] Analyzing regimes...")
    regimes = trainer.predict(X.values)
    regime_probs = trainer.predict_proba(X.values)
    
    # Regime distribution
    unique, counts = np.unique(regimes, return_counts=True)
    print(f"    Regime distribution:")
    for u, c in zip(unique, counts):
        print(f"      Regime {u}: {c} bars ({100*c/len(regimes):.1f}%)")
    
    # Model summary
    print("\n[6] Model Summary:")
    summary = trainer.summary()
    for regime_name, details in summary['regimes'].items():
        print(f"    {regime_name}:")
        print(f"      Persistence: {details['persistence']:.2%}")
        print(f"      Mean returns: {details['mean'].get('returns', 0):.6f}")
        print(f"      Mean volatility: {details['mean'].get('volatility', 0):.6f}")
    
    # Export to JSON
    json_path = data_dir / "hmm_model.json"
    print(f"\n[7] Exporting to JSON: {json_path}")
    trainer.export_to_json(json_path)
    
    # Export to MQL5
    mqh_path = mql5_dir / "HMMRegimeDetector.mqh"
    print(f"\n[8] Generating MQL5 header: {mqh_path}")
    exporter = MQL5Exporter(json_path)
    exporter.generate_mqh(mqh_path, class_name="CHMMRegimeDetector")
    
    # Save full model
    model_path = data_dir / "hmm_model.joblib"
    print(f"\n[9] Saving full model: {model_path}")
    trainer.save(model_path)
    
    print("\n" + "=" * 60)
    print("EXPORT COMPLETE!")
    print("=" * 60)
    print(f"\nFiles generated:")
    print(f"  - {json_path} (model parameters)")
    print(f"  - {mqh_path} (MQL5 include file)")
    print(f"  - {model_path} (Python model)")
    print(f"\nTo use in MQL5:")
    print(f'  #include "HMMRegimeDetector.mqh"')
    print(f"  CHMMRegimeDetector hmm;")
    print(f"  double obs[] = {{returns, volatility, range, volume_ratio, trend}};")
    print(f"  int regime = hmm.Update(obs);")
    print(f"\nRegime labels: {summary['regimes'].keys()}")


if __name__ == "__main__":
    main()
