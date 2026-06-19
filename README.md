# Pair Trading Monitor - README

## Overview

This project monitors a portfolio of statistically selected pair trades and generates alerts when predefined entry, exit or stop-loss conditions are met.

The system:

1. Downloads market data from Yahoo Finance.
2. Calculates hedge ratios using Ordinary Least Squares (OLS) regression.
3. Calculates spread and Z-score for each pair.
4. Calculates mean-reversion half-life.
5. Evaluates trading signals.
6. Sends email alerts when actionable events occur.

Initially developed around:

| Pair            | Description                       |
| --------------- | --------------------------------- |
| MA / V          | Mastercard vs Visa                |
| AMZN / META     | Amazon vs Meta                    |
| ICE / V         | Intercontinental Exchange vs Visa |
| BARC.L / LLOY.L | Barclays vs Lloyds                |

---

# Strategy

## Core Concept

Pair trading seeks to exploit temporary divergences between two historically related securities.

Example:

```text
Visa rises much faster than Mastercard

↓

Relationship becomes stretched

↓

Spread reaches extreme level

↓

Expect spread to revert

↓

Long Mastercard
Short Visa
```

The strategy attempts to profit from:

```text
Relative movement
```

rather than:

```text
Overall market direction
```

---

# Statistical Model

## Hedge Ratio

A hedge ratio is calculated using OLS regression.

Formula:

Where:

* P₁ = Asset 1 price
* P₂ = Asset 2 price
* β = Hedge ratio

Example:

```text
MA / V

β = 1.72
```

---

## Z-Score

The Z-score measures how far today's spread is from its historical average.

Interpretation:

| Z-score | Interpretation         |
| ------- | ---------------------- |
| 0       | Normal                 |
| ±1      | Slightly stretched     |
| ±2      | Significant divergence |
| ±3      | Extreme divergence     |

---

## Half-Life

Half-life estimates how long a spread takes to revert halfway back to equilibrium.

Typical interpretation:

| Half-life  | Meaning    |
| ---------- | ---------- |
| < 10 days  | Very fast  |
| 10–40 days | Attractive |
| 40–90 days | Tradable   |
| > 120 days | Weak       |

Example:

```text
MA / V

Half-life ≈ 40 trading days
```

---

# Trading Rules

## Entry

Long Pair 1 / Short Pair 2 when:

```text
Z <= -2.0
```

Example:

```text
MA / V

Z = -2.39

Signal:
Long MA
Short V
```

---

## Exit

Take profit when:

```text
Z >= -0.5
```

---

## Stop Loss

Close trade when:

```text
Z <= -3.5
```

---

## Time Stop

Close trade after:

```text
90 calendar days
```

if mean reversion has not occurred.

---

# Project Structure

```text
project/

├── pair_monitor.py
├── pair_trading_candidates.csv
├── multi_pair_backtest_results.csv
├── logs/
│   └── signal_history.csv
├── output/
│   └── daily_report.csv
└── README.md
```

---

# Installation

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install yfinance
pip install pandas
pip install numpy
pip install statsmodels
pip install matplotlib
```

Or:

```bash
pip install -r requirements.txt
```

Example requirements.txt:

```text
yfinance
pandas
numpy
statsmodels
matplotlib
```

---

# Configuration

Edit:

```python
PAIRS = [
    ("MA", "V"),
    ("AMZN", "META"),
    ("ICE", "V"),
    ("BARC.L", "LLOY.L")
]
```

Add additional pairs as desired.

---

# Email Alert Configuration

For Gmail:

1. Enable Two Factor Authentication.
2. Create an App Password.

Google Account:

```text
Security
↓
2-Step Verification
↓
App Passwords
```

Update:

```python
EMAIL_FROM = "you@gmail.com"
EMAIL_TO = "you@gmail.com"
EMAIL_APP_PASSWORD = "xxxxxxxx"
```

---

# Example Output

```text
Pair Trading Monitor

MA/V

Current Z-score: -2.39

Signal:
ENTRY ZONE

Suggested Trade:
Long MA
Short V

Half-life:
40.3 trading days
```

---

# Daily Workflow

```text
Download Prices
        ↓
Calculate Hedge Ratio
        ↓
Calculate Spread
        ↓
Calculate Z-Score
        ↓
Evaluate Rules
        ↓
Generate Signals
        ↓
Send Alerts
```

---

# Automation Options

## Local PC

Windows Task Scheduler:

```text
Daily
07:00
Run pair_monitor.py
```

---

## GitHub Actions

Suitable for cloud-based execution.

Benefits:

* Free
* No PC required
* Scheduled runs
* Version controlled

---

## PythonAnywhere

Simple hosted alternative.

Benefits:

* Easy setup
* Scheduled tasks
* Email support

---

# Current Research Findings

## MA / V

Latest model results:

| Metric                | Value   |
| --------------------- | ------- |
| Correlation           | 0.99    |
| Cointegration p-value | 0.007   |
| Hedge Ratio           | 1.72    |
| Half-life             | 40 days |
| Current Z-score       | -2.39   |

Current model status:

```text
ENTRY SIGNAL ACTIVE

Long Mastercard
Short Visa
```

---

# Future Enhancements

## Version 2.1

* Monthly hedge-ratio recalculation
* Trade state persistence
* Signal history database

## Version 3

* Earnings event detection
* News analysis
* Fundamental scoring

## Version 4

* Portfolio optimisation
* Position sizing engine
* Risk budgeting

## Version 5

* Interactive Brokers execution
* Paper trading
* Automated order management

---

# Disclaimer

This project is for research and educational purposes.

Backtested performance does not guarantee future results.

Before trading with real capital:

* Validate using paper trading.
* Check borrow availability.
* Include financing costs.
* Consider tax implications.
* Apply appropriate risk management.
