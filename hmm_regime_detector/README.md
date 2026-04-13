# HMM Regime Detector

A **Hidden Markov Model (HMM)**-based market regime detection system for algorithmic trading. Trained in Python, exported for **MetaTrader 5 (MQL5)** integration.

---

## 🎯 What This Is

This module detects market regimes (e.g., **trending up**, **ranging**, **high volatility**) using a Gaussian Hidden Markov Model trained on OHLCV price data. Once trained, the model parameters are exported to a **standalone MQL5 include file** — no ONNX, no Python runtime, no DLLs required inside MT5.

Perfect for:
- **Project Ferrari** — statistical arbitrage regime switching
- **Project Stallion** — equity momentum/mean reversion adaptation
- Any MQL5 EA that needs to know *what kind of market it's in*

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   OHLCV Data    │────►│  Python HMM     │────►│  MQL5 .mqh      │
│   (CSV/MT5)     │     │  Trainer        │     │  Export         │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌─────────────────┐
                        │  JSON params    │
                        │  (backup/debug) │
                        └─────────────────┘
```

---

## 📦 Installation

```bash
cd hmm_regime_detector
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### 1. Train and Export

```bash
python examples/train_and_export.py
```

This generates three files:
- `data/hmm_model.json` — model parameters
- `data/hmm_model.joblib` — full Python model
- `mql5/HMMRegimeDetector.mqh` — **drop-in MQL5 include file**

### 2. Use in MQL5

```mql5
#include "HMMRegimeDetector.mqh"

CHMMRegimeDetector hmm;

// On every tick or bar
double observation[5];
observation[0] = iClose(_Symbol, PERIOD_CURRENT, 0) / iClose(_Symbol, PERIOD_CURRENT, 1) - 1;  // returns
observation[1] = iATR(_Symbol, PERIOD_CURRENT, 20);                                           // volatility proxy
observation[2] = (iHigh(_Symbol, PERIOD_CURRENT, 0) - iLow(_Symbol, PERIOD_CURRENT, 0)) / iClose(_Symbol, PERIOD_CURRENT, 0);  // range
observation[3] = (double)iVolume(_Symbol, PERIOD_CURRENT, 0) / iMAOnArray(volumes, 20);       // volume ratio
observation[4] = (iClose(_Symbol, PERIOD_CURRENT, 0) - iMA(_Symbol, PERIOD_CURRENT, 20, 0, MODE_SMA, PRICE_CLOSE)) / iClose(_Symbol, PERIOD_CURRENT, 0);  // trend strength

int regime = hmm.Update(observation);

if(regime == 0)      { /* Trend Up logic */ }
else if(regime == 1) { /* Range logic */ }
else if(regime == 2) { /* High Vol logic */ }

// Soft probabilities for position sizing
double probTrend = hmm.GetRegimeProb(0);
```

---

## 🧠 How It Works

### Features Engineered

| Feature | Description | MQL5 Equivalent |
|---------|-------------|-----------------|
| `returns` | Bar-to-bar close return | `Close[0]/Close[1] - 1` |
| `volatility` | 20-bar rolling std of returns | `StdDev(returns, 20)` |
| `range` | `(High - Low) / Close` | `(High[0]-Low[0])/Close[0]` |
| `volume_ratio` | Volume / 20-bar MA volume | `Volume[0] / MA(Volume,20)` |
| `trend_strength` | `(Close - MA20) / Close` | `(Close[0]-MA20)/Close[0]` |

### HMM States

The model learns **3 hidden regimes** by default:
- **trend_up** — positive returns, moderate volatility
- **range** — near-zero returns, low volatility
- **high_vol** — erratic returns, elevated volatility

*(Labels are auto-assigned based on mean characteristics.)*

### Why HMM?

| Advantage | Benefit |
|-----------|---------|
| **Transition matrix** | Knows probability of *staying* in a regime vs. switching |
| **Soft probabilities** | Position size based on regime confidence |
| **Lightweight inference** | Forward algorithm = simple matrix math in MQL5 |
| **No ONNX opset hell** | Pure math, no external dependencies in MT5 |

---

## 🧪 Testing

```bash
python -m pytest tests/test_hmm.py -v
```

All tests verify:
- Feature engineering correctness
- HMM convergence and valid predictions
- Transition matrix properties
- JSON export roundtrip
- MQL5 header generation

---

## 🔌 Integration with Existing EAs

### Project Ferrari (Stat Arb)
Use HMM regime to **switch between** mean-reversion and momentum legs:
- Range regime → tighter z-score thresholds
- Trend regime → allow directional drift, widen thresholds

### Project Stallion (FundedElite)
Use HMM regime to **select strategy**:
- Trend up → momentum breakout
- Range → mean reversion
- High vol → reduce position size or skip

*The transition matrix tells you if a regime is **persistent** — useful for hold-time decisions.*

---

## ⚙️ Training on Real Data

Replace the sample data generator in `examples/train_and_export.py` with your own price feed:

```python
df = pd.read_csv("your_mt5_export.csv", parse_dates=['time'])
df = df.rename(columns={'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close', 'tick_volume': 'volume'})
```

Retrain monthly or quarterly as market dynamics shift.

---

## 📁 File Structure

```
hmm_regime_detector/
├── core/
│   ├── __init__.py
│   ├── hmm_trainer.py         # HMM training + export
│   └── mql5_exporter.py       # JSON → MQL5 converter
├── data/
│   ├── hmm_model.json         # Exported parameters
│   └── hmm_model.joblib       # Full Python model
├── examples/
│   └── train_and_export.py    # End-to-end example
├── mql5/
│   └── HMMRegimeDetector.mqh  # MQL5 include file
├── tests/
│   └── test_hmm.py            # Unit tests
├── README.md
└── requirements.txt
```

---

## 📝 Notes

- `covariance_type="diag"` is used for robustness and easy MQL5 export
- The forward algorithm in MQL5 uses `log` Gaussian PDF to prevent underflow
- Reset the HMM state at the start of each trading session with `hmm.Reset()`

---

**Built for Bob's brain. Deployed in MQL5. No loading screens.** 🧠⚡
